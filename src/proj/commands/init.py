"""First-run initialization command."""
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from proj.config import Config, ensure_dirs, get_config_file

console = Console()


def init_command(
    force: bool = typer.Option(
        False, "--force", "-f", help="Overwrite existing config"
    ),
):
    """Initialize proj configuration."""
    config_file = get_config_file()

    if config_file.exists() and not force:
        console.print(
            f"[yellow]Config already exists at {config_file}[/yellow]"
        )
        if not Confirm.ask("Overwrite?"):
            raise typer.Abort()

    console.print(
        Panel.fit(
            "[bold green]Welcome to proj![/bold green]\n\n"
            "Let's set up your configuration.",
            title="🚀 proj-cli",
        )
    )

    # Get API URL
    api_url = Prompt.ask(
        "work-prod API URL",
        default="http://localhost:5000",
    )

    # Get GitHub username
    github_username = Prompt.ask(
        "GitHub username (for inventory scanning)",
        default="",
    )

    # Get local scan directories
    console.print(
        "\n[dim]Enter directories to scan for local projects "
        "(comma-separated)[/dim]"
    )
    default_dir = str(Path.home() / "Projects")
    scan_dirs_str = Prompt.ask(
        "Local scan directories",
        default=default_dir,
    )
    scan_dirs = [d.strip() for d in scan_dirs_str.split(",") if d.strip()]

    # Create config
    ensure_dirs()
    config = Config(
        api_url=api_url,
        github_username=github_username or None,
        local_scan_dirs=scan_dirs,
    )
    config.save()

    console.print(f"\n[green]✓ Configuration saved to {config_file}[/green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Run [cyan]proj list[/cyan] to see projects")
    console.print(
        "  2. Run [cyan]proj inv scan github[/cyan] to scan GitHub repos"
    )
    console.print("  3. Run [cyan]proj --help[/cyan] for all commands")
