from src.lib.data import AI
from dotenv import load_dotenv
from src.lib.config import config
from src.utils.basics import terminal
# from .models.anthropic.llm import LLM as AnthropicLLM
# from .models.dymo.llm import LLM as DymoLLM
from .models.google.llm import LLM as GoogleLLM
from .models.groq.llm import LLM as GroqLLM
# from .models.meta.llm import LLM as MetaLLM
from .models.openai.llm import LLM as OpenAILLM
# from .models.ollama.llm import LLM as OllamaLLM
# from .models.perplexity.llm import LLM as PerplexityLLM

load_dotenv(override=True)

def main(prompt):
    provider = config.ai.provider.lower()
    model = config.ai.model.lower()
    # Obtain the models from the specified supplier.
    for prov in AI["providers"]:
        if prov["name"].lower() == provider:
            if model in [m.lower() for m in prov["models"]]:
                if provider == "anthropic": ... #return AnthropicLLM().process_request(prompt)
                elif provider == "dymo": ... #return DymoLLM().process_request(prompt)
                elif provider == "google": return GoogleLLM().process_request(prompt)
                elif provider == "groq": return GroqLLM().process_request(prompt)
                elif provider == "meta": ... #return MetaLLM().process_request(prompt)
                elif provider == "ollama": ... #return OllamaLLM().process_request(prompt)
                elif provider == "openai": return OpenAILLM().process_request(prompt)
                elif provider == "perplexity": ... #return PerplexityLLM().process_request(prompt)
                else: return terminal("e", f"Provider '{provider}' and model '{model}' found but no action defined.")
            else: return terminal("e", f"Model '{model}' not found for provider '{provider}'.")        
    # Handle the case in which the supplier is not defined or is not valid.
    return terminal("e", "Provider not recognized or model not found.")