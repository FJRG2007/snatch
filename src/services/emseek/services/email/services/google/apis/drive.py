from ..objects.base import GHuntCreds
from ..errors import *
from .. import globals as gb
from ..objects.apis import GAPI
from ..parsers.drive import DriveCommentList, DriveFile, DriveChildList
from ..knowledge import drive as drive_knowledge
from typing import *
import json, httpx, inspect


class DriveHttp(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        
        if not headers:
            headers = gb.config.headers

        base_headers = {}

        headers = {**headers, **base_headers}

        # Android OAuth fields
        self.api_name = "drive"
        self.package_name = "com.google.android.apps.docs"
        self.scopes = [
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file"
        ]

        self.hostname = "www.googleapis.com"
        self.scheme = "https"

        self.authentication_mode = "oauth" # sapisidhash, cookies_only, oauth or None
        self.require_key = None # key name, or None

        self._load_api(creds, headers)

    async def get_file(self, as_client: httpx.AsyncClient, file_id: str) -> Tuple[bool, DriveFile]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/drive/v2internal/files/{file_id}"
        data_type = None # json, data or None

        params = {
            "fields": ','.join(drive_knowledge.request_fields),
            "supportsAllDrives": True
        }

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)
        drive_file = DriveFile()
        if "error" in data:
            return False, drive_file

        drive_file._scrape(data)

        return True, drive_file

    async def get_comments(self, as_client: httpx.AsyncClient, file_id: str, page_token: str="") -> Tuple[bool, str, DriveCommentList]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/drive/v2internal/files/{file_id}/comments"
        data_type = None # json, data or None

        params = {
            "supportsAllDrives": True,
            "maxResults": 100
        }

        if page_token:
            params["pageToken"] = page_token

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)
        drive_comments = DriveCommentList()
        if "error" in data:
            return False, "", drive_comments

        next_page_token = data.get("nextPageToken", "")

        drive_comments._scrape(data)

        return True, next_page_token, drive_comments

    async def get_childs(self, as_client: httpx.AsyncClient, file_id: str, page_token: str="") -> Tuple[bool, str, DriveChildList]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/drive/v2internal/files/{file_id}/children"
        data_type = None # json, data or None

        params = {
            "supportsAllDrives": True,
            "maxResults": 1000
        }

        if page_token:
            params["pageToken"] = page_token

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)
        drive_childs = DriveChildList()
        if "error" in data:
            return False, "", drive_childs

        next_page_token = data.get("nextPageToken", "")

        drive_childs._scrape(data)

        return True, next_page_token, drive_childs