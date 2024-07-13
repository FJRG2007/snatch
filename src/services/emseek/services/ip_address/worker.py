import asyncio, requests
import src.lib.colors as cl
from datetime import datetime
from src.utils.basics import cls, terminal, setColor, getTypeString

from .services.os import getOSName
from .services.proton import checkIPProtonVPN

def geoip(ip):
    dict_data = {"city": None, "region": None, "country": None, "org": None}
    for x in ["city", "region", "country", "org"]:
        response = requests.get(f"https://ipinfo.io/{ip}/{x}")
        if response.status_code == 200:
            result = response.content.decode("utf-8").replace("\n", "")
            if result != "": dict_data[x] = result
            else: dict_data[x] = "Unknown."
        else: dict_data[x] = 404
    if dict_data["city"] == 404: return "IP address out of range or forbidden."
    else: return dict_data

def main(ip):
    # Add Banner.
    print(f"" + "-" * 50)
    print(f"Scanning IP address: {ip}")
    print(f"Scanning started at: {str(datetime.now())}")
    print("-" * 50 + f"\n{cl.w}")
    ip_data = {
        "found_in": {
            "protonVPN": checkIPProtonVPN(ip)
        },
        "os": asyncio.run(getOSName(ip)),
        "geo": geoip(ip)
    }
    if isinstance(ip_data["geo"], dict) and ip_data["geo"]["city"]: geo_show = f"""
            City: {ip_data["geo"]["city"]}
            Region: {ip_data["geo"]["region"]}
            Country: {ip_data["geo"]["region"]}
            ISP: {ip_data["geo"]["org"]}
"""   
    else: geo_show = f"{cl.y}{ip_data['geo']}"
    result = f"""{cl.w}
    IP: {ip}
        {cl.b}> {cl.w} IP affiliated to ProtonVPN: {setColor(ip_data["found_in"]["protonVPN"])}
        {cl.b}> {cl.w} Operating system: {setColor(ip_data["os"])}
        {cl.b}> {cl.w} Geolocation: {geo_show}
"""
    print(result)
