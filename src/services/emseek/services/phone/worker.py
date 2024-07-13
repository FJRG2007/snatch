import os, requests
import src.lib.colors as cl
from src.lib.config import config
from src.utils.basics import cls, noToken, terminal

def fetch_dymo_data(params):
    try:
        response = requests.get("https://api.tpeoficial.com/v1/private/secure/verify", params=params, headers={"Authorization": f"Bearer {os.getenv('DYMO_API_KEY')}"})
        if response.status_code == 200: 
            r = response.json()
            if not (r["error"]): return r
            elif r["error"] == "❌ Access denied, token expired or incorrect.":
                terminal("e", "Invalid Dymo API Key.")
                return {"tel": {}}
            else: 
                terminal("e", r["error"])
                return {"tel": {}}
        else: 
            terminal("e", "An error occurred while making a Dymo API request.")
            return {"tel": {}}
    except: terminal("e", "Invalid Dymo API Key.")

def main(tel):
    dymo_data = fetch_dymo_data({"tel": tel}) if os.getenv("DYMO_API_KEY") else {"tel": {}}
    data_tel = {
        "disposable": False,
        "prefix": dymo_data["tel"].get("prefix", noToken("Dymo API")),
        "number": dymo_data["tel"].get("number", noToken("Dymo API")),
        "country": dymo_data["tel"].get("country", noToken("Dymo API")),
        "countryCode": dymo_data["tel"].get("countryCode", noToken("Dymo API"))
    }
    # dymo_data["email"].get("disposable", noToken("Dymo API")),
    result = f"""
        Phone: {tel}
            {cl.b}> {cl.w} Valid: True
            {cl.b}> {cl.w} Disposable or Scam: {data_tel['disposable']}
            {cl.b}> {cl.w} Prefix: {data_tel['prefix']}
            {cl.b}> {cl.w} Number: {data_tel['number']}
            {cl.b}> {cl.w} Country: {data_tel['country']}
            {cl.b}> {cl.w} Country Code: {data_tel['countryCode']}
    """
    print(result)