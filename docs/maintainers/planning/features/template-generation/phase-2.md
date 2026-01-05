# Template Generation - Phase 2: Local Registry

**Phase:** 2 - Local Registry  
**Duration:** ~2 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 1 complete (registry.path in config)  
**Last Updated:** 2025-01-05

---

## 📋 Overview

Create a local registry module to track template-created projects. The registry stores project metadata in a JSON file at the XDG-compliant location, enabling future sync features.

**Success Definition:** Can add, remove, and lookup projects in the registry with proper JSON persistence.

---

## 🎯 Goals

1. **Create `registry.py` module** - New module for registry operations
2. **Implement read/write functions** - Load and save registry JSON
3. **Implement project lookup** - Find projects by path or name
4. **Handle first-use creation** - Create registry file if it doesn't exist
5. **Support API linkage** - Store `work_prod_id` for linked projects

---

## 📝 Tasks

### Task 1: Create RegistryProject Model

**Purpose:** Define the data model for projects stored in the registry.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Create `tests/test_registry.py`
   - [ ] Write test for `RegistryProject` existence and fields
   - [ ] Verify test fails (no implementation yet)

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
   - [ ] Create `src/proj/registry.py`
   - [ ] Define `RegistryProject` dataclass/model
   - [ ] Run tests, verify they pass

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
   - [ ] Consider using Pydantic model for validation (like Config)
   - [ ] Add docstrings to class and fields
   - [ ] Ensure tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 2: Create Registry Model with Version

**Purpose:** Define the registry container that holds all projects.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Write test for `Registry` class existence
   - [ ] Test version field and projects list
   - [ ] Verify test fails

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
       
       project = RegistryProject(
           id="test-uuid",
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           created_at=datetime.now(),
       )
       
       registry = Registry(projects=[project])
       
       assert len(registry.projects) == 1
       assert registry.projects[0].name == "my-project"
   ```

2. **GREEN - Implement:**
   - [ ] Add `Registry` dataclass to `registry.py`
   - [ ] Set default version to "1.0"
   - [ ] Default empty projects list

   **Implementation:**
   ```python
   @dataclass
   class Registry:
       """Local registry containing all tracked projects."""
       
       version: str = "1.0"
       projects: list[RegistryProject] = field(default_factory=list)
   ```

3. **REFACTOR:**
   - [ ] Add type hints
   - [ ] Add docstrings

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 3: Implement Registry Load Function

**Purpose:** Load registry from JSON file at XDG path.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Test loading registry from existing file
   - [ ] Test loading from non-existent file (should create empty)
   - [ ] Use `tmp_path` fixture for isolation

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
       
       registry_data = {
           "version": "1.0",
           "projects": [
               {
                   "id": "test-uuid",
                   "name": "my-project",
                   "path": "/Users/me/Projects/my-project",
                   "template": "standard-project",
                   "template_version": "0.8.0",
                   "created_at": "2025-01-05T10:30:00",
                   "work_prod_id": None,
                   "metadata": {},
               }
           ],
       }
       with open(registry_file, "w") as f:
           json.dump(registry_data, f)
       
       from proj.registry import load_registry
       
       registry = load_registry()
       
       assert registry.version == "1.0"
       assert len(registry.projects) == 1
       assert registry.projects[0].name == "my-project"
   ```

