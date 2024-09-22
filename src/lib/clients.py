import os
from dymoapi import DymoAPI

DYMO_API_KEY = os.getenv("DYMO_API_KEY")

if DYMO_API_KEY and len(DYMO_API_KEY) > 15:
    dymo_client = DymoAPI({
        "api_key": os.getenv("DYMO_API_KEY")
    })
else: dymo_client = None