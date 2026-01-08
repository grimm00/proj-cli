# Release Notes - v0.3.2

**Release Date:** 2026-01-08  
**Status:** ✅ Final  
**Type:** Patch Release

---

## Summary

This patch release focuses on internal code quality improvements with no user-facing changes. The main `projects.py` module (943 lines) has been refactored into a well-organized package, and the test suite has been reorganized into a hierarchical structure. A bug fix for blank "path" fields in inventory export is also included.

---

## Bug Fixes

### Inventory Export Path Fix (BUG-001)

- **Fixed:** Inventory export was producing blank "path" values
- **Cause:** Field name mismatch between proj-cli (`local_path`) and work-prod API (`path`)
- **Solution:** Updated inventory export to use `path` field name to match work-prod API schema

---

## Internal Improvements

### Code Structure Refactoring

**Source Code (PR #25):**

Split `src/proj/commands/projects.py` (943 lines, 14 functions) into a focused package:

```
src/proj/commands/projects/
├── __init__.py      # Re-exports for backward compatibility
├── helpers.py       # Shared utilities (~100 lines)
├── list.py          # list_projects, search_projects (~200 lines)
├── crud.py          # get, update, delete, archive (~150 lines)
├── create.py        # create_project and helpers (~515 lines)
└── import_export.py # import_json (~60 lines)
```

**Benefits:**

- Better code organization and maintainability
- Easier navigation and understanding
- Focused modules with single responsibilities
- No breaking changes - all imports still work

**Test Structure (PR #26):**

Reorganized flat `tests/` directory into hierarchical structure:

```
tests/
├── unit/           # Unit tests (7 files)
├── integration/    # Integration tests (3 files)
├── commands/       # CLI command tests
│   └── projects/   # Project command tests (4 files)
└── create/         # Create workflow tests (9 files)
```

**Benefits:**

- Clear test categorization
- Mirrors source code structure
- Easier test discovery and maintenance

### Code Quality Fixes (PRs #27, #28, #29)

All Sourcery review issues from PR #26 have been addressed:

- **PR #27:** Added test assertions for helper interactions, regression test for patching
- **PR #28:** Removed unused `_get_client()` function (dead code)
- **PR #29:** Created `assert_command_exists()` helper, refactored 16 tests

---

## Technical Details

### Changes Summary

- **PRs Merged:** 5 (+ 1 direct fix)
- **Files Changed:** ~30
- **Tests:** 238 passing (4 pre-existing failures unrelated)
- **Coverage:** ~92% maintained

### Key PRs

| PR | Description |
|----|-------------|
| #25 | refactor: Split projects.py into focused modules (Phase 1) |
| #26 | refactor: Test Structure Reorganization (Phase 2) |
| #27 | fix: Test regression coverage improvements |
| #28 | fix: Remove unused _get_client() function |
| #29 | fix: Parametrize command-existence tests |

---

## Breaking Changes

None. All changes are internal refactoring with full backward compatibility.

---

## Migration Guide

No migration needed. This is a drop-in replacement for v0.3.1.

---

## Known Issues

- 4 pre-existing test failures (unrelated to this release):
  - Version mismatch test (pyproject.toml vs `__init__.py`)
  - CLI no-args exit code test
  - Integration tests requiring backend
  - Template prompt test

---

**Last Updated:** 2026-01-08  
**Next Release:** v0.4.0 (Work-Prod Integration)
