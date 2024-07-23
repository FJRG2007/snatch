import src.lib.colors as cl
from rich.panel import Panel
from cartesia import Cartesia
from rich import print as rprint
from rich.console import Console
from urllib.parse import urlparse
from rich.markdown import Markdown
import os, re, sys, time, pyaudio, importlib, threading

# It is imported in this way to avoid the circular import error.
config_module = importlib.import_module("src.lib.config")

def playVoice(prompt) -> None:
    if not config_module.config.ai.text_to_speech: return
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key or len(api_key) < 7: return terminal("h", "You can set Cartesia's API Key to listen to your assistant.")
    client = Cartesia(api_key=api_key)
    voice = client.voices.get(id="79a125e8-cd45-4c13-8a67-188112f4dd22")
    p = pyaudio.PyAudio()
    stream = None
    # Generate and stream audio.
    for output in client.tts.sse(
        model_id="sonic-english",
        transcript=prompt,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    ):
        if not stream: stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        # Write the audio data to the stream.
        stream.write(output["audio"])
    stream.stop_stream()
    stream.close()
    p.terminate()

console = Console()

def cls() -> None:
    print(f"{cl.b}{cl.ENDC}", end="")
    if sys.platform == "win32": os.system("cls")
    else: os.system("clear")

def coloredText(word, hex_color) -> str:
    try:
        if not word.startswith("#"): word = f"#{str(word)}"
        rgb = tuple(int(hex_color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{str(word)}\033[0m"
    except: return word

def quest(prompt, newline=False, lowercase=False, tab=False, format_type=str):
    prefix = f"\n" if newline else ''
    prefix += f"\t" if tab else ''
    while True:
        try:
            response = input(f"{prefix}{cl.b}[{cl.w}?{cl.b}]{cl.w} {prompt}: ")
            if format_type == int: return int(response)
            elif format_type == str and lowercase: return response.lower()
            return response
        except ValueError: terminal("e", "Enter a valid value.", timer=True)

def getPositive(q, default=True) -> bool:
    positive_responses = ["y", "yes", "yeah", "continue", "s", "si", "sí", "oui", "wa", "ja"]
    if default: positive_responses.append("")
    return q.lower() in positive_responses

def noToken(name) -> str: 
    return f"{cl.y}Set up your {name} token.{cl.w}"

def validURL(url) -> bool:
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc])
    except ValueError: return False
    
def getTypeString(v) -> str:
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', v): return "email"
    elif re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', v): return "tel"
    else: return "unknown"
    
def setColor(v):
    return f"{cl.g}True{cl.w}" if v == "True" or v == True else \
           f"{cl.r}False{cl.w}" if v == "False" or v == False else \
           f"{cl.r}{v}{cl.w}" if any(term in str(v).lower() for term in ["not", "error"]) else \
           f"{cl.y}{v}{cl.w}" if any(term in str(v).lower() for term in ["coming soon"]) else \
           f"{v}"

def validTarget(target) -> bool:
    # Validate IP address (IPv4).
    if re.compile(r"^(\d{1,3}\.){3}\d{1,3}$").match(target):
        if all(0 <= int(part) <= 255 for part in target.split(".")): return True
    # Validate domain.
    return re.compile(r"^(?=.{1,253}$)(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,10}$").match(target)

def terminal(typeMessage, string="", exitScript=False, clear="n", newline=True, timer=False) -> None:
    if (clear == "b" or typeMessage == "iom"): cls()
    if isinstance(typeMessage, str):
        if typeMessage == "e": print(f"\n{cl.R} ERROR {cl.w} {string}") # X or ❌
        if typeMessage == "s": print(f"\n{cl.g}✅ {string}{cl.w}") # ✓ or ✅
        if typeMessage == "i": rprint(f"{'\n' if newline else ''}[cyan]{string}[/cyan]")
        if typeMessage == "w": rprint(f"\n[bold yellow]Warning:[/bold yellow] [yellow]{string}[/yellow]")
        if typeMessage == "h": print(f"\n{cl.B}💡 TIP {cl.w} {string}") # X or ❌
        if typeMessage == "nmi": print(f"\n{cl.R} ERROR {cl.w} Could not install {string}. Please install it manually.")
        if typeMessage == "nei": print(f"\n{cl.R} ERROR {cl.w} {string} is not installed or not found in PATH. Please install it manually.")
        if typeMessage == "l": print("\nThis may take a few seconds...")
        if typeMessage == "ai": 
            console.print(Panel(Markdown(string), title="Model's Response", title_align="left", expand=False, style="bold white"))
            tr = threading.Thread(target=playVoice, args=(string,))
            tr.daemon = True
            tr.start()
        if typeMessage == "info": console.print(Panel(Markdown(string), title="Snatch", title_align="left", expand=False, style="bold white"))
        if typeMessage == "iom": 
            print(f"\n{cl.R} ERROR {cl.w} Please enter a valid option.")
            time.sleep(2)
    elif isinstance(typeMessage, type) and issubclass(typeMessage, BaseException):
        if typeMessage == KeyboardInterrupt: print(f"\n{cl.R} ERROR {cl.w} Exiting Program: Canceled by user.")
        sys.exit(1)
    else: print(f"\nUnhandled typeMessage: {typeMessage}")
    if exitScript: sys.exit(1 if typeMessage == "e" else 0)
    if clear == "a" or typeMessage == "iom": cls()
    if timer: time.sleep(2)

def fileManager(path, filename, create=True):
    directory = f"output/{path}/{filename}"
    filename = re.sub(r'[^A-Za-z0-9._@-]', "", filename)
    if create: os.makedirs(os.path.dirname(directory), exist_ok=True)
    return directory