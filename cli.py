import click, pyfiglet
from dotenv import load_dotenv
from src.lib.config import config
from src.utils.snatch import Snatch
from textual.widgets import Markdown
from src.utils.basics import terminal
from src.lib import data, colors as cl
from textual.app import App, ComposeResult

# Functionalities.
from src.services.ai.worker import main as aiWoker
from src.services.downloader.worker import main as downloaderWorker
from src.services.emseek.worker import main as emseekWorker
from src.services.metadata_extractor.worker import main as exdataWorker
from src.services.directory_listing.worker import main as directoryListing
from src.services.portscanner.worker import main as portscanner
from src.services.pwd_generator.worker import main as pwdGeneratorWorker
from src.services.settings.worker import main as settingsWorker
from src.services.whatsapp.worker import main as whatsappWorker
from src.services.wifiscanner.worker import main as wifiscanWorker
from src.services.ai.worker import main as aiWoker

@click.group()
def cli():
    print(pyfiglet.figlet_format("SNATCH"))
    print(f'\n{cl.des_space}{cl.b}>> {cl.w}Welcome to Snatch, remember to use it responsibly. \n{cl.des_space}{cl.b}>> {cl.w}Join to our Discord server on tpeoficial.com/dsc\n{cl.des_space}{cl.b}>> {cl.w}Version: {data.version}\n')
    load_dotenv(override=True)

@cli.command()
def info():
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()
        class MarkdownExampleApp(App):
            def compose(self) -> ComposeResult:
                yield Markdown(content)
        app = MarkdownExampleApp()
        app.run()

@cli.command()
def ai():
    aiWoker()

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
@click.argument("email_or_username", required=False)
@click.option("-n", "--name", type=str, help="Name.")
@click.option("-f", "--first", type=str, help="First name.")
@click.option("-l", "--last", type=str, help="Last name.")
@click.option("-b", "--birthdate", type=str, help="Birthdate in ddmmyyyy format,type * if you dont know(ex:****1967,3104****).")
@click.option("-a", "--addinfo", help="Additional info to help guessing the email(ex:king,345981)", nargs="+")
@click.option("-u", "--username", help="Checks 100+ email providers for the availability of username@provider.com", type=str)
@click.option("-c", "--company", help="Company domain", type=str)
@click.option("-p", "--providers", help="Email provider domains", nargs="+")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
@click.option("-v","--validate", help="Check which emails are valid and returns information of each one")
@click.option("--datalist", help="File containing list of emails", type=str)
def emseek(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, datalist):
    if not email_or_username: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} emseek --help\" for further help.")
    emseekWorker(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, datalist)

@cli.command()
@click.option("-t", "--tool", default="snatch", type=str, help="Use an advanced tool [exiftool (default), snatch].")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
def exdata(tool, saveonfile):
    exdataWorker(tool, saveonfile)

@cli.command()
@click.argument("target", required=True)
@click.option("--wordlist", default="./src/lib/files/directory_listing.txt", type=str, help="Dictionary with routes.")
def dirlist(target, wordlist):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} dirlist --help\" for further help.")
    directoryListing(target, wordlist)

@cli.command()
@click.argument("target", required=True)
@click.option("-p", "--ports", default="*", type=str, help="Ports to be scanned (1,2,3 or 16-24 or *-24 or 24-* or * or common).")
@click.option("-t", "--threads", default=50, type=int, help="Number of simultaneous threads for the requests.")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the open ports in a file.")
def portscan(target, ports, threads, saveonfile):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} portscan --help\" for further help.")
    portscanner(target, ports, threads, saveonfile)

@cli.command()
@click.option("-c", "--characters", default="a", type=str, help="...")
@click.option("-l", "--length", default=20, type=int, help="...")
@click.option("-i", "--iterations", default=50, type=int, help="...")
def pwdgen(characters, length, iterations):
    pwdGeneratorWorker(characters, length, iterations)

@cli.command()
@click.argument("option", required=True)
@click.option("--help", is_flag=True, type=bool, help="Displays help on this command.")
def settings(option, help):
    if not option: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} settings --help\" for further help.")
    settingsWorker(option, help)

@cli.command()
@click.argument("username", required=True)
@click.argument("language", required=True)
def whatsapp(username, language):
    if not username or not language: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} whatsapp --help\" for further help.")
    whatsappWorker(username, language)

@cli.command()
def wifiscan():
    wifiscanWorker()

def main():
    try: cli()
    except KeyboardInterrupt as e: terminal(KeyboardInterrupt)
    except Snatch.InvalidOption as e: terminal("iom")

if __name__ == "__main__":
    main()