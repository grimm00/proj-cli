# Migration Reference: work-prod project_cli

**Purpose:** Reference document for Phase 2 migration from work-prod
**Status:** 📋 Reference
**Last Updated:** 2025-12-16

---

## 📋 Overview

This document captures the structure and patterns of the original `work-prod/scripts/project_cli/` for migration to proj-cli in Phase 2.

---

## 📁 Source File Mapping

### Files to Migrate

| Source (work-prod) | Lines | Destination (proj-cli) | Notes |
|--------------------|-------|------------------------|-------|
| `cli.py` | ~108 | `cli.py` | Click → Typer conversion |
| `api_client.py` | ~215 | `api_client.py` | Mostly reusable |
| `config.py` | ~125 | ~~Already replaced~~ | Pydantic config exists |
| `error_handler.py` | ~248 | `error_handler.py` (new) | Rich panels, good patterns |
| `progress.py` | ~?? | May use Typer built-in | Spinner utility |
| `commands/*.py` | ~12 files | `commands/projects.py` | Consolidate or keep separate |

### Commands to Migrate (12 total)

| Command | Source File | Description |
|---------|-------------|-------------|
| `list` | `commands/list_cmd.py` | List projects with filters |
| `get` | `commands/get_cmd.py` | Get project details |
| `create` | `commands/create_cmd.py` | Create new project |
| `update` | `commands/update_cmd.py` | Update project |
| `delete` | `commands/delete_cmd.py` | Delete project |
| `archive` | `commands/archive_cmd.py` | Archive project |
| `import` | `commands/import_cmd.py` | Import from JSON |
| `config` | `commands/config_cmd.py` | Manage configuration |
| `stats` | `commands/stats_cmd.py` | Show statistics |
| `recent` | `commands/recent_cmd.py` | Show recent projects |
| `active` | `commands/active_cmd.py` | Show active projects |
| `mine` | `commands/mine_cmd.py` | Show user's projects |

---

## 🔄 Key Conversion Patterns

### CLI Framework: Click → Typer

**Original Click pattern:**

```python
import click

@click.command()
@click.option('--status', '-s', type=click.Choice(['active', 'paused']))
@click.option('--search', help='Search term')
def list_projects(status, search):
    """List all projects."""
    pass

# Registration
cli.add_command(list_projects, name='list')
```

**New Typer pattern:**

```python
import typer
from typing import Optional

@app.command(name="list")
def list_projects(
    status: Optional[str] = typer.Option(None, "--status", "-s", help="Filter by status"),
    search: Optional[str] = typer.Option(None, "--search", help="Search term"),
):
    """List all projects."""
    pass
```

### Key Differences

| Aspect | Click (work-prod) | Typer (proj-cli) |
|--------|-------------------|------------------|
| Type hints | Optional | Required (for auto-completion) |
| Option definition | Decorator | Function parameter |
| Choice types | `click.Choice([...])` | `Annotated[str, typer.Option(...)]` or enum |
| Help text | `help=` parameter | `help=` parameter (same) |
| Command registration | `cli.add_command()` | `@app.command()` decorator |

---

## ⚙️ Configuration Differences

### Original (work-prod): INI-based

```ini
# ~/.projrc
[api]
base_url = http://localhost:5000/api

[display]
max_rows = 50
color = true
```

**Pattern:** Singleton `Config` class with `configparser`

### New (proj-cli): YAML + Pydantic

```yaml
# ~/.config/proj/config.yaml
api_url: http://localhost:5000
github_username: null
local_scan_dirs:
  - ~/Projects
```

**Pattern:** `pydantic_settings.BaseSettings` with `Config.load()`

### Migration Notes

- Environment variable prefix: `PROJ_` (same)
- Original uses `/api` suffix in base_url, new does not
- Need to decide: support legacy `~/.projrc` or clean break?

---

## 🛠️ API Client

The `api_client.py` is largely reusable with minor changes:

### Keep As-Is

- `APIClient` class structure
- HTTP methods (list, get, create, update, delete, archive, import)
- Request/response handling
- Timeout settings (10s for most, 30s for import)

### Changes Needed

1. **Import Config:** Change from `from .config import Config` to new Pydantic config
2. **Base URL:** May need to adjust `/api` suffix handling
3. **Error handling:** Keep `error_handler.py` patterns

---

## 📊 Error Handler

The `error_handler.py` has excellent Rich panel patterns worth preserving:

```python
from rich.console import Console
from rich.panel import Panel

def handle_error(error: Exception, console: Console = None):
    """Handle errors and display friendly messages."""
    # Connection errors → helpful startup instructions
    # HTTP 404 → "Not Found" with context
    # HTTP 500 → Server error with restart instructions
    # Generic → Technical details + suggestions
```

### Custom Exceptions

```python
class CLIError(Exception): pass
class BackendConnectionError(CLIError): pass
class APIError(CLIError):
    def __init__(self, message, status_code=None, response_data=None): ...
```

---

## 📋 Command Patterns

### List Command Example (list_cmd.py)

Key features to preserve:
- Rich Table output with dynamic columns
- `--wide` flag for all columns
- Automatic column visibility based on filters
- Spinner during API calls

```python
# Dynamic column visibility
show_status = wide or status is not None
show_org = wide or organization is not None

# Rich table building
table = Table(title=f"Projects ({len(projects)})", expand=True)
table.add_column("ID", style="cyan", justify="right")
table.add_column("Name", style="green", no_wrap=False)
```

---

## 🗂️ Test Structure (work-prod)

```
tests/
├── conftest.py           # Shared fixtures
└── integration/
    ├── cli_loader.py     # CLI import helper
    ├── test_config_cmd.py
    ├── test_convenience_cmds.py
    ├── test_crud_cmds.py
    ├── test_edge_cases.py
    ├── test_error_handling.py
    ├── test_get_cmd.py
    ├── test_helpers.py
    ├── test_import_cmd.py
    └── test_list_cmd.py
```

### Test Approach

- Integration tests using Click's `CliRunner` (need Typer equivalent)
- Mocked API responses
- Error scenario coverage

---

## ✅ Migration Checklist

### Phase 2 Tasks

- [ ] Create `error_handler.py` (copy/adapt from work-prod)
- [ ] Update `api_client.py` to use new config
- [ ] Create `commands/projects.py` with Typer commands
- [ ] Migrate each command:
  - [ ] `list` - high priority
  - [ ] `get` - high priority
  - [ ] `create` - high priority
  - [ ] `update` - high priority
  - [ ] `delete` - high priority
  - [ ] `archive`
  - [ ] `import`
  - [ ] `config`
  - [ ] `stats`
  - [ ] `recent`
  - [ ] `active`
  - [ ] `mine`
- [ ] Add integration tests
- [ ] Verify all commands work against work-prod API

---

## 🔗 Related Documents

- [Phase 2: Migrate Project Commands](phase-2.md)
- [ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)
- [Feature Plan](feature-plan.md)

---

**Last Updated:** 2025-12-16


