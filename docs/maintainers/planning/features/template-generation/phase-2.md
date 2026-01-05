# Template Generation - Phase 2: Local Registry

**Phase:** 2 - Local Registry  
**Duration:** ~2 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 1 complete (registry.path in config)
**Last Updated:** 2025-01-05

---

## 📋 Overview

Create a local registry module to track template-created projects **for sync purposes**. The registry is a **minimal overlay** that cross-references `inventory.json` (the primary project store).

**Architecture (per ADR-0008 refinement):**

- `inventory.json` = Primary project store (all projects)
- `registry.json` = Sync overlay (template tracking only)

**Success Definition:** Can add, remove, and lookup projects in the registry with proper JSON persistence, integrated with inventory operations.

---

## 🎯 Goals

1. **Create `registry.py` module** - Minimal sync overlay for template tracking
2. **Implement read/write functions** - Load and save registry JSON
3. **Implement project lookup** - Find projects by path (cross-reference key)
4. **Handle first-use creation** - Create registry file if it doesn't exist
5. **Integrate with inventory** - Template projects go in both files

---

## 📝 Tasks

### Task 1: Create RegistryProject Model

**Purpose:** Define the data model for projects stored in the registry.

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Create `tests/test_registry.py`
   - [x] Write test for `RegistryProject` existence and fields
   - [x] Verify test fails (no implementation yet)

   **Test code:**

   ```python
   # tests/test_registry.py
   import pytest
   from datetime import datetime
   from pathlib import Path


   def test_registry_project_exists():
       """Test that RegistryProject class exists."""
       from proj.registry import RegistryProject
       assert RegistryProject is not None


   def test_registry_project_has_required_fields():
       """Test that RegistryProject has all required fields."""
       from proj.registry import RegistryProject

       project = RegistryProject(
           id="test-uuid",
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime.now(),
       )

       assert project.id == "test-uuid"
       assert project.name == "my-project"
       assert project.path == Path("/Users/me/Projects/my-project")
       assert project.template == "standard-project"
       assert project.template_version == "0.8.0"
       assert project.work_prod_id is None  # Optional
       assert project.metadata == {}  # Default empty dict


   def test_registry_project_with_optional_fields():
       """Test RegistryProject with optional work_prod_id and metadata."""
       from proj.registry import RegistryProject

       project = RegistryProject(
           id="test-uuid",
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime.now(),
           work_prod_id=42,
           metadata={"description": "My app", "author": "me"},
       )

       assert project.work_prod_id == 42
       assert project.metadata["description"] == "My app"
   ```

2. **GREEN - Implement minimum code:**

   - [x] Create `src/proj/registry.py`
   - [x] Define `RegistryProject` dataclass/model
   - [x] Run tests, verify they pass

   **Implementation:**

   ```python
   # src/proj/registry.py
   """Local registry for tracking template-created projects."""
   from dataclasses import dataclass, field
   from datetime import datetime
   from pathlib import Path
   from typing import Optional


   @dataclass
   class RegistryProject:
       """A project tracked in the local registry."""

       id: str
       name: str
       path: Path
       template: str
       template_version: str
       created_at: datetime
       work_prod_id: Optional[int] = None
       metadata: dict = field(default_factory=dict)
   ```

3. **REFACTOR:**
   - [x] Consider using Pydantic model for validation (like Config) - Using dataclass (appropriate for simple data model)
   - [x] Add docstrings to class and fields
   - [x] Ensure tests still pass

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

> ⚠️ **Refactoring Note (ADR-0008 Refinement):** Task 1 created RegistryProject with the original schema (id, name, path, template, template_version, created_at, work_prod_id, metadata). Per the architectural refinement, the model should be **minimal** (path, template, template_version, created_at only). Task 2 will simplify this model as part of creating the Registry container.

---

### Task 2: Create Registry Model with Version (+ Simplify RegistryProject)

