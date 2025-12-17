# proj-cli - Phase 2: Migrate Project Commands

**Phase:** 2 of 4  
**Duration:** ~3-4 hours  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 1 complete

---

## 📋 Overview

Migrate existing `proj` commands from work-prod (`scripts/project_cli/`) to the new `proj-cli` repository. Convert from argparse to Typer while maintaining feature parity.

**Success Definition:** All existing `proj` commands work identically in the new CLI, with the same output format and behavior.

---

## 🎯 Goals

1. Migrate API client from work-prod to proj-cli
2. Convert all project commands from argparse to Typer
3. Maintain feature parity with current CLI
4. Integrate config for API URL
5. Test all commands against work-prod API

---

## 📝 Tasks

### Task 1: Write Tests for API Client (RED)

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
```

**Expected Result:** Tests fail (RED)

---

### Task 2: Migrate API Client (GREEN)

**Goal:** Copy and adapt API client from work-prod

**Source:** `work-prod/scripts/project_cli/api_client.py`  
**Destination:** `proj-cli/src/proj/api_client.py`

**Steps:**

- [ ] Read current API client implementation
- [ ] Copy to new location
- [ ] Update imports
- [ ] Add config integration
- [ ] Run tests

**File:** `src/proj/api_client.py`

```python
"""API client for work-prod backend."""
import json
from typing import Any, Optional
from urllib.parse import urljoin

import requests

from proj.config import Config


