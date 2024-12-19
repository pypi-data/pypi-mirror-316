import click
from git import GitCommandError
from rich.prompt import Prompt

from pygitmate.utils import choose_option, get_branches, get_repo, get_timestamp
from pygitmate.console import console


# Dynamic options for branch and commit types
BRANCH_TYPES = ["feature", "hotfix", "enhance", "chore"]
COMMIT_TYPES = ["feat", "fix", "enhance", "docs", "chore"]


# CLI Group
@click.group()
def cli():
    """Git Mate - A CLI tool to simplify Git workflows."""
    pass


# Command: Create a new branch
@click.command()
@click.option("--branch-type", help="Type of branch (feature, hotfix, enhance, chore).")
@click.option("--base", default="master", help="Base branch to create from.")
@click.argument("name", required=False)
def new_branch(branch_type, base, name):
    """Create a new branch interactively."""
    repo = get_repo()

    # Dynamic prompts if options are not provided
    branch_type = branch_type or choose_option("Branch Type", BRANCH_TYPES)
    base = base or Prompt.ask("Enter base branch", default="master")
    branches = get_branches(repo)

    console.print("Recent branches:", style="info")
    for i, branch in enumerate(branches, start=1):
        console.print(f"{i}. {branch}", style="info")
    console.print(
        "Use full for making a new branch for fixes and enhancements", style="info"
    )

    name = name or Prompt.ask("Enter branch name (without spaces)")

    try:
        if repo.is_dirty():
            console.print("Warning: Working directory not clean.", style="warning")

        if "origin" not in repo.remotes:
            console.print(
                "No remote named 'origin' found. Skipping fetch.", style="warning"
            )
        else:
            console.print(f"Fetching latest changes from '{base}'...", style="info")
            repo.remotes.origin.fetch()

        console.print(f"Switching to base branch '{base}'...", style="highlight")
        repo.git.checkout(base)
        # repo.git.pull()

        branch_name = f"{branch_type}/{name}"
        console.print(f"Creating new branch '{branch_name}'...", style="info")
        repo.git.checkout("-b", branch_name)

        console.print(
            f"Successfully created and switched to '{branch_name}'.", style="success"
        )
    except GitCommandError as e:
        console.print(f"Error: {e}", style="danger")


# Command: Commit with standard guidelines
@click.command()
@click.option("--type", help="Commit type (feat, fix, enhance, docs, chore).")
@click.option("--summary", help="Short summary of changes.")
@click.option("--description", help="Detailed description of the commit.")
def commit(type, summary, description):
    """Add, commit, and push changes interactively with standard format."""
    repo = get_repo()

    # Dynamic prompts if options are not provided
    type = type or choose_option("Commit Type", COMMIT_TYPES)
    summary = summary or Prompt.ask("Enter short summary (max 50 chars)")
    description = description or Prompt.ask("Enter detailed description")

    try:
        # Stage all changes
        console.print("Staging all changes...", style="info")
        repo.git.add("--all")

        # Commit
        commit_message = f"{type}: {summary}\n\n{description}"
        console.print("Committing changes...", style="info")
        repo.git.commit("-m", commit_message)
        console.print("Successfully Committed message", style="highlight")

        # Push changes
        if "origin" in repo.remotes:
            current_branch = repo.active_branch.name
            console.print(
                f"Pushing changes to branch '{current_branch}'...", style="highlight"
            )
            repo.git.push("origin", current_branch)
            console.print("Successfully pushed changes.", style="success")

    except GitCommandError as e:
        console.print(f"Error: {e}", style="danger")


# Command: Merge the current branch into target branch


@click.command()
@click.argument("target", required=False)
def merge(target):
    """Merge the current branch into a specified target branch."""
    repo = get_repo()

    try:
        # Get a list of the most recent 10 branches
        branches = get_branches(repo)

        if not target:
            console.print("Recent branches:", style="info")
            for i, branch in enumerate(branches, start=1):
                console.print(f"{i}. {branch}", style="info")
            console.print(f"{len(branches) + 1}. master (default)", style="info")

            choice = Prompt.ask(
                "Select the target branch by number or enter branch name",
                choices=[str(i) for i in range(1, len(branches) + 2)] + branches,
                default=str(len(branches) + 1),
            )

            if choice.isdigit() and int(choice) <= len(branches):
                target = branches[int(choice) - 1]
            elif choice == str(len(branches) + 1):
                target = "master"
            else:
                target = choice

        current_branch = repo.active_branch.name

        # Check if the working directory is clean
        if repo.is_dirty():
            console.print(
                "Warning: Uncommitted changes detected in the working directory.",
                style="warning",
            )
            should_stash = Prompt.ask(
                "Do you want to stash the changes? (yes/no)",
                choices=["yes", "no"],
                default="yes",
            )

            if should_stash == "yes":
                timestamp = get_timestamp()
                stash_message = f"Stash before merging into {target} at {timestamp}"
                console.print("Stashing uncommitted changes...", style="info")
                repo.git.stash("push", "-m", stash_message)
                console.print(
                    f"Changes have been stashed with message: '{stash_message}'.",
                    style="success",
                )
            else:
                console.print("Aborting merge to avoid data loss.", style="danger")
                return

        # Proceed with the merge
        console.print(f"Switching to target branch '{target}'...", style="highlight")
        repo.git.checkout(target)

        console.print(
            f"Merging branch '{current_branch}' into '{target}'...", style="info"
        )
        repo.git.merge(current_branch)

        console.print(
            f"Successfully merged '{current_branch}' into '{target}'.", style="success"
        )

        # Apply the stash back, if any
        if repo.git.stash("list"):
            console.print("Applying stashed changes...", style="info")
            repo.git.stash("pop")
            console.print("Stashed changes have been applied.", style="success")

    except GitCommandError as e:
        console.print(f"Error: {e}", style="danger")


# Add commands to the main CLI
cli.add_command(new_branch)
cli.add_command(commit)
cli.add_command(merge)

# Main entry point
if __name__ == "__main__":
    cli()
