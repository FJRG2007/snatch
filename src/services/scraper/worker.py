import importlib
from src.utils.basics import terminal

def get_function(module_name, function_name="main"):
    return getattr(importlib.import_module(f"src.services.scraper.platforms.{module_name}.worker"), function_name)

def main(platforms, userid, intitle, intext, site, inurl, filetype, ext, engine, num_results, saveonfile):
    # To avoid code repetitions.
    query_dorks = { "intitle": intitle, "intext": intext, "site": site, "inurl": inurl, "filetype": filetype, "ext": ext }

    platforms = platforms.strip().lower()
    functions = [
        ("discord", {"userId": userid}),
        ("dorks", {"query": query_dorks, "engine": engine, "num_results": num_results, "saveonfile": saveonfile}),
    ]
    if platforms == "all":
        for i, (function_name, params) in enumerate(functions):
            get_function(function_name)(**params)
    else: 
        platforms = platforms.split(",")
        if not platforms or len(platforms) == 0: return terminal("e", "Select at least one platform.")
        if "discord" in platforms: get_function("discord")(userid)
        if "dorks" in platforms: get_function("dorks")(query_dorks, engine, num_results, saveonfile)