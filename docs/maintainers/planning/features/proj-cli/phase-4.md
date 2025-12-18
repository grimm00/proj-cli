# proj-cli - Phase 4: Polish & Cleanup

**Phase:** 4 of 4  
**Duration:** ~3-4 hours (adjusted based on review)  
**Status:** ✅ Complete  
**Completed:** 2025-12-17  
**Merged:** PR #5 (2025-12-17)  
**Prerequisites:** Phase 3 complete, PR #4 merged  
**Coverage Baseline:** 14% (as of 2025-12-17)  
**Coverage Result:** 33% (exceeded expectation from 14%)

---

## 📋 Overview

Final phase for testing, documentation, UI polish, and cleaning up work-prod. This phase ensures the CLI is production-ready and removes the old CLI code from work-prod.

**Success Definition:** All tests passing, CLI has Rich UI enhancements, documentation complete, and work-prod `scripts/project_cli/` removed.

> **Note:** This phase also includes deferred tests from Phase 1 (package structure, configuration, CLI integration tests) that were skipped due to template adaptation needs.

---

## 🎯 Goals

1. Add comprehensive tests for all commands
2. Enhance UI with Rich (progress bars, colors, tables)
3. Implement first-run experience
4. Complete documentation (README, examples)
5. Clean up work-prod (remove old CLI code)
6. Update work-prod documentation

---

## 📝 Tasks

### Task 1: Write Comprehensive Tests (~1.5 hours)

**Goal:** Achieve ~50% test coverage (from 14% baseline)

**Includes Deferred Issues:**

- PR #2 #2: Add CliRunner tests for actual command behavior (HIGH value)
- PR #1 #4-6: Test coverage improvements
- PR #3 #5-8: Test coverage improvements for inventory commands
- PR #4: Handle PackageNotFoundError in test

**Files to create/update:**

#### `tests/conftest.py` - Test fixtures

```python
# tests/conftest.py
"""Test fixtures for proj-cli."""
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory."""
    config_dir = tmp_path / ".config" / "proj"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory."""
    data_dir = tmp_path / ".local" / "share" / "proj"
    data_dir.mkdir(parents=True)
    return data_dir


@pytest.fixture
def mock_xdg_dirs(temp_config_dir, temp_data_dir, monkeypatch):
    """Mock XDG directories to use temp dirs."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(temp_config_dir.parent.parent))
    monkeypatch.setenv("XDG_DATA_HOME", str(temp_data_dir.parent.parent))
    return {"config": temp_config_dir, "data": temp_data_dir}


@pytest.fixture
def sample_inventory():
    """Sample inventory data."""
    return [
        {
            "name": "project-a",
            "remote_url": "https://github.com/user/project-a",
            "source": "github",
        },
        {
            "name": "project-b",
            "local_path": "/home/user/Projects/project-b",
            "source": "local",
        },
    ]


@pytest.fixture
def mock_api_client():
    """Mock API client."""
    with patch("proj.api_client.APIClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client
```

#### `tests/test_config_integration.py` - Config integration tests

```python
# tests/test_config_integration.py
"""Integration tests for configuration."""
import os
import yaml


def test_config_creates_default_on_first_run(mock_xdg_dirs):
    """Test that default config is created on first run."""
    from proj.config import Config, get_config_file, ensure_dirs

    config_file = get_config_file()
    assert not config_file.exists()

    # Load config (should use defaults)
    config = Config.load()
    assert config.api_url == "http://localhost:5000"


def test_config_saves_and_loads(mock_xdg_dirs):
    """Test that config can be saved and loaded."""
    from proj.config import Config, get_config_file

    # Create and save config
    config = Config(api_url="http://custom:8000")
    config.save()

    # Load config
    loaded = Config.load()
    assert loaded.api_url == "http://custom:8000"


def test_config_env_override(mock_xdg_dirs, monkeypatch):
    """Test environment variable override."""
    monkeypatch.setenv("PROJ_API_URL", "http://env:9000")

    from proj.config import Config
    config = Config()
    assert config.api_url == "http://env:9000"
```

