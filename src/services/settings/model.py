import os, sys, time
import src.lib.colors as cl
from src.lib.data import AI
from src.utils.basics import cls, terminal

def restart():
    terminal("iom")
    model()

def show_models(provider):
    cls()  # Clear the screen.
    provider_data = next((prov for prov in AI["providers"] if prov["name"] == provider), None)
    if not provider_data: return terminal("e", "Provider not found.")
    for i, model_name in enumerate(provider_data["models"], 1):
        print(f"{cl.space}{cl.b}[{cl.w}{i}{cl.b}]{cl.w} {model_name}")
         # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(provider_data["models"]): print(f"{cl.space} {cl.w}|")
    try:
        selector = int(input(f"{cl.space}{cl.b}[{cl.w}?{cl.b}]{cl.w} Select a number:{cl.b} "))
        if 1 <= selector <= len(provider_data["models"]): print(f"You have selected model: {provider_data['models'][selector - 1]}")
        else: terminal("e", "Invalid selection.")
    except ValueError: terminal("e", "Invalid input. Please enter a number.")
def model():
    # Show available providers.
    providers = [
        ("1", "Anthropic (Coming Soon)"),
        ("2", "Dymo (Coming Soon)"),
        ("3", "Google"),
        ("4", "Groq"),
        ("5", "Meta (Coming Soon)"),
        ("6", "OpenAI"),
        ("7", "Perplexity")
    ]
    
    for i, (number, name) in enumerate(providers, 1):
        print(f"{cl.space}{cl.b}[{cl.w}{number}{cl.b}]{cl.w} {name}")
        # Add separator for visual clarity every 3 items.
        if i % 3 == 0 and i != len(providers): print(f"{cl.space} {cl.w}|")
    selector = input(f"{cl.space}{cl.b}[{cl.w}?{cl.b}]{cl.w} Select a number:{cl.b} ").lower()
    provider_map = {
        "1": "Anthropic",
        "2": "Dymo",
        "3": "Google",
        "4": "Groq",
        "5": "Meta",
        "6": "OpenAI",
        "7": "Perplexity"
    }
    if selector in provider_map: show_models(provider_map[selector])
    else: restart()