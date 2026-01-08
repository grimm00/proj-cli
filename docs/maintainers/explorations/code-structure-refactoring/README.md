# Code Structure Refactoring - Exploration Hub

**Purpose:** Standardize code organization - split large modules and organize tests  
**Status:** 🟡 Ready for Implementation  
**Created:** 2025-01-05  
**Last Updated:** 2026-01-07

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Research, options, and decisions
- **[Research Topics](research-topics.md)** - Research questions (some deferred)
- **[Implementation Plan](implementation-plan.md)** - Concrete PR plan for v0.4.0

---

## 🎯 Overview

This exploration examines how to improve code organization in proj-cli:

1. **Source Code** - Split `projects.py` (943 lines) into focused modules
2. **Tests** - Reorganize flat test structure (24 files) into subdirectories

### Why Now?

- `projects.py` at 943 lines is hard to navigate and maintain
- Test structure doesn't match sibling projects (dev-infra, work-prod)
- Work-prod integration will add more complexity - better to refactor first
- ~4-5 hours effort, low risk

---

## 📊 Status

| Phase | Status |
|-------|--------|
| Exploration | ✅ Complete |
| Research | 🟡 Partial (enough to proceed) |
| Decision | ✅ Option B selected (subdirectories) |
| Implementation | 🔴 Not Started |

**Next Step:** Begin implementation with PR #1 (create `projects/` package)

---

## 🎯 Decision Summary

**Source Code:** Convert `projects.py` to `projects/` package with 5 modules

**Tests:** Adopt subdirectory structure matching ecosystem:
- `unit/` - Mocked tests
- `integration/` - Real interaction tests  
- `commands/` - Command-specific tests (mirrors source)
- `create/` - Detailed create mode tests

**Rationale:** See [exploration.md](exploration.md) Option B analysis

---

## 📁 Target Structures

### Source (Part 1)

```
src/proj/commands/projects/
├── __init__.py      # Re-exports
├── helpers.py       # Shared utilities
├── list.py          # list, search
├── crud.py          # get, update, delete, archive
├── create.py        # create (all modes)
└── import_export.py # import_json
```

### Tests (Part 2)

```
tests/
├── unit/            # Mocked tests
├── integration/     # Real interaction tests
├── commands/        # Command tests
│   └── projects/    # Mirrors source
└── create/          # Create mode tests
```

---

## 🔗 Related

- **[Work-Prod Integration](../work-prod-integration/)** - Will benefit from cleaner structure
- **Original Proposal:** `tmp/refactor-projects-module.md`

---

**Last Updated:** 2026-01-07