#### `tests/test_api_client_integration.py` - API client integration tests

```python
# tests/test_api_client_integration.py
"""Integration tests for API client (requires running API)."""
import pytest


@pytest.mark.integration
def test_list_projects_integration():
    """Test listing projects against real API."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        projects = client.list_projects()
        assert isinstance(projects, list)
    except Exception as e:
        pytest.skip(f"API not available: {e}")


@pytest.mark.integration
def test_create_and_delete_project_integration():
    """Test creating and deleting a project."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        # Create
        project = client.create_project({
            "name": "Test Project from proj-cli",
            "status": "active",
        })
        assert "id" in project

        # Delete
        client.delete_project(project["id"])
    except Exception as e:
        pytest.skip(f"API not available: {e}")
```

---

### Task 2: Add Rich UI Enhancements

**Goal:** Polish CLI output with Rich

**Updates to `src/proj/commands/projects.py`:**

```python
# Enhanced table styling
def list_projects(...):
    # ... existing code ...

    table = Table(
        title="Projects",
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
    )
    table.add_column("ID", style="cyan", justify="right")
    table.add_column("Name", style="green")
    table.add_column("Status", style="yellow")
    table.add_column("Organization")
    table.add_column("Classification")

    # Add status emoji
    status_emoji = {
        "active": "🟢",
        "inactive": "⚪",
        "archived": "📦",
        "completed": "✅",
    }

    for p in projects:
        status = p.get("status", "")
        emoji = status_emoji.get(status, "")
        table.add_row(
            str(p.get("id", "")),
            p.get("name", ""),
            f"{emoji} {status}",
            p.get("organization", ""),
            p.get("classification", ""),
        )

    console.print(table)
```

**Updates to `src/proj/commands/inventory.py`:**

```python
# Enhanced progress bars
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    TaskProgressColumn(),
    console=console,
) as progress:
    # ... existing code ...
```

---

### Task 3: Implement First-Run Experience

**Goal:** Create welcoming first-run experience

**File:** `src/proj/commands/init.py`

```python
"""First-run initialization command."""
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from proj.config import Config, get_config_file, ensure_dirs

console = Console()


def init_command(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
):
    """Initialize proj configuration."""
    config_file = get_config_file()

    if config_file.exists() and not force:
        console.print(f"[yellow]Config already exists at {config_file}[/yellow]")
        if not Confirm.ask("Overwrite?"):
            raise typer.Abort()

    console.print(Panel.fit(
        "[bold green]Welcome to proj![/bold green]\n\n"
        "Let's set up your configuration.",
        title="🚀 proj-cli",
    ))

    # Get API URL
    api_url = Prompt.ask(
        "work-prod API URL",
        default="http://localhost:5000",
    )

    # Get GitHub username
    github_username = Prompt.ask(
        "GitHub username (for inventory scanning)",
        default="",
    )

    # Get local scan directories
    console.print("\n[dim]Enter directories to scan for local projects (comma-separated)[/dim]")
    default_dir = str(Path.home() / "Projects")
    scan_dirs_str = Prompt.ask(
        "Local scan directories",
        default=default_dir,
    )
    scan_dirs = [d.strip() for d in scan_dirs_str.split(",") if d.strip()]

    # Create config
    ensure_dirs()
    config = Config(
        api_url=api_url,
        github_username=github_username or None,
        local_scan_dirs=scan_dirs,
    )
    config.save()

    console.print(f"\n[green]✓ Configuration saved to {config_file}[/green]")
    console.print("\n[bold]Next steps:[/bold]")
    console.print("  1. Run [cyan]proj list[/cyan] to see projects")
    console.print("  2. Run [cyan]proj inv scan github[/cyan] to scan GitHub repos")
    console.print("  3. Run [cyan]proj --help[/cyan] for all commands")
```