2. **GREEN - Implement:**
   - [ ] Import `get_data_dir` from config or create helper
   - [ ] Implement `load_registry()` function
   - [ ] Handle JSON parsing with datetime conversion

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
           projects.append(
               RegistryProject(
                   id=proj_data["id"],
                   name=proj_data["name"],
                   path=Path(proj_data["path"]),
                   template=proj_data["template"],
                   template_version=proj_data["template_version"],
                   created_at=datetime.fromisoformat(proj_data["created_at"]),
                   work_prod_id=proj_data.get("work_prod_id"),
                   metadata=proj_data.get("metadata", {}),
               )
           )
       
       return Registry(version=data.get("version", "1.0"), projects=projects)
   ```

3. **REFACTOR:**
   - [ ] Extract JSON parsing to helper
   - [ ] Add error handling for malformed JSON

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 4: Implement Registry Save Function

**Purpose:** Save registry to JSON file with atomic writes.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Test saving registry creates file
   - [ ] Test saved JSON is valid and human-readable
   - [ ] Test atomic write (no corruption on error)

   **Test code:**
   ```python
   def test_save_registry_creates_file(tmp_path, monkeypatch):
       """Test that save_registry creates registry file."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import Registry, RegistryProject, save_registry
       from datetime import datetime
       from pathlib import Path
       
       project = RegistryProject(
           id="test-uuid",
           name="my-project",
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
       
       project = RegistryProject(
           id="test-uuid",
           name="my-project",
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
       assert data["projects"][0]["name"] == "my-project"
   ```

2. **GREEN - Implement:**
   - [ ] Implement `save_registry()` function
   - [ ] Create directory if it doesn't exist
   - [ ] Write with indentation for readability

   **Implementation:**
   ```python
   def save_registry(registry: Registry) -> None:
       """Save registry to disk with atomic write."""
       registry_path = _get_registry_path()
       
       # Ensure directory exists
       registry_path.parent.mkdir(parents=True, exist_ok=True)
       
       # Convert to JSON-serializable dict
       data = {
           "version": registry.version,
           "projects": [
               {
                   "id": proj.id,
                   "name": proj.name,
                   "path": str(proj.path),
                   "template": proj.template,
                   "template_version": proj.template_version,
                   "created_at": proj.created_at.isoformat(),
                   "work_prod_id": proj.work_prod_id,
                   "metadata": proj.metadata,
               }
               for proj in registry.projects
           ],
       }
       
       # Write with indentation for human readability
       with open(registry_path, "w") as f:
           json.dump(data, f, indent=2)
   ```

3. **REFACTOR:**
   - [ ] Add atomic write with temp file + rename
   - [ ] Add error handling

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 5: Implement Add Project Function

**Purpose:** Add a new project to the registry.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Test adding project to empty registry
   - [ ] Test adding project generates UUID
   - [ ] Test adding project sets created_at

   **Test code:**
   ```python
   def test_add_project_to_registry(tmp_path, monkeypatch):
       """Test adding a project to the registry."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, load_registry
       from pathlib import Path
       
       project = add_project(
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )
       
       assert project.name == "my-project"
       assert project.id is not None  # UUID generated
       assert project.created_at is not None  # Timestamp set
       
       # Verify persisted
       registry = load_registry()
       assert len(registry.projects) == 1
       assert registry.projects[0].name == "my-project"


   def test_add_project_with_work_prod_id(tmp_path, monkeypatch):
       """Test adding a project with API linkage."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, load_registry
       from pathlib import Path
       
       project = add_project(
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           work_prod_id=42,
       )
       
       assert project.work_prod_id == 42
   ```

2. **GREEN - Implement:**
   - [ ] Implement `add_project()` function
   - [ ] Generate UUID for id
   - [ ] Set created_at to now
   - [ ] Load, append, save

   **Implementation:**
   ```python
   import uuid
   from typing import Optional


   def add_project(
       name: str,
       path: Path,
       template: str,
       template_version: str,
       work_prod_id: Optional[int] = None,
       metadata: Optional[dict] = None,
   ) -> RegistryProject:
       """Add a new project to the registry."""
       project = RegistryProject(
           id=str(uuid.uuid4()),
           name=name,
           path=path,
           template=template,
           template_version=template_version,
           created_at=datetime.now(),
           work_prod_id=work_prod_id,
           metadata=metadata or {},
       )
       
       registry = load_registry()
       registry.projects.append(project)
       save_registry(registry)
       
       return project
   ```

3. **REFACTOR:**
   - [ ] Ensure no duplicates by path
   - [ ] Add validation

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 6: Implement Remove Project Function

**Purpose:** Remove a project from the registry by path.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Test removing existing project
   - [ ] Test removing non-existent project (no error)

   **Test code:**
   ```python
   def test_remove_project_from_registry(tmp_path, monkeypatch):
       """Test removing a project from the registry."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, remove_project, load_registry
       from pathlib import Path
       
       # Add a project first
       add_project(
           name="my-project",
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
   - [ ] Implement `remove_project()` function
   - [ ] Filter out project by path
   - [ ] Return True if removed, False if not found

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
   - [ ] Add remove by id option
   - [ ] Return removed project instead of bool?

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 7: Implement Lookup Functions

**Purpose:** Find projects by path, name, or work_prod_id.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Test lookup by path (exact match)
   - [ ] Test lookup by name (partial match)
   - [ ] Test lookup by work_prod_id
   - [ ] Test lookup returns None if not found

   **Test code:**
   ```python
   def test_get_project_by_path(tmp_path, monkeypatch):
       """Test finding a project by its path."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, get_project_by_path
       from pathlib import Path
       
       add_project(
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )
       
       project = get_project_by_path(Path("/Users/me/Projects/my-project"))
       
       assert project is not None
       assert project.name == "my-project"


   def test_get_project_by_path_not_found(tmp_path, monkeypatch):
       """Test get_project_by_path returns None if not found."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import get_project_by_path
       from pathlib import Path
       
       project = get_project_by_path(Path("/nonexistent/path"))
       
       assert project is None


   def test_get_project_by_name(tmp_path, monkeypatch):
       """Test finding a project by name."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, get_project_by_name
       from pathlib import Path
       
       add_project(
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
       )
       
       project = get_project_by_name("my-project")
       
       assert project is not None
       assert project.path == Path("/Users/me/Projects/my-project")


   def test_get_project_by_work_prod_id(tmp_path, monkeypatch):
       """Test finding a project by work_prod_id."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       
       from proj.registry import add_project, get_project_by_work_prod_id
       from pathlib import Path
       
       add_project(
           name="my-project",
           path=Path("/Users/me/Projects/my-project"),
           template="standard-project",
           template_version="0.8.0",
           work_prod_id=42,
       )
       
       project = get_project_by_work_prod_id(42)
       
       assert project is not None
       assert project.name == "my-project"
   ```

2. **GREEN - Implement:**
   - [ ] Implement `get_project_by_path()`
   - [ ] Implement `get_project_by_name()`
   - [ ] Implement `get_project_by_work_prod_id()`

   **Implementation:**
   ```python
   def get_project_by_path(path: Path) -> Optional[RegistryProject]:
       """Find a project by its path."""
       registry = load_registry()
       for project in registry.projects:
           if project.path == path:
               return project
       return None


   def get_project_by_name(name: str) -> Optional[RegistryProject]:
       """Find a project by its name."""
       registry = load_registry()
       for project in registry.projects:
           if project.name == name:
               return project
       return None


   def get_project_by_work_prod_id(work_prod_id: int) -> Optional[RegistryProject]:
       """Find a project by its work_prod_id."""
       registry = load_registry()
       for project in registry.projects:
           if project.work_prod_id == work_prod_id:
               return project
       return None
   ```

3. **REFACTOR:**
   - [ ] Consider combining into single `get_project()` with keyword args
   - [ ] Add list_projects() function

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 8: Implement List Projects Function

**Purpose:** List all projects in the registry.

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
           name="project-1",
           path=Path("/Users/me/Projects/project-1"),
           template="standard-project",
           template_version="0.8.0",
       )
       add_project(
           name="project-2",
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
           name="project-1",
           path=Path("/Users/me/Projects/project-1"),
           template="standard-project",
           template_version="0.8.0",
       )
       add_project(
           name="project-2",
           path=Path("/Users/me/Projects/project-2"),
           template="learning-project",
           template_version="0.8.0",
       )
       
       projects = list_projects(template="standard-project")
       
       assert len(projects) == 1
       assert projects[0].name == "project-1"
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
   - [ ] Add pagination for large registries

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

