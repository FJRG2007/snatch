import importlib
from src.utils.basics import terminal

def get_function(module_name, function_name="main"):
    module = importlib.import_module(f"src.services.scraper.platforms.{module_name}")
    return getattr(module, function_name)

def main(platforms, dscuserid):
     platforms = platforms.strip().lower()
     if platforms == "all":
        get_function("discord")(dscuserid)