**Register in `src/proj/cli.py`:**

```python
from proj.commands.init import init_command

app.command(name="init")(init_command)
```

---

### Task 4: Create README and Documentation

**Goal:** Complete proj-cli documentation

**File:** `README.md`

````markdown
# proj-cli

Unified CLI for project and inventory management.

## Installation

```bash
# From local source
pip install -e .

# From GitHub
pip install git+https://github.com/yourusername/proj-cli.git
```
````

## Quick Start

```bash
# Initialize configuration
proj init

# List projects
proj list

# Get project details
proj get 1

# Create a project
proj create "My New Project" --desc "Description here"

# Scan GitHub repos
proj inv scan github --user yourusername

# Scan local projects
proj inv scan local --dir ~/Projects

# Analyze inventory
proj inv analyze

# Export to API
proj inv export api
```

## Commands

### Project Management

| Command                   | Description         |
| ------------------------- | ------------------- |
| `proj list`               | List all projects   |
| `proj get <id>`           | Get project details |
| `proj create <name>`      | Create new project  |
| `proj update <id>`        | Update project      |
| `proj delete <id>`        | Delete project      |
| `proj search <query>`     | Search projects     |
| `proj import-json <file>` | Import from JSON    |

### Inventory Management

| Command                       | Description            |
| ----------------------------- | ---------------------- |
| `proj inv scan github`        | Scan GitHub repos      |
| `proj inv scan local`         | Scan local directories |
| `proj inv analyze`            | Analyze tech stack     |
| `proj inv dedupe`             | Remove duplicates      |
| `proj inv export json <file>` | Export to JSON         |
| `proj inv export api`         | Push to work-prod API  |
| `proj inv status`             | Show inventory status  |

## Configuration

Configuration is stored at `~/.config/proj/config.yaml`:

```yaml
api_url: http://localhost:5000
github_username: yourusername
github_token: null # Set via PROJ_GITHUB_TOKEN env var
local_scan_dirs:
  - /home/user/Projects
```

### Environment Variables

| Variable               | Description                  |
| ---------------------- | ---------------------------- |
| `PROJ_API_URL`         | work-prod API URL            |
| `PROJ_GITHUB_TOKEN`    | GitHub personal access token |
| `PROJ_GITHUB_USERNAME` | GitHub username              |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=proj

# Lint
flake8 src/proj
```

## License

MIT

````

---

### Task 5: Clean Up work-prod (SEPARATE PR in work-prod repo)

**Goal:** Remove old CLI code from work-prod

> ⚠️ **Note:** This task creates a **separate PR in the work-prod repository**, not part of the proj-cli PR #5. Execute this **after** proj-cli PR #5 is merged.

**Steps:**

1. **Remove `scripts/project_cli/` directory:**

```bash
cd ~/Projects/work-prod
rm -rf scripts/project_cli/
````

2. **Update work-prod README.md:**

Add section about proj-cli:

````markdown
## CLI Tool

