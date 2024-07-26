from ..objects.base import GHuntCreds
from ..errors import *
from .. import globals as gb
from ..objects.apis import GAPI
from typing import *
import httpx, inspect


class Accounts(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = gb.config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        # Android OAuth fields
        self.api_name = "chrome"
        self.package_name = "com.android.chrome"
        self.scopes = [
            "https://www.google.com/accounts/OAuthLogin"
        ]
        
        self.hostname = "accounts.google.com"
        self.scheme = "https"

        self.authentication_mode = "oauth" # sapisidhash, cookies_only, oauth or None
        self.require_key = None # key name, or None

        self._load_api(creds, headers)

    async def OAuthLogin(self, as_client: httpx.AsyncClient) -> str:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/OAuthLogin"
        data_type = None # json, data or None

        params = {
            "source": "ChromiumBrowser",
            "issueuberauth": 1
        }

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        uber_auth = req.text

        return True, uber_auth