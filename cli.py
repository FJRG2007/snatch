import click
import pyfiglet
from src.lib import data
from src.lib.config import config
from textual.widgets import Markdown
from src.utils.basics import terminal

from textual.app import App, ComposeResult

# Functionalities.
from src.services.ai.worker import main as aiWoker
from src.services.downloader.worker import main as downloaderWorker
from src.services.directory_listing.worker import main as directoryListing
from src.services.portscanner.worker import main as portscanner
from src.services.whatsapp.worker import main as whatsappWorker
from src.services.ai.worker import main as aiWoker

@click.group()
def cli():
    print(pyfiglet.figlet_format("SNATCH"))

@cli.command()
def info():
    class MarkdownExampleApp(App):
        def compose(self) -> ComposeResult:
            yield Markdown(data.INFO_MARKDOWN)
    app = MarkdownExampleApp()
    app.run()

@cli.command()
@click.argument("prompt", required=True)
def ai(prompt):
    if not prompt: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} ai --help\" for further help.")
    aiWoker(prompt)

@cli.command()
@click.argument("url", required=False)
@click.argument("local", type=click.File("rb"), required=False)
@click.option("--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("--format", default="auto", type=str, help="In case of reloading a resource, choose the format.")
def download(url, local, dtype, format):
    if not url and not local: terminal("e", f"[red]Error: Enter a valid option; run \"{data.pre_cmd} download --help\" for further help.[/red]")
    if (url): downloaderWorker(url, dtype, format)
    elif (local): downloaderWorker(local, dtype, format)

@cli.command()
@click.argument("target", required=True)
@click.option("--wordlist", default="./src/lib/files/directory_listing.txt", type=str, help="Dictionary with routes.")
def dirlist(target, wordlist):
    if not target: terminal("e", f"[red]Error: Enter a valid option; run \"{data.pre_cmd} dirlist --help\" for further help.[/red]")
    directoryListing(target, wordlist)

@cli.command()
@click.argument("ip", required=True)
@click.option("--ports", default="*", type=str, help="Ports to be scanned (1,2,3 or 16-24 or *-24 or 24-* or * or common).")
@click.option("--saveonfile", default=False, type=bool, help="Saves the open ports in a file.")
def portscan(ip, ports, saveonfile):
    if not ip: terminal("e", f"[red]Error: Enter a valid option; run \"{data.pre_cmd} portscan --help\" for further help.[/red]")
    portscanner(ip, ports, saveonfile)
    
@cli.command()
@click.argument("username", required=True)
@click.argument("language", required=True)
def whatsapp(username, language):
    if not username or not language: terminal("e", f"[red]Error: Enter a valid option; run \"{data.pre_cmd} whatsapp --help\" for further help.[/red]")
    whatsappWorker(username, language)

if __name__ == "__main__":
    cli()