"""Project import/export commands."""

import json
from pathlib import Path

import typer

from proj.error_handler import (
    handle_error,
    APIError,
    BackendConnectionError,
    TimeoutError,
)

from .helpers import get_client, console


def import_json(
    file: Path = typer.Argument(
        ..., help="JSON file to import", exists=True
    ),
):
    """Import projects from JSON file."""
    try:
        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            projects = data
        elif isinstance(data, dict) and "projects" in data:
            projects = data["projects"]
        else:
            msg = (
                "[red]Error: Invalid JSON format. "
                "Expected list or {projects: [...]}[/red]"
            )
            console.print(msg)
            raise typer.Exit(1)

        client = get_client()
        result = client.import_projects(projects)

        imported = result.get('imported', 0)
        skipped = result.get('skipped', 0)
        console.print(f"[green]✓ Imported: {imported}[/green]")
        console.print(f"[yellow]  Skipped: {skipped}[/yellow]")
        if result.get("errors"):
            console.print(
                f"[red]  Errors: {len(result.get('errors', []))}[/red]"
            )
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON: {e}[/red]")
        raise typer.Exit(1)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
