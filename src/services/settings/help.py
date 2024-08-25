from src.lib import data
import src.lib.colors as cl
from src.utils.basics import cls, quest, terminal, getPositive

# Options.
from .model import model
from .verify import verifySnatch

def restart():
    terminal("iom")
    help()

def help():
    terminal("info", f"""Welcome to the Snatch help center, select an option below to continue.""")
    providers = [
        ("1", "Set up AI model"),
        ("2", "Verify Snatch version and files")
    ]
    for i, (number, name) in enumerate(providers, 1):
        print(f"{cl.b}[{cl.w}{number}{cl.b}]{cl.w} {name}")
        # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(providers): print(f" {cl.w}|")
    selector = quest("Select a number")
    cls()
    if selector == "1":
        terminal("info", 
        f"""To set up an **AI model**, set the API Key if necessary (most cases), and run the `{data.pre_cmd} settings model` command to choose your preferred model.  
Do you want me to execute the command for you? [Y]/N: """)
        if getPositive(quest(f"You")):
            cls()
            model("models")
    elif selector == "2":
        terminal("info", 
        f"""To verify the Snatch files, run the `{data.pre_cmd} settings verify`.  
Do you want me to execute the command for you? [Y]/N: """)
        if getPositive(quest(f"You")):
            cls()
            verifySnatch()
    else: restart()