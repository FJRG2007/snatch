from src.utils.basics import cls, terminal

# Options.
from .model import model
from .help import help
from .verify import verifySnatch

def main(option, suboption, helpParam):
    option = option.lower().strip()
    suboption = suboption.lower().strip() if suboption else "default"
    if not len(option) > 3: return terminal("e", "Select a valid option.")
    cls()
    if option == "help" or helpParam: return help()
    if option == "model": return model(suboption)
    if option == "verify": return verifySnatch()