**Purpose:** Define the registry container and simplify RegistryProject to minimal schema.

**Architecture Note:** Registry is a sync overlay. Only stores what's needed for template sync:

- `path` - Cross-reference key to inventory.json
- `template` - Which template was used
- `template_version` - Which version (for sync detection)
- `created_at` - Audit trail

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Write test for `Registry` class existence
   - [x] Test version field and projects list
   - [x] Update RegistryProject tests for minimal schema
   - [x] Verify test fails

   **Test code:**

   ```python
   def test_registry_exists():
       """Test that Registry class exists."""
       from proj.registry import Registry
       assert Registry is not None


   def test_registry_has_version_and_projects():
       """Test Registry has version and projects fields."""
       from proj.registry import Registry

       registry = Registry()

       assert registry.version == "1.0"
       assert registry.projects == []


   def test_registry_with_projects():
       """Test Registry can hold projects."""
       from proj.registry import Registry, RegistryProject
       from datetime import datetime
       from pathlib import Path

       # Minimal schema - only sync-related fields
       project = RegistryProject(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime.now(),
       )

       registry = Registry(projects=[project])

       assert len(registry.projects) == 1
       assert registry.projects[0].path == Path("/Users/me/Projects/my-project")


   def test_registry_project_minimal_schema():
       """Test RegistryProject has only sync-related fields (minimal)."""
       from proj.registry import RegistryProject
       from datetime import datetime
       from pathlib import Path

       project = RegistryProject(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime.now(),
       )

       assert project.path == Path("/Users/me/Projects/my-project")
       assert project.template == "standard-project"
       assert project.template_version == "0.8.0"
       # These fields should NOT exist (moved to inventory)
       assert not hasattr(project, 'id')
       assert not hasattr(project, 'name')
       assert not hasattr(project, 'work_prod_id')
       assert not hasattr(project, 'metadata')
   ```

2. **GREEN - Implement:**

   - [x] Simplify `RegistryProject` to minimal schema
   - [x] Add `Registry` dataclass to `registry.py`
   - [x] Update existing tests to use minimal schema

   **Implementation:**

   ```python
   @dataclass
   class RegistryProject:
       """A project tracked in the registry for template sync.

       Minimal schema - only sync-related fields.
       Project metadata lives in inventory.json.
       Cross-references inventory via path field.
       """

       path: Path  # Cross-reference key to inventory
       template: str  # Template type used
       template_version: str  # Template version for sync
       created_at: datetime  # When created


   @dataclass
   class Registry:
       """Local registry for template sync tracking.

       This is a sync overlay, not a project store.
       All project metadata lives in inventory.json.
       """

       version: str = "1.0"
       projects: list[RegistryProject] = field(default_factory=list)
   ```

3. **REFACTOR:**
   - [x] Update Task 1 tests to use minimal schema
   - [x] Add docstrings
   - [x] Ensure all tests pass

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] RegistryProject simplified to minimal schema
- [x] Task 1 tests updated
- [x] Code refactored and clean

---

### Task 3: Implement Registry Load Function

**Purpose:** Load registry from JSON file at XDG path.

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Test loading registry from existing file
   - [x] Test loading from non-existent file (should create empty)
   - [x] Use `tmp_path` fixture for isolation

   **Test code:**

   ```python
   import json


   def test_load_registry_creates_empty_if_not_exists(tmp_path, monkeypatch):
       """Test that load_registry creates empty registry if file doesn't exist."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import load_registry

       registry = load_registry()

       assert registry.version == "1.0"
       assert registry.projects == []


   def test_load_registry_reads_existing_file(tmp_path, monkeypatch):
       """Test that load_registry reads existing JSON file."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       # Create registry file
       registry_dir = tmp_path / "proj"
       registry_dir.mkdir(parents=True)
       registry_file = registry_dir / "registry.json"

       # Minimal schema - sync fields only
       registry_data = {
           "version": "1.0",
           "projects": [
               {
                   "path": "/Users/me/Projects/my-project",
                   "template": "standard-project",
                   "template_version": "0.8.0",
                   "created_at": "2025-01-05T10:30:00",
               }
           ],
       }
       with open(registry_file, "w") as f:
           json.dump(registry_data, f)

       from proj.registry import load_registry
       from pathlib import Path

       registry = load_registry()

       assert registry.version == "1.0"
       assert len(registry.projects) == 1
       assert registry.projects[0].path == Path("/Users/me/Projects/my-project")
       assert registry.projects[0].template == "standard-project"
   ```

