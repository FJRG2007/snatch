from pathlib import Path
from PIL import Image
from typing import *
from time import time
from datetime import timezone
from dateutil.parser import isoparse
from copy import deepcopy
import json, httpx, hashlib, imagehash, jsonpickle
from io import BytesIO
from ..lib.httpx import AsyncClient

def get_httpx_client() -> httpx.AsyncClient:
    # Returns a customized to better support the needs of GHunt CLI users.
    return AsyncClient(http2=True, timeout=15)
    # return AsyncClient(http2=True, timeout=15, proxies="http://127.0.0.1:8282", verify=False)

def oprint(obj: any) -> str:
    print(json.dumps(json.loads(jsonpickle.encode(obj)), indent=2))

def within_docker() -> bool:
    return Path('/.dockerenv').is_file()

def gen_sapisidhash(sapisid: str, origin: str, timestamp: str = str(int(time()))) -> str:
    return f"{timestamp}_{hashlib.sha1(' '.join([timestamp, sapisid, origin]).encode()).hexdigest()}"

def inject_osid(cookies: Dict[str, str], osids: Dict[str, str], service: str) -> Dict[str, str]:
    cookies_with_osid = deepcopy(cookies)
    cookies_with_osid["OSID"] = osids[service]
    return cookies_with_osid
    
def is_headers_syntax_good(headers: Dict[str, str]) -> bool:
    try:
        httpx.Headers(headers)
        return True
    except: return False

async def get_url_image_flathash(as_client: httpx.AsyncClient, image_url: str) -> str:
    return str(imagehash.average_hash(Image.open(BytesIO(await as_client.get(image_url).content))))

async def is_default_profile_pic(as_client: httpx.AsyncClient, image_url: str) -> Tuple[bool, str]:
    """
        Returns a boolean which indicates if the image_url
        is a default profile picture, and the flathash of
        the image.
    """
    flathash = await get_url_image_flathash(as_client, image_url)
    if imagehash.hex_to_flathash(flathash, 8) - imagehash.hex_to_flathash("000018183c3c0000", 8) < 10 : return True, str(flathash)
    return False, str(flathash)

def get_class_name(obj) -> str:
        return str(obj).strip("<>").split(" ")[0]

def get_datetime_utc(date_str):
    # Converts ISO to datetime object in UTC.
    date = isoparse(date_str)
    return date.replace(tzinfo=timezone.utc) - date.utcoffset()

def ppnb(nb: float|int) -> float:
    """
        Pretty print float number
        Ex: 3.9 -> 3.9
            4.0 -> 4
            4.1 -> 4.1
    """
    try: return int(nb) if nb % int(nb) == 0.0 else nb
    except ZeroDivisionError:
        if nb == 0.0: return 0
        else: return nb

def parse_oauth_flow_response(body: str):
    """
        Correctly format the response sent by android.googleapis.com
        during the Android OAuth2 Login Flow.
    """
    return {sp[0]:'='.join(sp[1:]) for x in body.split("\n") if (sp := x.split("="))}

def humanize_list(array: List[any]):
    """
        Transforms a list to a human sentence.
        Ex : ["reader", "writer", "owner"] -> "reader, writer and owner".
    """
    if len(array) <= 1: return ''.join(array)
    final = ""
    for nb, item in enumerate(array):
        if nb == 0: final += f"{item}"
        elif nb+1 < len(array): final += f", {item}"
        else: final += f" and {item}"
    return final

def unicode_patch(txt: str):
    bad_chars = {
        "é": "e",
        "è": "e",
        "ç": "c",
        "à": "a"
    }
    return txt.replace(''.join([*bad_chars.keys()]), ''.join([*bad_chars.values()]))