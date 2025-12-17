# proj-cli - Phase 3: Add Inventory Commands

**Phase:** 3 of 4  
**Duration:** ~3-4 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 2 complete  
**Last Updated:** 2025-12-17

---

## 📋 Overview

Add `proj inv` subcommand group for inventory management. This wraps existing inventory scripts from work-prod as CLI subcommands, providing scan, analyze, dedupe, and export functionality.

**Success Definition:** Running `proj inv scan github` scans GitHub repos, `proj inv analyze` analyzes tech stack, and `proj inv export api` pushes to work-prod API.

---

## 🎯 Goals

1. Create `proj inv` subcommand group using Typer
2. Implement scan commands (github, local)
3. Implement analysis commands (analyze, dedupe)
4. Implement export commands (json, api)
5. Add status command for inventory state

---

## 📝 Tasks

### Task 1: Write Tests for Inventory Command Group (RED)

**Goal:** Define expected inventory subcommand structure

**File:** `tests/test_commands_inventory.py`

```python
# tests/test_commands_inventory.py
"""Tests for inventory commands."""
import subprocess
import sys


def test_inv_command_group_exists():
    """Test that inv command group exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scan" in result.stdout.lower()


def test_inv_scan_github_exists():
    """Test that inv scan github command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "scan", "github", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_scan_local_exists():
    """Test that inv scan local command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "scan", "local", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_analyze_exists():
    """Test that inv analyze command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "analyze", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_dedupe_exists():
    """Test that inv dedupe command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "dedupe", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_export_json_exists():
    """Test that inv export json command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "export", "json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_export_api_exists():
    """Test that inv export api command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "export", "api", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_status_exists():
    """Test that inv status command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "status", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
```

**Expected Result:** Tests fail (RED)

---

### Task 2: Create Inventory Command Group Structure (GREEN) ✅

**Goal:** Create Typer subcommand groups for inventory

**File:** `src/proj/commands/inventory.py`

```python
"""Inventory management commands."""
import json
import subprocess
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

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
        with open(inv_file) as f:
            return json.load(f)
    return []


def save_inventory(data: list[dict]) -> None:
    """Save inventory to data file."""
    inv_file = get_inventory_file()
    inv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(inv_file, "w") as f:
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
```

---

### Task 3: Register Inventory Commands in Main CLI ✅

**Goal:** Add inv command group to main CLI

**Update:** `src/proj/cli.py`

Add these lines after project command registrations:

```python
from proj.commands.inventory import inv_app

# Register inventory command group
app.add_typer(inv_app, name="inv")
```

**Run tests:**

```bash
pytest tests/test_commands_inventory.py -v
```

**Expected Result:** Tests pass (GREEN) - command structure exists

---

### Task 4: Implement Scan GitHub Command ✅

**Goal:** Wrap existing GitHub scan script

**Source script:** `work-prod/scripts/inventory/fetch-github-repos.sh`

**Update:** `src/proj/commands/inventory.py` - replace `scan_github`

```python
@scan_app.command(name="github")
def scan_github(
    username: Optional[str] = typer.Option(None, "--user", "-u", help="GitHub username"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file"),
):
    """Scan GitHub repositories for a user."""
    config = get_config()

    # Get username from option or config
    gh_user = username or config.github_username
    if not gh_user:
        console.print("[red]Error: GitHub username required. Use --user or set in config.[/red]")
        raise typer.Exit(1)

    # Check for GitHub token
    gh_token = config.github_token
    if not gh_token:
        console.print("[yellow]Warning: No GitHub token set. Rate limits may apply.[/yellow]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"Scanning GitHub repos for {gh_user}...", total=None)

        try:
            # Use GitHub API directly
            import requests

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

            progress.update(task, description=f"Found {len(repos)} repositories")

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
                with open(output, "w") as f:
                    json.dump(inventory_items, f, indent=2)
                console.print(f"[green]✓ Saved {len(inventory_items)} repos to {output}[/green]")
            else:
                # Merge with existing inventory
                existing = load_inventory()
                # Add source tag
                for item in inventory_items:
                    item["scan_source"] = "github"

                # Simple merge (will be deduped later)
                combined = existing + inventory_items
                save_inventory(combined)
                console.print(f"[green]✓ Added {len(inventory_items)} GitHub repos to inventory[/green]")

        except requests.RequestException as e:
            console.print(f"[red]Error: GitHub API error: {e}[/red]")
            raise typer.Exit(1)
```

