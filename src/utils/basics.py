import src.lib.colors as cl
from rich.panel import Panel
# from rich.syntax import Syntax
from textual.timer import Timer
from rich import print as rprint
from rich.console import Console
from urllib.parse import urlparse
from rich.markdown import Markdown
from cartesia import AsyncCartesia
from textual.app import App, ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Footer, ProgressBar
import os, re, sys, time, asyncio, pyaudio, concurrent.futures

async def playVoice(prompt) -> None:
    api_key = os.getenv("CARTESIA_API_KEY")
    if not api_key or len(api_key) < 7: return terminal("h", "You can set Cartesia's API Key to listen to your assistant.")
    client = AsyncCartesia(api_key=api_key)
    voice = client.voices.get(id="79a125e8-cd45-4c13-8a67-188112f4dd22")
    p = pyaudio.PyAudio()
    stream = None
    # Generate and stream audio.
    async for output in await client.tts.sse(
        model_id="sonic-english",
        transcript=prompt,
        voice_embedding=voice["embedding"],
        stream=True,
        output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    ):
        buffer = output["audio"]

        if not stream: stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=True)
        # Write the audio data to the stream.
        stream.write(buffer)
    stream.stop_stream()
    stream.close()
    p.terminate()
    await client.close()

console = Console()

def cls() -> None:
    print(cl.b, end="")
    if sys.platform == "win32": os.system("cls")
    else: os.system("clear")

def getPositive(q):
    return q.lower() in ["", "y", "yes", "yeah", "continue", "s", "si", "sí", "oui", "wah", "ja"]

def noToken(name): 
    return f"{cl.y}Set up your {name} token.{cl.w}"

def validURL(url):
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc])
    except ValueError: return False
    
def getTypeString(v):
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', v): return "email"
    elif re.match(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$', v): return "tel"
    else: return "unknown"
    
def setColor(v):
    if (v == "True" or v == True): return f"{cl.g}True{cl.w}"
    elif (v == "False" or v == False): return f"{cl.r}False{cl.w}"
    else: return f"{v}"

def validTarget(target):
    # Validate IP address (IPv4).
    if re.compile(r"^(\d{1,3}\.){3}\d{1,3}$").match(target):
        parts = target.split(".")
        if all(0 <= int(part) <= 255 for part in parts): return True
    # Validate domain.
    return re.compile(r"^(?=.{1,253}$)(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,10}$").match(target)

def terminal(typeMessage, string="", exitScript=False, clear="n"):
    asyncio.run(playVoice("This is a wonderful test in Snatch"))
    if (clear == "b" or typeMessage == "iom"): cls()
    if isinstance(typeMessage, str):
        if typeMessage == "e": print(f"{cl.R} ERROR {cl.w} {string}") # X or ❌
        if typeMessage == "s": rprint(f"[green]✅ {string}[/green]") # ✓ or ✅
        if typeMessage == "i": rprint(f"[cyan]{string}[/cyan]")
        if typeMessage == "w": rprint(f"[bold yellow]Warning:[/bold yellow] [yellow]{string}[/yellow]")
        if typeMessage == "h": print(f"{cl.B}💡 TIP {cl.w} {string}") # X or ❌
        if typeMessage == "nmi": print(f"{cl.R} ERROR {cl.w} Could not install {string}. Please install it manually.")
        if typeMessage == "nei": print(f"{cl.R} ERROR {cl.w} {string} is not installed or not found in PATH. Please install it manually.")
        if typeMessage == "l": print("This may take a few seconds...")
        if typeMessage == "ai": 
            console.print(Panel(Markdown(string), title="Model's Response", title_align="left", expand=False, style="bold white"))
            playVoice(string)
        if typeMessage == "info": console.print(Panel(Markdown(string), title="Snatch", title_align="left", expand=False, style="bold white"))
        if typeMessage == "iom": 
            print(f"{cl.R} ERROR {cl.w} Please enter a valid option.")
            time.sleep(2)
    elif isinstance(typeMessage, type) and issubclass(typeMessage, BaseException):
        if typeMessage == KeyboardInterrupt: print(f"{cl.R} ERROR {cl.w} Exiting Program: Canceled by user.")
        sys.exit(1)
    else: print("Unhandled typeMessage:", typeMessage)
    if (exitScript): sys.exit(1)
    if (clear == "a" or typeMessage == "iom"): cls()
    
def progressBar():
    class IndeterminateProgressBar(App[None]):
        BINDINGS = [("s", "start", "Start")]
        progress_timer: Timer
        """Timer to simulate progress happening."""
        def compose(self) -> ComposeResult:
            with Center():
                with Middle():
                    yield ProgressBar()
            yield Footer()

        def on_mount(self) -> None:
            """Set up a timer to simulate progess happening."""
            self.progress_timer = self.set_interval(1 / 10, self.make_progress, pause=True)

        def make_progress(self) -> None:
            """Called automatically to advance the progress bar."""
            self.query_one(ProgressBar).advance(1)

        def action_start(self) -> None:
            """Start the progress tracking."""
            self.query_one(ProgressBar).update(total=100)
            self.progress_timer.resume()

    IndeterminateProgressBar().run()