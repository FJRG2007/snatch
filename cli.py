from dotenv import load_dotenv
import click, pyfiglet, importlib
from src.lib.config import config
from src.utils.snatch import Snatch
from textual.widgets import Markdown
from src.utils.basics import cls, terminal
from src.lib import data, colors as cl
from textual.app import App, ComposeResult

def get_function(module_name, function_name="main"):
    module = importlib.import_module(f"src.services.{module_name}.worker")
    cls()
    return getattr(module, function_name)

@click.group()
def cli():
    cls()
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
@click.argument("prompt", required=False)
def ai(prompt):
    get_function("ai")(prompt)

@cli.command()
@click.argument("url", required=False)
@click.argument("local", type=click.File("rb"), required=False)
@click.option("-dt", "--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("-f", "--format", default="auto", type=str, help="In case of reloading a resource, choose the format.")
def download(url, local, dtype, format):
    if not url and not local: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} download --help\" for further help.")
    if (url): get_function("downloader")(url, dtype, format)
    elif (local): get_function("downloader")(local, dtype, format)

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
    get_function("emseek")(email_or_username, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, datalist)

@cli.command()
@click.option("-t", "--tool", default="snatch", type=str, help="Use an advanced tool [exiftool (default), snatch].")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
def exdata(tool, saveonfile):
    get_function("metadata_extractor")(tool, saveonfile)

@cli.command()
@click.argument("target", required=True)
@click.option("--wordlist", default="./src/lib/files/directory_listing.txt", type=str, help="Dictionary with routes.")
def dirlist(target, wordlist):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} dirlist --help\" for further help.")
    get_function("directory_listing")(target, wordlist)

@cli.command()
@click.argument("target", required=True)
@click.option("-p", "--ports", default="*", type=str, help="Ports to be scanned (1,2,3 or 16-24 or *-24 or 24-* or * or common).")
@click.option("-t", "--threads", default=50, type=int, help="Number of simultaneous threads for the requests.")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the open ports in a file.")
def portscan(target, ports, threads, saveonfile):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} portscan --help\" for further help.")
    get_function("portscanner")(target, ports, threads, saveonfile)

@cli.command()
def pwdgen():
    get_function("pwd_generator")()

@cli.command()
@click.option("-p", "--platforms", default="all", type=str, help="Platforms to scrape [all (default)...]")
@click.option("--dscuserid", type=str, help="ID of the Discord user to investigate.")
def scraper(platforms, dscuserid):
    get_function("scraper")(platforms, dscuserid)

@cli.command()
@click.argument("option", required=True)
@click.option("--help", is_flag=True, type=bool, help="Displays help on this command.")
def settings(option, help):
    if not option: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} settings --help\" for further help.")
    get_function("settings")(option, help)

@cli.command()
@click.argument("username", required=True)
@click.argument("language", required=True)
def whatsapp(username, language):
    if not username or not language: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} whatsapp --help\" for further help.")
    get_function("whatsapp")(username, language)

@cli.command()
def wifiscan():
    get_function("wifiscanner")()

def main():
    try: cli()
    except KeyboardInterrupt as e: terminal(KeyboardInterrupt)
    except Snatch.InvalidOption as e: terminal("iom")
if __name__ == "__main__":
    main()