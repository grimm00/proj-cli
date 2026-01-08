"""Shared helpers for project commands."""

import logging
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console

# Import these at module level so they can be patched in tests
# Tests patch proj.commands.projects.APIClient which re-exports from here
import proj.api_client
import proj.config
from proj.error_handler import (
    APIError,
    BackendConnectionError,
    TimeoutError,
)

console = Console()
logger = logging.getLogger(__name__)

# Status emoji mapping (shared constant)
STATUS_EMOJI = {
    "active": "🟢",
    "inactive": "⚪",
    "archived": "📦",
    "completed": "✅",
}

# Re-export for backward compatibility with tests
APIClient = proj.api_client.APIClient
Config = proj.config.Config


def get_client():
    """Get configured API client.
    
    Note: Uses module-level APIClient and Config references
    so tests can patch proj.commands.projects.APIClient.
    """
    # Import from package to use patched versions
    from proj.commands import projects
    return projects.APIClient(projects.Config.load())


def sync_to_api(
    client: APIClient,
    name: str,
    path: Path,
    template: str,
    description: Optional[str] = None,
    console: Optional[Console] = None,
) -> Optional[int]:
    """Sync project to work-prod API.

    Args:
        client: APIClient instance
        name: Project name
        path: Local project path
        template: Template type used
        description: Optional project description
        console: Console for output (optional)

    Returns:
        work_prod_id if successful, None if failed
    """
    try:
        project_data = {
            "name": name,
            "path": str(path),
            "description": description or f"Created from {template} template",
            "status": "active",
        }
        result = client.create_project(project_data)
        return result.get("id")
    except (APIError, BackendConnectionError, TimeoutError) as e:
        # Log full exception for debugging
        logger.debug(f"API sync failed: {e}", exc_info=True)

        if console:
            # Show user-friendly message without internal details
            console.print(
                "[yellow]⚠ Could not sync to API. "
                "Project created locally.[/yellow]"
            )
        return None


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
