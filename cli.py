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
from src.services.emseek.worker import main as emseekWorker
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
@click.option("-dt", "--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("-f", "--format", default="auto", type=str, help="In case of reloading a resource, choose the format.")
def download(url, local, dtype, format):
    if not url and not local: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} download --help\" for further help.")
    if (url): downloaderWorker(url, dtype, format)
    elif (local): downloaderWorker(local, dtype, format)

@cli.command()
@click.argument("email", required=True)
@click.option("-f", "--first", type=str, help="First name.")
@click.option("-m", "--middle", type=str, help="Middle name.")
@click.option("-l", "--last", type=str, help="Last name.")
@click.option("-b", "--birthdate", type=str, help="Birthdate in ddmmyyyy format,type * if you dont know(ex:****1967,3104****).")
@click.option("-a", "--addinfo", help="Additional info to help guessing the email(ex:king,345981)",nargs="+")
@click.option("-u", "--username", help="Checks 100+ email providers for the availability of username@provider.com",type=str)
@click.option("-c", "--company", help="Company domain",type=str)
@click.option("-p", "--providers", help="Email provider domains",nargs="+")
@click.option("-s", "--saveonfile", default=False, type=bool, help="Saves the information in a file.")
@click.option("-v","--validate", help="Check which emails are valid and returns information of each one")
@click.option("--list", help="File containing list of emails",type=str)
def emseek(email, first, middle, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list):
    if not email: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} emseek --help\" for further help.")
    emseekWorker(email, first, middle, last, birthdate, addinfo, username, company, providers, saveonfile, validate, list)

@cli.command()
@click.argument("target", required=True)
@click.option("--wordlist", default="./src/lib/files/directory_listing.txt", type=str, help="Dictionary with routes.")
def dirlist(target, wordlist):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} dirlist --help\" for further help.")
    directoryListing(target, wordlist)

@cli.command()
@click.argument("ip", required=True)
@click.option("-p", "--ports", default="*", type=str, help="Ports to be scanned (1,2,3 or 16-24 or *-24 or 24-* or * or common).")
@click.option("-s", "--saveonfile", default=False, type=bool, help="Saves the open ports in a file.")
def portscan(ip, ports, saveonfile):
    if not ip: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} portscan --help\" for further help.")
    portscanner(ip, ports, saveonfile)
    
@cli.command()
@click.argument("username", required=True)
@click.argument("language", required=True)
def whatsapp(username, language):
    if not username or not language: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} whatsapp --help\" for further help.")
    whatsappWorker(username, language)

if __name__ == "__main__":
    cli()