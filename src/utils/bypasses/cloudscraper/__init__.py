from requests.sessions import Session
import ssl, sys, time, logging, requests
from requests_toolbelt.utils import dump
from requests.adapters import HTTPAdapter
try: import brotli
except ImportError: pass
try: import copyreg
except ImportError: import copy_reg as copyreg
try: from urlparse import urlparse
except ImportError: from urllib.parse import urlparse
from src.utils.basics import terminal
from .main import Cloudflare
from .user_agent import User_Agent
from .exceptions import (CloudflareLoopProtection, CloudflareIUAMError)

class CipherSuiteAdapter(HTTPAdapter):
    __attrs__ = [
        "ssl_context",
        "max_retries",
        "config",
        "_pool_connections",
        "_pool_maxsize",
        "_pool_block",
        "source_address"
    ]

    def __init__(self, *args, **kwargs):
        self.ssl_context = kwargs.pop("ssl_context", None)
        self.cipherSuite = kwargs.pop("cipherSuite", None)
        self.source_address = kwargs.pop("source_address", None)
        self.server_hostname = kwargs.pop("server_hostname", None)
        self.ecdhCurve = kwargs.pop("ecdhCurve", "prime256v1")
        if self.source_address:
            if isinstance(self.source_address, str): self.source_address = (self.source_address, 0)
            if not isinstance(self.source_address, tuple): raise TypeError("source_address must be IP address string or (ip, port) tuple")
        if not self.ssl_context:
            self.ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.ssl_context.orig_wrap_socket = self.ssl_context.wrap_socket
            self.ssl_context.wrap_socket = self.wrap_socket
            if self.server_hostname: self.ssl_context.server_hostname = self.server_hostname
            self.ssl_context.set_ciphers(self.cipherSuite)
            self.ssl_context.set_ecdh_curve(self.ecdhCurve)
            self.ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
            self.ssl_context.maximum_version = ssl.TLSVersion.TLSv1_3
        super(CipherSuiteAdapter, self).__init__(**kwargs)

    def wrap_socket(self, *args, **kwargs):
        if hasattr(self.ssl_context, "server_hostname") and self.ssl_context.server_hostname:
            kwargs["server_hostname"] = self.ssl_context.server_hostname
            self.ssl_context.check_hostname = False
        else: self.ssl_context.check_hostname = True
        return self.ssl_context.orig_wrap_socket(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        kwargs["source_address"] = self.source_address
        return super(CipherSuiteAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        kwargs["ssl_context"] = self.ssl_context
        kwargs["source_address"] = self.source_address
        return super(CipherSuiteAdapter, self).proxy_manager_for(*args, **kwargs)

class CloudScraper(Session):
    visited_domains = []

    def __init__(self, *args, **kwargs):
        self.debug = kwargs.pop("debug", False)
        self.disableCloudflareV1 = kwargs.pop("disableCloudflareV1", False)
        self.delay = kwargs.pop("delay", None)
        self.captcha = kwargs.pop("captcha", {})
        self.doubleDown = kwargs.pop("doubleDown", True)
        self.interpreter = kwargs.pop("interpreter", "native")
        self.requestPreHook = kwargs.pop("requestPreHook", None)
        self.requestPostHook = kwargs.pop("requestPostHook", None)
        self.cipherSuite = kwargs.pop("cipherSuite", None)
        self.ecdhCurve = kwargs.pop("ecdhCurve", "prime256v1")
        self.source_address = kwargs.pop("source_address", None)
        self.server_hostname = kwargs.pop("server_hostname", None)
        self.ssl_context = kwargs.pop("ssl_context", None)
        self.allow_brotli = kwargs.pop("allow_brotli", True if "brotli" in sys.modules.keys() else False)
        self.user_agent = User_Agent(allow_brotli=self.allow_brotli, browser=kwargs.pop("browser", None))
        self._solveDepthCnt = 0
        self.solveDepth = kwargs.pop("solveDepth", 3)
        super(CloudScraper, self).__init__(*args, **kwargs)
        # pylint: disable=E0203
        if "requests" in self.headers["User-Agent"]:
            self.headers = self.user_agent.headers
            if not self.cipherSuite: self.cipherSuite = self.user_agent.cipherSuite
        if isinstance(self.cipherSuite, list): self.cipherSuite = ":".join(self.cipherSuite)
        self.mount("https://", CipherSuiteAdapter(cipherSuite=self.cipherSuite, ecdhCurve=self.ecdhCurve, server_hostname=self.server_hostname, source_address=self.source_address, ssl_context=self.ssl_context))
        copyreg.pickle(ssl.SSLContext, lambda obj: (obj.__class__, (obj.protocol,)))

    def __getstate__(self):
        return self.__dict__

    def perform_request(self, method, url, *args, **kwargs):
        return super(CloudScraper, self).request(method, url, *args, **kwargs)

    def simpleException(self, exception, msg):
        self._solveDepthCnt = 0
        sys.tracebacklimit = 0
        raise exception(msg)

    @staticmethod
    def debugRequest(req):
        try: print(dump.dump_all(req).decode("utf-8", errors="backslashreplace"))
        except ValueError as e: terminal("e", getattr(e, "message", e))

    def decodeBrotli(self, resp):
        if requests.packages.urllib3.__version__ < "1.25.1" and resp.headers.get("Content-Encoding") == "br":
            if self.allow_brotli and resp._content: resp._content = brotli.decompress(resp.content)
            else: logging.warning(f'You\'re running urllib3 {requests.packages.urllib3.__version__}, Brotli content detected, ' "Which requires manual decompression, " "But option allow_brotli is set to False, " "We will not continue to decompress.")
        return resp

    def has_cloudflare_waf(self, method, url, *args, **kwargs):
        try:
            response = requests.request(method, url, *args, **kwargs)
            has_cloudflare = "server" in response.headers and "cloudflare" in response.headers["server"].lower()
            response.has_cloudflare = has_cloudflare
            return response
        except requests.RequestException as error:
            terminal("e", f"An error occurred while bypassing Cloudflare: {error}")
            class ErrorResponse:
                has_cloudflare = False
            return ErrorResponse()

    def request(self, method, url, *args, **kwargs):
        domain = urlparse(url).netloc
        if domain not in self.visited_domains:
            has_cloudflare = self.has_cloudflare_waf(method, url, *args, **kwargs)
            if not has_cloudflare.has_cloudflare:
                del has_cloudflare.has_cloudflare
                return has_cloudflare
            terminal("i", "I have detected that this site is protected with Cloudflare,\nI will have to bypass your security, it will take a few seconds.\n")
            start_time = time.time()
            for _ in range(5):
                elapsed_time = time.time() - start_time
                if elapsed_time > 13:
                    print("Pre-fetching took too long, restarting...")
                    break
                print(f"Pre-fetching {domain} for bypassing Cloudflare... x{_+1}", end="\r")
                self.perform_request(method, url, *args, **kwargs)
            print("\n")
            self.visited_domains.append(domain)
        # pylint: disable=E0203
        if kwargs.get("proxies") and kwargs.get("proxies") != self.proxies: self.proxies = kwargs.get("proxies")
        if self.requestPreHook: (method, url, args, kwargs) = self.requestPreHook(self, method, url, *args, **kwargs)
        response = self.decodeBrotli(self.perform_request(method, url, *args, **kwargs))
        if self.debug: self.debugRequest(response)
        if self.requestPostHook:
            newResponse = self.requestPostHook(self, response)
            if response != newResponse:
                response = newResponse
                if self.debug:
                    print("==== requestPostHook Debug ====")
                    self.debugRequest(response)
        if not self.disableCloudflareV1:
            cloudflareV1 = Cloudflare(self)
            if cloudflareV1.is_Challenge_Request(response):
                if self._solveDepthCnt >= self.solveDepth:
                    _ = self._solveDepthCnt
                    self.simpleException(CloudflareLoopProtection, f"!!Loop Protection!! We have tried to solve {_} time(s) in a row.")
                self._solveDepthCnt += 1
                response = cloudflareV1.Challenge_Response(response, **kwargs)
            elif not response.is_redirect and response.status_code not in [429, 503]: self._solveDepthCnt = 0
        return response

    @classmethod
    def create_scraper(cls, sess=None, **kwargs):
        scraper = cls(**kwargs)
        if sess:
            for attr in ["auth", "cert", "cookies", "headers", "hooks", "params", "proxies", "data"]:
                val = getattr(sess, attr, None)
                if val is not None: setattr(scraper, attr, val)
        return scraper

    @classmethod
    def get_tokens(cls, url, **kwargs):
        scraper = cls.create_scraper(
            **{
                field: kwargs.pop(field, None) for field in [
                    "allow_brotli",
                    "browser",
                    "debug",
                    "delay",
                    "doubleDown",
                    "captcha",
                    "interpreter",
                    "source_address",
                    "requestPreHook",
                    "requestPostHook"
                ] if field in kwargs
            }
        )
        try:
            resp = scraper.get(url, **kwargs)
            resp.raise_for_status()
        except Exception:
            logging.error(f'"{url}" returned an error. Could not collect tokens.')
            raise
        domain = urlparse(resp.url).netloc
        # noinspection PyUnusedLocal
        cookie_domain = None
        for d in scraper.cookies.list_domains():
            if d.startswith(".") and d in (f".{domain}"): cookie_domain = d; break
        else: cls.simpleException(cls, CloudflareIUAMError, "Unable to find Cloudflare cookies. Does the site actually " "have Cloudflare IUAM (I'm Under Attack Mode) enabled?")
        return ({ "cf_clearance": scraper.cookies.get("cf_clearance", "", domain=cookie_domain) }, scraper.headers["User-Agent"])

    @classmethod
    def get_cookie_string(cls, url, **kwargs):
        tokens, user_agent = cls.get_tokens(url, **kwargs)
        return "; ".join("=".join(pair) for pair in tokens.items()), user_agent

if ssl.OPENSSL_VERSION_INFO < (1, 1, 1): print(f"DEPRECATION: The OpenSSL being used by this python install ({ssl.OPENSSL_VERSION}) does not meet the minimum supported " "version (>= OpenSSL 1.1.1) in order to support TLS 1.3 required by Cloudflare, " "You may encounter an unexpected Captcha or cloudflare 1020 blocks.")

create_scraper = CloudScraper.create_scraper
session = CloudScraper.create_scraper
get_tokens = CloudScraper.get_tokens
get_cookie_string = CloudScraper.get_cookie_string