# Code Structure Refactoring - Feature Plan

**Feature:** Code Structure Refactoring  
**Status:** 🔴 Not Started  
**Priority:** Medium  
**Type:** Refactor (no new functionality)  
**Target Version:** v0.4.0  
**Effort:** ~4-5 hours  
**Created:** 2026-01-07  
**Last Updated:** 2026-01-07

---

## 📋 Overview

Split the large `projects.py` module (943 lines, 14 functions) into focused submodules and reorganize the flat test directory (24 files, 4312 lines) into a structured hierarchy.

**Problem:**
- `projects.py` is hard to navigate with 4 different create modes
- Test files scattered in root directory with `_integration` suffix convention
- Structure doesn't match sibling projects (dev-infra, work-prod)
- Changes have large blast radius

**Solution:**
- Convert `projects.py` to `projects/` package with 5 focused modules
- Organize tests into `unit/`, `integration/`, `commands/`, `create/` directories

---

## 🎯 Goals

1. **Improve Maintainability** - Smaller, focused modules are easier to understand
2. **Reduce Risk** - Changes to `create` don't affect `list` operations
3. **Ecosystem Consistency** - Match patterns used in dev-infra and work-prod
4. **Enable Future Growth** - Clear place to add new commands and tests
5. **Prepare for Integration** - Work-prod integration will add complexity

---

## ✅ Success Criteria

- [ ] All tests pass after each change
- [ ] No functionality changes (pure refactor)
- [ ] Test coverage maintained at 97%
- [ ] No linting errors
- [ ] Clear module boundaries established
- [ ] Tests mirror source structure where appropriate

---

## 📊 Current State

### Source Code

| File | Lines | Issue |
|------|-------|-------|
| `src/proj/commands/projects.py` | 943 | ⚠️ Too large |
| `src/proj/commands/inventory.py` | 637 | Borderline (defer) |
| `src/proj/commands/init.py` | 99 | ✓ Good |

### Tests

| Category | Files | Lines |
|----------|-------|-------|
| `test_create_*.py` | 10 | ~1,700 |
| `test_templates.py` | 1 | 669 |
| `test_registry.py` | 1 | 660 |
| Other | 12 | ~1,283 |
| **Total** | **24** | **4,312** |

---

## 🏗️ Target Structure

### Source (Phase 1)

```
src/proj/commands/projects/
├── __init__.py      # Re-exports (~20 lines)
├── helpers.py       # Shared utilities (~100 lines)
├── list.py          # list, search (~180 lines)
├── crud.py          # get, update, delete, archive (~150 lines)
├── create.py        # create - all modes (~350 lines)
└── import_export.py # import_json (~50 lines)
```

### Tests (Phase 2)

```
tests/
├── conftest.py
├── unit/            # Mocked tests
├── integration/     # Real interaction tests
├── commands/        # Command-specific tests
│   └── projects/    # Mirrors source
└── create/          # Create mode tests (10 files)
```

---

## 📅 Implementation Phases

### Phase 1: Source Code Refactoring (~2.5 hours)

**Goal:** Split `projects.py` into `projects/` package

**Tasks:**
1. Create package structure + `__init__.py`
2. Extract `helpers.py` (shared utilities)
3. Extract `import_export.py` (smallest, lowest risk)
4. Extract `crud.py` (get, update, delete, archive)
5. Extract `list.py` (list, search)
6. Extract `create.py` (complex, last)
7. Delete original `projects.py`

**Deliverables:**
- `projects/` package with 5 modules
- All existing tests passing
- No functionality changes

### Phase 2: Test Structure Reorganization (~2 hours)

**Goal:** Organize tests into subdirectories

**Tasks:**
1. Create directory structure (`unit/`, `integration/`, `commands/`, `create/`)
2. Move unit tests to `unit/`
3. Move integration tests to `integration/`
4. Move command tests to `commands/`
5. Move create tests to `create/`
6. Split `test_commands_projects.py` to match source structure
7. Update pytest configuration if needed

**Deliverables:**
- Organized test directory
- All tests passing
- pytest discovers all tests

---

## 🔗 Related

- **[Exploration](../../explorations/code-structure-refactoring/)** - Research and decisions
- **[Work-Prod Integration](../../explorations/work-prod-integration/)** - Next feature
- **[Original Proposal](../../../tmp/refactor-projects-module.md)** - Detailed analysis

---

**Last Updated:** 2026-01-07
