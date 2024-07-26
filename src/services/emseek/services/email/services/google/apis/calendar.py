from ..objects.base import GHuntCreds
from ..errors import *
from .. import globals as gb
from ..objects.apis import GAPI
from ..parsers.calendar import Calendar, CalendarEvents

import httpx

from typing import *
import inspect
import json
from datetime import datetime, timezone


class CalendarHttp(GAPI):
    def __init__(self, creds: GHuntCreds, headers: Dict[str, str] = {}):
        super().__init__()
        if not headers: headers = gb.config.headers
        base_headers = {}
        headers = {**headers, **base_headers}
        self.hostname = "clients6.google.com"
        self.scheme = "https"

        self.authentication_mode = "sapisidhash" # sapisidhash, cookies_only, oauth or None
        self.require_key = "calendar" # key name, or None

        self._load_api(creds, headers)

    async def get_calendar(self, as_client: httpx.AsyncClient, calendar_id: str) -> Tuple[bool, Calendar]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/calendar/v3/calendars/{calendar_id}"
        data_type = None # json, data or None

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, None, None, data_type)

        # Parsing
        data = json.loads(req.text)

        calendar = Calendar()
        if "error" in data:
            return False, calendar
        
        calendar._scrape(data)

        return True, calendar

    async def get_events(self, as_client: httpx.AsyncClient, calendar_id: str, params_template="next_events",
                        time_min=datetime.today().replace(tzinfo=timezone.utc).isoformat(), max_results=250, page_token="") -> Tuple[bool, CalendarEvents]:
        endpoint_name = inspect.currentframe().f_code.co_name

        verb = "GET"
        base_url = f"/calendar/v3/calendars/{calendar_id}/events"
        data_type = None # json, data or None
        params_templates = {
            "next_events": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": max_results,
                "timeMin": time_min # ISO Format
            },
            "from_beginning": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": max_results
            },
            "max_from_beginning": {
                "calendarId": calendar_id,
                "singleEvents": True,
                "maxAttendees": 1,
                "maxResults": 2500 # Max
            }
        }

        if not params_templates.get(params_template):
            raise GHuntParamsTemplateError(f"The asked template {params_template} for the endpoint {endpoint_name} wasn't recognized by ..")

        params = params_templates[params_template]
        if page_token:
            params["pageToken"] = page_token

        self._load_endpoint(endpoint_name)
        req = await self._query(as_client, verb, endpoint_name, base_url, params, None, data_type)

        # Parsing
        data = json.loads(req.text)

        events = CalendarEvents()
        if not data:
            return False, events
        
        events._scrape(data)

        return True, events