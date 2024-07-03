import json
import click
from rich import print as rprint
from urllib.parse import urlparse
from ...utils.basics import validURL
from .downloader import downloader
from urllib.parse import urljoin, urlparse

# Functions / services.
from .services import *

def main(inputData, dtype, format):
    if inputData.startswith("http"):
        domain = urlparse(inputData).netloc
        parsed_url = urlparse(inputData)
        destination_folder = f"downloads/{parsed_url.netloc}/{parsed_url.path.strip("/").replace("/", "-")}"
        if not os.path.exists(destination_folder): os.makedirs(destination_folder)
        if (validURL(inputData)):
            if domain in ["www.youtube.com", "youtube.com", "youtu.be"]: return youtube.youtube(inputData, dtype, format)
            if domain in ["x.com", "twitter.com", "t.co"]: return x_twitter.x_twitter(inputData, dtype, format)
            downloader(inputData)
        else: click.echo("[red]Invalid URL.[/red]", err= True)
    else:
        try:
            with open("downloads.json", "r") as file:
                data = json.load(file)
                if len(data) == 0: return rprint(f"[red]Error: The \"downloads.json\" file has no links to download.[/red]")
                ...
        except KeyboardInterrupt:
            rprint("[red]Exiting Program: Canceled by user.[/red]")
        except FileNotFoundError:
            with open("downloads.json", "w") as file:
                json.dump([], file)
            rprint(f"[red]Error: The \"downloads.json\" file has no links to download.[/red]")
        except json.JSONDecodeError: rprint(f"[red]Error: Decoding error \"downloads.json\".[/red]")