from rich.console import Console, Group
from rich.markdown import Markdown
from rich.theme import Theme
from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule

mono_theme = Theme ({
    "markdown.h1": "bold white",
    "markdown.h2": "bold white",
    "markdown.h3": "bold white underline",
    "markdown.code": "grey70 on grey15",
    "markdown.item.bullet": "grey70",
    "markdown.block_quote": "italic grey50",
    "hcai.header": "bold white",
    "hcai.subtle": "grey58",
    "hcai.you": "bold cyan",
    "hcai.model": "bold white",
    "hcai.footer": "grey50"
})

console = Console(theme=mono_theme)

def print_banner(config, model_name: str) -> None:
    header = Text()
    header.append("HCAI", style = "hcai.header")
    header.append(" v1.0.2", style = "hcai.subtle")

    right = Text(f"{model_name} . {config['provider']}", style = "hcai.subtle")

    line = Text()
    line.append_text(header)
    pad = console.width - len(header.plain) - len(right.plain) - 4
    if pad > 0:
        line.append(" " * pad)
    line.append_text(right)

    console.print(Panel(line, border_style = "grey42", padding = (0, 1)))
    console.print()


def print_user_message(prompt: str) -> None:
    console.print(Panel(prompt, title = "You", title_align = "left", 
                        border_style = "grey42", style = "hcai.you", 
                        padding = (0, 1)))


def format_footer(elapsed: float | None, total_tokens: int | None) -> str:
    parts = []

    if elapsed is not None:
        parts.append(f"⏱ {elapsed:.1f}s")

    if total_tokens is not None:
        parts.append(f"{total_tokens} tokens")

    return " . ".join(parts)


def render_response(text: str) -> None:
    console.print(Markdown(text))


def render_stream(chunks, model_name: str = "HCAI", meta: dict | None = None):
    
    full_response = ""

    with Live(Text(""), console = console, refresh_per_second = 20) as live:

        for chunk in chunks:
            full_response += chunk 

            body = Markdown(full_response) if full_response.strip() else Text("")

            panel = Panel (
                body, 
                title = model_name,
                title_align = "left",
                border_style = "grey42",
                padding = (0, 1)
            )

            live.update(panel)

        if meta:
            footer_text = format_footer(meta.get("elapsed"), meta.get("total_tokens"))

            if footer_text:
                body = Markdown(full_response) if full_response.strip() else Text("")
                group = Group(body, Rule(style = "grey27"), Text(footer_text, style = "hcai.footer"))

                panel = Panel (
                    group,
                    title = model_name,
                    title_align = "left",
                    border_style = "grey42",
                    padding = (0, 1)
                )

                live.update(panel)

    console.print()

    return full_response
