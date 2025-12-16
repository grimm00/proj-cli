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
- [ ] All existing `proj` commands work identically (list, get, create, update, delete, search, import)
- [ ] New `proj inv` subcommands functional (scan, analyze, dedupe, export)
- [x] Configuration via `~/.config/proj/config.yaml`
- [x] XDG directory compliance
- [ ] work-prod `scripts/project_cli/` removed
- [ ] work-prod README references new CLI package
- [x] Basic tests passing

---

## 📦 Functional Requirements

### Project Commands (Migrated from work-prod)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| List projects | `proj list` | 🔴 High | 🔴 Pending |
| Get project details | `proj get <id>` | 🔴 High | 🔴 Pending |
| Create project | `proj create` | 🔴 High | 🔴 Pending |
| Update project | `proj update <id>` | 🔴 High | 🔴 Pending |
| Delete project | `proj delete <id>` | 🔴 High | 🔴 Pending |
| Search projects | `proj search` | 🔴 High | 🔴 Pending |
| Import projects | `proj import` | 🔴 High | 🔴 Pending |

### Inventory Commands (New)

| Requirement | Command | Priority | Status |
|-------------|---------|----------|--------|
| Scan GitHub repos | `proj inv scan github` | 🔴 High | 🔴 Pending |
| Scan local dirs | `proj inv scan local` | 🔴 High | 🔴 Pending |
| Analyze tech stack | `proj inv analyze` | 🔴 High | 🔴 Pending |
| Deduplicate | `proj inv dedupe` | 🟡 Medium | 🔴 Pending |
| Export to JSON | `proj inv export json` | 🔴 High | 🔴 Pending |
| Export to API | `proj inv export api` | 🔴 High | 🔴 Pending |
| Show status | `proj inv status` | 🟡 Medium | 🔴 Pending |

### Configuration

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| Config file | `~/.config/proj/config.yaml` | 🔴 High | ✅ Done |
| Data directory | `~/.local/share/proj/` | 🔴 High | ✅ Done |
| Env override | `PROJ_*` variables | 🔴 High | ✅ Done |
| First-run setup | Create default config | 🟡 Medium | 🔴 Pending |

---

## 🏗️ Non-Functional Requirements

| Requirement | Description | Priority | Status |
|-------------|-------------|----------|--------|
| **NFR-1** | Typer CLI framework | 🔴 High | ✅ Done |
| **NFR-2** | Rich terminal output | 🟡 Medium | ✅ Done |
| **NFR-3** | Pydantic config validation | 🔴 High | ✅ Done |
| **NFR-4** | XDG directory compliance | 🔴 High | ✅ Done |
| **NFR-5** | Pip installable | 🔴 High | ✅ Done |
| **NFR-6** | Error handling | 🔴 High | 🔴 Pending |
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

---

### Phase 2: Migrate Project Commands (~3-4 hours)

**Goal:** Move existing `proj` commands to new CLI

- Migrate `scripts/project_cli/` code
- Convert argparse to Typer
- Migrate API client
- Test all existing commands

**Deliverables:**
- All `proj` commands working
- Feature parity with current CLI
- API client migrated

---

### Phase 3: Add Inventory Commands (~3-4 hours)

**Goal:** Add `proj inv` subcommand group

- Create inventory command group
- Wrap existing scripts as subcommands
- Add error handling
- Test inventory workflows

**Deliverables:**
- `proj inv scan github/local` working
- `proj inv analyze/dedupe` working
- `proj inv export json/api` working

---

### Phase 4: Polish & Cleanup (~2-3 hours)

**Goal:** Testing, documentation, work-prod cleanup

- Add tests
- First-run config creation
- Progress bars and colors
- Remove `scripts/project_cli/` from work-prod
- Update work-prod README

**Deliverables:**
- Tests passing
- Polish complete
- work-prod cleaned up

---

## 🚀 Next Steps

1. Create PR for Phase 1
2. Start Phase 2 implementation
3. Begin API client migration

---

## 📚 References

- [ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Repository Setup](phase-1.md)
- [Phase 2: Migrate Project Commands](phase-2.md)

---

**Last Updated:** 2025-12-16

