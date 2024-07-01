
import os
import json
from . import data
import shutil
from rich import print as rprint

class DictToObj:
    def __init__(self, dict_):
        for key, value in dict_.items():
            if isinstance(value, dict):
                value = DictToObj(value)
            self.__dict__[key] = value

    def __getattr__(self, name):
        return self.__dict__.get(name)

class Config:
    def __init__(self):
        try:
            # Read config.json file.
            with open("./config.json", "r") as file:
                config_dict = json.load(file)
            self.config = DictToObj(config_dict)
            if os.path.exists(data.dirs["temporal"]):
                shutil.rmtree(data.dirs["temporal"])
            os.makedirs(data.dirs["temporal"])
        except FileNotFoundError: rprint("[red]Error: \"config.json\" file not found.[/red]")
        except json.JSONDecodeError: rprint("[red]Error: Invalid JSON format in \"config.json\" file.[/red]")
        except KeyError as e: rprint(f"[red]Error: Missing key {e} in \"config.json\" file.[/red]")

    def __getattr__(self, name):
        return getattr(self.config, name)

config = None

try:
    config = Config()
except Exception as e:
    rprint(f"[red]An error occurred: {e}[/red]")
    exit(1)