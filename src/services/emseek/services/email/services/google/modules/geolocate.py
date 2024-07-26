from ghunt import globals as gb
from ghunt.helpers.utils import get_httpx_client
from ghunt.apis.geolocation import GeolocationHttp
from ghunt.helpers import auth

import httpx
from geopy.geocoders import Nominatim

from typing import *
from pathlib import Path
import json


async def main(as_client: httpx.AsyncClient, bssid: str, input_file: Path, json_file: Path=None):
    # Verifying args
    body = None
    if input_file:
        if not input_file.exists(): exit(f"[-] The input file \"{input_file}\" doesn't exist.")
        with open(input_file, "r", encoding="utf-8") as f:
            try: body = json.load(f)
            except json.JSONDecodeError: exit("[-] The input file is not a valid JSON file.")

    if not as_client: as_client = get_httpx_client()
    ghunt_creds = await auth.load_and_auth(as_client)
    geo_api = GeolocationHttp(ghunt_creds)
    found, resp = await geo_api.geolocate(as_client, bssid=bssid, body=body)
    if not found: exit("[-] The location wasn't found.")
    geolocator = Nominatim(user_agent="nominatim")
    location = geolocator.reverse(f"{resp.location.latitude}, {resp.location.longitude}", timeout=10)
    raw_address = location.raw['address']
    address = location.address
    print("📍 Location found !\n", style="plum2")
    print(f"🛣️ [italic]Accuracy : {resp.accuracy} meters[/italic]\n")
    print(f"Latitude : {resp.location.latitude}", style="bold")
    print(f"Longitude : {resp.location.longitude}\n", style="bold")
    print(f"🏠 Estimated address : {address}\n")
    print(f"🗺️ link=https://www.google.com/maps/search/?q={resp.location.latitude},{resp.location.longitude} \n")
    if json_file:
        from ..objects.encoders import GHuntEncoder;
        with open(json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps({
                "accuracy": resp.accuracy,
                "latitude": resp.location.latitude,
                "longitude": resp.location.longitude,
                "address": raw_address,
                "pretty_address": address
            }, cls=GHuntEncoder, indent=4))
        print(f"[+] JSON output wrote to {json_file} !")
    await as_client.aclose()