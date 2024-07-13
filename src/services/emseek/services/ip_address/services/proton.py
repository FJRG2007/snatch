import requests

# Find if your IP is currently affiliated to ProtonVPN.
def checkIPProtonVPN(ip):
    return str(ip) in requests.get("https://api.protonmail.ch/vpn/logicals").text