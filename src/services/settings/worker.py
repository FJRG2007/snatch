import src.lib.colors as cl
from src.lib.config import config
from ...utils.basics import cls, terminal
from .model import model
from .help import help
def main(option, helpParam):
    option = option.lower().strip()
    if not len(option) > 3: return terminal("e", "Select a valid option.")
    cls()
    if option == "help" or helpParam: return help()
    if option == "model": return model()