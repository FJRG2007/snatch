import importlib
from src.utils.basics import terminal

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.scraper.platforms.{module_name}"), function_name)

def main(platforms, dscuserid):
    platforms = platforms.strip().lower()
    if platforms == "all":
        get_function("discord")(dscuserid)
    else: 
        platforms = platforms.split(",")
        if not platforms or len(platforms) == 0: return terminal("e", "Select at least one platform.")
        if "discord" in platforms:
            get_function("discord")(dscuserid)