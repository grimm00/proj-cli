# proj-cli - Status and Next Steps

**Feature:** Unified CLI Tool  
**Status:** 🟠 In Progress  
**Current Phase:** Phase 2 - Migrate Project Commands (PR #2 Open)  
**Last Updated:** 2025-12-17

---

## 📊 Current Status

| Phase | Focus | Effort | Status |
|-------|-------|--------|--------|
| 1 | Repository Setup | ~2-3 hrs | ✅ Complete (PR #1) |
| 2 | Migrate Project Commands | ~4-5 hrs | ✅ Complete (PR #2 Open) |
| 3 | Add Inventory Commands | ~3-4 hrs | 🔴 Not Started |
| 4 | Polish & Cleanup | ~2-3 hrs | 🔴 Not Started |
| **Total** | | **~10-14 hrs** | **50%** |

---

## ✅ Completed

### Phase 1: Repository Setup ✅ (PR #1, 2025-12-17)

- **Package structure:** `src/proj/` layout
- **CLI framework:** Typer with Rich output
- **Configuration:** Pydantic + XDG compliance
- **Tests:** 13 tests passing (package, config, CLI)
- **Commands:** `proj --version`, `proj --help`
- **Documentation:** Clean up template, migration reference doc
- **Review:** Sourcery review completed, 2 HIGH items fixed, 6 items deferred to Phase 4

**Merged via PR #1** (2025-12-17)

---

## 🟠 In Progress

### Phase 2: Migrate Project Commands ✅ (PR #2 Open, 2025-12-17)

- **Error handler:** `src/proj/error_handler.py` migrated
- **API client:** `src/proj/api_client.py` migrated
- **Project commands:** 8 commands implemented (list, get, create, update, delete, search, import-json, archive)
- **Tests:** 38 tests passing
- **Review:** Sourcery review completed, 1 HIGH item fixed, 4 items deferred to Phase 4
- **PR #2:** Open, targeting `develop`

---

## 🔜 Next Steps

### Immediate

1. **Merge PR #2:**
   - Approve and merge PR #2 to `develop`
   - Run `/post-pr 2 --phase 2` after merge

2. **Start Phase 3:**
   ```
   /pre-phase-review 3
   /task-phase 3 1
   ```

### Phase 3 Key Tasks

1. Create inventory commands (`src/proj/commands/inventory.py`)
2. Implement scan command for GitHub repos
3. Implement scan command for local directories
4. Add export functionality
5. Write tests for inventory commands

### Deferred from Phase 1 & 2 (to Phase 4)

**From PR #1 (Phase 1):**
See [PR #1 Sourcery Review](../../feedback/sourcery/pr1.md) for details:
- #1: Add explicit encoding for config file
- #3: Fix brittle return code test
- #4-6: Test coverage improvements
- #7: Version metadata test

**From PR #2 (Phase 2):**
See [PR #2 Sourcery Review](../../feedback/sourcery/pr2.md) for details:
- #2: Add CliRunner tests for actual command behavior
- API URL validation in APIClient constructor
- Format option validation with typer.Choice
- URL building helper extraction

---

## 📋 Requirements Checklist

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1 | Single entry point (`proj`) | 🔴 High | ✅ Done |
| FR-2 | Project commands (list, get, create, etc.) | 🔴 High | ✅ Done |
| FR-3 | Scan commands | 🔴 High | 🔴 Pending |
| FR-4 | Export commands | 🔴 High | 🔴 Pending |
| FR-5 | Config file support | 🔴 High | ✅ Done |
| FR-6 | Environment overrides | 🔴 High | ✅ Done |

### Non-Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| NFR-1 | Typer framework | 🔴 High | ✅ Done |
| NFR-2 | Rich terminal output | 🟡 Medium | ✅ Done |
| NFR-3 | Pydantic validation | 🔴 High | ✅ Done |
| NFR-4 | XDG compliance | 🔴 High | ✅ Done |
| NFR-5 | Pip installable | 🔴 High | ✅ Done |
| NFR-6 | Error handling | 🔴 High | ✅ Done |

---

## 🎯 Success Criteria

- [x] `proj` command installable via `pip install .`
- [x] All existing `proj` commands work (list, get, create, update, delete, search, import-json, archive)
- [ ] New `proj inv` subcommands functional
- [x] Configuration via `~/.config/proj/config.yaml`
- [x] XDG directory compliance
- [ ] work-prod `scripts/project_cli/` removed
- [x] Basic tests passing

---

## 📚 References

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Transition Plan](transition-plan.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-16

