from ..objects.base import GHuntCreds
from ..errors import *
from .. import globals as gb
from ..objects.apis import GAPI
from ..parsers.clientauthconfig import CacBrand
from typing import *
import json, httpx, inspect

class ClientAuthConfigHttp(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = gb.config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        self.hostname = "clientauthconfig.googleapis.com"
        self.scheme = "https"

        self.authentication_mode = None # sapisidhash, cookies_only, oauth or None
        self.require_key = "pantheon" # key name, or None

        self._load_api(creds, headers)

    async def get_brand(self, as_client: httpx.AsyncClient, project_number: int) -> Tuple[bool, CacBrand]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/v1/brands/lookupkey/brand/{project_number}"
        data_type = None # json, data or None

        params = {
            "readMask": "*",
            "$outputDefaults": True
        }

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)

        brand = CacBrand()
        if "error" in data:
            return False, brand
        
        brand._scrape(data)

        return True, brand