import src.lib.colors as cl
from src.lib.data import AI
from src.lib.config import config
from src.utils.basics import cls, terminal
# from .models.anthropic.llm import LLM as AnthropicLLM
# from .models.dymo.llm import LLM as DymoLLM
from .models.google.llm import LLM as GoogleLLM
from .models.groq.llm import LLM as GroqLLM
# from .models.meta.llm import LLM as MetaLLM
from .models.openai.llm import LLM as OpenAILLM
# from .models.ollama.llm import LLM as OllamaLLM
# from .models.perplexity.llm import LLM as PerplexityLLM

# Obtain the models from the specified supplier.
def init_model(prompt):
    cls()
    provider = config.ai.provider.lower()
    model = config.ai.model.lower()
    for prov in AI["providers"]:
        if prov["name"].lower() == provider:
            if model in [m["name"].lower() for m in prov["models"]]:
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
    return terminal("e", "Provider not recognized or model not found.")

def main(prompt):
    if prompt and prompt.lower() != "tips" and len(prompt) < 10: terminal("e", "Please enter a valid prompt, it must be at least 10 characters long.", clear="b")
    elif prompt and prompt.lower() != "tips": init_model(prompt)
    else:
        terminal("info", f"""Remember to give me all the information I need to take the necessary actions. If you think you need **tips**, write "tips".""")
        prompt = input(f"{cl.b}[{cl.w}?{cl.b}]{cl.w} You: ")
        if prompt.lower() == "tips": 
            cls()
            terminal("info", 
f"""We believe these tips can help you improve your results with Snatch.
* Write down all the **relevant information** you know.
* We recommend writing the prompt in **English**.
* **Structure your prompt** well and keep it from being confusing.""")
            main(prompt)
        elif len(prompt) > 10: init_model(prompt)
        else: terminal("e", "Please enter a valid prompt, it must be at least 10 characters long.", clear="b")