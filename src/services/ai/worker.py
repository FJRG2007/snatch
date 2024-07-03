<<<<<<< HEAD
from . import llm
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv(override=True)

def main(prompt):
    response, _ = llm.LLM().process_request(prompt)
    rprint(f"[green]AI: {response}[/green]")
=======
from dotenv import load_dotenv
load_dotenv(override=True)
from . import llm
from rich import print as rprint

def main(prompt):
    response, _ = llm.LLM().process_request(prompt)
    rprint(f"[green]AI: {response}[/green]")
>>>>>>> 25abe91ea07b09966a6c86288c23e87bf5eb5ffb
