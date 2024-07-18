
from . import data
import os, json, shutil, random
from ..utils.basics import terminal

class DictToObj:
    def __init__(self, dict_):
        for key, value in dict_.items():
            if isinstance(value, dict): value = DictToObj(value)
            self.__dict__[key] = value

    def __getattr__(self, name):
        return self.__dict__.get(name)
    
    def __setattr__(self, name, value):
        if name in ["_parent", "_path"]: super().__setattr__(name, value)
        else:
            self.__dict__[name] = value
            if self._parent: self._parent._update_config(self._path, value)
            self._save_to_file()
    
    def _update_config(self, key, value):
        if isinstance(value, DictToObj): value = value.__dict__
        self.__dict__[key] = value
        if self._parent: self._parent._update_config(self._path, self)
        else: self._save_to_file()

    def _save_to_file(self):
        # Save the entire configuration to file
        with open("./config.json", "r+") as file:
            data = json.load(file)
            self._update_data(data, self.__dict__)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

    def _update_data(self, data, updates):
        for key, value in updates.items():
            if isinstance(value, DictToObj): value = value.__dict__
            if key in data:
                if isinstance(data[key], dict) and isinstance(value, dict): self._update_data(data[key], value)
                else: data[key] = value
            else: data[key] = value

class Config:
    def __init__(self):
        try:
            # Read config.json file.
            with open("./config.json", "r") as file:
                config_dict = json.load(file)
            self.config = DictToObj(config_dict)
            if os.path.exists(data.dirs["temporal"]): shutil.rmtree(data.dirs["temporal"])
            os.makedirs(data.dirs["temporal"])
        except FileNotFoundError: terminal("e", "\"config.json\" file not found.")
        except json.JSONDecodeError: terminal("e", "Invalid JSON format in \"config.json\" file.")
        except KeyError as e: terminal("e", f"Missing key {e} in \"config.json\" file.")

    def get_api_key(self, name):
        if (name == "HUNTER"):
            api_key = os.getenv("HUNTER_API_KEY")
            if len(api_key) < 7: return random.choice(data.DEFAULT_API_KEYS["HUNTER"])
            elif len(api_key) >= 7: return api_key
            else: terminal("e", "Invalid Hunter API Key.", True)

    def __getattr__(self, name):
        return getattr(self.config, name)

config = None

try: config = Config()
except Exception as e: terminal("e", e, exitScript=True)