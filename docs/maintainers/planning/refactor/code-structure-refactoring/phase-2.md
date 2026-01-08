# Code Structure Refactoring - Phase 2: Test Structure Reorganization

**Phase:** 2 - Test Structure Reorganization  
**Duration:** ~2 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 1 complete  
**Last Updated:** 2026-01-08

---

## 📋 Overview

Reorganize flat test directory (24 files, 4312 lines) into structured subdirectories matching ecosystem patterns.

**Success Definition:** All tests organized into `unit/`, `integration/`, `commands/`, `create/` directories, pytest discovers all tests, coverage maintained.

---

## 🎯 Goals

1. **Create directory structure** - `unit/`, `integration/`, `commands/`, `create/`
2. **Organize by test type** - Unit vs integration separation
3. **Mirror source structure** - `commands/projects/` mirrors source
4. **Group create tests** - All 9 create mode tests in `create/`

---

## 📊 Progress Tracking

| Task                           | Status         | Notes |
| ------------------------------ | -------------- | ----- |
| Task 1: Create Directories     | ✅ Complete    |       |
| Task 2: Move Unit Tests        | 🔴 Not Started |       |
| Task 3: Move Integration Tests | 🔴 Not Started |       |
| Task 4: Move Command Tests     | 🔴 Not Started |       |
| Task 5: Move Create Tests      | 🔴 Not Started |       |
| Task 6: Split Projects Tests   | 🔴 Not Started |       |
| Task 7: Fix Deferred Items     | 🔴 Not Started |       |
| Task 8: Update Configuration   | 🔴 Not Started |       |

---

## 📝 Tasks

### Task 1: Create Directory Structure

**Purpose:** Set up the new test directory hierarchy.

**Steps:**

1. Create the directory structure:

   ```bash
   mkdir -p tests/unit
   mkdir -p tests/integration
   mkdir -p tests/commands/projects
   mkdir -p tests/create
   ```

2. Create `__init__.py` files for pytest discovery:

   ```bash
   touch tests/unit/__init__.py
   touch tests/integration/__init__.py
   touch tests/commands/__init__.py
   touch tests/commands/projects/__init__.py
   touch tests/create/__init__.py
   ```

3. Verify structure:
   ```bash
   tree tests/ -I __pycache__
   ```

**Checklist:**

- [x] `tests/unit/` created
- [x] `tests/integration/` created
- [x] `tests/commands/` created
- [x] `tests/commands/projects/` created
- [x] `tests/create/` created
- [x] All `__init__.py` files created
- [x] Run tests to verify no breakage: 238 passed, 4 pre-existing failures

---

### Task 2: Move Unit Tests

**Purpose:** Move unit test files to `tests/unit/` directory.

**Files to move (7 files):**

| Current Location        | New Location                 |
| ----------------------- | ---------------------------- |
| `test_api_client.py`    | `unit/test_api_client.py`    |
| `test_config.py`        | `unit/test_config.py`        |
| `test_error_handler.py` | `unit/test_error_handler.py` |
| `test_package.py`       | `unit/test_package.py`       |
| `test_cli.py`           | `unit/test_cli.py`           |
| `test_registry.py`      | `unit/test_registry.py`      |
| `test_templates.py`     | `unit/test_templates.py`     |

**Steps:**

1. Move each file:

   ```bash
   git mv tests/test_api_client.py tests/unit/
   git mv tests/test_config.py tests/unit/
   git mv tests/test_error_handler.py tests/unit/
   git mv tests/test_package.py tests/unit/
   git mv tests/test_cli.py tests/unit/
   git mv tests/test_registry.py tests/unit/
   git mv tests/test_templates.py tests/unit/
   ```

2. Run tests to verify:

   ```bash
   python3 -m pytest tests/unit/ -v 2>&1 | tail -20
   ```

3. Verify test count unchanged:
   ```bash
   python3 -m pytest tests/ --collect-only 2>&1 | grep "test session starts" -A 2
   ```

**Checklist:**

- [ ] 7 files moved to `unit/`
- [ ] All unit tests pass
- [ ] Test count unchanged
- [ ] No import errors

---

### Task 3: Move Integration Tests

