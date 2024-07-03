import re
from textual.timer import Timer
from urllib.parse import urlparse
from textual.app import App, ComposeResult
from textual.containers import Center, Middle
from textual.widgets import Footer, ProgressBar

def validURL(url):
    try:
        r = urlparse(url)
        return all([r.scheme, r.netloc])
    except ValueError:
        return False
    
def validTarget(target):
    # Validate IP address (IPv4).
    if re.compile(r"^(\d{1,3}\.){3}\d{1,3}$").match(target):
        parts = target.split(".")
        if all(0 <= int(part) <= 255 for part in parts): return True
    
    # Validate domain.
    if re.compile(r"^(?=.{1,253}$)(?:(?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$").match(target): return True
    return False
    
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