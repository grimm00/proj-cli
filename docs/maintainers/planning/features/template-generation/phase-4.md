# Template Generation - Phase 4: Create Command Extension

**Phase:** 4 - Create Command Extension  
**Duration:** ~3 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** Phase 2 (registry) and Phase 3 (templates) complete

---

## 📋 Overview

Extend the existing `proj create` command with template modes, interactive prompts, and integration with the registry and templates modules. This is the user-facing integration phase.

**Success Definition:** `proj create` works in all modes (interactive, template, api-only, local-only) with proper backward compatibility.

---

## 🎯 Goals

1. **Add `--template` flag** - Create project from specified template
2. **Add `--api-only` flag** - Preserve current behavior (backward compat)
3. **Add `--local-only` flag** - Work without API connectivity
4. **Implement interactive mode** - Default behavior with prompts
5. **Integrate registry** - Register created projects automatically
6. **Integrate templates** - Use templates module for project creation
7. **Support git initialization** - Optional git init for new projects

---

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan template-generation --expand --phase 4` to add detailed TDD tasks.

### Task Categories

- [ ] **Command Flags** - Add new flags to create command
- [ ] **Interactive Mode** - Implement Rich prompts for all inputs
- [ ] **Template Mode** - Wire up template copying integration
- [ ] **API-Only Mode** - Preserve existing behavior
- [ ] **Local-Only Mode** - Work without API when configured
- [ ] **Registry Integration** - Register projects after creation
- [ ] **Git Integration** - Optional git init with --no-git flag
- [ ] **Tests** - Integration tests for all modes

---

## ✅ Completion Criteria

- [ ] `proj create` (no args) launches interactive mode
- [ ] `proj create my-app --template standard` creates from template
- [ ] `proj create "My App" --api-only` works (backward compat)
- [ ] `proj create my-app --local-only` works without API
- [ ] `proj create my-app --dry-run` previews without creating
- [ ] Projects automatically registered in local registry
- [ ] Git initialized by default (--no-git to skip)
- [ ] All modes work correctly
- [ ] Backward compatibility verified
- [ ] All tests pass

---

## 📦 Deliverables

- Extended `src/proj/commands/projects.py` create command
- New integration tests for all create modes
- Updated `proj --help` documentation

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-CREATE-1 | Interactive mode (default) | 🔴 Pending |
| FR-CREATE-2 | Template-based creation | 🔴 Pending |
| FR-CREATE-3 | API-only mode | 🔴 Pending |
| FR-CREATE-4 | Local-only mode | 🔴 Pending |
| FR-PORT-5 | Git initialization | 🔴 Pending |
| FR-PORT-6 | Interactive prompts | 🔴 Pending |
| FR-PORT-7 | Non-interactive mode | 🔴 Pending |
| NFR-CREATE-1 | Backward compatibility | 🔴 Pending |

---

## 📄 Command Usage (from ADR-0008)

```bash
# Interactive mode (default) - prompts for all options
proj create

# Non-interactive with template
proj create my-app --template standard

# Full non-interactive (for CI/scripts)
proj create my-app \
  --template standard \
  --desc "My app" \
  --target-dir ~/Projects \
  --no-git \
  --register

# API-only mode (backward compatible)
proj create "My Application" --api-only

# Local-only mode (offline)
proj create my-app --template standard --local-only

# Dry-run to preview
proj create my-app --template standard --dry-run
```

---

## 🔗 Dependencies

### Prerequisites

- Phase 2 complete (registry module)
- Phase 3 complete (templates module)

### Blocks

- Phase 5 (integration testing)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 3 - Template Copying](phase-3.md)
- [Next Phase: Phase 5 - Testing & Polish](phase-5.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan template-generation --expand --phase 4`


