# Code Structure Refactoring - Implementation Plan

**Purpose:** Concrete implementation plan for source and test restructuring  
**Status:** 🟡 Planned  
**Priority:** Medium  
**Effort:** ~4-5 hours total  
**Target Version:** v0.4.0  
**Created:** 2026-01-07  
**Last Updated:** 2026-01-07

---

## 📋 Quick Links

- **[Exploration](exploration.md)** - Research and options analysis
- **[Research Topics](research-topics.md)** - Outstanding research questions
- **[Original Proposal](../../../tmp/refactor-projects-module.md)** - Detailed projects.py refactor proposal

---

## 🎯 Overview

This plan addresses two related code quality issues:

1. **Large command module** - `projects.py` at 943 lines with 14 functions
2. **Flat test structure** - 24 test files in root `tests/` directory (4312 lines)

Both issues make the codebase harder to navigate, test, and maintain.

---

## 📊 Current State

### Source Code

| File | Lines | Issue |
|------|-------|-------|
| `src/proj/commands/projects.py` | 943 | ⚠️ Too large, 4 create modes |
| `src/proj/commands/inventory.py` | 637 | Borderline |
| `src/proj/commands/init.py` | 99 | ✓ Good |

### Tests

| Category | Files | Lines | Issue |
|----------|-------|-------|-------|
| `test_create_*.py` | 10 | ~1,700 | ⚠️ Scattered, should be grouped |
| `test_templates.py` | 1 | 669 | ⚠️ Large |
| `test_registry.py` | 1 | 660 | ⚠️ Large |
| `test_commands_projects.py` | 1 | 292 | Will shrink after source refactor |
| Other test files | 11 | ~991 | ✓ Reasonable |
| **Total** | 24 | 4,312 | |

---

## 🏗️ Part 1: Split `projects.py` Module

### Target Structure

```
src/proj/commands/
├── __init__.py
├── init.py                      # 99 lines ✓
├── inventory.py                 # 637 lines (defer)
└── projects/                    # NEW: Package
    ├── __init__.py             # Re-exports (~20 lines)
    ├── helpers.py              # Shared utilities (~100 lines)
    ├── list.py                 # list_projects, search_projects (~180 lines)
    ├── crud.py                 # get, update, delete, archive (~150 lines)
    ├── create.py               # create_project - all modes (~350 lines)
    └── import_export.py        # import_json (~50 lines)
```

### Migration Steps

| Step | Description | Risk |
|------|-------------|------|
| 1 | Create package structure + `__init__.py` | Low |
| 2 | Extract `helpers.py` (shared code) | Low |
| 3 | Extract `import_export.py` (smallest) | Low |
| 4 | Extract `crud.py` (simple functions) | Low |
| 5 | Extract `list.py` (read-only) | Low |
| 6 | Extract `create.py` (complex, last) | Medium |
| 7 | Delete original `projects.py` | Low |

### Module Contents

**`helpers.py`** (~100 lines):
- `STATUS_EMOJI` constant
- `get_client()` - API client factory
- `sync_to_api()` - API sync helper
- `init_git()` - Git initialization

**`list.py`** (~180 lines):
- `list_projects()` - List with filters
- `search_projects()` - Search by name/description

**`crud.py`** (~150 lines):
- `get_project()` - Get by ID
- `update_project()` - Update fields
- `delete_project()` - Delete from API
- `archive_project()` - Archive project

**`create.py`** (~350 lines):
- `detect_create_mode()` - Mode detection
- `prompt_for_create_options()` - Interactive prompts
- `_create_project_via_api()` - API-only helper
- `create_project()` - Main command (4 modes)

**`import_export.py`** (~50 lines):
- `import_json()` - Import from JSON file
- (Future: `export_json()`)

---

## 🧪 Part 2: Organize Test Structure

### Target Structure (Option B from exploration.md)