**Purpose:** Move integration test files to `tests/integration/` directory.

**Files to move (3 files):**

| Current Location                 | New Location                     |
| -------------------------------- | -------------------------------- |
| `test_api_client_integration.py` | `integration/test_api_client.py` |
| `test_config_integration.py`     | `integration/test_config.py`     |
| `test_cli_integration.py`        | `integration/test_cli.py`        |

**Note:** Remove `_integration` suffix as directory already indicates type.

**Steps:**

1. Move and rename files:

   ```bash
   git mv tests/test_api_client_integration.py tests/integration/test_api_client.py
   git mv tests/test_config_integration.py tests/integration/test_config.py
   git mv tests/test_cli_integration.py tests/integration/test_cli.py
   ```

2. Run tests to verify:
   ```bash
   python3 -m pytest tests/integration/ -v 2>&1 | tail -20
   ```

**Checklist:**

- [ ] 3 files moved to `integration/`
- [ ] Files renamed (removed `_integration` suffix)
- [ ] All integration tests pass (or expected failures for backend-dependent)
- [ ] No import errors

---

### Task 4: Move Command Tests

**Purpose:** Move command test files to `tests/commands/` directory.

**Files to move (2 files):**

| Current Location             | New Location                 |
| ---------------------------- | ---------------------------- |
| `test_commands_init.py`      | `commands/test_init.py`      |
| `test_commands_inventory.py` | `commands/test_inventory.py` |

**Note:** Remove `_commands` prefix as directory already indicates scope.

**Steps:**

1. Move and rename files:

   ```bash
   git mv tests/test_commands_init.py tests/commands/test_init.py
   git mv tests/test_commands_inventory.py tests/commands/test_inventory.py
   ```

2. Run tests to verify:
   ```bash
   python3 -m pytest tests/commands/ -v 2>&1 | tail -20
   ```

**Checklist:**

- [ ] 2 files moved to `commands/`
- [ ] Files renamed (removed `_commands` prefix)
- [ ] All command tests pass
- [ ] No import errors

---

### Task 5: Move Create Tests

**Purpose:** Move create-related test files to `tests/create/` directory.

**Files to move (9 files):**

| Current Location             | New Location                 |
| ---------------------------- | ---------------------------- |
| `test_create_api_only.py`    | `create/test_api_only.py`    |
| `test_create_api_sync.py`    | `create/test_api_sync.py`    |
| `test_create_dry_run.py`     | `create/test_dry_run.py`     |
| `test_create_git.py`         | `create/test_git.py`         |
| `test_create_integration.py` | `create/test_integration.py` |
| `test_create_interactive.py` | `create/test_interactive.py` |
| `test_create_local_only.py`  | `create/test_local_only.py`  |
| `test_create_template.py`    | `create/test_template.py`    |
| `test_cli_create_flags.py`   | `create/test_cli_flags.py`   |

**Note:** Remove `_create` prefix/infix as directory already indicates scope.

**Steps:**

1. Move and rename files:

   ```bash
   git mv tests/test_create_api_only.py tests/create/test_api_only.py
   git mv tests/test_create_api_sync.py tests/create/test_api_sync.py
   git mv tests/test_create_dry_run.py tests/create/test_dry_run.py
   git mv tests/test_create_git.py tests/create/test_git.py
   git mv tests/test_create_integration.py tests/create/test_integration.py
   git mv tests/test_create_interactive.py tests/create/test_interactive.py
   git mv tests/test_create_local_only.py tests/create/test_local_only.py
   git mv tests/test_create_template.py tests/create/test_template.py
   git mv tests/test_cli_create_flags.py tests/create/test_cli_flags.py
   ```

2. Run tests to verify:
   ```bash
   python3 -m pytest tests/create/ -v 2>&1 | tail -30
   ```

**Checklist:**

- [ ] 9 files moved to `create/`
- [ ] Files renamed (removed `_create` prefix)
- [ ] All create tests pass
- [ ] No import errors

---

### Task 6: Split Projects Tests

**Purpose:** Split `test_commands_projects.py` into multiple files mirroring source structure.

**Source:** `tests/test_commands_projects.py` (~8930 lines)

