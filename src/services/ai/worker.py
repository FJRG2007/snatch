from dotenv import load_dotenv
load_dotenv(override=True)
from . import llm
from rich import print as rprint

def main(prompt):
    response, _ = llm.LLM().process_request(prompt)
    rprint(f"[green]AI: {response}[/green]")
