# proj-cli - Feature Hub

**Feature:** Unified CLI Tool for Project and Inventory Management  
**Status:** 🟠 In Progress  
**Created:** 2025-12-16  
**Repository:** https://github.com/grimm00/proj-cli

---

## 📋 Quick Links

### Phase Documents

- **[Phase 1: Repository Setup](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/phase-1.md)** - ✅ Complete (2025-12-16)
- **[Phase 2: Migrate Project Commands](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/phase-2.md)** - 🔴 Not Started
- **[Phase 3: Add Inventory Commands](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/phase-3.md)** - 🔴 Not Started
- **[Phase 4: Polish & Cleanup](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/phase-4.md)** - 🔴 Not Started

### Supporting Documents

- **[Feature Plan](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/feature-plan.md)** - Requirements and success criteria
- **[Status & Next Steps](status-and-next-steps.md)** - Current progress tracking
- **[Transition Plan](../../../../../../work-prod/docs/maintainers/planning/features/proj-cli/transition-plan.md)** - Migration strategy
- **[ADR-0007](../../../../../../work-prod/docs/maintainers/decisions/ADR-0007-inventory-system-cli-tool-architecture.md)** - Architecture decision

### Fix Documentation

- **[Fix Hub](fix/README.md)** - Troubleshooting and issue tracking

---

## 🎯 Overview

The `proj-cli` is a unified CLI tool that provides:

1. **Project Management** - Commands to interact with the work-prod API
2. **Inventory Scanning** - Commands to scan GitHub repos and local directories
3. **Unified Interface** - Single `proj` command for all functionality

### Target Commands

```bash
# Project commands (migrating from work-prod)
proj list            # List projects
proj get <id>        # Get project details
proj create          # Create new project
proj update <id>     # Update project
proj delete <id>     # Delete project
proj search          # Search projects
proj import          # Import from JSON

# Inventory commands (new)
proj inv scan github     # Scan GitHub repos
proj inv scan local      # Scan local directories
proj inv export api      # Push to work-prod API
```

---

## 📊 Progress Summary

| Phase | Focus | Effort | Status |
|-------|-------|--------|--------|
| 1 | Repository Setup | ~2-3 hrs | ✅ Complete |
| 2 | Migrate Project Commands | ~3-4 hrs | 🔴 Not Started |
| 3 | Add Inventory Commands | ~3-4 hrs | 🔴 Not Started |
| 4 | Polish & Cleanup | ~2-3 hrs | 🔴 Not Started |
| **Total** | | **~10-14 hrs** | **25%** |

---

## ✅ Phase 1 Complete (2025-12-16)

### Deliverables

| Item | Status |
|------|--------|
| Package structure (`src/proj/`) | ✅ |
| Typer CLI framework | ✅ |
| Pydantic configuration | ✅ |
| XDG compliance | ✅ |
| 13 tests passing | ✅ |
| `proj --version` | ✅ |
| `proj --help` | ✅ |

### Verification Results

```bash
$ proj --version
proj version 0.1.0

$ proj --help
Usage: proj [OPTIONS] COMMAND [ARGS]...

Unified CLI for project and inventory management.

$ python -c "from proj.config import get_config_dir, get_data_dir; print(get_config_dir()); print(get_data_dir())"
/Users/cdwilson/.config/proj
/Users/cdwilson/.local/share/proj
```

---

## 🚀 Next Steps

1. **Create PR for Phase 1:** Merge `feat/phase-1-cli-setup` to `main`
2. **Run `/pre-phase-review 2`:** Review Phase 2 before starting
3. **Start Phase 2:** `/task-phase 2 1` - Begin API client implementation

---

## 📚 Related Projects

### work-prod Repository

The `proj-cli` is being extracted from `work-prod`, which will become API-only after migration:

- **Repository:** https://github.com/grimm00/work-prod
- **Planning Hub:** `~/Projects/work-prod/docs/maintainers/planning/features/proj-cli/`
- **Current State:** Backend MVP complete (v0.1.0)

### Migration Strategy

1. **Phase 2:** Migrate existing `proj` commands from `work-prod/scripts/project_cli/`
2. **Phase 4:** Remove CLI code from `work-prod`, making it API-only

---

**Last Updated:** 2025-12-16  
**Branch:** `feat/phase-1-cli-setup`

