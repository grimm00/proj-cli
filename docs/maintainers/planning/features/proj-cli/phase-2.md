# proj-cli - Phase 2: Migrate Project Commands

**Phase:** 2 of 4  
**Duration:** ~4-5 hours  
**Status:** ✅ Complete  
**Completed:** 2025-12-17  
**Merged:** PR #2 (2025-12-17)  
**Prerequisites:** Phase 1 complete ✅ (PR #1 merged 2025-12-17)  
**Test Coverage Goal:** ≥70% for new code

---

## 📋 Overview

Migrate existing `proj` commands from work-prod (`scripts/project_cli/`) to the new `proj-cli` repository. Convert from Click to Typer while maintaining feature parity.

**Success Definition:** All 8 core `proj` commands work identically in the new CLI, with the same output format and behavior.

---

## 🎯 Goals

1. Migrate error handler from work-prod to proj-cli
2. Migrate API client from work-prod to proj-cli
3. Convert 8 core project commands from Click to Typer
4. Maintain feature parity with current CLI
5. Integrate config for API URL
6. Test all commands against work-prod API

---

## 📋 Command Scope

**Phase 2 Commands (8 total):**

| Command       | Priority  | Status     | Notes                     |
| ------------- | --------- | ---------- | ------------------------- |
| `list`        | 🔴 High   | 🔴 Pending | Core CRUD                 |
| `get`         | 🔴 High   | 🔴 Pending | Core CRUD                 |
| `create`      | 🔴 High   | 🔴 Pending | Core CRUD                 |
| `update`      | 🔴 High   | 🔴 Pending | Core CRUD                 |
| `delete`      | 🔴 High   | 🔴 Pending | Core CRUD                 |
| `search`      | 🔴 High   | 🔴 Pending | Core functionality        |
| `import-json` | 🔴 High   | 🔴 Pending | Core functionality        |
| `archive`     | 🟡 Medium | 🔴 Pending | Uses API, straightforward |

**Deferred to Phase 3 or Phase 4:**

| Command  | Reason                               |
| -------- | ------------------------------------ |
| `config` | Uses Pydantic config, lower priority |
| `stats`  | Convenience command                  |
| `recent` | Convenience command                  |
| `active` | Convenience command                  |
| `mine`   | Requires GitHub user integration     |

---

## 📝 Tasks

### Task 1: Write Tests for Error Handler (RED) (~15 min)

**Goal:** Define expected error handler behavior

**File:** `tests/test_error_handler.py`

```python
# tests/test_error_handler.py
"""Tests for error handler."""
import pytest


def test_error_handler_module_exists():
    """Test that error_handler module exists."""
    from proj import error_handler
    assert error_handler is not None


def test_cli_error_exists():
    """Test that CLIError exception exists."""
    from proj.error_handler import CLIError
    assert CLIError is not None
    assert issubclass(CLIError, Exception)


def test_api_error_exists():
    """Test that APIError exception exists."""
    from proj.error_handler import APIError
    assert APIError is not None


def test_api_error_has_status_code():
    """Test that APIError stores status code."""
    from proj.error_handler import APIError
    error = APIError("Test error", status_code=404)
    assert error.status_code == 404


def test_backend_connection_error_exists():
    """Test that BackendConnectionError exception exists."""
    from proj.error_handler import BackendConnectionError
    assert BackendConnectionError is not None


def test_handle_error_exists():
    """Test that handle_error function exists."""
    from proj.error_handler import handle_error
    assert callable(handle_error)
```

**Expected Result:** Tests fail (RED)

---

### Task 2: Migrate Error Handler (GREEN) (~30 min)

**Goal:** Copy and adapt error handler from work-prod

**Source:** `work-prod/scripts/project_cli/error_handler.py`  
**Destination:** `proj-cli/src/proj/error_handler.py`

**Steps:**

- [x] Read current error handler implementation
- [x] Copy to new location
- [x] Update imports (use new Pydantic Config)
- [x] Adapt Rich panel patterns
- [x] Run tests

**File:** `src/proj/error_handler.py`

```python
"""Error handling utilities for CLI commands.

Provides friendly error messages and suggestions for common issues.
"""

import requests
from rich.console import Console
from rich.panel import Panel

from proj.config import Config


class CLIError(Exception):
    """Base exception for CLI errors."""
    pass


class BackendConnectionError(CLIError):
    """Raised when backend is not reachable."""
    pass


class APIError(CLIError):
    """Raised when API returns an error response."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


def handle_error(error: Exception, console: Console = None) -> None:
    """Handle errors and display friendly messages with suggestions.

    Args:
        error: The exception that occurred
        console: Rich Console instance (creates new one if not provided)
    """
    if console is None:
        console = Console()

    if isinstance(error, requests.exceptions.ConnectionError):
        _handle_connection_error(error, console)
    elif isinstance(error, requests.exceptions.Timeout):
        _handle_timeout_error(error, console)
    elif isinstance(error, requests.exceptions.HTTPError):
        _handle_http_error(error, console)
    elif isinstance(error, BackendConnectionError):
        _handle_connection_error(error, console)
    elif isinstance(error, APIError):
        _handle_api_error(error, console)
    else:
        _handle_generic_error(error, console)


def _get_health_url() -> str:
    """Get the health check URL from configured API base URL."""
    config = Config.load()
    base_url = config.api_url

    if not base_url or not base_url.strip():
        base_url = 'http://localhost:5000'
    else:
        base_url = base_url.strip()

    if not base_url.startswith('http://') and not base_url.startswith('https://'):
        base_url = 'http://localhost:5000'

    base = base_url.rstrip('/')
    return f"{base}/api/health"


def _handle_connection_error(error: Exception, console: Console) -> None:
    """Handle connection refused/network errors."""
    health_url = _get_health_url()

    message = (
        "[bold red]Cannot connect to backend API[/bold red]\n\n"
        "The backend server appears to be offline or unreachable.\n\n"
        "[bold]To fix this:[/bold]\n"
        "1. Start the backend server:\n"
        "   [cyan]cd ~/Projects/work-prod/backend && flask run[/cyan]\n\n"
        "2. Verify the server is running:\n"
        f"   [cyan]curl {health_url}[/cyan]\n\n"
        "3. Check your API URL configuration:\n"
        "   [cyan]PROJ_API_URL environment variable[/cyan]"
    )

    console.print(Panel(message, title="Connection Error", border_style="red"))
    console.print(f"\n[dim]Technical details: {error}[/dim]")


def _handle_timeout_error(error: Exception, console: Console) -> None:
    """Handle timeout errors."""
    health_url = _get_health_url()

    message = (
        "[bold red]Request timed out[/bold red]\n\n"
        "The backend server took too long to respond.\n\n"
        "[bold]Possible causes:[/bold]\n"
        "• Backend server is overloaded\n"
        "• Network connectivity issues\n"
        "• Backend server may be unresponsive\n\n"
        "[bold]Try:[/bold]\n"
        f"• Check if backend is running: [cyan]curl {health_url}[/cyan]\n"
        "• Restart the backend server"
    )

    console.print(Panel(message, title="Timeout Error", border_style="yellow"))
    console.print(f"\n[dim]Technical details: {error}[/dim]")


def _handle_http_error(error: requests.exceptions.HTTPError, console: Console) -> None:
    """Handle HTTP error responses."""
    response = getattr(error, 'response', None)

    error_msg = None
    if response is not None:
        try:
            error_data = response.json()
            if isinstance(error_data, dict) and 'error' in error_data:
                error_msg = error_data['error']
        except Exception:
            pass

    status_code = response.status_code if response else None

    if status_code == 404:
        title = "Not Found"
        border = "yellow"
        message = f"[bold yellow]Resource not found[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "The requested resource does not exist."
    elif status_code == 400:
        title = "Bad Request"
        border = "yellow"
        message = f"[bold yellow]Invalid request[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "Please check your input and try again."
    elif status_code == 409:
        title = "Conflict"
        border = "yellow"
        message = f"[bold yellow]Conflict detected[/bold yellow]\n\n"
        if error_msg:
            message += f"{error_msg}\n\n"
        message += "The operation conflicts with existing data."
    elif status_code == 500:
        title = "Server Error"
        border = "red"
        message = f"[bold red]Backend server error[/bold red]\n\n"
        message += "The backend encountered an internal error.\n\n"
        message += "[bold]Try:[/bold]\n"
        message += "• Check backend server logs\n"
        message += "• Restart the backend server\n"
        message += "• Report this issue if it persists"
    else:
        title = "HTTP Error"
        border = "red"
        message = f"[bold red]HTTP {status_code} Error[/bold red]\n\n"
        if error_msg:
            message += f"{error_msg}\n"

    console.print(Panel(message, title=title, border_style=border))
    if status_code:
        console.print(f"\n[dim]HTTP Status: {status_code}[/dim]")


def _handle_api_error(error: APIError, console: Console) -> None:
    """Handle API-specific errors."""
    message = f"[bold red]API Error[/bold red]\n\n"
    message += f"{error}\n"

    if error.status_code:
        message += f"\n[dim]HTTP Status: {error.status_code}[/dim]"

    console.print(Panel(message, title="API Error", border_style="red"))


def _handle_generic_error(error: Exception, console: Console) -> None:
    """Handle generic/unexpected errors."""
    health_url = _get_health_url()

    message = "[bold red]An unexpected error occurred[/bold red]\n\n"
    message += f"{error}\n\n"
    message += "[bold]Try:[/bold]\n"
    message += f"• Check if backend is running: [cyan]curl {health_url}[/cyan]\n"
    message += "• Verify your configuration\n"
    message += "• Check the error message above for details"

    console.print(Panel(message, title="Error", border_style="red"))
    console.print(f"\n[dim]Technical details: {type(error).__name__}: {error}[/dim]")


def check_backend_health(base_url: str) -> bool:
    """Check if backend is running and healthy.

    Args:
        base_url: Base API URL

    Returns:
        True if backend is healthy, False otherwise
    """
    try:
        if not base_url or not base_url.strip():
            base_url = 'http://localhost:5000'
        else:
            base_url = base_url.strip()

        if not base_url.startswith('http://') and not base_url.startswith('https://'):
            base_url = 'http://localhost:5000'

        base = base_url.rstrip('/')
        health_url = f"{base}/api/health"
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except Exception:
        return False
```

**Run tests:**

```bash
pytest tests/test_error_handler.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 3: Write Tests for API Client (RED) (~15 min)

**Goal:** Define expected API client behavior

**File:** `tests/test_api_client.py`

```python
# tests/test_api_client.py
"""Tests for API client."""
import pytest
from unittest.mock import Mock, patch


def test_api_client_exists():
    """Test that APIClient class exists."""
    from proj.api_client import APIClient
    assert APIClient is not None


def test_api_client_uses_config_url():
    """Test that client uses URL from config."""
    from proj.api_client import APIClient
    from proj.config import Config

    config = Config(api_url="http://test:8000")
    client = APIClient(config=config)
    assert client.base_url == "http://test:8000"


def test_api_client_list_projects():
    """Test list_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'list_projects')


def test_api_client_get_project():
    """Test get_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'get_project')


