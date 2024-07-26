from ..helpers.utils import *
from ..errors import *
from ..objects.base import SmartObj

from typing import *

class TMPrinter(SmartObj):
    def __init__(self):
        self.max_len = 0

    def out(self, text: str):
        if len(text) > self.max_len:
            self.max_len = len(text)
        else:
            text += (" " * (self.max_len - len(text)))
        print(text, end='\r')

    def clear(self):
    	print(" " * self.max_len, end="\r")