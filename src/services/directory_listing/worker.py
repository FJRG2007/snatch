import os, requests
from datetime import datetime
from src.lib.data import requestsHeaders
from src.utils.basics import terminal, validTarget
import src.utils.bypasses.cloudscraper as cloudscraper

def parse_hide_codes(hide):
    hide_codes = set()
    hide = hide.replace(" ", "")
    for r in hide.split(","):
        if not r: continue
        if "XX" in r:
            if len(r) != 3 or not r[0].isdigit(): raise ValueError(f"Invalid range: {r}")
            base = int(r[0]) * 100
            hide_codes.update(range(base, base + 100))
        else:
            if not r.isdigit(): raise ValueError(f"Invalid code: {r}")
            hide_codes.add(int(r))
    
    return hide_codes

def main(target, wordlist, hide):
    try:
        # Add Banner.
        print("-" * 50)
        print(f"Scanning Target: {target}")
        print(f"Codes that are not displayed: {hide}")
        print(f"Scanning started at: {str(datetime.now())}")
        print("-" * 50)
        if not validTarget(target): return terminal("e", "Enter a valid URL.")
        try: hide = parse_hide_codes(hide)
        except: return terminal("e", "Invalid range for \"hide codes\".", exitScript=True)
        # Validate that "wordlist" is a .txt file inside the "customs" folder.
        if wordlist != "./src/lib/files/directory_listing.txt":
            custom_path = os.path.join("customs", "directory_listing", wordlist)
            if not (os.path.isfile(custom_path) and custom_path.endswith(".txt")): return terminal("e", "\"wordlist\" must be a .txt file inside the \"customs\" folder.")
            else: terminal("s", f"Using custom wordlist: {custom_path}")
        else: terminal("i", "Using auto wordlist.")

        if not validTarget(target): return terminal("e", "Enter a valid URL.")
        # Read the wordlist file.
        with open(wordlist, "r") as file:
            scraper = cloudscraper.create_scraper()
            for line in file:
                word = line.strip()
                # Check if HTTPS or HTTP is used.
                url = f"https://{target}/{word}"
                try:
                    response = scraper.get(url, headers={**requestsHeaders, "referer": url})
                    if response.status_code in hide: continue
                    if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                    else: terminal("w", f"Found: {url} - {response.status_code}")
                except requests.exceptions.RequestException:
                    url = f"http://{target}/{word}"
                    try:
                        response = scraper.get(url, headers={**requestsHeaders, "referer": url})
                        if response.status_code in hide: continue
                        if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                        else: terminal("s", f"Found: {url} - {response.status_code}")
                    except requests.exceptions.RequestException as e: terminal("e", e)
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except requests.exceptions.RequestException as e: terminal("e", e)
    except Exception as e: terminal("e", e)