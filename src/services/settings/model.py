import os, sys, time
import src.lib.colors as cl
from src.lib.data import AI
from ...utils.basics import cls, terminal, restart

def show_models(provider):
    cls()
    isValid = False
    for prov in AI["providers"]:
        if prov["name"] == provider: 
            for i, model_name in enumerate(prov["models"], 1):
                print(f"{cl.space}{cl.b}[{cl.w}{i}{cl.b}]{cl.w} {model_name}")
            selector = str(input(f"{cl.space}{cl.b}[{cl.w}?{cl.b}]{cl.w} Select a number:{cl.b} ").lower())
    if isValid: terminal("e", "An error has occurred.")
def model():
    # Show available providers.
    print(f"{cl.space}{cl.b}[{cl.w}1{cl.b}]{cl.w} Anthropic (Coming Soon)")
    print(f"{cl.space}{cl.b}[{cl.w}2{cl.b}]{cl.w} Dymo (Coming Soon)")
    print(f"{cl.space}{cl.b}[{cl.w}3{cl.b}]{cl.w} Google")
    print(f"{cl.space} {cl.w}|")
    print(f"{cl.space}{cl.b}[{cl.w}4{cl.b}]{cl.w} Groq")
    print(f"{cl.space}{cl.b}[{cl.w}5{cl.b}]{cl.w} Meta (Coming Soon)")
    print(f"{cl.space}{cl.b}[{cl.w}6{cl.b}]{cl.w} OpenAI")
    print(f"{cl.space} {cl.w}|")
    print(f"{cl.space}{cl.b}[{cl.w}7{cl.b}]{cl.w} Perplexity")
    selector = str(input(f"{cl.space}{cl.b}[{cl.w}?{cl.b}]{cl.w} Select a number:{cl.b} ").lower())
    # Show available models.
    if selector == "1": show_models("Anthropic")
    elif selector == "2": show_models("Dymo")
    elif selector == "3": show_models("Google")
    elif selector == "4": show_models("Groq")
    elif selector == "5": show_models("Meta")
    elif selector == "5": show_models("OpenAI")
    elif selector == "5": show_models("Perplexity")
    else: restart()