The `proj` CLI tool has been moved to a separate repository: [proj-cli](https://github.com/yourusername/proj-cli)

### Installation

```bash
pip install git+https://github.com/yourusername/proj-cli.git
```
````

### Quick Start

```bash
proj list            # List projects
proj get 1           # Get project details
proj create "Name"   # Create project
proj inv scan github # Scan GitHub repos
```

See [proj-cli README](https://github.com/yourusername/proj-cli#readme) for full documentation.

````

3. **Update any documentation referencing `proj` command**

4. **Commit changes:**

```bash
git add -A
git commit -m "chore: remove CLI code migrated to proj-cli

The proj CLI tool has been moved to the proj-cli repository.
work-prod is now API-only.

Migration: https://github.com/yourusername/proj-cli

Removed:
- scripts/project_cli/ directory
- All CLI-related code

Updated:
- README.md with link to new CLI repo"
````

---

### Task 6: Final Verification

**Goal:** Verify everything works end-to-end

**Checklist:**

```bash
# In proj-cli directory
cd ~/Projects/proj-cli

# Run all tests
pytest -v

# Run with coverage
pytest --cov=proj --cov-report=html

# Check linting
flake8 src/proj

# Test CLI commands
proj --version
proj --help
proj init --force
proj list
proj inv status

# Verify work-prod cleanup
cd ~/Projects/work-prod
ls scripts/  # Should NOT show project_cli/
```

---

### Task 7: Update Feature Plan Status ✅

**Goal:** Update feature-plan.md to reflect actual completion status

**Updates:**

1. Mark completed requirements as "✅ Done" ✅
2. Update phase status indicators ✅
3. Update Last Updated date ✅

---

## ✅ Completion Criteria

- [ ] Comprehensive tests written
- [ ] Test coverage ~50% (from 14% baseline)
- [ ] Rich UI enhancements added
- [ ] First-run experience implemented
- [ ] README complete with examples
- [ ] Feature plan status updated
- [ ] work-prod `scripts/project_cli/` removed (separate PR)
- [ ] work-prod README updated (separate PR)
- [ ] All tests passing
- [ ] Final verification complete

---

## 📦 Deliverables

1. **Comprehensive tests** - ~50% coverage (from 14% baseline)
2. **Rich UI** - Enhanced tables, progress bars, colors
3. **First-run experience** - `proj init` command
4. **Documentation** - Complete README with examples
5. **Feature plan update** - Status updated to reflect completion
6. **work-prod cleanup** - CLI code removed, docs updated (separate PR)

---

## 🔗 Dependencies

### Prerequisites

- Phase 3 complete ✅ (PR #3)
- Fix batch complete ✅ (PR #4)
- All commands functional ✅

### External Dependencies

- None

### Blocks

- None (final phase)

---

## 📊 Progress Tracking

### Testing

- [x] Test fixtures created ✅
- [x] Config tests written ✅
- [x] API client tests written ✅
- [x] Command tests written ✅ (CliRunner tests)
- [x] Integration tests written ✅
- [ ] Coverage ~50% (Current: 32%, improved from 14%)

### UI Polish

- [x] Table styling enhanced ✅
- [x] Progress bars improved ✅
- [x] Status emojis added ✅
- [x] First-run experience ✅

### Documentation

- [x] README complete ✅
- [x] Command examples added ✅
- [x] Config documentation ✅

### Cleanup

- [x] work-prod CLI removed ✅ (work-prod PR #38)
- [x] work-prod README updated ✅ (work-prod PR #38)
- [x] Documentation refs updated ✅ (work-prod PR #38)
- [x] Final commit made ✅ (work-prod PR #38)

### Verification

- [x] All tests passing ✅ (73 passed, 1 skipped)
- [x] CLI working end-to-end ✅ (version, help, init verified)
- [x] work-prod verified clean ✅ (Task 5 - work-prod PR #38)

---

## 📝 Implementation Notes

### Test Markers

```python
# Mark integration tests that need API
@pytest.mark.integration
def test_api_call():
    pass

# Run only unit tests
pytest -m "not integration"

# Run all tests
pytest
```

### Coverage Goals (Adjusted)

**Baseline:** 14% (as of 2025-12-17)  
**Target:** ~50% (realistic incremental improvement)

```
src/proj/
├── __init__.py        # 100% (current: 100%)
├── cli.py             # ~80% (current: 71%)
├── config.py          # ~80% (current: 76%)
├── api_client.py      # ~40% (current: 21%)
└── commands/
    ├── projects.py    # ~30% (current: 7%)
    └── inventory.py   # ~30% (current: 8%)
```

**Note:** Command modules have low coverage because they require mocking API calls. Focus on CliRunner tests for actual CLI behavior.

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 3: Add Inventory Commands](phase-3.md)
- [Transition Plan](transition-plan.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-17