---

### Task 5: Implement Scan Local Command ✅

**Goal:** Wrap existing local scan script

**Source script:** `work-prod/scripts/inventory/scan-local-projects.sh`

**Update:** `src/proj/commands/inventory.py` - replace `scan_local`

```python
@scan_app.command(name="local")
def scan_local(
    directory: Optional[Path] = typer.Option(None, "--dir", "-d", help="Directory to scan"),
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
                console.print(f"[yellow]Warning: {scan_dir} does not exist[/yellow]")
                continue

            progress.update(task, description=f"Scanning {scan_dir}...")

            # Find projects by looking for markers
            markers = [".git", "package.json", "pyproject.toml", "Cargo.toml", "go.mod"]

            for marker in markers:
                for project_dir in scan_dir.glob(f"**/{marker}"):
                    if project_dir.parts.count("node_modules") > 0:
                        continue
                    if project_dir.parts.count(".git") > 1:
                        continue

                    # Get project root
                    if marker == ".git":
                        root = project_dir.parent
                    else:
                        root = project_dir.parent

                    # Check depth
                    rel_depth = len(root.relative_to(scan_dir).parts)
                    if rel_depth > depth:
                        continue

                    # Get git remote if available
                    remote_url = ""
                    git_dir = root / ".git"
                    if git_dir.exists():
                        try:
                            result = subprocess.run(
                                ["git", "-C", str(root), "remote", "get-url", "origin"],
                                capture_output=True,
                                text=True,
                            )
                            if result.returncode == 0:
                                remote_url = result.stdout.strip()
                        except Exception:
                            pass

                    # Add to projects if not already added
                    if not any(p["local_path"] == str(root) for p in projects):
                        projects.append({
                            "name": root.name,
                            "local_path": str(root),
                            "remote_url": remote_url,
                            "source": "local",
                            "marker": marker,
                        })

        progress.update(task, description=f"Found {len(projects)} local projects")

        # Merge with existing inventory
        existing = load_inventory()
        for item in projects:
            item["scan_source"] = "local"

        combined = existing + projects
        save_inventory(combined)

        console.print(f"[green]✓ Added {len(projects)} local projects to inventory[/green]")
```

---

### Task 6: Implement Analysis Commands ✅

**Goal:** Implement analyze and dedupe commands

**Source scripts:**

- `work-prod/scripts/inventory/analyze-tech-stack.py`
- `work-prod/scripts/inventory/deduplicate-projects.py`

**Update:** `src/proj/commands/inventory.py` - replace `analyze` and `dedupe`

