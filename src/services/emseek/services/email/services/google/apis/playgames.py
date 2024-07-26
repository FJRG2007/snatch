from ..objects.base import GHuntCreds
from ..errors import *
from .. import globals as gb
from ..objects.apis import GAPI
from ..parsers.playgames import PlayedGames, PlayerAchievements, PlayerProfile
from typing import *
import json, httpx, inspect

class PlayGames(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        if not headers: headers = gb.config.headers
        base_headers = {}
        headers = {**headers, **base_headers}
        # Android OAuth fields
        self.api_name = "playgames"
        self.package_name = "com.google.android.play.games"
        self.scopes = [
            "https://www.googleapis.com/auth/games.firstparty",
            "https://www.googleapis.com/auth/googleplay"
        ]
        self.hostname = "www.googleapis.com"
        self.scheme = "https"
        self.authentication_mode = "oauth" # sapisidhash, cookies_only, oauth or None
        self.require_key = None # key name, or None
        self._load_api(creds, headers)

    async def get_profile(self, as_client: httpx.AsyncClient, player_id: str) -> Tuple[bool, PlayerProfile]:
        endpoint_name = inspect.currentframe().f_code.co_name
        verb = "GET"
        base_url = f"/games/v1whitelisted/players/{player_id}"
        data_type = None # json, data or None
        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, None, None, data_type)
        # Parsing
        data = json.loads(req.text)
        player_profile = PlayerProfile()
        if not "displayPlayer" in data: return False, player_profile
        player_profile._scrape(data["displayPlayer"])
        player_profile.id = player_id
        return True, player_profile

    async def get_played_games(self, as_client: httpx.AsyncClient, player_id: str, page_token: str="") -> Tuple[bool, str, PlayedGames]:
        endpoint_name = inspect.currentframe().f_code.co_name
        verb = "GET"
        base_url = f"/games/v1whitelisted/players/{player_id}/applications/played"
        data_type = None # json, data or None
        params = {}
        if page_token: params = {"pageToken": page_token}
        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)
        # Parsing
        data = json.loads(req.text)
        played_games = PlayedGames()
        if not "items" in data:
            print(req)
            print(req.text)
            return False, "", played_games
        next_page_token = data.get("nextPageToken", "")
        played_games._scrape(data["items"])
        return True, next_page_token, played_games

    async def get_achievements(self, as_client: httpx.AsyncClient, player_id: str, page_token: str="") -> Tuple[bool, str, PlayerAchievements]:
        endpoint_name = inspect.currentframe().f_code.co_name
        params = {
            "state": "UNLOCKED",
            "returnDefinitions": True,
            "sortOrder": "RECENT_FIRST"
        }
        data = {}
        if page_token: params["pageToken"] = page_token
        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, "POST", endpoint_name, f"/games/v1whitelisted/players/{player_id}/achievements", params, data, "json")
        # Parsing
        data = json.loads(req.text)
        achievements = PlayerAchievements()
        if not "items" in data:
            print(req)
            print(req.text)
            return False, "", achievements
        next_page_token = ""
        if "nextPageToken" in data: next_page_token = data["nextPageToken"]
        achievements._scrape(data)
        return True, next_page_token, achievements