**Target structure:**

```
tests/commands/projects/
├── __init__.py
├── test_list.py       # list_projects, search_projects tests
├── test_crud.py       # get_project, update_project, delete_project, archive_project tests
├── test_create.py     # create_project, prompt tests
└── test_import.py     # import_json tests
```

**Steps:**

1. **Analyze current test file:**

   ```bash
   grep -n "^def test_" tests/test_commands_projects.py | head -30
   ```

2. **Categorize tests by function being tested:**

   - List tests: `test_list_*`, `test_search_*`
   - CRUD tests: `test_get_*`, `test_update_*`, `test_delete_*`, `test_archive_*`
   - Create tests: `test_create_*`, `test_prompt_*`
   - Import tests: `test_import_*`

3. **Create new test files with appropriate tests:**

   **test_list.py:**

   - Move all `test_list_*` and `test_search_*` tests
   - Add necessary imports from conftest

   **test_crud.py:**

   - Move all `test_get_*`, `test_update_*`, `test_delete_*`, `test_archive_*` tests
   - Add necessary imports

   **test_create.py:**

   - Move all `test_create_*` and `test_prompt_*` tests
   - Add necessary imports

   **test_import.py:**

   - Move all `test_import_*` tests
   - Add necessary imports

4. **Update imports in each file:**

   - Each file needs standard imports
   - Reference `proj.commands.projects` for patching

5. **Verify each file works:**

   ```bash
   python3 -m pytest tests/commands/projects/test_list.py -v
   python3 -m pytest tests/commands/projects/test_crud.py -v
   python3 -m pytest tests/commands/projects/test_create.py -v
   python3 -m pytest tests/commands/projects/test_import.py -v
   ```

6. **Remove original file after all tests pass:**
   ```bash
   git rm tests/test_commands_projects.py
   ```

**Checklist:**

- [ ] Tests categorized by function
- [ ] `test_list.py` created with list/search tests
- [ ] `test_crud.py` created with CRUD tests
- [ ] `test_create.py` created with create/prompt tests
- [ ] `test_import.py` created with import tests
- [ ] All split tests pass individually
- [ ] Original file removed
- [ ] Total test count unchanged

---

### Task 7: Fix Deferred Items from PR #25

**Purpose:** Address Sourcery review items deferred from Phase 1.

