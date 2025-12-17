"""Inventory management commands."""
import json
import subprocess
from pathlib import Path
from typing import Optional

import requests
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from proj.config import Config, get_data_dir
from proj.error_handler import (
    handle_error, APIError, BackendConnectionError, TimeoutError
)

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


@scan_app.command(name="github")
def scan_github(
    username: Optional[str] = typer.Option(
        None, "--user", "-u", help="GitHub username"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file"
    ),
):
    """Scan GitHub repositories for a user."""
    config = get_config()

    # Get username from option or config
    gh_user = username or config.github_username
    if not gh_user:
        msg = (
            "[red]Error: GitHub username required. "
            "Use --user or set in config.[/red]"
        )
        console.print(msg)
        raise typer.Exit(1)

    # Check for GitHub token
    gh_token = config.github_token
    if not gh_token:
        msg = (
            "[yellow]Warning: No GitHub token set. "
            "Rate limits may apply.[/yellow]"
        )
        console.print(msg)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(
            f"Scanning GitHub repos for {gh_user}...", total=None
        )

        try:
            url = f"https://api.github.com/users/{gh_user}/repos"
            headers = {}
            if gh_token:
                headers["Authorization"] = f"token {gh_token}"

            params = {"per_page": 100, "sort": "updated"}
            repos = []

            while url:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                repos.extend(response.json())

                # Check for pagination
                url = response.links.get("next", {}).get("url")
                params = {}  # Clear params for subsequent requests

            repo_count = len(repos)
            desc = f"Found {repo_count} repositories"
            progress.update(task, description=desc)

            # Transform to inventory format
            inventory_items = []
            for repo in repos:
                item = {
                    "name": repo["name"],
                    "remote_url": repo["html_url"],
                    "description": repo.get("description", ""),
                    "source": "github",
                    "language": repo.get("language", ""),
                    "updated_at": repo.get("updated_at", ""),
                }
                inventory_items.append(item)

            # Save to file or inventory
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    json.dump(inventory_items, f, indent=2)
                msg = (
                    f"[green]✓ Saved {len(inventory_items)} repos "
                    f"to {output}[/green]"
                )
                console.print(msg)
            else:
                # Merge with existing inventory
                existing = load_inventory()
                # Add source tag
                for item in inventory_items:
                    item["scan_source"] = "github"

                # Simple merge (will be deduped later)
                combined = existing + inventory_items
                save_inventory(combined)
                count = len(inventory_items)
                msg = (
                    f"[green]✓ Added {count} GitHub repos "
                    f"to inventory[/green]"
                )
                console.print(msg)

        except requests.RequestException as e:
            # Handle GitHub API errors
            if isinstance(e, requests.exceptions.ConnectionError):
                handle_error(BackendConnectionError(str(e)), console)
            elif isinstance(e, requests.exceptions.Timeout):
                handle_error(TimeoutError(str(e)), console)
            elif isinstance(e, requests.exceptions.HTTPError):
                status_code = None
                if e.response:
                    status_code = e.response.status_code
                error = APIError(str(e), status_code=status_code)
                handle_error(error, console)
            else:
                console.print(f"[red]Error: GitHub API error: {e}[/red]")
            raise typer.Exit(1)


@scan_app.command(name="local")
def scan_local(
    directory: Optional[Path] = typer.Option(
        None, "--dir", "-d", help="Directory to scan"
    ),
    depth: int = typer.Option(2, "--depth", help="Max depth to scan"),
):
    """Scan local directories for projects."""
    config = get_config()

    # Get directories to scan
    if directory:
        scan_dirs = [directory]
    else:
        scan_dirs = [Path(d) for d in config.local_scan_dirs]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning local projects...", total=None)

        projects = []

        for scan_dir in scan_dirs:
            if not scan_dir.exists():
                msg = f"[yellow]Warning: {scan_dir} does not exist[/yellow]"
                console.print(msg)
                continue

            desc = f"Scanning {scan_dir}..."
            progress.update(task, description=desc)

            # Find projects by looking for markers
            markers = [
                ".git", "package.json", "pyproject.toml",
                "Cargo.toml", "go.mod"
            ]

            for marker in markers:
                pattern = f"**/{marker}"
                for project_dir in scan_dir.glob(pattern):
                    # Skip node_modules and nested .git
                    if project_dir.parts.count("node_modules") > 0:
                        continue
                    if project_dir.parts.count(".git") > 1:
                        continue

                    # Get project root
                    root = project_dir.parent

                    # Check depth
                    try:
                        rel_path = root.relative_to(scan_dir)
                        rel_depth = len(rel_path.parts)
                        if rel_depth > depth:
                            continue
                    except ValueError:
                        # Path not relative (shouldn't happen)
                        continue

                    # Get git remote if available
                    remote_url = ""
                    git_dir = root / ".git"
                    if git_dir.exists():
                        try:
                            result = subprocess.run(
                                [
                                    "git", "-C", str(root),
                                    "remote", "get-url", "origin"
                                ],
                                capture_output=True,
                                text=True,
                            )
                            if result.returncode == 0:
                                remote_url = result.stdout.strip()
                        except Exception:
                            pass

                    # Add to projects if not already added
                    path_str = str(root)
                    if not any(p["local_path"] == path_str for p in projects):
                        projects.append({
                            "name": root.name,
                            "local_path": str(root),
                            "remote_url": remote_url,
                            "source": "local",
                            "marker": marker,
                        })

        project_count = len(projects)
        desc = f"Found {project_count} local projects"
        progress.update(task, description=desc)

        # Merge with existing inventory
        existing = load_inventory()
        for item in projects:
            item["scan_source"] = "local"

        combined = existing + projects
        save_inventory(combined)

        msg = (
            f"[green]✓ Added {project_count} local projects "
            f"to inventory[/green]"
        )
        console.print(msg)


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
