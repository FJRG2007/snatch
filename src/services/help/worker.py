from textual.widgets import Markdown
from src.utils.basics import terminal
from textual.app import App, ComposeResult

general = ["welcome", "commands"]

def main(section):
    section = "welcome" if not section or section.lower().strip() == "help" else section.lower().strip()
    try:
        with open(f"docs/help/{"" if section in general else "commands/"}{section}.md", "r", encoding="utf-8") as file:
            content = file.read()
            class MarkdownExampleApp(App):
                def compose(self) -> ComposeResult:
                    yield Markdown(content)
            MarkdownExampleApp().run()
    except FileNotFoundError: return terminal("e", f"No documentation exists for \"{section}\".")