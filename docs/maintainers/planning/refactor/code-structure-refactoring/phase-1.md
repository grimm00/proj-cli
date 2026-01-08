# Code Structure Refactoring - Phase 1: Source Code Refactoring

**Phase:** 1 - Source Code Refactoring  
**Duration:** ~2.5 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** None  
**Last Updated:** 2026-01-07

---

## 📋 Overview

Split `projects.py` (943 lines, 14 functions) into a `projects/` package with focused submodules.

**Success Definition:** All 14 functions distributed across 5 modules, all tests passing, no functionality changes.

---

## 🎯 Goals

1. **Create package structure** - Convert file to directory with `__init__.py`
2. **Extract shared utilities** - `helpers.py` with common functions
3. **Separate by responsibility** - list, crud, create, import_export modules
4. **Maintain backward compatibility** - Re-exports in `__init__.py`

---

## 📊 Progress Tracking

| Task                          | Status      | Notes |
| ----------------------------- | ----------- | ----- |
| Task 1: Package Structure     | ✅ Complete |       |
| Task 2: Extract Helpers       | ✅ Complete |       |
| Task 3: Extract Import/Export | ✅ Complete |       |
| Task 4: Extract CRUD          | ✅ Complete |       |
| Task 5: Extract List          | ✅ Complete |       |
| Task 6: Extract Create        | ✅ Complete |       |
| Task 7: Cleanup & Verify      | ✅ Complete |       |

---

## 📝 Tasks

### Task 1: Package Structure

**Purpose:** Create the `projects/` package directory and `__init__.py` with re-exports.

**Steps:**

1. Create package directory:

   ```bash
   mkdir -p src/proj/commands/projects
   ```

2. Create `__init__.py` with re-exports:

   **File:** `src/proj/commands/projects/__init__.py`

   ```python
   """Project management commands."""

   # Re-export all commands for backward compatibility
   # These will be populated as we extract each module

   __all__ = [
       # From helpers
       "STATUS_EMOJI",
       "get_client",
       "sync_to_api",
       "init_git",
       # From list
       "list_projects",
       "search_projects",
       # From crud
       "get_project",
       "update_project",
       "delete_project",
       "archive_project",
       # From create
       "create_project",
       "detect_create_mode",
       "prompt_for_create_options",
       # From import_export
       "import_json",
   ]
   ```

