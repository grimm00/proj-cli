"""Inventory management commands."""
import json
from pathlib import Path

import typer
from rich.console import Console

from proj.config import Config, get_data_dir

console = Console()

# Main inventory command group
inv_app = typer.Typer(
    name="inv",
    help="Inventory management commands.",
    no_args_is_help=True,
)

# Scan subcommand group
scan_app = typer.Typer(
    name="scan",
    help="Scan commands for discovering projects.",
    no_args_is_help=True,
)

# Export subcommand group
export_app = typer.Typer(
    name="export",
    help="Export commands for inventory data.",
    no_args_is_help=True,
)

# Add subgroups to main inv app
inv_app.add_typer(scan_app, name="scan")
inv_app.add_typer(export_app, name="export")


def get_config() -> Config:
    """Get loaded config."""
    return Config.load()


def get_inventory_file() -> Path:
    """Get path to inventory data file."""
    return get_data_dir() / "inventory.json"


def load_inventory() -> list[dict]:
    """Load inventory from data file."""
    inv_file = get_inventory_file()
    if inv_file.exists():
        with open(inv_file, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_inventory(data: list[dict]) -> None:
    """Save inventory to data file."""
    inv_file = get_inventory_file()
    inv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(inv_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# Placeholder commands - will be implemented in subsequent tasks
@scan_app.command(name="github")
def scan_github():
    """Scan GitHub repositories."""
    console.print("[yellow]Not implemented yet[/yellow]")


@scan_app.command(name="local")
def scan_local():
    """Scan local project directories."""
    console.print("[yellow]Not implemented yet[/yellow]")


@inv_app.command(name="analyze")
def analyze():
    """Analyze tech stack of scanned projects."""
    console.print("[yellow]Not implemented yet[/yellow]")


@inv_app.command(name="dedupe")
def dedupe():
    """Deduplicate inventory entries."""
    console.print("[yellow]Not implemented yet[/yellow]")


@export_app.command(name="json")
def export_json():
    """Export inventory to JSON file."""
    console.print("[yellow]Not implemented yet[/yellow]")


@export_app.command(name="api")
def export_api():
    """Push inventory to work-prod API."""
    console.print("[yellow]Not implemented yet[/yellow]")


@inv_app.command(name="status")
def status():
    """Show inventory status."""
    console.print("[yellow]Not implemented yet[/yellow]")
