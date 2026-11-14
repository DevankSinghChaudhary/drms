from rich.console import Console
from rich.panel import Panel

console = Console()


def header(title: str | int, sub_title: str | int):
    console.clear()
    console.print(
        Panel(
            f"[bold orange1]{title}[/bold orange1]\n[white]{sub_title}[/white]",
            border_style="orange1",
        )
    )
