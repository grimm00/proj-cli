"""Project management commands."""

import json
import subprocess
from pathlib import Path
from typing import Optional

import click
import typer
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from proj.api_client import APIClient
from proj.config import Config
from proj.error_handler import (
    handle_error, APIError, BackendConnectionError, TimeoutError
)
from proj.registry import add_project
from proj.templates import (
    create_from_template,
    get_templates_source,
    list_templates,
    TemplateError,
)

console = Console()

# Status emoji mapping (shared constant)
STATUS_EMOJI = {
    "active": "🟢",
    "inactive": "⚪",
    "archived": "📦",
    "completed": "✅",
}


def get_client() -> APIClient:
    """Get configured API client."""
    return APIClient(Config.load())


def init_git(project_path: Path) -> bool:
    """Initialize git repository in project.

    Args:
        project_path: Path to project directory.

    Returns:
        True if successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "init"],
            cwd=project_path,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except Exception:
        return False


def prompt_for_create_options(config: Config) -> dict:
    """Prompt user for create options interactively.

    Args:
        config: proj-cli configuration.

    Returns:
        Dict with user choices: name, template, target_dir, description.

    Raises:
        KeyboardInterrupt: If user cancels (Ctrl+C).
    """
    name = Prompt.ask("Project name")

    # List available templates
    templates_source = get_templates_source(config)
    available = list_templates(templates_source)
    default_template = (
        config.templates.default if hasattr(config, 'templates') and
        hasattr(config.templates, 'default') else None
    )
    template = Prompt.ask(
        "Template type",
        choices=available,
        default=default_template or available[0] if available else None,
    )

    default_target = (
        str(config.default_project_dir.expanduser().resolve())
        if config.default_project_dir
        else str(Path.home() / "Projects")
    )
    target_dir_str = Prompt.ask(
        "Target directory",
        default=default_target,
    )
    target_dir = Path(target_dir_str).expanduser().resolve()

    description = Prompt.ask("Description (optional)", default="")

    return {
        "name": name,
        "template": template,
        "target_dir": target_dir,
        "description": description or None,
    }


def _create_project_via_api(
    name: str,
    description: Optional[str] = None,
    status: str = "active",
    organization: Optional[str] = None,
    classification: Optional[str] = None,
    path: Optional[str] = None,
    remote_url: Optional[str] = None,
) -> dict:
    """Create project via API (API-only mode).

    Args:
        name: Project name (required).
        description: Project description.
        status: Project status.
        organization: Organization name.
        classification: Project classification.
        path: Local path.
        remote_url: Remote repository URL.

    Returns:
        Created project data from API.

    Raises:
        APIError: If API call fails.
        BackendConnectionError: If backend is unreachable.
        TimeoutError: If request times out.
    """
    data = {"name": name, "status": status}
    if description:
        data["description"] = description
    if organization:
        data["organization"] = organization
    if classification:
        data["classification"] = classification
    if path:
        data["path"] = path
    if remote_url:
        data["remote_url"] = remote_url

    client = get_client()
    return client.create_project(data)


def detect_create_mode(
    config: Config,
    template: Optional[str],
    api_only: bool,
    local_only: bool,
) -> str:
    """Detect which create mode to use.

    Args:
        config: proj-cli configuration.
        template: Template type if specified.
        api_only: Force API-only mode.
        local_only: Force local-only mode.

    Returns:
        Mode string: "interactive", "api-only", "local-only", "template"

    Raises:
        ValueError: If conflicting flags provided.
    """
    if api_only and local_only:
        raise ValueError(
            "Cannot use --api-only and --local-only together (conflict)"
        )

    if api_only:
        return "api-only"
    if local_only:
        return "local-only"
    if template:
        return "template"

    # Default: interactive
    return "interactive"


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
    try:
        client = get_client()
        projects = client.list_projects(
            status=status,
            organization=organization,
            classification=classification,
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
                row.append(p.get("path", "") or "")
                if wide or search:
                    row.append(p.get("description", "") or "")
                row.append(
                    p.get("created_at", "")[:10] if p.get("created_at") else ""
                )
                table.add_row(*row)

            console.print(table)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


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


def create_project(
    name: Optional[str] = typer.Argument(
        None, help="Project name (required for non-interactive)"
    ),
    description: Optional[str] = typer.Option(
        None, "--desc", "-d", help="Description"
    ),
    status: str = typer.Option("active", "--status", "-s", help="Status"),
    organization: Optional[str] = typer.Option(
        None, "--org", "-o", help="Organization"
    ),
    classification: Optional[str] = typer.Option(
        None, "--class", "-c", help="Classification"
    ),
    path: Optional[str] = typer.Option(
        None, "--path", "-p", help="Local path (for API mode)"
    ),
    remote_url: Optional[str] = typer.Option(
        None, "--url", "-u", help="Remote URL"
    ),
    # New flags for template generation
    template: Optional[str] = typer.Option(
        None, "--template", "-t",
        help="Template type (e.g., standard-project, learning-project)"
    ),
    api_only: bool = typer.Option(
        False, "--api-only",
        help="Create in API only (original behavior)"
    ),
    local_only: bool = typer.Option(
        False, "--local-only",
        help="Create locally only (no API, requires --template)"
    ),
    target_dir: Optional[Path] = typer.Option(
        None, "--target-dir",
        help=(
            "Target directory for template "
            "(default: config.default_project_dir)"
        )
    ),
    no_git: bool = typer.Option(
        False, "--no-git",
        help="Skip git initialization"
    ),
    register: bool = typer.Option(
        True, "--register/--no-register",
        help="Register project in local registry (default: True)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run",
        help="Preview creation without side effects"
    ),
):
    """Create a new project.

    MODES:
    - Interactive (default): Prompts for all options
    - Template: Creates from dev-infra template
    - API-only: Original behavior (backward compatible)
    - Local-only: Template creation without API
    """
    try:
        # Load config for mode detection
        config = Config.load()

        # Handle dry-run mode (preview without side effects)
        if dry_run:
            console.print(
                "[yellow]🔍 Dry-run mode: Preview only[/yellow]"
            )
            console.print("")

            if template:
                # Template mode preview
                templates_source = get_templates_source(config)
                if target_dir:
                    target = Path(target_dir).expanduser().resolve()
                else:
                    if config.default_project_dir:
                        target = (
                            config.default_project_dir.expanduser()
                            .resolve()
                        )
                    else:
                        target = Path.home() / "Projects"
                project_name = name or "[project-name]"
                project_path = target / project_name

                console.print(
                    f"[cyan]Would create project:[/cyan] {project_name}"
                )
                console.print(f"[cyan]Template:[/cyan] {template}")
                console.print(
                    f"[cyan]Target directory:[/cyan] {project_path}"
                )
                if description:
                    console.print(
                        f"[cyan]Description:[/cyan] {description}"
                    )
                if not no_git:
                    console.print(
                        "[cyan]Git initialization:[/cyan] Yes"
                    )
                if register:
                    console.print("[cyan]Registry:[/cyan] Yes")
            elif api_only:
                # API-only mode preview
                console.print(
                    f"[cyan]Would create project via API:[/cyan] {name}"
                )
                if description:
                    console.print(
                        f"[cyan]Description:[/cyan] {description}"
                    )
                if status:
                    console.print(f"[cyan]Status:[/cyan] {status}")
                if organization:
                    console.print(
                        f"[cyan]Organization:[/cyan] {organization}"
                    )
                if classification:
                    console.print(
                        f"[cyan]Classification:[/cyan] {classification}"
                    )
            else:
                # Default mode preview
                project_name = name or "[project-name]"
                console.print(
                    f"[cyan]Would create project:[/cyan] {project_name}"
                )
                if description:
                    console.print(
                        f"[cyan]Description:[/cyan] {description}"
                    )

            console.print("")
            console.print("[dim]No changes made (dry-run mode)[/dim]")
            return

        # Interactive mode (when name is None and no explicit mode)
        # Check this BEFORE mode detection so we can prompt first
        if not name and not api_only and not template:
            try:
                # Prompt for options
                options = prompt_for_create_options(config)

                # Use prompted values
                name = options["name"]
                template = options["template"]
                if target_dir is None:
                    target_dir = options["target_dir"]
                if options["description"]:
                    description = options["description"]
            except KeyboardInterrupt:
                console.print("\n[yellow]Cancelled[/yellow]")
                raise typer.Exit(1)

        # Detect create mode (after interactive prompts if applicable)
        mode = detect_create_mode(
            config=config,
            template=template,
            api_only=api_only,
            local_only=local_only,
        )

        # Validate local-only mode requires template
        if mode == "local-only" and not template:
            console.print(
                "[red]Error: --local-only mode requires --template flag[/red]"
            )
            raise typer.Exit(1)

        # Handle API-only mode (backward compatibility)
        if mode == "api-only":
            if not name:
                console.print(
                    "[red]Error: Project name is required "
                    "for API-only mode[/red]"
                )
                raise typer.Exit(1)

            project = _create_project_via_api(
                name=name,
                description=description,
                status=status,
                organization=organization,
                classification=classification,
                path=path,
                remote_url=remote_url,
            )

            project_id = project.get('id')
            project_name = project.get('name')
            console.print(
                f"[green]✓ Created project {project_id}: "
                f"{project_name}[/green]"
            )
            return

        # Handle template mode (when --template is provided or from interactive)
        # Also handle local-only mode when template is provided
        if mode == "template" or (
            mode == "local-only" and template
        ):
            if not name:
                console.print(
                    "[red]Error: Project name is required "
                    "for template mode[/red]"
                )
                raise typer.Exit(1)

            if not template:
                console.print(
                    "[red]Error: Template type is required "
                    "for template mode[/red]"
                )
                raise typer.Exit(1)

            # Get templates source
            templates_source = get_templates_source(config)

            # Determine target directory
            if target_dir:
                target = Path(target_dir).expanduser().resolve()
            else:
                target = (
                    config.default_project_dir.expanduser().resolve()
                    if config.default_project_dir
                    else Path.home() / "Projects"
                )

            # Create project from template
            try:
                project_path = create_from_template(
                    project_name=name,
                    template_type=template,
                    target_dir=target,
                    templates_source=templates_source,
                    description=description,
                )

                # Initialize git (unless --no-git)
                if not no_git:
                    if init_git(project_path):
                        console.print(
                            "[dim]✓ Initialized git repository[/dim]"
                        )
                    else:
                        console.print(
                            "[yellow]⚠ Failed to initialize git "
                            "repository[/yellow]"
                        )

                # Register project (unless --no-register)
                if register:
                    try:
                        add_project(
                            path=project_path,
                            template=template,
                            # TODO: Get from dev-infra
                            template_version="unknown",
                        )
                        console.print(
                            "[dim]✓ Registered project in local registry[/dim]"
                        )
                    except ValueError as e:
                        # Project already registered - not an error
                        console.print(f"[dim]ℹ {e}[/dim]")

                console.print(
                    f"[green]✓ Created project from template: "
                    f"{project_path}[/green]"
                )
                return

            except TemplateError as e:
                console.print(f"[red]Error: {e}[/red]")
                raise typer.Exit(1)

        # Default to API-only if name provided (backward compat)
        if name and not template and not api_only:
            project = _create_project_via_api(
                name=name,
                description=description,
                status=status,
                organization=organization,
                classification=classification,
                path=path,
                remote_url=remote_url,
            )

            project_id = project.get('id')
            project_name = project.get('name')
            console.print(
                f"[green]✓ Created project {project_id}: "
                f"{project_name}[/green]"
            )
        elif not name and not template and not api_only:
            # Should not reach here (interactive mode handled above)
            console.print(
                "[yellow]Please provide project name or use "
                "--api-only flag.[/yellow]"
            )
            raise typer.Exit(1)

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
    try:
        client = get_client()
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
