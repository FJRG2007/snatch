import src.lib.colors as cl
from src.lib.config import config
from ...utils.basics import cls, terminal
from .model import model
def main(option):
    option = option.lower().strip()
    if not len(option) > 3: return terminal("e", "Select a valid option.")
    cls()
    if (option == "model"): return model()