# Code Structure Refactoring - Phase 2: Test Structure Reorganization

**Phase:** 2 - Test Structure Reorganization  
**Duration:** ~2 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** Phase 1 complete

---

## 📋 Overview

Reorganize flat test directory (24 files, 4312 lines) into structured subdirectories matching ecosystem patterns.

**Success Definition:** All tests organized into `unit/`, `integration/`, `commands/`, `create/` directories, pytest discovers all tests, coverage maintained.

---

## 🎯 Goals

1. **Create directory structure** - `unit/`, `integration/`, `commands/`, `create/`
2. **Organize by test type** - Unit vs integration separation
3. **Mirror source structure** - `commands/projects/` mirrors source
4. **Group create tests** - All 10 create mode tests in `create/`

---

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan code-structure-refactoring --expand --phase 2` to add detailed tasks.

### Task Categories

- [ ] **Task 1: Create Directories** - Set up `unit/`, `integration/`, `commands/`, `create/`
- [ ] **Task 2: Move Unit Tests** - Move 6 unit test files to `unit/`
- [ ] **Task 3: Move Integration Tests** - Move 3 integration test files to `integration/`
- [ ] **Task 4: Move Command Tests** - Move init, inventory tests to `commands/`
- [ ] **Task 5: Move Create Tests** - Move 10 create test files to `create/`
- [ ] **Task 6: Split Projects Tests** - Split `test_commands_projects.py` to mirror source
- [ ] **Task 7: Update Configuration** - Update pytest config if needed, verify discovery

---

## ✅ Completion Criteria

- [ ] All 24 test files moved to appropriate directories
- [ ] `test_commands_projects.py` split into `commands/projects/test_*.py`
- [ ] pytest discovers all tests
- [ ] All tests pass
- [ ] Coverage maintained at 97%
- [ ] No test import errors

---

## 📦 Deliverables

**Directory Structure:**

```
tests/
├── conftest.py
├── unit/                    # 6 files
├── integration/             # 3 files
├── commands/
│   ├── test_init.py
│   ├── test_inventory.py
│   └── projects/            # Split from test_commands_projects.py
│       ├── test_list.py
│       ├── test_crud.py
│       ├── test_create.py
│       └── test_import.py
└── create/                  # 10 files (renamed from test_create_*.py)
```

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

---

**Last Updated:** 2026-01-07  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan code-structure-refactoring --expand --phase 2`