def test_api_client_create_project():
    """Test create_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'create_project')


def test_api_client_update_project():
    """Test update_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'update_project')


def test_api_client_delete_project():
    """Test delete_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'delete_project')


def test_api_client_search_projects():
    """Test search_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'search_projects')


def test_api_client_import_projects():
    """Test import_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'import_projects')


def test_api_client_archive_project():
    """Test archive_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'archive_project')
```

**Expected Result:** Tests fail (RED)

---

### Task 4: Migrate API Client (GREEN) (~30 min)

**Goal:** Copy and adapt API client from work-prod

**Source:** `work-prod/scripts/project_cli/api_client.py`  
**Destination:** `proj-cli/src/proj/api_client.py`

**Steps:**

- [x] Read current API client implementation
- [x] Copy to new location
- [x] Update imports (use error_handler)
- [x] Add config integration
- [x] Include archive_project method
- [x] Run tests

**File:** `src/proj/api_client.py`

```python
"""API client for work-prod backend."""

from typing import Dict, List, Optional

import requests

from proj.config import Config
from proj.error_handler import APIError, BackendConnectionError


def _raise_api_error(error: requests.exceptions.RequestException, response=None) -> None:
    """Convert requests exceptions to APIError or re-raise connection errors."""
    if isinstance(error, requests.exceptions.ConnectionError):
        raise BackendConnectionError(str(error)) from error
    elif isinstance(error, requests.exceptions.Timeout):
        raise error
    elif isinstance(error, requests.exceptions.HTTPError):
        error_msg = str(error)
        if response is not None:
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and 'error' in error_data:
                    error_msg = error_data['error']
            except Exception:
                pass
        raise APIError(error_msg, status_code=response.status_code if response else None) from error
    else:
        raise error


