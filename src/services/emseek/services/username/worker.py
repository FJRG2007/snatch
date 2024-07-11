import os, sys, time, json, requests, subprocess
import src.lib.colors as cl
from requests.exceptions import Timeout
from .....utils.basics import cls, terminal



validator_url = "https://ftp-mj-washer-maritime.trycloudflare.com/" # https://raw.githubusercontent.com/mishakorzik/MailFinder/main/.validator
headers = {"User-Agent":"Opera/9.80 (J2ME/MIDP; Opera Mini/9.80 (S60; SymbOS; Opera Mobi/23.334; U; id) Presto/2.5.25 Version/10.54"}

def auto():
    cls()
    banner()

def banner():
    print(f'\n{cl.des_space}{cl.b}>> {cl.w}To find the username you need, write your last name and \n{cl.des_space}{cl.b}>> {cl.w}first name in different ways. For example: vuiko, vuikoo, vu\n{cl.des_space}{cl.b}>> {cl.w}It still takes a long time to find your e-mail.\n')

def restart():
    terminal("e", "You forgot to write something...")
    time.sleep(2)
    cls()
    os.execl(sys.executable, sys.executable, *sys.argv)

def selecttype(username, saveonfile):
    print(f"{cl.space}{cl.b}[{cl.w}1{cl.b}]{cl.w} Search in social media")
    print(f"{cl.space}{cl.b}[{cl.w}2{cl.b}]{cl.w} Check username on emails domains")
    print(f"{cl.space} {cl.w}|")
    print(f"{cl.space}{cl.b}[{cl.w}3{cl.b}]{cl.w} Scanner")
    print(f"{cl.space}{cl.b}[{cl.w}4{cl.b}]{cl.w} Search e-mail via fullname")
    print(f"{cl.space} {cl.w}|")
    type = str(input(f"{cl.space}{cl.b}[{cl.w}?{cl.b}]{cl.w} Select a number:{cl.b} ").lower())
    if type == "1" or type == "01": search_username(username, saveonfile)
    elif type == "2" or type == "02": validator(username)
    elif type == "3" or type == "03": ...
    elif type == "4" or type == "04": ...
    elif type == "5" or type == "05": ...
    else: restart()




def search_username(username, saveonfile):
    try:
        try: subprocess.check_output("pip install sherlock-project", shell=True, text=True)
        except subprocess.CalledProcessError: return terminal("nmi", "Sherlock")
        process = subprocess.Popen(f"sherlock {username} --nsfw --print-found --folderoutput ./temporal", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
        # Open file for writing if saveonfile is True.
        if saveonfile:
            os.makedirs("output/emseek", exist_ok=True)
            file = open(f"output/emseek/{username}_results.txt", "w")
        while True:
            output = process.stdout.readline().strip()
            if output.startswith("[") and output[2] == "]": output = output[4:]
            if output == "" and len(output) > 10 and process.poll() is not None: break
            if output.startswith("Checking username "): terminal("i", f"{output}\nThis may take a few minutes...")
            elif output.startswith("Search completed with "): 
                terminal("s", f"{output}.");
                if os.path.isfile(f"temporal/{username}.txt"): os.remove(f"temporal/{username}.txt")
                break
            elif len(output) > 10: 
                print(output)
                if saveonfile: file.write(f"{output}\n")
        return process.poll()
    except KeyboardInterrupt: terminal(KeyboardInterrupt)
    except Exception as e: terminal("e", f"Error obtaining Sherlock data: {e}")

def validator(user):
    if not user: return terminal("e", "You must define a valid user name.")
    auto()
    print(cl.w+cl.lines)
    with open("src/lib/files/emseek/data.json", "r") as file:
        data = json.load(file)
    try:
        for domain in data.get("emails_providers", []):
            email = f"{user}@{domain}"
            try:
                response = requests.get(f"{validator_url}validate?{email}", timeout=15).text
                if "ok::1" in response: print(f"{cl.space}{cl.B} DONE {cl.w} Status: {cl.g}valided{cl.w} Email: {email}")
                else: print(f"{cl.space}{cl.R} FAIL {cl.w} Status: {cl.g}invalid{cl.w} Email: {email}")
            except Timeout: print(f"{cl.space}{cl.Y} EXIT {cl.w} Status: {cl.g}timeout{cl.w} Email: {cl.email}")
    except KeyboardInterrupt: print("\r"),;sys.stdout.flush()

def main(username, saveonfile):
    banner()
    selecttype(username, saveonfile)