```
tests/
├── conftest.py                  # Shared fixtures
├── README.md                    # Test documentation
│
├── unit/                        # Unit tests (mocked dependencies)
│   ├── test_api_client.py
│   ├── test_config.py
│   ├── test_error_handler.py
│   ├── test_package.py
│   ├── test_registry.py
│   └── test_templates.py
│
├── integration/                 # Integration tests (real interactions)
│   ├── test_api_client.py
│   ├── test_cli.py
│   └── test_config.py
│
├── commands/                    # Command-specific tests
│   ├── test_init.py            # (from test_commands_init.py)
│   ├── test_inventory.py       # (from test_commands_inventory.py)
│   │
│   └── projects/               # Projects command tests (mirrors source)
│       ├── test_list.py        # List/search tests
│       ├── test_crud.py        # Get/update/delete/archive tests
│       ├── test_create.py      # Core create tests
│       └── test_import.py      # Import tests
│
└── create/                      # Create mode tests (detailed)
    ├── test_api_only.py        # (from test_create_api_only.py)
    ├── test_api_sync.py        # (from test_create_api_sync.py)
    ├── test_dry_run.py         # (from test_create_dry_run.py)
    ├── test_git.py             # (from test_create_git.py)
    ├── test_integration.py     # (from test_create_integration.py)
    ├── test_interactive.py     # (from test_create_interactive.py)
    ├── test_local_only.py      # (from test_create_local_only.py)
    ├── test_template.py        # (from test_create_template.py)
    └── test_flags.py           # (from test_cli_create_flags.py)
```

### Test File Mapping

| Current | New Location |
|---------|--------------|
| `test_api_client.py` | `unit/test_api_client.py` |
| `test_api_client_integration.py` | `integration/test_api_client.py` |
| `test_cli.py` | `unit/test_cli.py` |
| `test_cli_integration.py` | `integration/test_cli.py` |
| `test_cli_create_flags.py` | `create/test_flags.py` |
| `test_commands_init.py` | `commands/test_init.py` |
| `test_commands_inventory.py` | `commands/test_inventory.py` |
| `test_commands_projects.py` | `commands/projects/test_*.py` (split) |
| `test_config.py` | `unit/test_config.py` |
| `test_config_integration.py` | `integration/test_config.py` |
| `test_create_*.py` (10 files) | `create/test_*.py` |
| `test_error_handler.py` | `unit/test_error_handler.py` |
| `test_package.py` | `unit/test_package.py` |
| `test_registry.py` | `unit/test_registry.py` |
| `test_templates.py` | `unit/test_templates.py` |

### pytest Configuration

Update `pyproject.toml` to ensure test discovery works:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "integration: marks tests as integration tests",
    "slow: marks tests as slow",
]
```

---

## 📅 Implementation Plan

### PR Strategy

| PR | Content | Effort |
|----|---------|--------|
| **PR #1** | Create `projects/` package + helpers | ~30 min |
| **PR #2** | Extract `crud.py` + `import_export.py` | ~45 min |
| **PR #3** | Extract `list.py` | ~30 min |
| **PR #4** | Extract `create.py` (big one) | ~1 hr |
| **PR #5** | Create test directory structure + move files | ~1.5 hr |
| **PR #6** | Split `test_commands_projects.py` to match source | ~30 min |

**Total:** ~4-5 hours

### Order Rationale

1. **Source first, tests second** - Tests depend on source structure
2. **Smallest extractions first** - Build confidence, reduce risk
3. **`create.py` last** - Most complex, needs stable foundation
4. **Test reorg after source** - Can align test structure with new source structure

---

## ✅ Success Criteria

- [ ] All tests pass after each PR
- [ ] No functionality changes (pure refactor)
- [ ] Test coverage maintained at 97%
- [ ] No linting errors
- [ ] Clear module boundaries
- [ ] Easy to find relevant code
- [ ] Tests mirror source structure where appropriate

---

## 🔗 Related

- **[Exploration Document](exploration.md)** - Research and options
- **[Research Topics](research-topics.md)** - Outstanding questions
- **Original Proposal:** `tmp/refactor-projects-module.md`
- **Work-Prod Integration:** Will benefit from cleaner structure
- **Future:** May also refactor `inventory.py` (637 lines)

---

## 📝 Decision Notes

**Why Option B (subdirectories)?**
- Matches ecosystem (dev-infra, work-prod both use subdirectories)
- Scales better as project grows
- Clear separation of unit vs integration tests
- Enables selective test running (`pytest tests/unit/`)

**Why source refactor first?**
- Tests depend on source imports
- Easier to mirror source structure once it's stable
- Creates clear boundaries for test organization

**Research topics to address later:**
- Detailed pytest configuration (Topic 3)
- Marker usage alongside directories (Topic 4)
- dev-infra template updates (Topic 7)

---

**Last Updated:** 2026-01-07
