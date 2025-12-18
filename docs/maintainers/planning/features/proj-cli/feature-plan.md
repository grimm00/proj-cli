# proj-cli - Feature Plan

**Status:** 🟠 In Progress  
**Created:** 2025-12-16  
**Priority:** High  
**ADR:** [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

## 📋 Overview

Build a unified CLI tool (`proj`) that consolidates project management commands and inventory scanning into a single, professional Python package. This CLI will:

- **Unify** existing `proj` commands from work-prod with new inventory functionality
- **Live** in its own repository (`proj-cli`) separate from work-prod
- **Make** work-prod API-only (cleaner separation)
- **Use** modern Python tooling (Typer, Pydantic, XDG compliance)

### Key Decisions (from ADR-0007)

| Decision Point | Choice | Rationale |
|----------------|--------|-----------|
| **Command Name** | `proj` | Preserves existing muscle memory |
| **Framework** | Typer | Modern, type hints, minimal boilerplate |
| **Configuration** | YAML + Pydantic + XDG | Standard locations, type-safe |
| **Repository** | Separate (`proj-cli`) | API-only work-prod, independent CLI |

---

## 🎯 Success Criteria

- [x] `proj` command installable via `pip install .`
- [x] All existing `proj` commands work identically (list, get, create, update, delete, search, import)
- [x] New `proj inv` subcommands functional (scan, analyze, dedupe, export)
- [x] Configuration via `~/.config/proj/config.yaml`
- [x] XDG directory compliance
- [x] work-prod `scripts/project_cli/` removed ✅ (work-prod PR #38)
- [x] work-prod `scripts/inventory/` removed ✅ (work-prod PR #38)
- [x] work-prod README references new CLI package ✅ (work-prod PR #38)
- [x] Basic tests passing (73 tests)

---

## 📦 Functional Requirements

### Project Commands (Migrated from work-prod)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| List projects | `proj list` | 🔴 High | ✅ Done |
| Get project details | `proj get <id>` | 🔴 High | ✅ Done |
| Create project | `proj create` | 🔴 High | ✅ Done |
| Update project | `proj update <id>` | 🔴 High | ✅ Done |
| Delete project | `proj delete <id>` | 🔴 High | ✅ Done |
| Search projects | `proj search` | 🔴 High | ✅ Done |
| Import projects | `proj import-json` | 🔴 High | ✅ Done |
| Archive project | `proj archive <id>` | 🟡 Medium | ✅ Done |

### Inventory Commands (New)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| Scan GitHub repos | `proj inv scan github` | 🔴 High | ✅ Done |
| Scan local dirs | `proj inv scan local` | 🔴 High | ✅ Done |
| Analyze tech stack | `proj inv analyze` | 🔴 High | ✅ Done |
| Deduplicate | `proj inv dedupe` | 🟡 Medium | ✅ Done |
| Export to JSON | `proj inv export json` | 🔴 High | ✅ Done |
| Export to API | `proj inv export api` | 🔴 High | ✅ Done |
| Show status | `proj inv status` | 🟡 Medium | ✅ Done |

### Configuration

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| Config file | `~/.config/proj/config.yaml` | 🔴 High | ✅ Done |
| Data directory | `~/.local/share/proj/` | 🔴 High | ✅ Done |
| Env override | `PROJ_*` variables | 🔴 High | ✅ Done |
| First-run setup | `proj init` command | 🟡 Medium | ✅ Done |

---

## 🏗️ Non-Functional Requirements

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| **NFR-1** | Typer CLI framework | 🔴 High | ✅ Done |
| **NFR-2** | Rich terminal output | 🟡 Medium | ✅ Done |
| **NFR-3** | Pydantic config validation | 🔴 High | ✅ Done |
| **NFR-4** | XDG directory compliance | 🔴 High | ✅ Done |
| **NFR-5** | Pip installable | 🔴 High | ✅ Done |
| **NFR-6** | Error handling | 🔴 High | ✅ Done |
| **NFR-7** | Python 3.10+ | 🔴 High | ✅ Done |

---

## 📅 Implementation Phases

### Phase 1: Repository Setup (~2-3 hours) ✅ Complete

**Goal:** Create `proj-cli` repository with package structure

- Create repository via `dev-infra/new-project.sh`
- Create `src/proj/` package structure
- Add `pyproject.toml` with `proj` entry point
- Create Pydantic config with XDG paths
- Add requirements.txt

**Deliverables:**
- Working `proj --help` command
- Basic config loading
- Repository structure ready

**PR:** #1 (merged to develop)

---

### Phase 2: Migrate Project Commands (~3-4 hours) ✅ Complete

**Goal:** Move existing `proj` commands to new CLI

- Migrate `scripts/project_cli/` code
- Convert argparse to Typer
- Migrate API client
- Test all existing commands

**Deliverables:**
- All `proj` commands working (8 commands)
- Feature parity with current CLI
- API client migrated
- Error handling implemented

**PR:** #2 (merged to develop)

---

### Phase 3: Add Inventory Commands (~3-4 hours) ✅ Complete

**Goal:** Add `proj inv` subcommand group

- Create inventory command group
- Wrap existing scripts as subcommands
- Add error handling
- Test inventory workflows

**Deliverables:**
- `proj inv scan github/local` working
- `proj inv analyze/dedupe` working
- `proj inv export json/api` working
- `proj inv status` working

**PR:** #3 (merged to develop)

---

### Phase 4: Polish & Cleanup (~3-4 hours) 🟠 In Progress

**Goal:** Testing, documentation, work-prod cleanup

- Add comprehensive tests
- First-run config creation (`proj init`)
- Progress bars and colors
- Remove `scripts/project_cli/` from work-prod
- Update work-prod README

**Deliverables:**
- Tests passing (73 tests, 35% coverage)
- Polish complete
- work-prod cleaned up (separate PR)

**PR:** #5 (in progress)

---

### Fix Batch: Quick Wins ✅ Complete

**Goal:** Address deferred issues from Sourcery reviews

- Explicit encoding for file operations
- Brittle test assertions
- Version metadata consistency
- URL normalization
- Format option validation
- Defensive JSON parsing

**PR:** #4 (merged to develop)

---

## 🚀 Next Steps

1. ~~Create PR for Phase 1~~ ✅
2. ~~Start Phase 2 implementation~~ ✅
3. ~~Begin API client migration~~ ✅
4. ~~Implement inventory commands~~ ✅
5. ~~Address deferred fixes~~ ✅
6. **Create PR for Phase 4** ← Current
7. **Clean up work-prod** (separate PR after Phase 4)

---

## 📚 References

- [ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Repository Setup](phase-1.md)
- [Phase 2: Migrate Project Commands](phase-2.md)
- [Phase 3: Add Inventory Commands](phase-3.md)
- [Phase 4: Polish & Cleanup](phase-4.md)
- [Status and Next Steps](status-and-next-steps.md)
- [Migration Reference](migration-reference.md)

---

**Last Updated:** 2025-12-17

