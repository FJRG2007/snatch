from . import llm
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv(override=True)

def main(prompt):
    response, _ = llm.LLM().process_request(prompt)
    rprint(f"[green]AI: {response}[/green]")