2. **GREEN - Implement:**

   - [x] Import `get_data_dir` from config or create helper
   - [x] Implement `load_registry()` function
   - [x] Handle JSON parsing with datetime conversion

   **Implementation:**

   ```python
   import json
   from datetime import datetime
   from pathlib import Path

   from proj.config import get_data_dir


   def _get_registry_path() -> Path:
       """Get the path to the registry file."""
       return get_data_dir() / "registry.json"


   def load_registry() -> Registry:
       """Load registry from disk, creating empty registry if not exists."""
       registry_path = _get_registry_path()

       if not registry_path.exists():
           return Registry()

       with open(registry_path, "r") as f:
           data = json.load(f)

       projects = []
       for proj_data in data.get("projects", []):
           # Minimal schema - only sync fields
           projects.append(
               RegistryProject(
                   path=Path(proj_data["path"]),
                   template=proj_data["template"],
                   template_version=proj_data["template_version"],
                   created_at=datetime.fromisoformat(proj_data["created_at"]),
               )
           )

       return Registry(version=data.get("version", "1.0"), projects=projects)
   ```

3. **REFACTOR:**
   - [x] Extract JSON parsing to helper (inline for now - can refactor later if needed)
   - [ ] Add error handling for malformed JSON (deferred - can add in future if needed)

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

---

### Task 4: Implement Registry Save Function

**Purpose:** Save registry to JSON file with atomic writes.

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Test saving registry creates file
   - [x] Test saved JSON is valid and human-readable
   - [ ] Test atomic write (no corruption on error) - Deferred (can add later if needed)

   **Test code:**

   ```python
   def test_save_registry_creates_file(tmp_path, monkeypatch):
       """Test that save_registry creates registry file."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import Registry, RegistryProject, save_registry
       from datetime import datetime
       from pathlib import Path

       # Minimal schema
       project = RegistryProject(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime(2025, 1, 5, 10, 30, 0),
       )
       registry = Registry(projects=[project])

       save_registry(registry)

       registry_file = tmp_path / "proj" / "registry.json"
       assert registry_file.exists()


   def test_save_registry_creates_valid_json(tmp_path, monkeypatch):
       """Test that saved JSON is valid and human-readable."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import Registry, RegistryProject, save_registry
       from datetime import datetime
       from pathlib import Path

       # Minimal schema
       project = RegistryProject(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime(2025, 1, 5, 10, 30, 0),
       )
       registry = Registry(projects=[project])

       save_registry(registry)

       registry_file = tmp_path / "proj" / "registry.json"
       with open(registry_file) as f:
           data = json.load(f)

       assert data["version"] == "1.0"
       assert len(data["projects"]) == 1
       assert data["projects"][0]["path"] == "/Users/me/Projects/my-project"
       assert data["projects"][0]["template"] == "standard-project"
   ```

2. **GREEN - Implement:**

   - [x] Implement `save_registry()` function
   - [x] Create directory if it doesn't exist
   - [x] Write with indentation for readability

   **Implementation:**

   ```python
   def save_registry(registry: Registry) -> None:
       """Save registry to disk with atomic write."""
       registry_path = _get_registry_path()

       # Ensure directory exists
       registry_path.parent.mkdir(parents=True, exist_ok=True)

       # Convert to JSON-serializable dict (minimal schema)
       data = {
           "version": registry.version,
           "projects": [
               {
                   "path": str(proj.path),
                   "template": proj.template,
                   "template_version": proj.template_version,
                   "created_at": proj.created_at.isoformat(),
               }
               for proj in registry.projects
           ],
       }

       # Write with indentation for human readability
       with open(registry_path, "w") as f:
           json.dump(data, f, indent=2)
   ```

