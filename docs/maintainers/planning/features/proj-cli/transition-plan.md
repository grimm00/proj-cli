# Feature Transition Plan - proj-cli

**Feature:** Unified CLI Tool (`proj`)  
**Status:** 🟠 In Progress  
**Created:** 2025-12-16  
**Source:** [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)  
**Type:** Feature

---

## Overview

Build a unified CLI tool named `proj` as a proper Python package in a separate repository (`proj-cli`). This CLI consolidates:

- **Project management:** Existing `proj` commands (list, get, create, update, delete, search, import)
- **Inventory management:** New `proj inv` subcommands (scan, analyze, dedupe, export)

After migration, work-prod becomes **API-only**.

---

## Transition Goals

From ADR-0007 success criteria:

- [x] Single entry point CLI command (`proj`)
- [ ] All existing project commands migrated and working
- [ ] New inventory commands functional as subcommands
- [x] Configuration support (YAML + Pydantic + XDG)
- [x] Pip installable from local or GitHub
- [ ] work-prod becomes API-only

---

## Pre-Transition Checklist

- [x] ADR-0007 reviewed and approved ✅
- [x] Requirements document reviewed
- [x] `dev-infra` project template available
- [ ] work-prod API running (for testing)
- [ ] GitHub token available (for inventory scanning)

---

## Transition Steps

### Phase 1: Repository Setup ✅ Complete

**Goal:** Create `proj-cli` repository with package structure and basic Typer app.

**Estimated Effort:** ~2-3 hours

**Deliverables:**

- `proj --version` works ✅
- `proj --help` shows structure ✅
- Config loads from XDG paths ✅
- 13 tests passing ✅

---

### Phase 2: Migrate Project Commands

**Goal:** Move existing `proj` commands from work-prod to new CLI with Typer.

**Estimated Effort:** ~3-4 hours

**Tasks:**

1. Migrate API client
2. Create projects command group
3. Migrate all 7 project commands
4. Test all commands against work-prod API

**Definition of Done:**

- [ ] All 7 project commands functional
- [ ] Output matches current CLI
- [ ] API client works with configurable URL

---

### Phase 3: Add Inventory Commands

**Goal:** Add `proj inv` subcommand group wrapping inventory scripts.

**Estimated Effort:** ~3-4 hours

**Tasks:**

1. Create inventory command group
2. Implement scan commands (github, local)
3. Implement analysis commands (analyze, dedupe)
4. Implement export commands (json, api)

**Definition of Done:**

- [ ] `proj inv scan github/local` functional
- [ ] `proj inv analyze/dedupe` functional
- [ ] `proj inv export json/api` functional
- [ ] Basic error handling

---

### Phase 4: Polish & Cleanup

**Goal:** Testing, documentation, Rich UI, and work-prod cleanup.

**Estimated Effort:** ~2-3 hours

**Tasks:**

1. Add comprehensive tests
2. Add Rich UI enhancements
3. Implement first-run experience
4. Documentation
5. Work-prod cleanup

**Definition of Done:**

- [ ] Basic tests passing
- [ ] Rich UI enhancements in place
- [ ] work-prod `scripts/project_cli/` removed
- [ ] work-prod README updated
- [ ] proj-cli README complete

---

## Post-Transition

After all phases complete:

- [ ] `proj-cli` repository tagged with v0.1.0
- [ ] work-prod API-only (no CLI code)
- [ ] Documentation updated in both repos
- [ ] Announcement of new CLI location

---

## Definition of Done (Overall)

- [ ] All 4 phases complete
- [ ] All project commands migrated and working
- [ ] All inventory commands working
- [ ] Tests passing
- [ ] work-prod cleaned up
- [ ] Documentation complete

---

## Source Code Migration Map

| Source (work-prod) | Destination (proj-cli) |
|--------------------|------------------------|
| `scripts/project_cli/cli.py` | `src/proj/commands/projects.py` |
| `scripts/project_cli/api_client.py` | `src/proj/api_client.py` |
| `scripts/project_cli/commands/*.py` | `src/proj/commands/projects.py` |
| `scripts/inventory/fetch-github-repos.sh` | `src/proj/scanners/github.py` |
| `scripts/inventory/scan-local-projects.sh` | `src/proj/scanners/local.py` |
| `scripts/inventory/analyze-tech-stack.py` | `src/proj/commands/inventory.py` |
| `scripts/inventory/classify-projects.py` | `src/proj/commands/inventory.py` |
| `scripts/inventory/deduplicate-projects.py` | `src/proj/commands/inventory.py` |
| `scripts/map_inventory_to_projects.py` | `src/proj/commands/inventory.py` |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API changes during migration | Low | Medium | Test against stable API |
| Shell script compatibility | Medium | Low | Keep scripts, wrap with subprocess |
| Config migration confusion | Low | Low | Document migration path |

---

## References

- [Feature Plan](feature-plan.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)
- [Phase 1: Repository Setup](phase-1.md)
- [Phase 2: Migrate Project Commands](phase-2.md)
- [Phase 3: Add Inventory Commands](phase-3.md)
- [Phase 4: Polish & Cleanup](phase-4.md)

---

**Last Updated:** 2025-12-16

