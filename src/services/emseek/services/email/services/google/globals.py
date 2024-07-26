from .objects.utils import TMPrinter
from rich.console import Console

from . import config as con

config = con
tmprinter = TMPrinter()
rc = Console(highlight=False)