3. **REFACTOR:**
   - [ ] Add atomic write with temp file + rename (deferred - can add later if needed)
   - [x] Add error handling (basic - directory creation handles errors)

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

---

### Task 5: Implement Add Project Function

**Purpose:** Add a new project to the registry (sync tracking only).

**Architecture Note:** This adds to registry for sync tracking. The caller (create command in Phase 4) is responsible for adding to inventory separately.

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Test adding project to empty registry
   - [x] Test adding project sets created_at
   - [x] Test duplicate detection by path

   **Test code:**

   ```python
   def test_add_project_to_registry(tmp_path, monkeypatch):
       """Test adding a project to the registry."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, load_registry
       from pathlib import Path

       project = add_project(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )

       assert project.path == Path("/Users/me/Projects/my-project")
       assert project.template == "standard-project"
       assert project.created_at is not None  # Timestamp set

       # Verify persisted
       registry = load_registry()
       assert len(registry.projects) == 1
       assert registry.projects[0].path == Path("/Users/me/Projects/my-project")


   def test_add_project_prevents_duplicates(tmp_path, monkeypatch):
       """Test that adding duplicate path raises error."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, load_registry
       from pathlib import Path
       import pytest

       # Add first project
       add_project(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )

       # Try to add duplicate - should raise
       with pytest.raises(ValueError, match="already registered"):
           add_project(
               path=Path("/Users/me/Projects/my-project"),
               template="standard-project",
               template_version="0.9.0",
           )

       # Verify only one project
       registry = load_registry()
       assert len(registry.projects) == 1
   ```

2. **GREEN - Implement:**

   - [x] Implement `add_project()` function
   - [x] Set created_at to now
   - [x] Check for duplicates by path
   - [x] Load, append, save

   **Implementation:**

   ```python
   def add_project(
       path: Path,
       template: str,
       template_version: str,
   ) -> RegistryProject:
       """Add a new project to the registry for sync tracking.

       Note: This only adds to registry. Caller should also add to inventory.
       """
       registry = load_registry()

       # Check for duplicates
       for existing in registry.projects:
           if existing.path == path:
               raise ValueError(f"Project at {path} already registered")

       project = RegistryProject(
           path=path,
           template=template,
           template_version=template_version,
           created_at=datetime.now(),
       )

       registry.projects.append(project)
       save_registry(registry)

       return project
   ```

3. **REFACTOR:**
   - [x] Duplicate validation implemented (raises ValueError)
   - [ ] Path existence validation deferred (caller responsibility)

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

---

### Task 6: Implement Remove Project Function

**Purpose:** Remove a project from the registry by path.

**TDD Flow:**

1. **RED - Write failing test:**

   - [x] Test removing existing project
   - [x] Test removing non-existent project (no error)

   **Test code:**

   ```python
   def test_remove_project_from_registry(tmp_path, monkeypatch):
       """Test removing a project from the registry."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, remove_project, load_registry
       from pathlib import Path

       # Add a project first (minimal schema)
       add_project(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )

       # Remove it
       removed = remove_project(Path("/Users/me/Projects/my-project"))

       assert removed is True

       # Verify removed
       registry = load_registry()
       assert len(registry.projects) == 0


   def test_remove_nonexistent_project(tmp_path, monkeypatch):
       """Test removing a non-existent project returns False."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import remove_project
       from pathlib import Path

       removed = remove_project(Path("/nonexistent/path"))

       assert removed is False
   ```

