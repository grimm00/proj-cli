# CHANGELOG Draft - v0.3.2

**Draft Created:** 2026-01-08  
**Status:** ✅ Merged into CHANGELOG.md

---

## [0.3.2] - 2026-01-08

### Fixed

- **Inventory Export:** Fixed blank "path" field in inventory export by using correct field name to match work-prod API schema (BUG-001)

### Changed

- **Code Structure:** Refactored `projects.py` (943 lines) into focused package with 5 modules: `helpers.py`, `list.py`, `crud.py`, `create.py`, `import_export.py` (PR #25)
- **Test Structure:** Reorganized tests into hierarchical structure: `unit/`, `integration/`, `commands/`, `create/` (PR #26)
- **Test Helper:** Created `assert_command_exists()` helper function, refactored 16 command-existence tests (PR #29)

### Removed

- **Dead Code:** Removed unused `_get_client()` function from `create.py` (PR #28)

### Internal

- Added test assertions for helper function interactions (PR #27)
- Added regression test for `get_package_imports` patching pattern (PR #27)
- Consolidated `Console` instances across modules
- Centralized `get_package_imports()` helper function

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct (Fixed/Changed/Removed/Internal)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing where applicable
- [x] Merged into CHANGELOG.md

---

**Merged:** ✅ 2026-01-08
