import os, requests
import src.lib.colors as cl
from src.lib.config import config
from src.lib.clients import dymo_client
from src.utils.basics import cls, noToken, terminal, setColor, getTypeString

# Utils.
from .services.proton.worker import main as protonMailManager
from .services.google.worker import main as gmailManager

def fetch_snatch_data(email):
    user, domain = email.split("@")
    if domain in ["protonmail.com", "proton.me", "protonmail.ch", "pm.me"]: protonMailManager(email)
    if domain == "gmail.com": gmailManager(email)

def fetch_dymo_data(params):
    try:
        if not dymo_client: 
            terminal("e", "Invalid Dymo API Key.")
            return {"email": {}}
        return dymo_client.is_valid_data(params)
    except: terminal("e", "Invalid Dymo API Key.")

def fetch_hunter_data(email):
    try:
        h_api = config.get_api_key("HUNTER")
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
        terminal("e", "Invalid Hunter API Key.")
        return {}
    
def fetch_trustfull_data(email):
    try:
        tf_api = config.get_api_key("TRUSTFULL")
        response = requests.post("https://api.fido.id/1.0/email", headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-api-key": tf_api
        }, params={
            "customer_id": os.getenv("TRUSTFULL_CUSTOMER_ID"),
            "claims": ["email"],
            "email": email
        })
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
        terminal("e", "Invalid Hunter API Key.")
        return {}

def scanner(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    cls()
    dymo_data = fetch_dymo_data({"email": input_data}) if os.getenv("DYMO_API_KEY") else {"email": {}}
    hunter_data = fetch_hunter_data(input_data)
    snatch_data = fetch_snatch_data(input_data)
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
            {cl.b}> {cl.w} Disposable or scam: {setColor(data_email['disposable'])}
            {cl.b}> {cl.w} Free subdomain: {setColor(data_email['freeSubdomain'])}
            {cl.b}> {cl.w} Corporate: {setColor(data_email['corporate'])}
            {cl.b}> {cl.w} User: {data_email['user']}
            {cl.b}> {cl.w} Role account: {setColor(data_email['roleAccount'])}
            {cl.b}> {cl.w} Gibberish: {setColor(data_email['gibberish'])}
            {cl.b}> {cl.w} MX records: {setColor(data_email['mx_records'])}
            {cl.b}> {cl.w} SMTP server: {setColor(data_email['smtp_server'])}
            {cl.b}> {cl.w} SMTP check: {setColor(data_email['smtp_check'])}
            {cl.b}> {cl.w} Domain: {data_email['domain']}
            {cl.b}> {cl.w} Pwned: {setColor(data_email['pwned'])}
            {cl.b}> {cl.w} Block: {setColor(data_email['block'])}
    """
    print(result)