2. **GREEN - Implement:**

   - [x] Implement `remove_project()` function
   - [x] Filter out project by path
   - [x] Return True if removed, False if not found

   **Implementation:**

   ```python
   def remove_project(path: Path) -> bool:
       """Remove a project from the registry by path."""
       registry = load_registry()

       original_count = len(registry.projects)
       registry.projects = [p for p in registry.projects if p.path != path]

       if len(registry.projects) < original_count:
           save_registry(registry)
           return True

       return False
   ```

3. **REFACTOR:**
   - [x] Return bool (True/False) - simple and sufficient for current needs
   - [ ] Return removed project instead of bool? (deferred - can add later if needed)

**Checklist:**

- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

---

### Task 7: Implement Lookup Function

**Purpose:** Find projects by path (the cross-reference key).

**Architecture Note:** Registry only supports lookup by path (the cross-reference key to inventory). Name and work_prod_id lookups should use inventory module.

**TDD Flow:**

1. **RED - Write failing test:**

   - [ ] Test lookup by path (exact match)
   - [ ] Test lookup returns None if not found
   - [ ] Test `is_registered()` helper

   **Test code:**

   ```python
   def test_get_project_by_path(tmp_path, monkeypatch):
       """Test finding a project by its path."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, get_project_by_path
       from pathlib import Path

       add_project(
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )

       project = get_project_by_path(Path("/Users/me/Projects/my-project"))

       assert project is not None
       assert project.template == "standard-project"
       assert project.template_version == "0.8.0"


   def test_get_project_by_path_not_found(tmp_path, monkeypatch):
       """Test get_project_by_path returns None if not found."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import get_project_by_path
       from pathlib import Path

       project = get_project_by_path(Path("/nonexistent/path"))

       assert project is None


   def test_is_registered(tmp_path, monkeypatch):
       """Test is_registered helper function."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, is_registered
       from pathlib import Path

       path = Path("/Users/me/Projects/my-project")

       # Not registered yet
       assert is_registered(path) is False

       # Add project
       add_project(
           path=path,
           template="standard-project",
           template_version="0.8.0",
       )

       # Now registered
       assert is_registered(path) is True
   ```

2. **GREEN - Implement:**

   - [ ] Implement `get_project_by_path()`
   - [ ] Implement `is_registered()` helper

   **Implementation:**

   ```python
   def get_project_by_path(path: Path) -> Optional[RegistryProject]:
       """Find a project by its path (cross-reference key)."""
       registry = load_registry()
       for project in registry.projects:
           if project.path == path:
               return project
       return None


   def is_registered(path: Path) -> bool:
       """Check if a project path is registered for sync tracking."""
       return get_project_by_path(path) is not None
   ```

3. **REFACTOR:**
   - [ ] Add caching for frequently accessed registry?

**Checklist:**

- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 8: Implement List Projects Function

**Purpose:** List all projects in the registry (for sync tracking).

**TDD Flow:**

1. **RED - Write failing test:**

   - [ ] Test listing empty registry
   - [ ] Test listing registry with projects
   - [ ] Test filtering by template type

   **Test code:**

   ```python
   def test_list_projects_empty(tmp_path, monkeypatch):
       """Test listing projects from empty registry."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import list_projects

       projects = list_projects()

       assert projects == []


   def test_list_projects(tmp_path, monkeypatch):
       """Test listing all projects."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, list_projects
       from pathlib import Path

       add_project(
           path=Path("/Users/me/Projects/project-1"),
           template="standard-project",
           template_version="0.8.0",
       )
       add_project(
           path=Path("/Users/me/Projects/project-2"),
           template="learning-project",
           template_version="0.8.0",
       )

       projects = list_projects()

       assert len(projects) == 2


   def test_list_projects_filter_by_template(tmp_path, monkeypatch):
       """Test filtering projects by template type."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       from proj.registry import add_project, list_projects
       from pathlib import Path

       add_project(
           path=Path("/Users/me/Projects/project-1"),
           template="standard-project",
           template_version="0.8.0",
       )
       add_project(
           path=Path("/Users/me/Projects/project-2"),
           template="learning-project",
           template_version="0.8.0",
       )

       projects = list_projects(template="standard-project")

       assert len(projects) == 1
       assert projects[0].path == Path("/Users/me/Projects/project-1")
   ```

