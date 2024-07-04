import openai
from .models.openai.llm import LLM as OpenAILLM
from dotenv import load_dotenv
from rich import print as rprint
from src.lib.config import config

load_dotenv(override=True)

def main(prompt):
    # try:
    if (config.ai.model in ["claude"]):
        ...
    if (config.ai.model in ["gemeni"]):
        ...
    if (config.ai.model in ["llama3"]):
        ...
    if (config.ai.model in ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]):
        OpenAILLM().process_request(prompt)
    # except openai.NotFoundError as e: rprint(f"[red]Error: Define a valid AI model.[/red]")
    # except openai.AuthenticationError as e: rprint(f"[red]Error: OpenAI Api Key invalid.[/red]")