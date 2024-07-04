import json
import click
from urllib.parse import urlparse
from .downloader import downloader
from ...utils.basics import terminal
from ...utils.basics import validURL

# Functions / services.
from .services import *

def main(inputData, dtype, format):
    if inputData.startswith("http"):
        domain = urlparse(inputData).netloc
        parsed_url = urlparse(inputData)
        destination_folder = f"output/downloads/{parsed_url.netloc}/{parsed_url.path.strip('/').replace('/', '-')}"
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
                if len(data) == 0: return terminal("e", f"[red]The \"output/downloads.json\" file has no links to download.")
                ...
        except KeyboardInterrupt: terminal(KeyboardInterrupt)
        except FileNotFoundError:
            with open("output/downloads.json", "w") as file:
                json.dump([], file)
            terminal("e", f"The \"output/downloads.json\" file has no links to download.")
        except json.JSONDecodeError: terminal("e", f"Decoding error \"output/downloads.json\".")