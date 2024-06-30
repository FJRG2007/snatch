import click
from src.worker import main as worker
from src.lib.data import pre_cmd, INFO_MARKDOWN
from rich import print as rprint
from textual.app import App, ComposeResult
from textual.widgets import Markdown

@click.group()
def cli():
    pass

@cli.command()
def info():
    class MarkdownExampleApp(App):
        def compose(self) -> ComposeResult:
            yield Markdown(INFO_MARKDOWN)
    app = MarkdownExampleApp()
    app.run()

@cli.command()
@click.argument("url", nargs=1, required=False)
@click.argument("local", type=click.File("rb"), nargs=1, required=False)
@click.option("--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("--format", default="auto", type=str, help="In case of reloading a resource, choose the format")
def download(url, local, dtype, format):
    if not url and not local: rprint(f"[red]Error: Enter a valid option; run \"{pre_cmd} download --help\" for further help[/red]")
    if (url): worker(url, dtype, format)
    elif (local): worker(local, dtype, format)

if __name__ == "__main__":
    cli()