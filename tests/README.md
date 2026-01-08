# Tests

**Purpose:** Test suite for proj-cli validation  
**Status:** ✅ Active  
**Last Updated:** 2026-01-08

---

## 📋 Quick Links

### Test Organization

- **[Unit Tests](unit/)** - Individual component testing (7 files)
- **[Integration Tests](integration/)** - Component interaction testing (3 files)
- **[Command Tests](commands/)** - CLI command testing
  - **[Projects Commands](commands/projects/)** - Project command tests (4 files)
  - **[Inventory Commands](commands/)** - Inventory command tests
- **[Create Tests](create/)** - Project creation testing (9 files)

---

## 🎯 Overview

The tests directory contains all test suites for validating proj-cli functionality. Tests are organized by type and mirror the source code structure where applicable.

### Testing Strategy

1. **Unit Tests** (`tests/unit/`) - Test individual functions and components
2. **Integration Tests** (`tests/integration/`) - Test component interactions
3. **Command Tests** (`tests/commands/`) - Test CLI command functionality
4. **Create Tests** (`tests/create/`) - Test project creation workflows

---

## 📁 Directory Structure

```
tests/
├── conftest.py                    # Shared pytest fixtures
├── README.md                      # This file
├── unit/                          # Unit tests (7 files)
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_error_handler.py
│   ├── test_package.py
│   ├── test_registry.py
│   └── test_templates.py
├── integration/                   # Integration tests (3 files)
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_cli.py
│   └── test_config.py
├── commands/                      # Command tests
│   ├── __init__.py
│   ├── test_init.py
│   ├── test_inventory.py
│   └── projects/                  # Project command tests (4 files)
│       ├── __init__.py
│       ├── test_list.py           # List and search tests
│       ├── test_crud.py           # Get, update, delete, archive tests
│       ├── test_create.py         # Create and prompt tests
│       └── test_import.py         # Import tests
└── create/                        # Create workflow tests (9 files)
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

---

## 🧪 Test Organization Principles

### Mirror Source Structure

Project command tests (`tests/commands/projects/`) mirror the source structure (`src/proj/commands/projects/`):

- `test_list.py` → `list.py`
- `test_crud.py` → `crud.py`
- `test_create.py` → `create.py`
- `test_import.py` → `import_export.py`

### Test Categories

- **Unit Tests**: Test individual functions/classes in isolation
- **Integration Tests**: Test component interactions (API client, CLI, config)
- **Command Tests**: Test CLI command behavior and output
- **Create Tests**: Test project creation workflows (template, API, local-only, etc.)

---

## 🚀 Running Tests

### Run All Tests

```bash
python3 -m pytest tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only
python3 -m pytest tests/unit/ -v

# Integration tests only
python3 -m pytest tests/integration/ -v

# Command tests only
python3 -m pytest tests/commands/ -v

# Create tests only
python3 -m pytest tests/create/ -v
```

### Run Specific Test Files

```bash
# Project command tests
python3 -m pytest tests/commands/projects/test_list.py -v
python3 -m pytest tests/commands/projects/test_crud.py -v
python3 -m pytest tests/commands/projects/test_create.py -v
python3 -m pytest tests/commands/projects/test_import.py -v
```

### Run with Coverage

```bash
python3 -m pytest tests/ --cov=src/proj --cov-report=term-missing
```

---

## 📊 Test Statistics

- **Total Tests**: 242 tests collected
- **Test Organization**: Organized by type and mirroring source structure
- **Coverage**: Maintained at project level (projects module: 76-100% coverage)

---

## 🔍 Test Discovery

pytest automatically discovers tests using the following configuration (`pyproject.toml`):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
```

All test files follow the `test_*.py` naming convention and are automatically discovered.

---

**Last Updated:** 2026-01-08  
**Status:** ✅ Active  
**Next:** Continue adding tests as features are developed
