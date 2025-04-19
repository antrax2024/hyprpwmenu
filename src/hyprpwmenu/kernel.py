from dotenv import load_dotenv
from rich.console import Console

cl = Console()


def printLine() -> None:
    cl.print("-" * 80, style="cyan")
