import click
import pyfiglet
import src.lib.data as data
from rich import print as rprint
from src.lib.config import config
from textual.widgets import Markdown

from textual.app import App, ComposeResult

# Functionalities.
from src.downloader.worker import main as downloaderWorker
from src.portscanner.worker import main as portscanner

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
@click.argument("url", required=False)
@click.argument("local", type=click.File("rb"), required=False)
@click.option("--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("--format", default="auto", type=str, help="In case of reloading a resource, choose the format.")
def download(url, local, dtype, format):
    if not url and not local: rprint(f"[red]Error: Enter a valid option; run \"{data.pre_cmd} download --help\" for further help.[/red]")
    if (url): downloaderWorker(url, dtype, format)
    elif (local): downloaderWorker(local, dtype, format)

@cli.command()
@click.argument("ip", required=True)
@click.option("--ports", default="*", type=str, help="Ports to be scanned (1,2,3 or 16-24 or *-24 or 24-* or * or common).")
@click.option("--saveonfile", default=False, type=bool, help="Saves the open ports in a file.")
def portscan(ip, ports, saveonfile):
    if not ip: rprint(f"[red]Error: Enter a valid option; run \"{data.pre_cmd} portscan --help\" for further help.[/red]")
    portscanner(ip, ports, saveonfile)

if __name__ == "__main__":
    cli()