## ✅ Completion Criteria

- [x] Registry module exists at `src/proj/registry.py`
- [ ] Can add project to registry
- [ ] Can remove project from registry
- [ ] Can lookup project by path
- [ ] Can lookup project by name
- [ ] Registry file is valid JSON and human-readable
- [ ] Registry created on first use at XDG data directory
- [ ] All tests pass

---

## 📦 Deliverables

- New `src/proj/registry.py` module
- New `tests/test_registry.py` test file
- Registry schema matching ADR-0008 specification

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Task 1: RegistryProject Model | 🔴 Not Started | |
| Task 2: Registry Model | 🔴 Not Started | |
| Task 3: Load Registry | 🔴 Not Started | |
| Task 4: Save Registry | 🔴 Not Started | |
| Task 5: Add Project | 🔴 Not Started | |
| Task 6: Remove Project | 🔴 Not Started | |
| Task 7: Lookup Functions | 🔴 Not Started | |
| Task 8: List Projects | 🔴 Not Started | |

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-REG-1 | Project tracking | 🔴 Pending |
| FR-REG-2 | Project path storage | 🔴 Pending |
| FR-REG-3 | Template info (type, version) | 🔴 Pending |
| FR-REG-4 | API linkage (work_prod_id) | 🔴 Pending |
| NFR-REG-1 | Human-readable (JSON) | 🔴 Pending |
| NFR-REG-2 | XDG-compliant location | 🔴 Pending |

---

## 📄 Registry Schema (from ADR-0008)

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "uuid",
      "name": "my-app",
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z",
      "work_prod_id": 42,
      "metadata": {
        "description": "My awesome app",
        "author": "me"
      }
    }
  ]
}
```

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
**Status:** ✅ Expanded  
**Next:** Begin implementation with Task 1
