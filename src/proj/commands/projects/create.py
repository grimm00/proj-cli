"""Project creation with multiple modes."""

import json
from pathlib import Path
from typing import Optional

import click
import typer
from rich.console import Console

from proj.error_handler import (
    handle_error,
    APIError,
    BackendConnectionError,
    TimeoutError,
)

from .helpers import sync_to_api

# Use console from helpers to avoid duplicate instance
from .helpers import console


def _get_package_imports():
    """Get imports from package level for test patching compatibility.
    
    This allows tests to patch proj.commands.projects.Config, etc.
    """
    from proj.commands import projects
    return projects


def _get_client():
    """Get API client using package-level import for patching."""
    pkg = _get_package_imports()
    return pkg.APIClient(pkg.Config.load())


def prompt_for_create_options(config) -> dict:
    """Prompt user for create options interactively.

    Args:
        config: proj-cli configuration.

    Returns:
        Dict with user choices: name, template, target_dir, description.

    Raises:
        KeyboardInterrupt: If user cancels (Ctrl+C).
    """
    pkg = _get_package_imports()
    
    name = pkg.Prompt.ask("Project name")

    # List available templates
    templates_source = pkg.get_templates_source(config)
    available = pkg.list_templates(templates_source)

    if not available:
        console.print("[red]Error:[/red] No templates available.")
        console.print(f"[dim]Templates source: {templates_source}[/dim]")
        raise typer.Exit(1)

    default_template = (
        config.templates.default if hasattr(config, 'templates') and
        hasattr(config.templates, 'default') else None
    )
    template = pkg.Prompt.ask(
        "Template type",
        choices=available,
        default=default_template or available[0] if available else None,
    )

    default_target = (
        str(config.default_project_dir.expanduser().resolve())
        if config.default_project_dir
        else str(Path.home() / "Projects")
    )
    target_dir_str = pkg.Prompt.ask(
        "Target directory",
        default=default_target,
    )
    target_dir = Path(target_dir_str).expanduser().resolve()

    description = pkg.Prompt.ask("Description (optional)", default="")

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
    pkg = _get_package_imports()
    
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

    # Use package-level get_client for test patching compatibility
    client = pkg.get_client()
    return client.create_project(data)


def detect_create_mode(
    template: Optional[str],
    api_only: bool,
    local_only: bool,
) -> str:
    """Detect which create mode to use.

    Args:
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
    return "interactive"


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
    pkg = _get_package_imports()
    
    try:
        # Load config for mode detection
        config = pkg.Config.load()

        # Handle dry-run mode (preview without side effects)
        if dry_run:
            # Validate mode conflicts even in dry-run
            detect_create_mode(
                template=template,
                api_only=api_only,
                local_only=local_only,
            )
            console.print(
                "[yellow]🔍 Dry-run mode: Preview only[/yellow]"
            )
            console.print("")

            if template:
                # Template mode preview
                templates_source = pkg.get_templates_source(config)
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

        # Handle template mode (--template or interactive)
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
            templates_source = pkg.get_templates_source(config)

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
                project_path = pkg.create_from_template(
                    project_name=name,
                    template_type=template,
                    target_dir=target,
                    templates_source=templates_source,
                    description=description,
                )

                # Initialize git (unless --no-git)
                if not no_git:
                    if pkg.init_git(project_path):
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
                        pkg.add_project(
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

                # Sync to API (unless --local-only or api_enabled=False)
                if not local_only and config.api_enabled:
                    client = pkg.APIClient(config)
                    work_prod_id = sync_to_api(
                        client=client,
                        name=name,
                        path=project_path,
                        template=template,
                        description=description,
                        console=console,
                    )
                    if work_prod_id:
                        pkg.update_project_work_prod_id(project_path, work_prod_id)
                        console.print(
                            f"[dim]✓ Synced to API (ID: {work_prod_id})[/dim]"
                        )
                elif local_only:
                    console.print(
                        "[dim]ℹ Skipped API sync (--local-only)[/dim]"
                    )
                elif not config.api_enabled:
                    console.print(
                        "[dim]ℹ Skipped API sync "
                        "(api_enabled=False)[/dim]"
                    )

                console.print(
                    f"[green]✓ Created project from template: "
                    f"{project_path}[/green]"
                )
                return

            except pkg.TemplateError as e:
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