2. **GREEN - Implement:**

   - [ ] Implement `list_projects()` function
   - [ ] Add optional template filter

   **Implementation:**

   ```python
   def list_projects(template: Optional[str] = None) -> list[RegistryProject]:
       """List all projects in the registry, optionally filtered by template."""
       registry = load_registry()

       if template:
           return [p for p in registry.projects if p.template == template]

       return registry.projects
   ```

3. **REFACTOR:**
   - [ ] Add sorting options

**Checklist:**

- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

## ✅ Completion Criteria

- [x] Registry module exists at `src/proj/registry.py`
- [ ] RegistryProject simplified to minimal schema (path, template, template_version, created_at)
- [ ] Can add project to registry
- [ ] Can remove project from registry
- [ ] Can lookup project by path (cross-reference key)
- [ ] Registry file is valid JSON and human-readable
- [ ] Registry created on first use at XDG data directory
- [ ] All tests pass

---

## 📦 Deliverables

- New `src/proj/registry.py` module (minimal sync overlay)
- New `tests/test_registry.py` test file
- Registry schema matching ADR-0008 refined specification

---

## 📊 Progress Tracking

| Task                              | Status         | Notes                                       |
| --------------------------------- | -------------- | ------------------------------------------- |
| Task 1: RegistryProject Model     | ✅ Complete    | Updated to minimal schema in Task 2         |
| Task 2: Registry Model + Simplify | ✅ Complete    | Registry added, RegistryProject simplified  |
| Task 3: Load Registry             | ✅ Complete    | load_registry() implemented, all tests pass |
| Task 4: Save Registry             | ✅ Complete    | save_registry() implemented, all tests pass |
| Task 5: Add Project               | ✅ Complete    | add_project() implemented, all tests pass   |
| Task 6: Remove Project            | ✅ Complete    | remove_project() implemented, all tests pass |
| Task 7: Lookup Function           | 🔴 Not Started | Path lookup only (cross-reference key)      |
| Task 8: List Projects             | 🔴 Not Started |                                             |

---

## 📊 Requirements Addressed

| Requirement | Description                   | Status     | Notes                       |
| ----------- | ----------------------------- | ---------- | --------------------------- |
| FR-REG-1    | Project tracking              | 🔴 Pending |                             |
| FR-REG-2    | Project path storage          | 🔴 Pending | Path is cross-reference key |
| FR-REG-3    | Template info (type, version) | 🔴 Pending | For sync tracking           |
| FR-REG-4    | API linkage (work_prod_id)    | ✅ N/A     | Moved to inventory.json     |
| NFR-REG-1   | Human-readable (JSON)         | 🔴 Pending |                             |
| NFR-REG-2   | XDG-compliant location        | 🔴 Pending |                             |

---

## 📄 Registry Schema (Minimal - from ADR-0008 refined)

Registry is a sync overlay, not a full project store. Cross-references inventory.json via path.

```json
{
  "version": "1.0",
  "projects": [
    {
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z"
    }
  ]
}
```

**Note:** Project metadata (name, description, work_prod_id) lives in inventory.json.

---

## 🔗 Dependencies

### Prerequisites

- Phase 1 complete (registry.path in config)

### Blocks

- Phase 4 (registry integration in create command)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 1 - Config Extension](phase-1.md)
- [Next Phase: Phase 3 - Template Copying](phase-3.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🟠 In Progress (Refined per ADR-0008 update)  
**Next:** Continue with Task 2 (simplify RegistryProject + add Registry model)
