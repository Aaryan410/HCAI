from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.live import Live
import time

mono_theme = Theme({
    "markdown.h1": "bold white",
    "markdown.h2": "bold white",
    "markdown.h3": "bold white underline",
    "markdown.code": "grey70 on grey15",
    "markdown.item.bullet": "grey70",
    "markdown.block_quote": "italic grey50"
})

console = Console(theme=mono_theme)

def render_response(text: str) -> None:
    console.print(Markdown(text))

def render_stream(chunks):
    full_response = ""
    last_refresh = time.monotonic()

    with Live(Markdown(""), console=console, vertical_overflow="visible") as live:

        for chunk in chunks:
            full_response += chunk

            now = time.monotonic()

            if now - last_refresh >= 0.05:
                live.update(Markdown(full_response))
                last_refresh = now

        live.update(Markdown(full_response))

    return full_response
