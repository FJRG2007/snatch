from . import data
import os, json, random
from types import SimpleNamespace
from src.utils.basics import terminal

class Config:

    path: str
    config: SimpleNamespace

    def __init__(self, path: str = "./config.json"):
        # Read config.json file.
        with open("./config.json", "r") as file:
            upd = file.read()
            self.config = json.loads(upd, object_hook=lambda d: SimpleNamespace(**d))
        self.path = path
        self.read_config()

    def get_api_key(self, name):
        if (name == "HUNTER"):
            api_key = os.getenv("HUNTER_API_KEY")
            if len(api_key) < 7: return random.choice(data.DEFAULT_API_KEYS["HUNTER"])
            elif len(api_key) >= 7: return api_key
            else: terminal("e", "Invalid Hunter API Key.", True)
        elif (name == "TRUSTFULL"):
            api_key = os.getenv("TRUSTFULL_API_KEY")
            if len(api_key) < 7: return random.choice(data.DEFAULT_API_KEYS["TRUSTFULL"])
            elif len(api_key) >= 7: return api_key
            else: terminal("e", "Invalid Trustfull API Key.", True)

    def __getattr__(self, name):
        return getattr(self.config, name)
    
    def read_config(self):
        # Read config.json file.
        with open(self.path, "r") as file:
            upd = file.read()
            # print(f"Read {self.path}: {upd}") # Dev mode.
            self.config = json.loads(
                upd, object_hook=lambda d: SimpleNamespace(**d))
        return self.config
    
    def save_config(self):
        # Convert the SimpleNamespace object back to a dictionary.
        upd = self._to_dict(self.config)
        # print(f"Update {self.path}: ", upd) # Dev mode.
        with open(self.path, "w") as file:
            file.write(upd)
        # update self.config
        self.read_config()
        return self.config

    def _to_dict(self, obj: SimpleNamespace):
        return json.dumps(obj, default=lambda o: o.__dict__)

config = None

try: config = Config()
except Exception as e: terminal("e", e, exitScript=True)