import json
import click
from src.lib.data import pre_cmd, INFO_MARKDOWN
from rich import print as rprint
from urllib.parse import urlparse
from .utils.basics import validURL

# Functions / services.
from .services import *

def main(inputData, dtype, format):
    if inputData.startswith("http"):
        domain = urlparse(inputData).netloc
        if (validURL(inputData)):
            if "youtube.com" in domain or domain == "youtu.be": youtube.youtube(inputData, dtype, format)
        else:
            click.echo("Invalid URL.", err= True)
    else:
        try:
            with open("downloads.json", "r") as file:
                data = json.load(file)
                if len(data) == 0: return rprint(f"[red]Error: The \"downloads.json\" file has no links to download.[/red]")
                ...
        except FileNotFoundError:
            with open("downloads.json", "w") as file:
                json.dump([], file)
            rprint(f"[red]Error: The \"downloads.json\" file has no links to download.[/red]")
        except json.JSONDecodeError:
            rprint(f"[red]Error: Decoding error \"downloads.json\".[/red]")