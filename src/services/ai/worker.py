from dotenv import load_dotenv
from src.lib.config import config
from .models.openai.llm import LLM as OpenAILLM

load_dotenv(override=True)

def main(prompt):
    # Provider / Athropic.
    if (config.ai.provider == "anthropic"):
        if (config.ai.model in ["claude"]): ...
    # Provider / Dymo.
    if (config.ai.provider == "dymo"):
        if (config.ai.model in ["dymo", "ela"]): ...
    # Provider / Google.
    if (config.ai.provider == "google"):
        if (config.ai.model in ["gemeni"]): ...
    # Provider / Meta.
    if (config.ai.provider == "meta"):
        if (config.ai.model in ["llama3"]): ...
    # Provider / OpenAI.
    if (config.ai.provider == "openai"):
        if (config.ai.model in ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]): return OpenAILLM().process_request(prompt)
    # Provider / Perplexity.
    if (config.ai.provider == "perplexity"):
        if (config.ai.model in ["llama3"]): ...
    
    # except openai.NotFoundError as e: rprint(f"[red]Error: Define a valid AI model.[/red]")
    # except openai.AuthenticationError as e: rprint(f"[red]Error: OpenAI Api Key invalid.[/red]")