3. Verify tests still pass (should fail initially - that's expected):
   ```bash
   python -m pytest tests/ -x -q
   ```

**Checklist:**

- [ ] Directory created: `src/proj/commands/projects/`
- [ ] `__init__.py` created with `__all__` list
- [ ] Ready for module extraction

---

### Task 2: Extract Helpers

**Purpose:** Move shared utilities that other modules depend on.

**Functions to extract:**

- `STATUS_EMOJI` (constant, line 36-42)
- `get_client()` (line 45-47)
- `sync_to_api()` (line 50-90)
- `init_git()` (line 93-112)
- `console` and `logger` instances

**Steps:**

1. Create `helpers.py`:

   **File:** `src/proj/commands/projects/helpers.py`

   ```python
   """Shared helpers for project commands."""

   import logging
   import subprocess
   from pathlib import Path
   from typing import Optional

   from rich.console import Console

   from proj.api_client import APIClient
   from proj.config import Config
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


   def get_client() -> APIClient:
       """Get configured API client."""
       return APIClient(Config.load())


   def sync_to_api(
       client: APIClient,
       name: str,
       path: Path,
       template: str,
       description: Optional[str] = None,
       console: Optional[Console] = None,
   ) -> Optional[int]:
       """Sync project to work-prod API."""
       # [Copy full implementation from projects.py lines 50-90]
       ...


   def init_git(project_path: Path) -> bool:
       """Initialize git repository in project."""
       # [Copy full implementation from projects.py lines 93-112]
       ...
   ```

2. Update `__init__.py` to import from helpers:

   ```python
   from .helpers import (
       STATUS_EMOJI,
       get_client,
       sync_to_api,
       init_git,
       console,
       logger,
   )
   ```

3. Run tests to verify helpers work:
   ```bash
   python -m pytest tests/ -x -q
   ```

**Checklist:**

- [ ] `helpers.py` created (~100 lines)
- [ ] All 4 functions + constants extracted
- [ ] Imports in `__init__.py` added
- [ ] Tests pass

---

### Task 3: Extract Import/Export

**Purpose:** Move the `import_json` function (smallest, lowest risk).

**Functions to extract:**

- `import_json()` (line 875-908)

**Steps:**

1. Create `import_export.py`:

   **File:** `src/proj/commands/projects/import_export.py`

   ```python
   """Project import/export commands."""

   import json
   from pathlib import Path

   import typer
   from rich.console import Console

   from .helpers import get_client

   console = Console()


   def import_json(
       file: Path = typer.Argument(..., help="JSON file to import"),
   ):
       """Import projects from JSON file."""
       # [Copy full implementation from projects.py lines 875-908]
       ...
   ```

2. Update `__init__.py`:

   ```python
   from .import_export import import_json
   ```

3. Verify tests pass:
   ```bash
   python -m pytest tests/test_commands_projects.py -x -q
   ```

**Checklist:**

- [ ] `import_export.py` created (~50 lines)
- [ ] `import_json` function extracted
- [ ] Import added to `__init__.py`
- [ ] Tests pass

---

### Task 4: Extract CRUD

**Purpose:** Move get, update, delete, archive operations.

**Functions to extract:**

- `get_project()` (line 347-376)
- `update_project()` (line 725-772)
- `delete_project()` (line 780-794)
- `archive_project()` (line 916-938)

**Steps:**

1. Create `crud.py`:

   **File:** `src/proj/commands/projects/crud.py`

   ```python
   """Project CRUD operations (get, update, delete, archive)."""

   from typing import Optional

   import typer
   from rich.console import Console
   from rich.table import Table

   from proj.error_handler import handle_error

   from .helpers import get_client, STATUS_EMOJI

   console = Console()


   def get_project(
       project_id: int = typer.Argument(..., help="Project ID to retrieve"),
   ):
       """Get a project by ID."""
       # [Copy implementation from projects.py lines 347-376]
       ...


   def update_project(
       project_id: int = typer.Argument(..., help="Project ID"),
       name: Optional[str] = typer.Option(None, "--name", "-n"),
       # ... other options
   ):
       """Update a project."""
       # [Copy implementation from projects.py lines 725-772]
       ...


   def delete_project(
       project_id: int = typer.Argument(..., help="Project ID"),
       force: bool = typer.Option(False, "--force", "-f"),
   ):
       """Delete a project permanently."""
       # [Copy implementation from projects.py lines 780-794]
       ...


   def archive_project(
       project_id: int = typer.Argument(..., help="Project ID"),
   ):
       """Archive a project."""
       # [Copy implementation from projects.py lines 916-938]
       ...
   ```

2. Update `__init__.py`:

   ```python
   from .crud import (
       get_project,
       update_project,
       delete_project,
       archive_project,
   )
   ```

3. Verify tests pass:
   ```bash
   python -m pytest tests/test_commands_projects.py -x -q
   ```

**Checklist:**

- [ ] `crud.py` created (~150 lines)
- [ ] All 4 CRUD functions extracted
- [ ] Imports added to `__init__.py`
- [ ] Tests pass

---

### Task 5: Extract List

**Purpose:** Move list and search operations.

**Functions to extract:**

- `list_projects()` (line 246-339)
- `search_projects()` (line 802-867)

**Steps:**

1. Create `list.py`:

   **File:** `src/proj/commands/projects/list.py`

   ```python
   """Project listing and search commands."""

   from typing import Optional

   import typer
   from rich.console import Console
   from rich.table import Table

   from proj.constants import PROJECT_TYPE_HELP
   from proj.error_handler import handle_error, InvalidProjectTypeError

   from .helpers import get_client, STATUS_EMOJI

   console = Console()


   def list_projects(
       format: str = typer.Option("table", "--format", "-f"),
       limit: int = typer.Option(50, "--limit", "-l"),
       classification: Optional[str] = typer.Option(None, "--class", "-c"),
       project_type: Optional[str] = typer.Option(
           None, "--type", "-t", help=PROJECT_TYPE_HELP
       ),
   ):
       """List all projects with optional filters."""
       # [Copy implementation from projects.py lines 246-339]
       ...


   def search_projects(
       query: str = typer.Argument(..., help="Search query"),
       format: str = typer.Option("table", "--format", "-f"),
   ):
       """Search projects by name or description."""
       # [Copy implementation from projects.py lines 802-867]
       ...
   ```

2. Update `__init__.py`:

   ```python
   from .list import list_projects, search_projects
   ```

3. Verify tests pass:
   ```bash
   python -m pytest tests/test_commands_projects.py -x -q
   ```

**Checklist:**

- [ ] `list.py` created (~180 lines)
- [ ] Both list functions extracted
- [ ] Imports added to `__init__.py`
- [ ] Tests pass

---

### Task 6: Extract Create

**Purpose:** Move the complex create_project command and related helpers.

**Functions to extract:**

- `prompt_for_create_options()` (line 114-160)
- `_create_project_via_api()` (line 168-204)
- `detect_create_mode()` (line 212-238)
- `create_project()` (line 384-717)

**Steps:**

1. Create `create.py`:

   **File:** `src/proj/commands/projects/create.py`

   ```python
   """Project creation with multiple modes."""

   import json
   from pathlib import Path
   from typing import Optional

   import click
   import typer
   from rich.console import Console
   from rich.prompt import Prompt

   from proj.config import Config
   from proj.error_handler import handle_error
   from proj.registry import add_project, update_project_work_prod_id
   from proj.templates import (
       create_from_template,
       get_templates_source,
       list_templates,
       TemplateError,
   )

   from .helpers import get_client, sync_to_api, init_git, console, logger

   console = Console()


   def prompt_for_create_options(config: Config) -> dict:
       """Prompt user for create options interactively."""
       # [Copy implementation from projects.py lines 114-160]
       ...


   def _create_project_via_api(
       name: str,
       description: Optional[str],
       # ... other params
   ) -> dict:
       """Create project via API (API-only mode)."""
       # [Copy implementation from projects.py lines 168-204]
       ...


   def detect_create_mode(
       template: Optional[str],
       api_only: bool,
       local_only: bool,
   ) -> str:
       """Detect which create mode to use."""
       # [Copy implementation from projects.py lines 212-238]
       ...


   def create_project(
       name: Optional[str] = typer.Argument(None, help="Project name"),
       # ... all the options
   ):
       """Create a new project.

       MODES:
       - Interactive (default): Prompts for all options
       - Template: Creates from dev-infra template
       - API-only: Original behavior (backward compatible)
       - Local-only: Template creation without API
       """
       # [Copy implementation from projects.py lines 384-717]
       ...
   ```

2. Update `__init__.py`:

   ```python
   from .create import (
       create_project,
       detect_create_mode,
       prompt_for_create_options,
   )
   ```

3. Verify tests pass:
   ```bash
   python -m pytest tests/test_create*.py -x -q
   python -m pytest tests/test_commands_projects.py -x -q
   ```

**Checklist:**

- [ ] `create.py` created (~350 lines)
- [ ] All 4 create functions extracted
- [ ] Imports added to `__init__.py`
- [ ] All create tests pass

---

### Task 7: Cleanup & Verify

**Purpose:** Delete original file, run full test suite, verify coverage.

**Steps:**

1. Verify `__init__.py` has all re-exports:

   ```python
   """Project management commands."""

   from .helpers import (
       STATUS_EMOJI,
       get_client,
       sync_to_api,
       init_git,
       console,
       logger,
   )
   from .list import list_projects, search_projects
   from .crud import (
       get_project,
       update_project,
       delete_project,
       archive_project,
   )
   from .create import (
       create_project,
       detect_create_mode,
       prompt_for_create_options,
   )
   from .import_export import import_json

   __all__ = [
       # Helpers
       "STATUS_EMOJI",
       "get_client",
       "sync_to_api",
       "init_git",
       "console",
       "logger",
       # List
       "list_projects",
       "search_projects",
       # CRUD
       "get_project",
       "update_project",
       "delete_project",
       "archive_project",
       # Create
       "create_project",
       "detect_create_mode",
       "prompt_for_create_options",
       # Import/Export
       "import_json",
   ]
   ```

2. Delete original `projects.py`:

   ```bash
   rm src/proj/commands/projects.py
   ```

3. Run full test suite:

   ```bash
   python -m pytest tests/ -v
   ```

4. Check coverage:

   ```bash
   python -m pytest tests/ --cov=src/proj --cov-report=term-missing
   ```

5. Run linting:

   ```bash
   flake8 src/proj/commands/projects/
   ```

6. Verify CLI still works:
   ```bash
   python -m proj list --help
   python -m proj create --help
   python -m proj get --help
   ```

**Checklist:**

- [ ] Original `projects.py` deleted
- [ ] All tests pass (should be same count as before)
- [ ] Coverage at 97%
- [ ] No linting errors
- [ ] CLI commands work

---

## ✅ Completion Criteria

- [ ] `projects/` package created with 5 modules
- [ ] All 14 functions properly distributed
- [ ] Re-exports in `__init__.py` maintain import compatibility
- [ ] All existing tests pass without modification
- [ ] No functionality changes
- [ ] Coverage maintained at 97%
- [ ] No linting errors

---

## 📦 Deliverables

| File                        | Lines | Contents                                        |
| --------------------------- | ----- | ----------------------------------------------- |
| `projects/__init__.py`      | ~40   | Re-exports, `__all__`                           |
| `projects/helpers.py`       | ~100  | STATUS_EMOJI, get_client, sync_to_api, init_git |
| `projects/list.py`          | ~180  | list_projects, search_projects                  |
| `projects/crud.py`          | ~150  | get, update, delete, archive                    |
| `projects/create.py`        | ~350  | create_project, detect_mode, prompts            |
| `projects/import_export.py` | ~50   | import_json                                     |
| **Total**                   | ~870  | (vs 943 original)                               |

---

## 🔗 Dependencies

### Prerequisites

- None (first phase)

### Blocks

- Phase 2 (test reorganization depends on stable source structure)

---

## 🔗 Related Documents

- [Refactor Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Next Phase: Phase 2](phase-2.md)
- [Exploration](../../../explorations/code-structure-refactoring/)

---

**Last Updated:** 2026-01-07  
**Status:** ✅ Expanded  
**Next:** Begin implementation with Task 1
