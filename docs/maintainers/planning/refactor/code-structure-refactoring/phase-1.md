# Code Structure Refactoring - Phase 1: Source Code Refactoring

**Phase:** 1 - Source Code Refactoring  
**Duration:** ~2.5 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** None

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

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan code-structure-refactoring --expand --phase 1` to add detailed tasks.

### Task Categories

- [ ] **Task 1: Package Structure** - Create `projects/` directory and `__init__.py`
- [ ] **Task 2: Extract Helpers** - Move shared utilities to `helpers.py`
- [ ] **Task 3: Extract Import/Export** - Move `import_json` to `import_export.py`
- [ ] **Task 4: Extract CRUD** - Move get, update, delete, archive to `crud.py`
- [ ] **Task 5: Extract List** - Move list_projects, search_projects to `list.py`
- [ ] **Task 6: Extract Create** - Move create_project to `create.py`
- [ ] **Task 7: Cleanup** - Delete original `projects.py`, verify tests

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

- `src/proj/commands/projects/__init__.py` (~20 lines)
- `src/proj/commands/projects/helpers.py` (~100 lines)
- `src/proj/commands/projects/list.py` (~180 lines)
- `src/proj/commands/projects/crud.py` (~150 lines)
- `src/proj/commands/projects/create.py` (~350 lines)
- `src/proj/commands/projects/import_export.py` (~50 lines)

---

## 🔗 Dependencies

### Prerequisites

- None (first phase)

### Blocks

- Phase 2 (test reorganization depends on stable source structure)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Next Phase: Phase 2](phase-2.md)
- [Exploration](../../../explorations/code-structure-refactoring/)

---

**Last Updated:** 2026-01-07  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan code-structure-refactoring --expand --phase 1`
