from pprint import pprint
from dateutil.parser import parse
from src.utils.basics import cls, terminal
import os, re, sys, time, json, whois, socket, requests

# Get domain IP Address.
def domain_ip(domain):
    try: domain_ip = socket.gethostbyname(domain)
    except Exception as e: return

    print("\n\033[0;35m\033[1mDomain IP: \033[1m\033[0;32m\n")
    print(domain_ip)

    ip_address = domain_ip
    print("\n\033[0;35m\033[1mIP Data:\n\033[0m\033[0;32m")
    pprint(requests.get(f'https://ipapi.co/{ip_address}/json/').json())

    print("\n\n\033[0;35m\033[1mDouble IP verification using IPinfo.io")
    print("\n\033[0;35m\033[1mResults:\033[0m\033[0;32m")

    data = json.loads(requests.get(f'https://ipinfo.io/{ip_address}/json').text)

    print("ip:", data['ip'])
    print("organization:", data['org'])
    print("city:", data['city'])
    print("region:", data['region']),\
    print("country:", data['country'])
    print("postal:", data['postal'])
    print("location:", data['loc'])
    print("timezone", data['timezone'])


# Reverse IP lookup using limited searches with the Hacker Target free test API to extract all domains using the same IP.
def rev_ip_free(domain_ip, domain):
    print("\n\033[0;32mOne moment ...checking Hackertarget.com status\033[0m")
    request = requests.get("http://api.hackertarget.com/reverseiplookup")
    if request.status_code == 200: print("\n\033[0;32mstatus code 200!\033[0m Hacker Target is \033[0;32m\033[1monline\033[0m\033[0;35m\033[1m\n\nReverse IP search results:\033[0m\033[0;32m\n")
    else: print('\033[0;32mResponse Failed, try again later')
    # Free Hacker Target API with limited searches. 
    print(requests.request("GET", "http://api.hackertarget.com/reverseiplookup", params={"q": domain_ip}).text)


# Reverse IP lookup using Hacker Target API to extract all domains using the same IP address.
def rev_ip_api(domain_ip, domain):
    api_key = os.getenv("HACKERTARGET_API_KEY")
    if not api_key or not len(api_key) > 7: return terminal("e", "Invalid Hacker Target API Key.") 
    print("\n\033[0;32mOne moment ...checking Hackertarget.com status\033[0m")
    request = requests.get("http://api.hackertarget.com/reverseiplookup")
    if request.status_code == 200: print("\n\n\033[0;32mstatus code 200!\033[0m Hacker Target is \033[0;32m\033[1monline\033[0m\033[0;35m\033[1m\n\nReverse IP search results:\033[0m\033[0;32m\n")
    else: print('\033[0;32mResponse Failed, try again later')

# Search DNS Records free.
def dns_records_free(domain):
    print("\n\033[0;35m\033[1mDNS Records search results:\033[0m\033[0;32m\n")
    print(requests.request("GET", "https://api.hackertarget.com/dnslookup/", params={"q": domain}).text)

# Using your own Hacker Target API to avoid restrictions.
def dns_records_api(domain):
    api_key = os.getenv("HACKERTARGET_API_KEY")
    if not api_key or not len(api_key) > 7: return terminal("e", "Invalid Hacker Target API Key.")
    print("\n\033[0;35m\033[1mDNS Records search results:\033[0m\033[0;32m\n")
    print(requests.request("GET", f"https://api.hackertarget.com/dnslookup/?q={domain}&apikey={api_key}", params={"q": domain}).text)

# Search further domain information with the Whois module.
def whois_search(domain):
    print("\n\n\033[0;35m\033[1mLet's try and find more domain information!\033[0m")
    whois_information = whois.whois(domain)
    # WHOis results easy to read.
    print("\n\033[0;32mDomain Name:", whois_information.domain_name)
    print("\nDomain registrar:", whois_information.registrar)
    print("\nWHOis server:", whois_information.whois_server)
    print("\nDomain creation date:", whois_information.creation_date)
    print("\nExpiration date:", whois_information.expiration_date)
    print("\nUpdated Date:", whois_information.updated_date)
    print("\nServers:", whois_information.name_servers)
    print("\nStatus:", whois_information.status)
    print("\nEmail Addresses:", whois_information.emails)
    print("\nName:", whois_information.name)
    print("\nOrg:", whois_information.org)
    print("\nAddress:", whois_information.address)
    print("\nCity:", whois_information.city)
    print("\nState:", whois_information.state)
    print("\nZipcode:", whois_information.zipcode)
    print("\nCountry:", whois_information.country)

