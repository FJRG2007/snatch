import os, requests
from datetime import datetime
from src.lib.data import requestsHeaders
from src.utils.basics import terminal, validTarget

def main(target, wordlist):
    try:
        # Add Banner.
        print("-" * 50)
        print(f"Scanning Target: {target}")
        print(f"Scanning started at: {str(datetime.now())}")
        print("-" * 50)
        if not validTarget(target): return terminal("e", "Enter a valid URL.")
        # Validate that "wordlist" is a .txt file inside the "customs" folder.
        if wordlist != "./src/lib/files/directory_listing.txt":
            custom_path = os.path.join("customs", "directory_listing", wordlist)
            if not (os.path.isfile(custom_path) and custom_path.endswith(".txt")): return terminal("e", "\"wordlist\" must be a .txt file inside the \"customs\" folder.")
            else: terminal("s", f"Using custom wordlist: {custom_path}")
        else: terminal("i", "Using auto wordlist.")

        if not validTarget(target): return terminal("e", "Enter a valid URL.")
        # Read the wordlist file.
        with open(wordlist, "r") as file:
            for line in file:
                word = line.strip()
                # Check if HTTPS or HTTP is used.
                url = f"https://{target}/{word}"
                try:
                    response = requests.get(url, headers={**requestsHeaders, "referer": url})
                    if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                    else: terminal("w", f"Found: {url} - {response.status_code}")
                except requests.exceptions.RequestException:
                    url = f"http://{target}/{word}"
                    try:
                        response = requests.get(url, headers={**requestsHeaders, "referer": url})
                        if response.status_code == 200: terminal("s", f"Found: {url} - {response.status_code}")
                        else: terminal("s", f"Found: {url} - {response.status_code}")
                    except requests.exceptions.RequestException as e: terminal("e", e)
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except requests.exceptions.RequestException as e: terminal("e", e)
    except Exception as e: terminal("e", e)