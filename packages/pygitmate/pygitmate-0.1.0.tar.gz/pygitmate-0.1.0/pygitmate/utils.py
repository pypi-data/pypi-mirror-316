from .console import console
from git import Repo
from rich.prompt import IntPrompt
from rich.table import Table
from datetime import datetime


# Utility function to get recent branches
def get_branches(repo: Repo, number=10):
    # Get a list of the most recent branches
    return [branch for branch in repo.branches][:number]


# Utility function to get the git repository
def get_repo() -> Repo:
    try:
        return Repo(".")
    except Exception:
        console.print("Error: Not a Git repository. Exiting.", style="danger")
        exit(1)


# Utility to display table options
def display_options(title, options):
    table = Table(title=f"[table.title]{title}")
    table.add_column("Option", style="magenta", justify="center")
    table.add_column("Value", style="white")
    for i, option in enumerate(options, start=1):
        table.add_row(str(i), option)
    console.print(table)


# Utility to get timestamp
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Function to dynamically choose from options
def choose_option(prompt_text, options):
    display_options(prompt_text, options)
    choice = IntPrompt.ask(
        f"Enter [highlight]{prompt_text}[/] number",
        choices=[str(i) for i in range(1, len(options) + 1)],
    )
    return options[choice - 1]
