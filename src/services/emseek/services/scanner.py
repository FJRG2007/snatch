import os, requests
import src.lib.colors as cl
from src.lib.config import config
from src.utils.basics import cls, terminal, setColor, getTypeString

params = {
    "email": "test@test.com",
    "tel": "+34617509462",
    "domain": "test.com",
    "creditCard": "5110929780543845",
    "ip": "52.94.236.248"
}

def noToken(name): return f"{cl.y}Set up your {name} token{cl.w}"

def fetch_dymo_data(params):
    try:
        response = requests.get("https://api.tpeoficial.com/v1/private/secure/verify", params=params, headers={"Authorization": f"Bearer {os.getenv('DYMO_API_KEY')}"})
        if response.status_code == 200: 
            r = response.json()
            if not (r["error"]): return r
            else: 
                terminal("e", r["error"])
                return {"email": {}}
        else: 
            terminal("e", "An error occurred while making a Dymo API request.")
            return {"email": {}}
    except: terminal("e", "Invalid Hunter API KEY.")
def fetch_hunter_data(email):
    try:
        h_api = config.getAPIKey("HUNTER")
        response = requests.get(f"https://api.hunter.io/v2/email-verifier", params={"email": email, "api_key": h_api})
        data = response.json()
        if not data.get("errors"):
            return {
                "regexp": data['data']['regexp'],
                "gibberish": data['data']['gibberish'],
                "mx_records": data['data']['mx_records'],
                "smtp_server": data['data']['smtp_server'],
                "smtp_check": data['data']['smtp_check'],
                "block": data['data']['block']
            }
        else: 
            terminal("e", data["errors"][0]["details"])
            return {}
    except Exception as e:
        terminal("e", "Invalid Hunter API KEY.")
        return {}

def scanner(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    cls()
    typeStr = getTypeString(input_data)
    if (typeStr == "email"):
        dymo_data = fetch_dymo_data({"email": input_data}) if os.getenv("DYMO_API_KEY") else {"email": {}}
        hunter_data = fetch_hunter_data(input_data)
        data_email = {
            "disposable": dymo_data["email"].get("disposable", noToken("Dymo API")),
            "freeSubdomain": dymo_data["email"].get("freeSubdomain", noToken("Dymo API")),
            "corporate": dymo_data["email"].get("corporate", noToken("Dymo API")),
            "user": input_data.split("@")[0],
            "roleAccount": dymo_data["email"].get("roleAccount", noToken("Dymo API")),
            "gibberish": hunter_data.get("gibberish", noToken("Hunter")),
            "domain": input_data.split("@")[1],
            "mx_records": hunter_data.get("mx_records", noToken("Hunter")),
            "smtp_server": hunter_data.get("smtp_server", noToken("Hunter")),
            "smtp_check": hunter_data.get("smtp_check", noToken("Hunter")),
            "pwned": dymo_data["email"].get("pwned", noToken("Dymo API")),
            "regexp": hunter_data.get("regexp", noToken("Hunter")),
            "block": hunter_data.get("block", noToken("Hunter"))
        }
        result = f"""
            Email: {input_data}
                {cl.b}> {cl.w} Valid: {cl.g}True{cl.w}
                {cl.b}> {cl.w} Disposable or Scam: {setColor(data_email['disposable'])}
                {cl.b}> {cl.w} Free Subdomain: {setColor(data_email['freeSubdomain'])}
                {cl.b}> {cl.w} Corporate: {setColor(data_email['corporate'])}
                {cl.b}> {cl.w} User: {data_email['user']}
                {cl.b}> {cl.w} Role Account: {setColor(data_email['roleAccount'])}
                {cl.b}> {cl.w} Gibberish: {setColor(data_email['gibberish'])}
                {cl.b}> {cl.w} MX Records: {setColor(data_email['mx_records'])}
                {cl.b}> {cl.w} SMTP Server: {setColor(data_email['smtp_server'])}
                {cl.b}> {cl.w} SMTP Check": {setColor(data_email['smtp_check'])}
                {cl.b}> {cl.w} Domain: {data_email['domain']}
                {cl.b}> {cl.w} Pwned: {setColor(data_email['pwned'])}
                {cl.b}> {cl.w} Block: {setColor(data_email['block'])}
        """
    elif (typeStr == "tel"):
        dymo_data = fetch_dymo_data({"tel": input_data}) if os.getenv("DYMO_API_KEY") else {"tel": {}}
        data_tel = {
            "disposable": False,
            "prefix": "34",
            "number": "617509462",
            "country": "Spain",
            "countryCode": "ES"
        }
        result = f"""
            Phone: {input_data}
                {cl.b}> {cl.w} Valid: True
                {cl.b}> {cl.w} Disposable or Scam: {data_tel['disposable']}
                {cl.b}> {cl.w} Prefix: {data_tel['prefix']}
                {cl.b}> {cl.w} Number: {data_tel['number']}
                {cl.b}> {cl.w} Country: {data_tel['country']}
                {cl.b}> {cl.w} Country Code: {data_tel['countryCode']}
        """
    print(result)
    