```python
@inv_app.command(name="analyze")
def analyze():
    """Analyze tech stack of inventory projects."""
    inventory = load_inventory()

    if not inventory:
        console.print("[yellow]No projects in inventory. Run scan first.[/yellow]")
        raise typer.Exit(1)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing projects...", total=len(inventory))

        for i, project in enumerate(inventory):
            progress.update(task, advance=1, description=f"Analyzing {project.get('name', 'unknown')}...")

            local_path = project.get("local_path")
            if not local_path or not Path(local_path).exists():
                continue

            root = Path(local_path)

            # Detect languages/frameworks
            languages = []
            frameworks = []

            if (root / "package.json").exists():
                languages.append("JavaScript")
                try:
                    with open(root / "package.json") as f:
                        pkg = json.load(f)
                        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                        if "react" in deps:
                            frameworks.append("React")
                        if "vue" in deps:
                            frameworks.append("Vue")
                        if "express" in deps:
                            frameworks.append("Express")
                except Exception:
                    pass

            if (root / "pyproject.toml").exists() or (root / "setup.py").exists():
                languages.append("Python")

            if (root / "Cargo.toml").exists():
                languages.append("Rust")

            if (root / "go.mod").exists():
                languages.append("Go")

            # Update project
            if languages:
                project["languages"] = languages
            if frameworks:
                project["frameworks"] = frameworks
            project["analyzed"] = True

        save_inventory(inventory)

        analyzed_count = sum(1 for p in inventory if p.get("analyzed"))
        console.print(f"[green]✓ Analyzed {analyzed_count} projects[/green]")


@inv_app.command(name="dedupe")
def dedupe():
    """Deduplicate inventory entries."""
    inventory = load_inventory()

    if not inventory:
        console.print("[yellow]No projects in inventory.[/yellow]")
        raise typer.Exit(1)

    original_count = len(inventory)

    # Dedupe by remote_url (primary) or name+local_path (secondary)
    seen_urls = set()
    seen_paths = set()
    unique = []

    for project in inventory:
        remote_url = project.get("remote_url", "").strip()
        local_path = project.get("local_path", "").strip()
        name = project.get("name", "")

        # Primary key: remote_url if available
        if remote_url:
            if remote_url not in seen_urls:
                seen_urls.add(remote_url)
                unique.append(project)
        # Secondary key: local_path
        elif local_path:
            if local_path not in seen_paths:
                seen_paths.add(local_path)
                unique.append(project)
        # Fallback: name (may have duplicates)
        else:
            unique.append(project)

    removed = original_count - len(unique)
    save_inventory(unique)

    console.print(f"[green]✓ Removed {removed} duplicates ({len(unique)} remaining)[/green]")
```

---

### Task 7: Implement Export Commands ✅

**Goal:** Implement export json and export api commands

**Source script:** `work-prod/scripts/map_inventory_to_projects.py`

**Update:** `src/proj/commands/inventory.py` - replace export commands

```python
@export_app.command(name="json")
def export_json(
    output: Path = typer.Argument(..., help="Output file path"),
    format: str = typer.Option("projects", "--format", "-f", help="Format: projects, raw"),
):
    """Export inventory to JSON file."""
    inventory = load_inventory()

    if not inventory:
        console.print("[yellow]No projects in inventory.[/yellow]")
        raise typer.Exit(1)

    if format == "projects":
        # Transform to work-prod project format
        projects = []
        for item in inventory:
            project = {
                "name": item.get("name", ""),
                "description": item.get("description", ""),
                "remote_url": item.get("remote_url", ""),
                "local_path": item.get("local_path", ""),
                "status": "active",
            }
            if item.get("languages"):
                project["languages"] = item["languages"]
            projects.append(project)

        data = {"projects": projects}
    else:
        data = inventory

    with open(output, "w") as f:
        json.dump(data, f, indent=2)

    console.print(f"[green]✓ Exported {len(inventory)} items to {output}[/green]")


@export_app.command(name="api")
def export_api(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show what would be imported"),
):
    """Push inventory to work-prod API."""
    from proj.api_client import APIClient, APIError

    inventory = load_inventory()

    if not inventory:
        console.print("[yellow]No projects in inventory.[/yellow]")
        raise typer.Exit(1)

    # Transform to project format
    projects = []
    for item in inventory:
        project = {
            "name": item.get("name", ""),
            "description": item.get("description", ""),
            "remote_url": item.get("remote_url", ""),
            "local_path": item.get("local_path", ""),
            "status": "active",
        }
        projects.append(project)

    if dry_run:
        console.print(f"[yellow]Dry run: Would import {len(projects)} projects[/yellow]")
        for p in projects[:5]:
            console.print(f"  - {p['name']}")
        if len(projects) > 5:
            console.print(f"  ... and {len(projects) - 5} more")
        return

    try:
        client = APIClient()
        result = client.import_projects(projects)

        console.print(f"[green]✓ Imported: {result.get('imported', 0)}[/green]")
        console.print(f"[yellow]  Skipped: {result.get('skipped', 0)}[/yellow]")
        if result.get("errors"):
            console.print(f"[red]  Errors: {len(result.get('errors', []))}[/red]")
    except APIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)
```