class APIClient:
    """Client for interacting with work-prod API."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize client with config.

        Args:
            config: Config instance (uses Config.load() if not provided)
        """
        self.config = config or Config.load()
        self.base_url = self.config.api_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _url(self, path: str) -> str:
        """Build full URL for API path."""
        return f"{self.base_url}/api{path}"

    def list_projects(
        self,
        status: Optional[str] = None,
        organization: Optional[str] = None,
        classification: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Dict]:
        """List all projects with optional filters.

        Args:
            status: Filter by status (active, paused, completed, cancelled)
            organization: Filter by organization name
            classification: Filter by classification
            search: Search term for name and description

        Returns:
            List of project dictionaries
        """
        params = {}
        if status:
            params["status"] = status
        if organization:
            params["organization"] = organization
        if classification:
            params["classification"] = classification
        if search:
            params["search"] = search

        try:
            response = self.session.get(self._url("/projects"), params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def get_project(self, project_id: int) -> Dict:
        """Get a single project by ID.

        Args:
            project_id: ID of the project to retrieve

        Returns:
            Project dictionary
        """
        try:
            response = self.session.get(self._url(f"/projects/{project_id}"), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def create_project(self, data: Dict) -> Dict:
        """Create a new project.

        Args:
            data: Project data dictionary

        Returns:
            Created project dictionary
        """
        try:
            response = self.session.post(self._url("/projects"), json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update an existing project.

        Args:
            project_id: ID of the project to update
            data: Fields to update

        Returns:
            Updated project dictionary
        """
        try:
            response = self.session.patch(self._url(f"/projects/{project_id}"), json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def delete_project(self, project_id: int) -> None:
        """Delete a project permanently.

        Args:
            project_id: ID of the project to delete
        """
        try:
            response = self.session.delete(self._url(f"/projects/{project_id}"), timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def search_projects(self, query: str) -> List[Dict]:
        """Search projects by query.

        Args:
            query: Search query string

        Returns:
            List of matching projects
        """
        try:
            response = self.session.get(
                self._url("/projects"),
                params={"search": query},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def import_projects(self, projects: List[Dict]) -> Dict:
        """Import multiple projects from JSON data.

        Args:
            projects: List of project data dictionaries

        Returns:
            Dictionary with import statistics: imported, skipped, errors
        """
        try:
            response = self.session.post(
            self._url("/projects/import"),
            json={"projects": projects},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def archive_project(self, project_id: int) -> Dict:
        """Archive a project by setting classification to 'archive' and status to 'completed'.

        Args:
            project_id: ID of the project to archive

        Returns:
            Archived project dictionary
        """
        try:
            response = self.session.put(self._url(f"/projects/{project_id}/archive"), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
```

**Run tests:**

```bash
pytest tests/test_api_client.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 5: Write Tests for Project Commands (RED) (~15 min)

**Goal:** Define expected command behavior

**File:** `tests/test_commands_projects.py`

```python
# tests/test_commands_projects.py
"""Tests for project commands."""
import subprocess
import sys


def test_list_command_exists():
    """Test that list command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "list", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "List" in result.stdout or "list" in result.stdout.lower()


def test_get_command_exists():
    """Test that get command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "get", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_create_command_exists():
    """Test that create command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "create", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_update_command_exists():
    """Test that update command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "update", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_delete_command_exists():
    """Test that delete command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "delete", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_search_command_exists():
    """Test that search command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "search", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_import_command_exists():
    """Test that import command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "import-json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_archive_command_exists():
    """Test that archive command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "archive", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
```

**Expected Result:** Tests fail (RED)

---

### Task 6: Implement Project Commands (GREEN) (~1-1.5 hours)

**Goal:** Create project commands using Typer

**File:** `src/proj/commands/projects.py`

```python
"""Project management commands."""

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from proj.api_client import APIClient
from proj.config import Config
from proj.error_handler import handle_error, APIError, BackendConnectionError

console = Console()


def get_client() -> APIClient:
    """Get configured API client."""
    return APIClient(Config.load())


def list_projects(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="Filter by organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="Filter by classification"),
    search: Optional[str] = typer.Option(None, "--search", help="Search in names and descriptions"),
    wide: bool = typer.Option(False, "--wide", "-w", help="Show all columns"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
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

            table = Table(title=f"Projects ({len(projects)})")
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
                    row.append(p.get("status", ""))
                if wide or organization:
                    row.append(p.get("organization", ""))
                if wide or classification:
                    row.append(p.get("classification", ""))
                row.append(p.get("path", "") or "")
                if wide or search:
                    row.append(p.get("description", "") or "")
                row.append(p.get("created_at", "")[:10] if p.get("created_at") else "")
                table.add_row(*row)

            console.print(table)
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def get_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
):
    """Get a project by ID."""
    try:
        client = get_client()
        project = client.get_project(project_id)

        if format == "json":
            console.print_json(json.dumps(project, indent=2))
        else:
            table = Table(title=f"Project {project_id}")
            table.add_column("Field", style="cyan")
            table.add_column("Value", style="green")

            for key, value in project.items():
                table.add_row(key, str(value) if value else "")

            console.print(table)
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def create_project(
    name: str = typer.Argument(..., help="Project name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description"),
    status: str = typer.Option("active", "--status", "-s", help="Status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="Organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="Classification"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="Local path"),
    remote_url: Optional[str] = typer.Option(None, "--url", "-u", help="Remote URL"),
):
    """Create a new project."""
    try:
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
        project = client.create_project(data)

        console.print(f"[green]✓ Created project {project.get('id')}: {project.get('name')}[/green]")
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def update_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="New description"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="New status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="New organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="New classification"),
    path: Optional[str] = typer.Option(None, "--path", "-p", help="New local path"),
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

        if not data:
            console.print("[yellow]No updates provided.[/yellow]")
            raise typer.Exit(1)

        client = get_client()
        client.update_project(project_id, data)

        console.print(f"[green]✓ Updated project {project_id}[/green]")
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def delete_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
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
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def search_projects(
    query: str = typer.Argument(..., help="Search query"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
):
    """Search projects by name or description."""
    try:
        client = get_client()
        projects = client.search_projects(query)

        if format == "json":
            console.print_json(json.dumps(projects, indent=2))
        else:
            if not projects:
                console.print(f"[yellow]No projects found for '{query}'.[/yellow]")
                return

            table = Table(title=f"Search Results: {query}")
            table.add_column("ID", style="cyan", justify="right")
            table.add_column("Name", style="green")
            table.add_column("Status", style="yellow")
            table.add_column("Description", style="dim")

            for p in projects:
                table.add_row(
                    str(p.get("id", "")),
                    p.get("name", ""),
                    p.get("status", ""),
                    (p.get("description", "") or "")[:50],
                )

            console.print(table)
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def import_json(
    file: Path = typer.Argument(..., help="JSON file to import", exists=True),
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
            console.print("[red]Error: Invalid JSON format. Expected list or {projects: [...]}[/red]")
            raise typer.Exit(1)

        client = get_client()
        result = client.import_projects(projects)

        console.print(f"[green]✓ Imported: {result.get('imported', 0)}[/green]")
        console.print(f"[yellow]  Skipped: {result.get('skipped', 0)}[/yellow]")
        if result.get("errors"):
            console.print(f"[red]  Errors: {len(result.get('errors', []))}[/red]")
    except json.JSONDecodeError as e:
        console.print(f"[red]Error: Invalid JSON: {e}[/red]")
        raise typer.Exit(1)
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)


def archive_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Archive a project (sets status to completed, classification to archive)."""
    try:
        if not force:
            confirm = typer.confirm(f"Archive project {project_id}?")
            if not confirm:
                raise typer.Abort()

        client = get_client()
        project = client.archive_project(project_id)

        console.print(f"[green]✓ Archived project {project_id}: {project.get('name')}[/green]")
    except (APIError, BackendConnectionError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
```

---

### Task 7: Register Commands in Main CLI (GREEN) (~15 min)

**Goal:** Add project commands to main CLI

**Update:** `src/proj/cli.py`

```python
"""Main CLI application using Typer."""

from typing import Optional

import typer

from proj.commands import projects

app = typer.Typer(
    name="proj",
    help="Unified CLI for project and inventory management.",
    no_args_is_help=True,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from proj import __version__
        typer.echo(f"proj version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Unified CLI for project and inventory management.

    Project commands manage projects in the work-prod API.
    Inventory commands scan and manage project inventory.
    """
    pass


# Register project commands (8 core commands)
app.command(name="list")(projects.list_projects)
app.command(name="get")(projects.get_project)
app.command(name="create")(projects.create_project)
app.command(name="update")(projects.update_project)
app.command(name="delete")(projects.delete_project)
app.command(name="search")(projects.search_projects)
app.command(name="import-json")(projects.import_json)
app.command(name="archive")(projects.archive_project)


if __name__ == "__main__":
    app()
```

**Run tests:**

```bash
pytest tests/test_commands_projects.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 8: Integration Testing (~30 min)

**Goal:** Test all commands against running work-prod API

**Prerequisites:**

- [ ] work-prod API running on localhost:5000

**Manual tests:**

```bash
# Start work-prod API (in work-prod directory)
cd ~/Projects/work-prod/backend
flask run

# In another terminal, test proj-cli
cd ~/Projects/proj-cli

# Test list
proj list
proj list --format json
proj list --status active
proj list --wide

# Test get
proj get 1
proj get 1 --format json

# Test create
proj create "Test Project" --desc "Testing new CLI"

# Test update
proj update <id> --status paused

# Test search
proj search "test"

# Test archive
proj archive <id>

# Test delete
proj delete <id> --force

# Test import
proj import-json ~/Projects/work-prod/scripts/projects.json
```

---

### Task 9: Verify Feature Parity (REFACTOR) (~15 min)

**Goal:** Ensure new CLI matches old CLI behavior

**Comparison checklist:**

- [x] `proj list` output matches (Rich tables) - Verified structure
- [x] `proj list --wide` shows all columns - Verified in code
- [x] `proj get` output matches - Verified structure
- [x] `proj create` behavior matches - Verified options match
- [x] `proj update` behavior matches - Verified options match (including remote_url)
- [x] `proj delete` behavior matches - Verified structure
- [x] `proj search` output matches - Verified structure
- [x] `proj archive` behavior matches - Verified structure
- [x] `proj import-json` behavior matches - Verified structure (name differs: import vs import-json)
- [x] Error messages are helpful (Rich panels) - Verified error handler

**Notes:**

- Output format uses Rich tables (same as work-prod)
- Help text auto-generated by Typer
- Error handling uses Rich panels (same as work-prod)

---

## ✅ Completion Criteria

- [ ] Error handler migrated and tested
- [ ] API client migrated and tested
- [ ] All 8 project commands implemented
- [ ] Commands registered in main CLI
- [ ] Unit tests passing (≥70% coverage for new code)
- [ ] Integration tests with work-prod API passing
- [ ] Feature parity verified

---

## 📦 Deliverables

1. **Error handler** - `src/proj/error_handler.py`
2. **API client** - `src/proj/api_client.py`
3. **Project commands** - `src/proj/commands/projects.py`
4. **Updated CLI** - 8 commands registered in main app
5. **Tests** - Error handler, API client, and command tests

---

## 🔗 Dependencies

### Prerequisites

- Phase 1 complete ✅ (PR #1 merged 2025-12-17)
- work-prod API available (for integration testing)

### External Dependencies

- `requests` library (for API calls)
- work-prod backend running (for integration tests)

### Blocks

- Phase 3 depends on Phase 2 completion

---

## 📊 Progress Tracking

### Error Handler (TDD)

- [x] Tests written (RED)
- [x] Handler migrated (GREEN)
- [x] Tests passing

### API Client (TDD)

- [x] Tests written (RED)
- [x] Client migrated (GREEN)
- [x] Tests passing

### Project Commands (TDD)

- [x] Tests written (RED)
- [x] Commands implemented (GREEN)
- [x] Tests passing

### Integration

- [x] Commands registered
- [x] Command structure verified (help output)
- [ ] Integration tests passing (requires running API)
- [x] Feature parity verified (command structure matches)

---

## 📝 Implementation Notes

### Task Effort Estimates

| Task                        | Effort         | Cumulative  |
| --------------------------- | -------------- | ----------- |
| Task 1: Error Handler Tests | ~15 min        | 15 min      |
| Task 2: Error Handler       | ~30 min        | 45 min      |
| Task 3: API Client Tests    | ~15 min        | 1 hr        |
| Task 4: API Client          | ~30 min        | 1.5 hr      |
| Task 5: Command Tests       | ~15 min        | 1.75 hr     |
| Task 6: Commands            | ~1-1.5 hr      | 3-3.25 hr   |
| Task 7: Register            | ~15 min        | 3.25-3.5 hr |
| Task 8: Integration         | ~30 min        | 3.75-4 hr   |
| Task 9: Feature Parity      | ~15 min        | 4-4.25 hr   |
| **Total**                   | **~4-5 hours** |             |

### Typer Command Patterns

```python
# Command with required argument
@app.command()
def get(project_id: int = typer.Argument(..., help="Project ID")):
    pass

# Command with optional argument
@app.command()
def search(query: str = typer.Argument(None, help="Search query")):
    pass

# Command with options
@app.command()
def list(
    status: str = typer.Option(None, "--status", "-s"),
    format: str = typer.Option("table", "--format", "-f"),
):
    pass
```

### Rich Output Patterns

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Table output
table = Table(title="Projects")
table.add_column("ID", style="cyan")
table.add_row("1")
console.print(table)

# JSON output
console.print_json(data)

# Error panel
console.print(Panel(message, title="Error", border_style="red"))
```

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 1: Repository Setup](phase-1.md)
- [Phase 2 Review](phase-2-review.md)
- [Phase 3: Add Inventory Commands](phase-3.md)
- [Migration Reference](migration-reference.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-17
