from rich.console import Console
from rich.theme import Theme

# Custom theme for consistent styling
custom_theme = Theme(
    {
        "info": "dim cyan",
        "success": "bold green",
        "warning": "magenta",
        "danger": "bold red",
        "highlight": "bold yellow",
        "table.title": "bold cyan",
    }
)

console = Console(theme=custom_theme)