---

### Task 8: Implement Status Command ✅

**Goal:** Show inventory state

**Update:** `src/proj/commands/inventory.py` - replace `status`

```python
@inv_app.command(name="status")
def status():
    """Show inventory status."""
    inventory = load_inventory()
    inv_file = get_inventory_file()

    table = Table(title="Inventory Status")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Projects", str(len(inventory)))
    table.add_row("Data File", str(inv_file))
    table.add_row("File Exists", "Yes" if inv_file.exists() else "No")

    if inventory:
        # Count by source
        github_count = sum(1 for p in inventory if p.get("scan_source") == "github")
        local_count = sum(1 for p in inventory if p.get("scan_source") == "local")
        analyzed_count = sum(1 for p in inventory if p.get("analyzed"))

        table.add_row("GitHub Projects", str(github_count))
        table.add_row("Local Projects", str(local_count))
        table.add_row("Analyzed", str(analyzed_count))

        # Languages
        all_langs = []
        for p in inventory:
            all_langs.extend(p.get("languages", []))
        if all_langs:
            from collections import Counter
            lang_counts = Counter(all_langs).most_common(5)
            langs_str = ", ".join(f"{l}({c})" for l, c in lang_counts)
            table.add_row("Top Languages", langs_str)

    console.print(table)
```

---

### Task 9: Full Integration Testing

**Goal:** Test complete inventory workflow

**Manual testing:**

```bash
# Test scan commands
proj inv scan github --user yourusername
proj inv scan local --dir ~/Projects

# Check status
proj inv status

# Analyze
proj inv analyze
proj inv status  # Should show analyzed count

# Dedupe
proj inv dedupe

# Export
proj inv export json /tmp/inventory.json
cat /tmp/inventory.json | head

# Export to API (with work-prod running)
proj inv export api --dry-run
proj inv export api
```

---

## ✅ Completion Criteria

- [ ] `proj inv` command group exists
- [ ] `proj inv scan github` functional
- [ ] `proj inv scan local` functional
- [ ] `proj inv analyze` functional
- [ ] `proj inv dedupe` functional
- [ ] `proj inv export json` functional
- [ ] `proj inv export api` functional
- [ ] `proj inv status` functional
- [ ] All tests passing
- [ ] Integration workflow tested

---

## 📦 Deliverables

1. **Inventory commands** - `src/proj/commands/inventory.py`
2. **Command structure** - `inv`, `scan`, `export` subgroups
3. **Data management** - `~/.local/share/proj/inventory.json`
4. **Tests** - Command structure tests

---

## 🔗 Dependencies

### Prerequisites

- Phase 2 complete
- GitHub token (for scan github)
- Local projects directory

### External Dependencies

- requests (GitHub API)
- work-prod API (for export api)

### Blocks

- Phase 4 depends on Phase 3 completion

---

## 📊 Progress Tracking

### Command Structure (TDD)

- [ ] Tests written (RED)
- [ ] Structure created (GREEN)
- [ ] Commands registered

### Scan Commands

- [ ] scan github implemented
- [ ] scan local implemented

### Analysis Commands

- [ ] analyze implemented
- [ ] dedupe implemented

### Export Commands

- [ ] export json implemented
- [ ] export api implemented
- [ ] status implemented

### Integration

- [ ] Full workflow tested

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 2: Migrate Project Commands](phase-2.md)
- [Phase 4: Polish & Cleanup](phase-4.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-16
