from typing import *
import httpx, asyncio
from bs4 import BeautifulSoup as bs
from .. import globals as gb
from ..objects.base import GHuntCreds
from ..errors import *
from ..helpers.utils import *
from ..helpers.knowledge import get_domain_of_service, get_package_sig
from ..knowledge.services import services_baseurls
from ..helpers.auth import *

async def android_master_auth(as_client: httpx.AsyncClient, oauth_token: str) -> Tuple[str, List[str], str, str]:
    """
        Takes an oauth_token to perform an android authentication
        to get the master token and other informations.

        Returns the master token, connected services, account email and account full name.
    """
    data = {
        "Token": oauth_token,
        "service": "ac2dm",
        "get_accountid": 1,
        "ACCESS_TOKEN": 1,
        "add_account": 1,
        "callerSig": "38918a453d07199354f8b19af05ec6562ced5788"
    }
    req = await as_client.post("https://android.googleapis.com/auth", data=data)
    resp = parse_oauth_flow_response(req.text)
    for keyword in ["Token", "Email", "services", "firstName", "lastName"]:
        if keyword not in resp: raise GHuntAndroidMasterAuthError(f'Expected "{keyword}" in the response of the Android Master Authentication.\nThe oauth_token may be expired.')
    return resp["Token"], resp["services"].split(","), resp["Email"], f'{resp["firstName"]} {resp["lastName"]}'

async def android_oauth_app(as_client: httpx.AsyncClient, master_token: str,
                package_name: str, scopes: List[str]) -> Tuple[str, List[str], int]:
    """
        Uses the master token to ask for an authorization token,
        with specific scopes and app package name.

        Returns the authorization token, granted scopes and expiry UTC timestamp.
    """
    client_sig = get_package_sig(package_name)
    data = {
        "app": package_name,
        "service": f"oauth2:{' '.join(scopes)}",
        "client_sig": client_sig,
        "Token": master_token
    }

    req = await as_client.post("https://android.googleapis.com/auth", data=data)
    resp = parse_oauth_flow_response(req.text)
    for keyword in ["Expiry", "grantedScopes", "Auth"]:
        if keyword not in resp: raise GHuntAndroidAppOAuth2Error(f'Expected "{keyword}" in the response of the Android App OAuth2 Authentication.\nThe master token may be revoked.')
    return resp["Auth"], resp["grantedScopes"].split(" "), int(resp["Expiry"])

async def gen_osid(as_client: httpx.AsyncClient, cookies: Dict[str, str], generated_osids: dict[str, str], service: str) -> None:
    domain = get_domain_of_service(service)
    params = {
        "service": service,
        "osid": 1,
        "continue": f"https://{domain}/",
        "followup": f"https://{domain}/",
        "authuser": 0
    }
    req = await as_client.get(f"https://accounts.google.com/ServiceLogin", params=params, cookies=cookies, headers=gb.config.headers)
    params = {x.attrs["name"]:x.attrs["value"] for x in bs(req.text, 'html.parser').find_all("input", {"type":"hidden"})}
    headers = {**gb.config.headers, **{"Content-Type": "application/x-www-form-urlencoded"}}
    req = await as_client.post(f"https://{domain}/accounts/SetOSID", cookies=cookies, data=params, headers=headers)
    if not "OSID" in req.cookies: raise GHuntOSIDAuthError("[-] No OSID header detected, exiting...")
    generated_osids[service] = req.cookies["OSID"]

async def gen_osids(as_client: httpx.AsyncClient, cookies: Dict[str, str], osids: List[str]) -> Dict[str, str]:
    """
        Generate OSIDs of given services names,
        contained in the "osids" dict argument.
    """
    generated_osids = {}
    tasks = [gen_osid(as_client, cookies, generated_osids, service) for service in osids]
    await asyncio.gather(*tasks)
    return generated_osids

async def check_cookies(as_client: httpx.AsyncClient, cookies: Dict[str, str]) -> bool:
    """Checks the validity of given cookies."""
    continue_url = "https://www.google.com/robots.txt"
    params = {"continue": continue_url}
    req = await as_client.get("https://accounts.google.com/CheckCookie", params=params, cookies=cookies)
    return req.status_code == 302 and not req.headers.get("Location", "").startswith(("https://support.google.com", "https://accounts.google.com/CookieMismatch"))

async def check_osid(as_client: httpx.AsyncClient, cookies: Dict[str, str], service: str) -> bool:
    """Checks the validity of given OSID."""
    domain = get_domain_of_service(service)
    wanted = ["authuser", "continue", "osidt", "ifkv"]
    req = await as_client.get(f"https://accounts.google.com/ServiceLogin?service={service}&osid=1&continue=https://{domain}/&followup=https://{domain}/&authuser=0",
                    cookies=cookies, headers=gb.config.headers)

    body = bs(req.text, 'html.parser')
    params = [x.attrs["name"] for x in body.find_all("input", {"type":"hidden"})]
    if not all([param in wanted for param in params]): return False
    return True

async def check_osids(as_client: httpx.AsyncClient, cookies: Dict[str, str], osids: Dict[str, str]) -> bool:
    """Checks the validity of given OSIDs."""
    return all(await asyncio.gather(*[check_osid(as_client, cookies, service) for service in osids]))

async def check_master_token(as_client: httpx.AsyncClient, master_token: str) -> str:
    """Checks the validity of the android master token."""
    try: await android_oauth_app(as_client, master_token, "com.google.android.play.games", ["https://www.googleapis.com/auth/games.firstparty"])
    except GHuntAndroidAppOAuth2Error: return False
    return True

async def gen_cookies_and_osids(as_client: httpx.AsyncClient, ghunt_creds: GHuntCreds, osids: list[str]=[*services_baseurls.keys()]):
    from ..apis.accounts import Accounts
    accounts_api = Accounts(ghunt_creds)
    is_logged_in, uber_auth = await accounts_api.OAuthLogin(as_client)
    if not is_logged_in: raise GHuntLoginError("[-] Not logged in.")
    params = {
        "uberauth": uber_auth,
        "continue": "https://www.google.com",
        "source": "ChromiumAccountReconcilor",
        "externalCcResult": "doubleclick:null,youtube:null"
    }
    req = await as_client.get("https://accounts.google.com/MergeSession", params=params)
    cookies = dict(req.cookies)
    ghunt_creds.cookies = cookies
    osids = await gen_osids(as_client, cookies, osids)
    ghunt_creds.osids = osids

async def check_and_gen(as_client: httpx.AsyncClient, ghunt_creds: GHuntCreds):
    """Checks the validity of the cookies and generate new ones if needed."""
    if not await check_cookies(as_client, ghunt_creds.cookies):
        await gen_cookies_and_osids(as_client, ghunt_creds)
        if not await check_cookies(as_client, ghunt_creds.cookies): raise GHuntLoginError("[-] Can't generate cookies after multiple retries. Exiting...")
    ghunt_creds.save_creds(silent=True)
    gb.rc.print("[+] Authenticated !\n", style="sea_green3")

async def load_and_auth(as_client: httpx.AsyncClient, help=True) -> GHuntCreds:
    # Returns an authenticated GHuntCreds object.
    creds = GHuntCreds()
    try: creds.load_creds()
    except GHuntInvalidSession as e:
        if help: raise GHuntInvalidSession(f"Please generate a new session by doing => ghunt login") from e
        else: raise e
    await check_and_gen(as_client, creds)
    return creds