# Site Certificate search with CRT.SH
def crt_sh(domain_name):
    try:
        r = requests.get("https://crt.sh/", params={'q': domain_name, 'output': 'json'})
        r.raise_for_status()
        nameparser = re.compile("([a-zA-Z]+)=(\"[^\"]+\"|[^,]+)")
        certs = []
        for c in r.json():
            if not c['entry_timestamp']: continue
            certs.append({
                'id': c['id'],
                'logged_at': parse(c['entry_timestamp']),
                'not_before': parse(c['not_before']),
                'not_after': parse(c['not_after']),
                'name': c['name_value'],
                'ca': {
                    'caid': c['issuer_ca_id'],
                    'name': c['issuer_name'],
                    'parsed_name': dict(nameparser.findall(c['issuer_name']))
                }
            })
    except: return terminal("e", "An error occurred while processing the certificates.")
    print("\n\033[0;35m\033[1mWebsite cert. search results:\033[0m\n\033[0;32m")
    pprint(certs[:6])
    api_key = os.getenv("WHOIS_XML_API_KEY")
    if not api_key or not len(api_key) > 7: return terminal("e", "Invalid Whois XML API Key.") 
    try:
        print("\n\033[0;35m\033[1mOK! Let's check domain reputation using WhoisXML API\n\033[0m")
        print("\n\n\033[0;35m\033[1mDomain Reputation check results:\n\n\033[0;32m")
        pprint(requests.request("GET", f"https://domain-reputation.whoisxmlapi.com/api/v2?apiKey={api_key}&domainName={domain_name}", params={"q": domain_name}).text)
    except: return terminal("e", "An error occurred while processing the certificates.")


# WebOSINT Subscan (Subdomain Scanner)
def subdomain_scanner(domain_name):
    subdomains_found = []
    sdsreq = requests.get(f'https://crt.sh/?q={domain_name}&output=json')
    if sdsreq.status_code == 200: print('\033[0;32m\033[1m\n\nScanning for subdomains now...')
    else:
        print("\033[0;32mThe subdomain scanner tool is currently offline, please try again in a few minutes!\033[0m")
        sys.exit(1)
    for (key, value) in enumerate(sdsreq.json()):
        subdomains_found.append(value['name_value'])
    print(f"\n\n\033[0;35m\033[1mYour chosen targeted Domain for the Subdomain scan:\033[0;32m{domain_name}\033[0m\033[0;32m\n")
    subdomains = sorted(set(subdomains_found))
    for sub_link in subdomains:
        print(f'\033[1m[✅ Subdomain Found]\033[0m\033[0;32m -->{sub_link}')
    print("\n\033[1m\033[0;35m\033[1mSubdomain Scan Completed!  \033[0;32m\033[1m- ALL Subdomains have been Found")

# Whois History using your WhoisFreaks API Key.
def whois_history(domain_name):
    api_key = os.getenv("WHOIS_FREAKS_API_KEY")
    if not api_key or not len(api_key) > 7: return terminal("e", "Invalid WhoisFreacks API Key.") 
    print("\n\033[0;35m\033[1mOK Let's do this and check Historical Whois using your Whois Freaks API ;-)\n\033[0m")

    time.sleep(2)

    print("\n\033[0;35m\033[1mHistorical Whois results:\n\n\033[0;32m")
    pprint(requests.request("GET", f"https://api.whoisfreaks.com/v1.0/whois?apiKey={api_key}&whois=historical&domainName={domain_name}", params={"q": domain_name}).text)


# Main.
def main(domain):
    cls()
    ip = domain_ip(domain)
    if not os.getenv("HACKERTARGET_API_KEY"): 
        rev_ip_free(ip, domain)
        dns_records_free(domain)
    else: 
        rev_ip_api(ip, domain)
        dns_records_api(domain)
    whois_search(domain)
    crt_sh(domain)
    subdomain_scanner(domain)
    whois_history(domain)
    terminal("s", "Domain scan successfully completed.", exitScript=True)