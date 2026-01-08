# Manual Testing Guide - Code Structure Refactoring

**Feature:** Code Structure Refactoring  
**Phases Covered:** Phase 1 (Source Code Refactoring)  
**Last Updated:** 2026-01-07  
**Status:** ✅ Active

---

## 📋 Overview

This guide provides step-by-step instructions for manually verifying that the code structure refactoring did not break existing functionality.

**Purpose:**
- Verify CLI commands still work after refactoring
- Confirm no breaking changes to import paths
- Validate that the refactored code behaves identically to the original

**Prerequisites:**
- `proj-cli` installed in development mode (`pip install -e .`)
- Virtual environment activated
- Terminal access

---

## 🧪 Phase 1: Source Code Refactoring

### Scenario 1.1: CLI Help - Verify Command Structure

**Objective:** Verify that CLI help displays correctly after refactoring.

**Steps:**

1. Run `proj --help` to see top-level help
2. Run `proj list --help` to see list command help
3. Run `proj create --help` to see create command help

**CLI Test:**

```bash
# Activate virtual environment
cd /Users/cdwilson/Projects/proj-cli
source venv/bin/activate

# Test top-level help
proj --help
# Expected: Shows all commands (list, get, create, update, delete, etc.)

# Test list command help
proj list --help
# Expected: Shows list command options (--format, --type, --status, etc.)

# Test create command help
proj create --help
# Expected: Shows create command options (--name, --type, --template, etc.)
```

**Expected Result:** ✅ All help commands display correctly without errors - PASSED

---

### Scenario 1.2: CLI Version - Verify Package Info

**Objective:** Verify that version command works after refactoring.

**Steps:**

1. Run `proj --version` to verify package version is accessible

**CLI Test:**

```bash
proj --version
# Expected: Displays version (e.g., "proj, version 0.3.1")
```

**Expected Result:** ✅ Version displays correctly - PASSED (0.3.1)

---

### Scenario 1.3: Import Compatibility - Verify Module Imports

**Objective:** Verify that the refactored package can be imported correctly.

**Steps:**

1. Open Python REPL
2. Import the projects module
3. Verify key functions are accessible

**Python Test:**

```python
# Start Python REPL
python3

# Import the package
>>> from proj.commands import projects

# Verify key exports are accessible
>>> hasattr(projects, 'list_projects')
True
>>> hasattr(projects, 'create_project')
True
>>> hasattr(projects, 'get_project')
True
>>> hasattr(projects, 'update_project')
True
>>> hasattr(projects, 'delete_project')
True
>>> hasattr(projects, 'import_json')
True
>>> hasattr(projects, 'get_client')
True
>>> hasattr(projects, 'STATUS_EMOJI')
True

# Verify console and logger are accessible (needed by tests)
>>> hasattr(projects, 'console')
True
>>> hasattr(projects, 'logger')
True

# Exit Python
>>> exit()
```

**Expected Result:** ✅ All imports work correctly, all key functions accessible - PASSED (10/10 imports verified)

---

### Scenario 1.4: Test Suite - Verify Tests Pass

**Objective:** Verify that automated tests pass after refactoring.

**Steps:**

1. Run the full test suite
2. Verify test count and pass rate

**CLI Test:**

```bash
cd /Users/cdwilson/Projects/proj-cli
source venv/bin/activate

# Run all tests
python3 -m pytest tests/ -v --tb=short 2>&1 | tail -20

# Expected: 234 passed (with 8 pre-existing failures)
# The 8 failures are pre-existing and not related to this refactoring
```

**Expected Result:** ✅ 234+ tests passing, no new failures - PASSED (234 passed, 8 pre-existing failures)

---

### Scenario 1.5: Package Structure - Verify Module Organization

**Objective:** Verify that the new package structure is correct.

**Steps:**

1. List the projects package directory
2. Verify all expected modules exist

**CLI Test:**

```bash
ls -la src/proj/commands/projects/

# Expected files:
# - __init__.py (main module with re-exports)
# - helpers.py (shared utilities)
# - list.py (list and search operations)
# - crud.py (get, update, delete, archive)
# - create.py (create project with multiple modes)
# - import_export.py (JSON import functionality)
```

**Expected Result:** ✅ All 6 expected files present in projects/ directory - PASSED

---

## ✅ Acceptance Criteria Checklist

- [x] Scenario 1.1 passes - CLI help displays correctly ✅
- [x] Scenario 1.2 passes - Version displays correctly ✅
- [x] Scenario 1.3 passes - Module imports work ✅
- [x] Scenario 1.4 passes - Test suite passes (no new failures) ✅
- [x] Scenario 1.5 passes - Package structure correct ✅

---

## 📝 Testing Notes

**Pre-existing Test Failures (8 tests):**
These failures existed before the refactoring and are NOT related to this PR:
- `test_version_matches_metadata` - Version mismatch between `pyproject.toml` and `__init__.py`
- `test_cli_no_args_shows_help` - Typer returns exit code 2 instead of 0
- `test_prompt_for_create_options_*` - Test patching issues with console instance

**What Changed:**
- `projects.py` (943 lines) → `projects/` package with 5 focused modules
- No functionality changes, only code organization
- Test patching compatibility maintained via re-exports in `__init__.py`

---

**Last Updated:** 2026-01-07
