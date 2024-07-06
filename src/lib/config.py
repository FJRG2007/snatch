
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
            if self._parent: self._parent._update_config(self._path, self)

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
        except FileNotFoundError: terminal("e", "\"config.json\" file not found.")
        except json.JSONDecodeError: terminal("e", "Invalid JSON format in \"config.json\" file.")
        except KeyError as e: terminal("e", f"Missing key {e} in \"config.json\" file.")

    def getAPIKey(self, name):
        if (name == "HUNTER"):
            api_key = os.getenv("HUNTER_API_KEY")
            if len(api_key) < 7: return random.choice(data.DEFAULT_API_KEYS["HUNTER"])
            elif len(api_key) >= 7: return api_key
            else: terminal("e", "Invalid Hunter API Key.", True)

    def _update_config(self, path, obj):
        keys = path.split(".")
        d = self.config
        for key in keys[:-1]:
            d = getattr(d, key)
        setattr(d, keys[-1], obj)
        self._save_config()

    def _save_config(self):
        with open("./config.json", "w") as file:
            json.dump(self._to_dict(self.config), file, indent=4)

    def _to_dict(self, obj):
        if isinstance(obj, DictToObj):return {k: self._to_dict(v) for k, v in obj.__dict__.items() if k not in ["_parent", "_path"]}
        else: return obj

    def __getattr__(self, name):
        return getattr(self.config, name)

config = None

try:
    config = Config()
except Exception as e:
    terminal("e", e)
    exit(1)