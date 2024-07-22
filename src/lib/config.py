from . import data
import os, json, random
from types import SimpleNamespace
from src.utils.basics import terminal

class Config:
    def __init__(self):
        # Read config.json file.
        with open("./config.json", "r") as file:
            upd = file.read()
            self.config = json.loads(upd, object_hook=lambda d: SimpleNamespace(**d))

    def get_api_key(self, name):
        if (name == "HUNTER"):
            api_key = os.getenv("HUNTER_API_KEY")
            if len(api_key) < 7: return random.choice(data.DEFAULT_API_KEYS["HUNTER"])
            elif len(api_key) >= 7: return api_key
            else: terminal("e", "Invalid Hunter API Key.", True)

    def __getattr__(self, name):
        return getattr(self.config, name)

    def __setattr__(self, name, value):
        if name == "config": super().__setattr__(name, value)
        else:
            setattr(self.config, name, value)
            self._save_config()
    
    def _save_config(self):
        # Convert the SimpleNamespace object back to a dictionary.
        config_dict = self._to_dict(self.config)
        upd = json.dumps(config_dict, indent=2)
        print(upd)
        with open("./config.json", "w") as file:
            file.write(upd)

    def _to_dict(self, obj):
        # Helper method to convert SimpleNamespace to dict.
        if isinstance(obj, SimpleNamespace): return {k: self._to_dict(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list): return [self._to_dict(i) for i in obj]
        else: return obj

config = None

try: config = Config()
except Exception as e: terminal("e", e, exitScript=True)