**Reference:** [PR #25 Sourcery Review](../../../feedback/sourcery/pr25.md)

#### 7a. Console Consolidation

**Issue:** Multiple modules instantiate their own `Console()` instead of using shared instance.

**Files to fix:**

- `src/proj/commands/projects/list.py`
- `src/proj/commands/projects/crud.py`
- `src/proj/commands/projects/import_export.py`

**Fix:**

```python
# Before (in each file):
from rich.console import Console
console = Console()

# After:
from .helpers import console  # Use shared instance
```

**Steps:**

1. Update `list.py`:

   ```python
   # Remove: from rich.console import Console
   # Remove: console = Console()
   # Add: from .helpers import console
   ```

2. Update `crud.py`:

   ```python
   # Remove: from rich.console import Console
   # Remove: console = Console()
   # Add: from .helpers import console
   ```

3. Update `import_export.py`:

   ```python
   # Remove: from rich.console import Console
   # Remove: console = Console()
   # Add: from .helpers import console
   ```

4. Verify tests still pass:
   ```bash
   python3 -m pytest tests/ -v -k "list or crud or import" 2>&1 | tail -20
   ```

**Checklist:**

- [ ] `list.py` updated to use shared console
- [ ] `crud.py` updated to use shared console
- [ ] `import_export.py` updated to use shared console
- [ ] All affected tests pass

---

#### 7b. Centralize `_get_package_imports()`

**Issue:** `_get_package_imports()` helper duplicated in `create.py` and `list.py`.

**Fix:** Move to `helpers.py` and import where needed.

**Steps:**

1. Add to `helpers.py`:

   ```python
   def get_package_imports():
       """Get package-level imports for test patching compatibility.

       This enables tests to patch proj.commands.projects.X and have
       the patches work correctly in submodules.
       """
       from proj.commands import projects
       return projects
   ```

2. Update `__init__.py` to export:

   ```python
   from .helpers import get_package_imports
   ```

3. Update `create.py`:

   ```python
   # Remove: def _get_package_imports(): ...
   # Add: from .helpers import get_package_imports
   # Replace: pkg = _get_package_imports()
   # With: pkg = get_package_imports()
   ```

4. Update `list.py`:

   ```python
   # Remove: def _get_package_imports(): ...
   # Add: from .helpers import get_package_imports
   # Replace: pkg = _get_package_imports()
   # With: pkg = get_package_imports()
   ```

5. Verify tests pass:
   ```bash
   python3 -m pytest tests/ -v -k "create or list" 2>&1 | tail -30
   ```

**Checklist:**

- [ ] `get_package_imports()` added to `helpers.py`
- [ ] Exported from `__init__.py`
- [ ] `create.py` updated to use shared helper
- [ ] `list.py` updated to use shared helper
- [ ] All affected tests pass

---

### Task 8: Update Configuration and Verify

**Purpose:** Ensure pytest configuration works with new structure.

**Steps:**

1. **Check pytest.ini or pyproject.toml:**

   ```bash
   grep -A 10 "\[tool.pytest" pyproject.toml
   ```

2. **Update testpaths if needed:**

   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   python_files = ["test_*.py"]
   python_classes = ["Test*"]
   python_functions = ["test_*"]
   ```

3. **Verify test discovery:**

   ```bash
   python3 -m pytest tests/ --collect-only 2>&1 | grep "test session starts" -A 5
   ```

4. **Run full test suite:**

   ```bash
   python3 -m pytest tests/ -v 2>&1 | tail -40
   ```

5. **Verify coverage:**

   ```bash
   python3 -m pytest tests/ --cov=src/proj --cov-report=term-missing 2>&1 | tail -20
   ```

6. **Update tests README.md:**
   - Document new directory structure
   - Explain test organization
   - Update any outdated references

**Checklist:**

- [ ] pytest configuration updated if needed
- [ ] Test discovery works
- [ ] All tests pass (same count as before)
- [ ] Coverage maintained at 97%
- [ ] Tests README updated

---

## ✅ Completion Criteria

- [ ] All test files moved to appropriate directories
- [ ] `test_commands_projects.py` split into `commands/projects/test_*.py`
- [ ] pytest discovers all tests
- [ ] All tests pass (234 expected to pass)
- [ ] Coverage maintained at 97%
- [ ] No test import errors
- [ ] Deferred items from PR #25 fixed
- [ ] Tests README updated

---

## 📦 Deliverables

**Final Directory Structure:**

```
tests/
├── conftest.py
├── README.md
├── unit/                        # 7 files
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_error_handler.py
│   ├── test_package.py
│   ├── test_registry.py
│   └── test_templates.py
├── integration/                 # 3 files
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_cli.py
│   └── test_config.py
├── commands/                    # 2 + 4 files
│   ├── __init__.py
│   ├── test_init.py
│   ├── test_inventory.py
│   └── projects/
│       ├── __init__.py
│       ├── test_list.py
│       ├── test_crud.py
│       ├── test_create.py
│       └── test_import.py
└── create/                      # 9 files
    ├── __init__.py
    ├── test_api_only.py
    ├── test_api_sync.py
    ├── test_cli_flags.py
    ├── test_dry_run.py
    ├── test_git.py
    ├── test_integration.py
    ├── test_interactive.py
    ├── test_local_only.py
    └── test_template.py
```

**File Count:**

- Unit: 7 files
- Integration: 3 files
- Commands: 2 files + 4 split files = 6 files
- Create: 9 files
- **Total:** 25 test files (from 24 original - test_commands_projects.py split into 4)

---

## 🔗 Dependencies

### Prerequisites

- [x] Phase 1 complete (source structure stable)

### Blocks

- None (final phase)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Previous Phase: Phase 1](phase-1.md)
- [Exploration](../../../explorations/code-structure-refactoring/)
- [PR #25 Sourcery Review](../../../feedback/sourcery/pr25.md)

---

**Last Updated:** 2026-01-08  
**Status:** ✅ Expanded  
**Next:** Begin implementation with Task 1
