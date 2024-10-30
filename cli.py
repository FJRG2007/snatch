from dotenv import load_dotenv
from src.utils.snatch import Snatch
from textual.widgets import Markdown
from src.lib import data, colors as cl
from textual.app import App, ComposeResult
import os, sys, click, pyfiglet, importlib, tensorflow as tf
from src.utils.basics import cls, terminal, set_terminal_title

def get_function(module_name, function_name="main"):
    cls()
    return getattr(importlib.import_module(f"src.services.{module_name}.worker"), function_name)

@click.group()
def cli():
    cls()
    print(pyfiglet.figlet_format("SNATCH"))
    set_terminal_title("SNATCH")
    print(f'\n{cl.des_space}{cl.b}>> {cl.w}Welcome to Snatch, remember to use it responsibly. \n{cl.des_space}{cl.b}>> {cl.w}Join to our Discord server on tpe.li/dsc\n{cl.des_space}{cl.b}>> {cl.w}Version: {data.version}\n')
    if not sys.version[0] in "3": return terminal("e", "Snatch only works properly with Pytnon 3. Please upgrade/use Python 3.", exitScript=True)
    load_dotenv(override=True)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    tf.get_logger().setLevel("ERROR")

@cli.command()
@click.argument("prompt", required=False)
def ai(prompt):
    get_function("ai")(prompt)

@cli.command()
@click.argument("target", required=True)
@click.option("-m", "--method", default="directory", type=str, help="Listing method [directory (default), subdomain].")
@click.option("-w", "--wordlist", default="./src/lib/files/directory_listing/directory_listing.txt", type=str, help="Dictionary with routes.")
@click.option("-h", "--hide", default="", type=str, help="Codes to hide [default None, ex: 5XX or 5XX, 404].")
@click.option("--wordpress-plugins", is_flag=True, default=False, type=bool, help="Scanning Wordpress plugins [default False].")
def dirlist(target, method, wordlist, hide, wordpress_plugins):
    if not target: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} dirlist --help\" for further help.")
    get_function("directory_listing")(target, method, wordlist, hide, wordpress_plugins)

@cli.command()
@click.argument("url", required=False)
@click.option("-d", "--dtype", default="source", type=str, help="Download type [source (default), video, audio...]")
@click.option("-f", "--format", default="auto", type=str, help="In case of reloading a resource, choose the format.")
def download(url, dtype, format):
    if not url: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} download --help\" for further help.")
    get_function("downloader")(url, dtype, format)

@cli.command()
@click.argument("input_data", required=False)
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
def emseek(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, datalist):
    if not input_data: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} emseek --help\" for further help.")
    get_function("emseek")(input_data, name, first, last, birthdate, addinfo, username, company, providers, saveonfile, validate, datalist)

@cli.command()
@click.argument("section", required=False)
def help(section):
    get_function("help")(section)

@cli.command()

@click.option("-l", "--language", default="en", help="Language.")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
def imganal(language, saveonfile):
    get_function("image_analysis")(language, saveonfile)

@cli.command()
def info():
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()
        class MarkdownExampleApp(App):
            def compose(self) -> ComposeResult:
                yield Markdown(content)
        MarkdownExampleApp().run()

@cli.command()
@click.option("-t", "--tool", default="snatch", type=str, help="Use an advanced tool [exiftool (default), snatch].")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
def exdata(tool, saveonfile):
    get_function("metadata_extractor")(tool, saveonfile)

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
    get_function("pwd_generator")() # Add args here too.

@cli.command()
@click.option("-p", "--platforms", default="all", type=str, help="Platforms to scrape [all (default)...]")
@click.option("--userid", type=str, help="Discord: User ID to investigate.")
@click.option("--intitle", type=str, help="Dorks: Search website by title.")
@click.option("--intext", type=str, help="Dorks: Search for content within a website.")
@click.option("--site", type=str, help="Dorks: Search website by domain.")
@click.option("--inurl", type=str, help="Dorks: Search website by path in url.")
@click.option("--filetype", type=str, help="Dorks: Search by file type.")
@click.option("--ext", type=str, help="Dorks: Search by extension type.")
@click.option("--engine", type=str, help="Dorks: Engine to use [all, bing, ecosia, duckduckgo, google, yandex, yahoo].")
@click.option("--numresults", default=50, type=int, help="Dorks: Number of results to display.")
@click.option("-s", "--saveonfile", is_flag=True, type=bool, help="Saves the information in a file.")
def scraper(platforms, userid, intitle, intext, site, inurl, filetype, ext, engine, numresults, saveonfile):
    get_function("scraper")(platforms, userid, intitle, intext, site, inurl, filetype, ext, engine, numresults, saveonfile)

@cli.command()
@click.argument("option", required=True)
@click.argument("suboption", required=False)
@click.option("--help", is_flag=True, type=bool, help="Displays help on this command.")
def settings(option, suboption, help):
    if not option: terminal("e", f"Enter a valid option; run \"{data.pre_cmd} settings --help\" for further help.")
    get_function("settings")(option, suboption, help)

@cli.command()
@click.argument("url", required=True)
def trackurl(url):
    if not url: terminal("e", f"Enter a valid URL; run \"{data.pre_cmd} trackurl --help\" for further help.")
    get_function("url_tracker")(url)

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

if __name__ == "__main__": main()