import time
import src.lib.colors as cl
from src.lib.data import AI
from src.lib.config import config
from src.utils.basics import cls, quest, terminal, getPositive

def restart():
    terminal("iom")
    model()

def show_models(provider):
    cls()  # Clear the screen.
    provider_data = next((prov for prov in AI["providers"] if prov["name"] == provider), None)
    if not provider_data: return terminal("e", "Provider not found.")
    terminal("info", f"Select a model to finish.")
    for i, model in enumerate(provider_data["models"], 1):
        tag = model.get("tag", "")
        print(f"{cl.b}[{cl.w}{i}{cl.b}]{cl.w} {f"{model['name']}{f' - {cl.y}{tag}{cl.w}' if tag else ''}"}")
         # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(provider_data["models"]): print(f" {cl.w}|")
    try:
        print(f" {cl.w}|")
        selector = int(quest("Select a number"))
        if 1 <= selector <= len(provider_data["models"]): 
            terminal("s", f"You have selected model: {provider_data['models'][selector - 1]['name']}")
            config.ai.provider = provider_data["name"].lower()
            config.ai.model = provider_data["models"][selector - 1]["name"]
            config.save_config()
        else: terminal("e", "Invalid selection.")
    except ValueError: terminal("e", "Invalid input. Please enter a number.")
def model(opt):
    cls()
    if opt == "default" or opt == "models":
        terminal("info", f"Select a provider to continue to select the model.")
        # Show available providers.
        for i, provider in enumerate(AI["providers"]):
            tag = provider.get("tag", "")
            print(f"{cl.b}[{cl.w}{i+1}{cl.b}]{cl.w} {provider["name"]}{f' - {cl.y}{tag}{cl.w}' if tag else ''}")
            # Add separator for visual clarity every 3 items.
            if i % 3 == 0 and i != len(AI["providers"]): print(f" {cl.w}|")
        print(f" {cl.w}|")
        selector = quest(f"Select a number")
        provider_map = { # Removing and using the object names from data.py.
            "1": "Anthropic",
            "2": "Dymo",
            "3": "Google",
            "4": "Groq",
            "5": "Meta",
            "6": "Ollama",
            "7": "OpenAI",
            "8": "Perplexity"
        }
        if selector in provider_map: show_models(provider_map[selector])
        else: restart()
    elif opt == "advanced":
        terminal("info", f"Select one of the advanced options to configure the AI model.")
        advanced = [
            ("1", "Second response (Default: enabled)"),
            ("2", "Speech to text (Default: disabled)")
        ]
        for i, (number, name) in enumerate(advanced, 1):
            print(f"{cl.b}[{cl.w}{number}{cl.b}]{cl.w} {name}")
            # Add separator for visual clarity every 3 items.
            if i % 3 == 0 and i != len(advanced): print(f" {cl.w}|")
        print(f" {cl.w}|")
        selector = quest(f"Select a number")

        if selector == "1": 
            if getPositive(quest(f"Do you want to {cl.BOLD}{"disable" if config.ai.second_response else "enable"}{cl.ENDC} second response? [Y]/N")):
                config.ai.second_response = not config.ai.second_response
                config.save_config()
            terminal("s", f"You have {"enabled" if config.ai.second_response else "disabled"} the second response for the AI model.")
        elif selector == "2":
            if getPositive(quest(f"Do you want to {cl.BOLD}{"disable" if config.ai.text_to_speech else "enable"}{cl.ENDC} \"text-to-speech\" transcription? [Y]/N")):
                config.ai.text_to_speech = not config.ai.text_to_speech
                config.save_config()
            terminal("s", f"You have {"enabled" if config.ai.text_to_speech else "disabled"} \"text-to-speech\" transcription for the AI model.")
        else: 
            terminal("e", "Select a valid option.")
            time.sleep(1.25)
            model(opt)
    else: return terminal("e", "Select a valid option.")