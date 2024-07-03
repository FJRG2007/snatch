import os
import requests
from datetime import datetime
from rich import print as rprint
from ...utils.basics import validTarget
from ...lib.data import requestsHeaders

def main(target, wordlist):
    try:
        # Add Banner.
        print("-" * 50)
        print(f"Scanning Target: {target}")
        print(f"Scanning started at: {str(datetime.now())}")
        print("-" * 50)
        if not validTarget(target): return rprint(f"[red]Error: Enter a valid URL. [/red]")
        # Validate that "wordlist" is a .txt file inside the "customs" folder.
        if wordlist != "./src/lib/files/directory_listing.txt":
            custom_path = os.path.join("customs", wordlist)
            if not (os.path.isfile(custom_path) and custom_path.endswith(".txt")): return rprint("[red]Error: \"wordlist\" must be a .txt file inside the \"customs\" folder.[/red]")
            else: rprint(f"[green]Using custom wordlist: {custom_path}[/green]")
        else: rprint("[cyan]Using auto wordlist.[/cyan]")

        if not validTarget(target): return rprint("[red]Error: Enter a valid URL.[/red]")
        # Read the wordlist file.
        with open(wordlist, "r") as file:
            for line in file:
                word = line.strip()
                # Check if HTTPS or HTTP is used.
                url = f"https://{target}/{word}"
                try:
                    response = requests.get(url, headers={**requestsHeaders, "referer": url})
                    if response.status_code == 200: rprint(f"[green]Found: {url} - {response.status_code}[/green]")
                    else: rprint(f"[yellow]Found: {url} - {response.status_code}[/yellow]")
                except requests.exceptions.RequestException:
                    url = f"http://{target}/{word}"
                    try:
                        response = requests.get(url, headers={**requestsHeaders, "referer": url})
                        if response.status_code == 200: rprint(f"[green]Found: {url} - {response.status_code}[/green]")
                        else: rprint(f"[yellow]Found: {url} - {response.status_code}[/yellow]")
                    except requests.exceptions.RequestException as e: rprint(f"[red]Request Exception: {e}[/red]")
    except KeyboardInterrupt: rprint("[red]Exiting Program: Canceled by user.[/red]")
    except requests.exceptions.RequestException as e: rprint(f"[red]Request Exception: {e}[/red]")
    except Exception as ex: rprint(f"[red]Error: {ex}[/red]")