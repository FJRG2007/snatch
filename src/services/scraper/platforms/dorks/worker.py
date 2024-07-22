import importlib
import src.lib.colors as cl
from src.utils.basics import cls, quest, terminal, getPositive

def get_function(module_name, function_name="main"):
    try:
        return getattr(importlib.import_module(f"src.services.scraper.platforms.dorks.engines.{module_name}"), function_name)
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"Error loading function: {e}")
        return None

engines = ["All", "Bing", "Ecosia", "DuckDuckGo", "Google", "Yandex", "Yahoo"]

def main(query, engine):
    # Arguments.
    if not query: query = quest("Searching with Dorks")
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

    for eng in engines_to_use:
        func = get_function(eng)
        if func: func(query)
        else: terminal("e", f"No function available for engine: {eng}")
