"""Project listing and search commands."""

import json
from typing import Optional

import click
import typer
from rich.console import Console
from rich.table import Table

from proj.constants import PROJECT_TYPE_HELP
from proj.error_handler import (
    handle_error,
    APIError,
    BackendConnectionError,
    InvalidProjectTypeError,
    TimeoutError,
)

from .helpers import STATUS_EMOJI

console = Console()


def _get_package_imports():
    """Get imports from package level for test patching compatibility."""
    from proj.commands import projects
    return projects


def list_projects(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status"
    ),
    organization: Optional[str] = typer.Option(
        None, "--org", "-o", help="Filter by organization"
    ),
    classification: Optional[str] = typer.Option(
        None, "--class", "-c", help="Filter by classification"
    ),
    project_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help=PROJECT_TYPE_HELP
    ),
    search: Optional[str] = typer.Option(
        None, "--search", help="Search in names and descriptions"
    ),
    wide: bool = typer.Option(
        False, "--wide", "-w", help="Show all columns"
    ),
    format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format: table, json",
        click_type=click.Choice(["table", "json"], case_sensitive=False),
    ),
):
    """List all projects with optional filters."""
    pkg = _get_package_imports()
    try:
        client = pkg.get_client()
        projects = client.list_projects(
            status=status,
            organization=organization,
            classification=classification,
            project_type=project_type,
            search=search,
        )

        if format == "json":
            console.print_json(json.dumps(projects, indent=2))
        else:
            if not projects:
                console.print("[yellow]No projects found.[/yellow]")
                return

            table = Table(
                title=f"Projects ({len(projects)})",
                show_header=True,
                header_style="bold magenta",
                border_style="blue",
            )
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name", style="green")

            if wide or status:
                table.add_column("Status", style="yellow")
            if wide or organization:
                table.add_column("Org", style="blue")
            if wide or classification:
                table.add_column("Classification", style="magenta")
            if wide or project_type:
                table.add_column("Type", style="cyan")

            table.add_column("Path", style="blue")

            if wide or search:
                table.add_column("Description", style="dim")

            table.add_column("Created", style="magenta")

            for p in projects:
                row = [str(p.get("id", "")), p.get("name", "")]
                if wide or status:
                    status_val = p.get("status", "")
                    emoji = STATUS_EMOJI.get(status_val, "")
                    if emoji:
                        row.append(f"{emoji} {status_val}")
                    else:
                        row.append(status_val)
                if wide or organization:
                    row.append(p.get("organization", ""))
                if wide or classification:
                    row.append(p.get("classification", ""))
                if wide or project_type:
                    row.append(p.get("project_type", "-"))
                row.append(p.get("path", "") or "")
                if wide or search:
                    row.append(p.get("description", "") or "")
                row.append(
                    p.get("created_at", "")[:10] if p.get("created_at") else ""
                )
                table.add_row(*row)

            console.print(table)
    except InvalidProjectTypeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def search_projects(
    query: str = typer.Argument(..., help="Search query"),
    wide: bool = typer.Option(
        False, "--wide", "-w", help="Show all columns"
    ),
    format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format: table, json",
        click_type=click.Choice(["table", "json"], case_sensitive=False),
    ),
):
    """Search projects by name or description."""
    pkg = _get_package_imports()
    try:
        client = pkg.get_client()
        projects = client.search_projects(query)

        if format == "json":
            console.print_json(json.dumps(projects, indent=2))
        else:
            if not projects:
                msg = f"[yellow]No projects found for '{query}'.[/yellow]"
                console.print(msg)
                return

            table = Table(
                title=f"Search Results: {query}",
                show_header=True,
                header_style="bold magenta",
                border_style="blue",
            )
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")

            if wide:
                table.add_column("Org", style="blue")
                table.add_column("Classification", style="magenta")
                table.add_column("Path", style="blue")

            table.add_column("Description", style="dim")

            if wide:
                table.add_column("Created", style="magenta")

            for p in projects:
                status_val = p.get("status", "")
                emoji = STATUS_EMOJI.get(status_val, "")
                if emoji:
                    status_display = f"{emoji} {status_val}"
                else:
                    status_display = status_val

                row = [
                    str(p.get("id", "")),
                    p.get("name", ""),
                    status_display,
                ]
                if wide:
                    row.append(p.get("organization", "") or "")
                    row.append(p.get("classification", "") or "")
                    row.append(p.get("path", "") or "")
                row.append((p.get("description", "") or "")[:50])
                if wide:
                    created = p.get("created_at", "")
                    row.append(created[:10] if created else "")
                table.add_row(*row)

            console.print(table)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
