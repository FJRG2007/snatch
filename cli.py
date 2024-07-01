import click
import src.lib.data as data
from rich import print as rprint
from src.lib.config import config
from textual.widgets import Markdown
from src.worker import main as worker
from textual.app import App, ComposeResult

@click.group()
def cli():
    pass

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
@click.option("--format", default="auto", type=str, help="In case of reloading a resource, choose the format")
def download(url, local, dtype, format):
    if not url and not local: rprint(f"[red]Error: Enter a valid option; run \"{data.pre_cmd} download --help\" for further help[/red]")
    if (url): worker(url, dtype, format)
    elif (local): worker(local, dtype, format)

if __name__ == "__main__":
    cli()