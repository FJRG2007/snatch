import importlib
import src.lib.colors as cl
from datetime import datetime
from src.utils.basics import cls, quest, terminal, getPositive

def get_function(module_name, function_name="main"):
    try: return getattr(importlib.import_module(f"src.services.scraper.platforms.dorks.engines.{module_name}"), function_name)
    except (ModuleNotFoundError, AttributeError) as e:
        terminal("e", f"Error loading function: {e}")
        return None

engines = ["All", "Bing", "Ecosia", "DuckDuckGo", "Google", "Yandex", "Yahoo"]

def main(query, engine, num_results, saveonfile):
    # Arguments.
    if not query: return terminal("e", "Please specify a query.", exitScript=True)
    if not engine:
        cls()
        for i, eng in enumerate(engines, 1):
            print(f"{cl.b}[{cl.w}{i}{cl.b}]{cl.w} {eng}")
            if i % 3 == 0 and i != len(engines): print(f" {cl.w}|")
        print(f" {cl.w}|")
        engine_input = quest("Engine (Enter number or name)", lowercase=True)
        # Handle case when input is a number.
        if engine_input.isdigit():
            index = int(engine_input) -1 
            if index < len(engines): engine = engines[index]
            else:
                terminal("e", "Invalid number. Defaulting to 'All'.")
                engine = "All"
        else: engine = engine_input
    if engine.lower() == "all": engines_to_use = [eng.lower() for eng in engines[1:]]  # Exclude "All" from the list.
    else: engines_to_use = [engine.lower()]
    if not num_results: num_results = quest("Number of results", format_type=int)
    # Add Banner.
    print("-" * 50)
    print(f"Scanning query: {{ {', '.join(f'{key}: {value}' for key, value in query.items() if value is not None)} }}")
    print(f"Engine: {next((eng for eng in engines if eng.lower() == engine.lower()), None)}")
    print(f"Number of results: {num_results}")
    print(f"Scanning started at: {str(datetime.now())}")
    print(f"{cl.G} Recommended resource {cl.w} https://tools.tpeoficial.com/tools/google-dorks-search")
    print("-" * 50)
    for eng in engines_to_use:
        func = get_function(eng)
        if func: func(query, num_results, saveonfile)
        else: terminal("e", f"No function available for engine: {eng}")
