"""Project CRUD operations (get, update, delete, archive)."""

import json
from typing import Optional

import click
import typer
from rich.table import Table

from proj.error_handler import (
    handle_error,
    APIError,
    BackendConnectionError,
    TimeoutError,
)

from .helpers import get_client, STATUS_EMOJI, console


def get_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format: table, json",
        click_type=click.Choice(["table", "json"], case_sensitive=False),
    ),
):
    """Get a project by ID."""
    try:
        client = get_client()
        project = client.get_project(project_id)

        if format == "json":
            console.print_json(json.dumps(project, indent=2))
        else:
            table = Table(
                title=f"Project {project_id}",
                show_header=True,
                header_style="bold magenta",
                border_style="blue",
            )
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")

            for key, value in project.items():
                display_value = str(value) if value else ""
                if key == "status" and value in STATUS_EMOJI:
                    display_value = f"{STATUS_EMOJI[value]} {display_value}"
                table.add_row(key, display_value)

            console.print(table)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def update_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    name: Optional[str] = typer.Option(
        None, "--name", "-n", help="New name"
    ),
    description: Optional[str] = typer.Option(
        None, "--desc", "-d", help="New description"
    ),
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="New status"
    ),
    organization: Optional[str] = typer.Option(
        None, "--org", "-o", help="New organization"
    ),
    classification: Optional[str] = typer.Option(
        None, "--class", "-c", help="New classification"
    ),
    path: Optional[str] = typer.Option(
        None, "--path", "-p", help="New local path"
    ),
    remote_url: Optional[str] = typer.Option(
        None, "--url", "-u", help="New remote URL"
    ),
):
    """Update a project."""
    try:
        data = {}
        if name:
            data["name"] = name
        if description:
            data["description"] = description
        if status:
            data["status"] = status
        if organization:
            data["organization"] = organization
        if classification:
            data["classification"] = classification
        if path:
            data["path"] = path
        if remote_url:
            data["remote_url"] = remote_url

        if not data:
            console.print("[yellow]No updates provided.[/yellow]")
            raise typer.Exit(1)

        client = get_client()
        client.update_project(project_id, data)

        console.print(f"[green]✓ Updated project {project_id}[/green]")
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def delete_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Skip confirmation"
    ),
):
    """Delete a project permanently."""
    try:
        if not force:
            confirm = typer.confirm(f"Delete project {project_id}?")
            if not confirm:
                raise typer.Abort()

        client = get_client()
        client.delete_project(project_id)

        console.print(f"[green]✓ Deleted project {project_id}[/green]")
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def archive_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(
        False, "--force", "-f", help="Skip confirmation"
    ),
):
    """Archive a project.

    Sets status to completed, classification to archive.
    """
    try:
        if not force:
            confirm = typer.confirm(f"Archive project {project_id}?")
            if not confirm:
                raise typer.Abort()

        client = get_client()
        project = client.archive_project(project_id)

        project_name = project.get('name')
        console.print(
            f"[green]✓ Archived project {project_id}: "
            f"{project_name}[/green]"
        )
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