class APIClient:
    """Client for interacting with work-prod API."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize client with config."""
        self.config = config or Config.load()
        self.base_url = self.config.api_url.rstrip("/")
    
    def _url(self, path: str) -> str:
        """Build full URL for API path."""
        return f"{self.base_url}/api{path}"
    
    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response, raising on errors."""
        if response.status_code >= 400:
            try:
                error = response.json().get("error", response.text)
            except json.JSONDecodeError:
                error = response.text
            raise APIError(f"API error ({response.status_code}): {error}")
        
        if response.status_code == 204:
            return {}
        
        return response.json()
    
    def list_projects(
        self,
        status: Optional[str] = None,
        organization: Optional[str] = None,
        classification: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """List all projects with optional filters."""
        params = {}
        if status:
            params["status"] = status
        if organization:
            params["organization"] = organization
        if classification:
            params["classification"] = classification
        if limit:
            params["limit"] = limit
        
        response = requests.get(self._url("/projects"), params=params)
        return self._handle_response(response)
    
    def get_project(self, project_id: int) -> dict:
        """Get a single project by ID."""
        response = requests.get(self._url(f"/projects/{project_id}"))
        return self._handle_response(response)
    
    def create_project(self, data: dict) -> dict:
        """Create a new project."""
        response = requests.post(
            self._url("/projects"),
            json=data,
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)
    
    def update_project(self, project_id: int, data: dict) -> dict:
        """Update an existing project."""
        response = requests.patch(
            self._url(f"/projects/{project_id}"),
            json=data,
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)
    
    def delete_project(self, project_id: int) -> dict:
        """Delete a project."""
        response = requests.delete(self._url(f"/projects/{project_id}"))
        return self._handle_response(response)
    
    def search_projects(self, query: str) -> list[dict]:
        """Search projects by query."""
        response = requests.get(
            self._url("/projects/search"),
            params={"q": query},
        )
        return self._handle_response(response)
    
    def import_projects(self, projects: list[dict]) -> dict:
        """Import multiple projects."""
        response = requests.post(
            self._url("/projects/import"),
            json={"projects": projects},
            headers={"Content-Type": "application/json"},
        )
        return self._handle_response(response)


class APIError(Exception):
    """API error exception."""
    pass
```

**Run tests:**

```bash
pytest tests/test_api_client.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 3: Write Tests for Project Commands (RED)

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
    # Note: 'import' is a Python keyword, so command might be named 'import-json' or similar
    result = subprocess.run(
        [sys.executable, "-m", "proj", "import-json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
```

**Expected Result:** Tests fail (RED)

---

### Task 4: Implement Project Commands (GREEN)

**Goal:** Create project commands using Typer

**File:** `src/proj/commands/projects.py`

```python
"""Project management commands."""
import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from proj.api_client import APIClient, APIError
from proj.config import Config

# Create Typer app for project commands
# Note: These will be added to main app, not as a subcommand group
console = Console()


def get_client() -> APIClient:
    """Get configured API client."""
    return APIClient(Config.load())


def list_projects(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="Filter by organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="Filter by classification"),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit number of results"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
):
    """List all projects."""
    try:
        client = get_client()
        projects = client.list_projects(
            status=status,
            organization=organization,
            classification=classification,
            limit=limit,
        )
        
        if format == "json":
            console.print_json(json.dumps(projects, indent=2))
        else:
            if not projects:
                console.print("[yellow]No projects found.[/yellow]")
                return
            
            table = Table(title="Projects")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status")
            table.add_column("Organization")
            table.add_column("Classification")
            
            for p in projects:
                table.add_row(
                    str(p.get("id", "")),
                    p.get("name", ""),
                    p.get("status", ""),
                    p.get("organization", ""),
                    p.get("classification", ""),
                )
            
            console.print(table)
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
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
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def create_project(
    name: str = typer.Argument(..., help="Project name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="Description"),
    status: str = typer.Option("active", "--status", "-s", help="Status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="Organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="Classification"),
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
        if remote_url:
            data["remote_url"] = remote_url
        
        client = get_client()
        project = client.create_project(data)
        
        console.print(f"[green]✓ Created project {project.get('id')}: {project.get('name')}[/green]")
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def update_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="New name"),
    description: Optional[str] = typer.Option(None, "--desc", "-d", help="New description"),
    status: Optional[str] = typer.Option(None, "--status", "-s", help="New status"),
    organization: Optional[str] = typer.Option(None, "--org", "-o", help="New organization"),
    classification: Optional[str] = typer.Option(None, "--class", "-c", help="New classification"),
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
        
        if not data:
            console.print("[yellow]No updates provided.[/yellow]")
            raise typer.Exit(1)
        
        client = get_client()
        project = client.update_project(project_id, data)
        
        console.print(f"[green]✓ Updated project {project_id}[/green]")
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def delete_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a project."""
    try:
        if not force:
            confirm = typer.confirm(f"Delete project {project_id}?")
            if not confirm:
                raise typer.Abort()
        
        client = get_client()
        client.delete_project(project_id)
        
        console.print(f"[green]✓ Deleted project {project_id}[/green]")
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def search_projects(
    query: str = typer.Argument(..., help="Search query"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
):
    """Search projects."""
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
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status")
            
            for p in projects:
                table.add_row(
                    str(p.get("id", "")),
                    p.get("name", ""),
                    p.get("status", ""),
                )
            
            console.print(table)
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def import_json(
    file: Path = typer.Argument(..., help="JSON file to import", exists=True),
):
    """Import projects from JSON file."""
    try:
        with open(file) as f:
            data = json.load(f)
        
        # Handle both {projects: [...]} and [...] formats
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
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
```

---

### Task 5: Register Commands in Main CLI (GREEN)

**Goal:** Add project commands to main CLI

**Update:** `src/proj/cli.py`

```python
"""Main CLI application using Typer."""
import typer
from typing import Optional

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
    """Unified CLI for project and inventory management."""
    pass


# Register project commands
app.command(name="list")(projects.list_projects)
app.command(name="get")(projects.get_project)
app.command(name="create")(projects.create_project)
app.command(name="update")(projects.update_project)
app.command(name="delete")(projects.delete_project)
app.command(name="search")(projects.search_projects)
app.command(name="import-json")(projects.import_json)


if __name__ == "__main__":
    app()
```

**Run tests:**

```bash
pytest tests/test_commands_projects.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 6: Integration Testing

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

# Test get
proj get 1
proj get 1 --format json

# Test create
proj create "Test Project" --desc "Testing new CLI"

# Test update
proj update <id> --status archived

# Test search
proj search "test"

# Test delete
proj delete <id>

# Test import
proj import-json ~/Projects/work-prod/scripts/projects.json
```

---

### Task 7: Verify Feature Parity (REFACTOR)

**Goal:** Ensure new CLI matches old CLI behavior

**Comparison checklist:**

- [ ] `proj list` output matches
- [ ] `proj get` output matches
- [ ] `proj create` behavior matches
- [ ] `proj update` behavior matches
- [ ] `proj delete` behavior matches
- [ ] `proj search` output matches
- [ ] Import behavior matches

**Notes:**

- Output format may differ (Rich tables vs plain text)
- Help text will be auto-generated by Typer
- Error messages may differ

---

## ✅ Completion Criteria

- [ ] API client migrated and tested
- [ ] All 7 project commands implemented
- [ ] Commands registered in main CLI
- [ ] Unit tests passing
- [ ] Integration tests with work-prod API passing
- [ ] Feature parity verified

---

## 📦 Deliverables

1. **API client** - `src/proj/api_client.py`
2. **Project commands** - `src/proj/commands/projects.py`
3. **Updated CLI** - Commands registered in main app
4. **Tests** - API client and command tests

---

## 🔗 Dependencies

### Prerequisites

- Phase 1 complete
- work-prod API available

### External Dependencies

- requests library (for API calls)
- work-prod backend running

### Blocks

- Phase 3 depends on Phase 2 completion

---

## 📊 Progress Tracking

### API Client (TDD)

- [ ] Tests written (RED)
- [ ] Client migrated (GREEN)
- [ ] Tests passing

### Project Commands (TDD)

- [ ] Tests written (RED)
- [ ] Commands implemented (GREEN)
- [ ] Tests passing

### Integration

- [ ] Commands registered
- [ ] Integration tests passing
- [ ] Feature parity verified

---

## 📝 Implementation Notes

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

console = Console()

# Table output
table = Table(title="Projects")
table.add_column("ID", style="cyan")
table.add_row("1")
console.print(table)

# JSON output
console.print_json(data)

# Colored messages
console.print("[green]Success![/green]")
console.print("[red]Error![/red]")
```

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 1: Repository Setup](phase-1.md)
- [Phase 3: Add Inventory Commands](phase-3.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-16

