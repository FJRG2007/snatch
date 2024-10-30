import os, requests
from datetime import datetime
from urllib.parse import urlparse
from src.lib.data import requestsHeaders
from src.utils.basics import terminal, validTarget
import src.utils.bypasses.cloudscraper as cloudscraper
from src.services.directory_listing.modules.wordpress_plugins_list_downloader import download_plugins_list

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

def scan_with_wordlist(target, wordlist, hide, method):
    scraper = cloudscraper.create_scraper()
    with open(wordlist, "r") as file:
        for line in file:
            word = line.strip()
            if method == "directory": url = f"https://{target}/{word}"
            elif method == "subdomain": url = f"https://{word}.{target}"
            try:
                response = scraper.get(url, headers={**requestsHeaders, "referer": url})
                if response.status_code in hide: continue
                if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                else: terminal("w", f"Found: {url} - {response.status_code}")
            except requests.exceptions.ConnectionError: pass
            except requests.exceptions.RequestException:
                if method == "directory": url = f"http://{target}/{word}"
                elif method == "subdomain": url = f"http://{word}.{target}"
                try:
                    response = scraper.get(url, headers={**requestsHeaders, "referer": url})
                    if response.status_code in hide: continue
                    if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                    else: terminal("w", f"Found: {url} - {response.status_code}")
                except requests.exceptions.ConnectionError: pass
                except requests.exceptions.RequestException as e: terminal("e", e)

def main(target, method, wordlist, hide, scan_wordpress_plugins):
    try:
        # Add Banner
        print("-" * 50)
        print(f"Scanning target: {target}")
        print(f"Codes that are not displayed: {hide}")
        print(f"Scanning started at: {str(datetime.now())}")
        print("-" * 50)

        if not validTarget(target): return terminal("e", "Enter a valid URL.")
        if method not in ["directory", "subdomain"]: return terminal("e", "Invalid method.", exitScript=True)

        try: hide = parse_hide_codes(hide)
        except: return terminal("e", "Invalid range for \"hide codes\".", exitScript=True)

        # Validate wordlist file path
        if wordlist != "./src/lib/files/directory_listing/directory_listing.txt":
            custom_path = os.path.join("customs", "directory_listing", wordlist)
            if not (os.path.isfile(custom_path) and custom_path.endswith(".txt")): return terminal("e", "\"wordlist\" must be a .txt file inside the \"customs\" folder.")
            else: terminal("s", f"Using custom wordlist: {custom_path}")

        if method == "directory":
            if scan_wordpress_plugins:
                terminal("i", "Downloading WordPress plugins list...")
                download_plugins_list()
                terminal("i", "Scanning WordPress plugins...")
                scan_with_wordlist(f"${urlparse(target).netloc}/wp-content/plugins", "./src/lib/files/directory_listing/wordpress/plugins.txt", hide, "directory")
                terminal("i", "Using auto wordlist...")
                scan_with_wordlist(target, wordlist, hide, method)
            else:
                terminal("i", "Using auto wordlist...")
                scan_with_wordlist(target, wordlist, hide, method)
                terminal("i", "Downloading WordPress plugins list...")
                download_plugins_list()
                terminal("i", "Scanning WordPress plugins...")
                scan_with_wordlist(f"${urlparse(target).netloc}/wp-content/plugins", "./src/lib/files/directory_listing/wordpress/plugins.txt", hide, "directory")
        else:
            if scan_wordpress_plugins: terminal("e", "Cannot scan WordPress plugins with subdomain method.", exitScript=True)
            else:
                terminal("i", "Using auto wordlist...")
                scan_with_wordlist(target, wordlist, hide, method)
    except KeyboardInterrupt: terminal("i", "Process interrupted by user.")
    except requests.exceptions.RequestException as e: terminal("e", e)
    except Exception as e: terminal("e", e)