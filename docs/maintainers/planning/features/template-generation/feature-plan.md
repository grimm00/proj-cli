# Template Generation Extension - Feature Plan

**Feature:** Extend proj create with template generation  
**Status:** 🔴 Not Started  
**Created:** 2025-01-05  
**Priority:** High  
**ADR:** [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

## 📋 Overview

Extend the existing `proj create` command to support project creation from dev-infra templates. This unifies the workflow that currently requires two separate tools:

1. **Current:** `proj create "Name"` - Creates API record only
2. **Current:** `dev-infra/scripts/new-project.sh` - Creates project directory

**After this feature:** `proj create` handles both API records AND template-based project creation with a single, interactive command.

### Context

- proj-cli (ADR-0007) provides unified CLI for project and inventory management
- dev-infra's `new-project.sh` is interactive and creates project directories
- No current tracking of template-created projects
- Users expect "create" to create projects (not just records)

---

## 🎯 Success Criteria

### Core Functionality

- [ ] `proj create` works interactively by default
- [ ] `proj create --template <type>` creates project from template
- [ ] `proj create --api-only` preserves current behavior
- [ ] `proj create --local-only` works without API
- [ ] Projects tracked in local registry

### Configuration

- [ ] `api_enabled` toggle in config
- [ ] `templates.source` path setting
- [ ] `registry.path` configurable
- [ ] Environment variable overrides work

### Quality

- [ ] All tests pass (>80% coverage)
- [ ] Backward compatible with existing `proj create` usage
- [ ] Documentation updated

---

## 📊 Requirements Coverage

### Functional Requirements (19 total)

| Category | Count | Status |
|----------|-------|--------|
| Command (CREATE-1 to CREATE-4) | 4 | 🔴 Pending |
| Config (CONFIG-1 to CONFIG-4) | 4 | 🔴 Pending |
| Template (TMPL-1 to TMPL-3) | 3 | 🔴 Pending |
| Registry (REG-1 to REG-4) | 4 | 🔴 Pending |
| Port (PORT-1 to PORT-7) | 4 | 🔴 Pending |

### Non-Functional Requirements (8 total)

| Requirement | Priority | Status |
|-------------|----------|--------|
| NFR-CREATE-1: Backward compatibility | High | 🔴 Pending |
| NFR-CONFIG-1: XDG registry location | Medium | 🔴 Pending |
| NFR-CONFIG-2: YAML format | Medium | 🔴 Pending |
| NFR-TMPL-1: Offline operation | High | 🔴 Pending |
| NFR-TMPL-2: Clear errors | Medium | 🔴 Pending |
| NFR-REG-1: Human-readable | Medium | 🔴 Pending |
| NFR-REG-2: XDG location | Medium | 🔴 Pending |
| NFR-PORT-1: Name sanitization | Low | 🔴 Pending |

**Full Requirements:** [requirements.md](../../research/proj-cli-architecture/requirements.md)

---

## 📅 Implementation Phases

### Phase 1: Config Extension (~2 hours)

**Goal:** Extend configuration with template and registry settings

**Tasks:**
- Add `api_enabled` field to Config
- Add `TemplateConfig` nested model
- Add `RegistryConfig` nested model  
- Add `default_project_dir` field
- Update `proj init` to handle new fields

**Requirements:** FR-CONFIG-1 to FR-CONFIG-4

**Details:** [phase-1.md](phase-1.md)

---

### Phase 2: Local Registry (~2 hours)

**Goal:** Create local registry module for project tracking

**Tasks:**
- Create `src/proj/registry.py` module
- Implement read/write functions
- Implement project lookup by path/name
- Handle registry creation on first use

**Requirements:** FR-REG-1 to FR-REG-4, NFR-REG-1, NFR-REG-2

**Details:** [phase-2.md](phase-2.md)

---

### Phase 3: Template Copying (~3 hours)

**Goal:** Port template operations from new-project.sh

**Tasks:**
- Create `src/proj/templates.py` module
- Port validation logic from new-project.sh
- Implement template copying with hidden files
- Implement placeholder replacement

**Requirements:** FR-TMPL-1 to FR-TMPL-3, FR-PORT-1 to FR-PORT-4

**Details:** [phase-3.md](phase-3.md)

---

### Phase 4: Create Command Extension (~3 hours)

**Goal:** Extend `proj create` with template modes

**Tasks:**
- Add `--template` flag to create command
- Add `--api-only` and `--local-only` flags
- Implement interactive prompts
- Wire up template + registry integration

**Requirements:** FR-CREATE-1 to FR-CREATE-4, FR-PORT-5 to FR-PORT-7

**Details:** [phase-4.md](phase-4.md)

---

### Phase 5: Testing & Polish (~2 hours)

**Goal:** Comprehensive testing and documentation

**Tasks:**
- Unit tests for new modules
- Integration tests for create modes
- Update documentation
- Manual testing

**Requirements:** All NFR requirements, quality criteria

**Details:** [phase-5.md](phase-5.md)

---

## 🚀 Next Steps

1. **Expand Phase 1** - Run `/transition-plan template-generation --expand --phase 1`
2. **Implement Phase 1** - Use `/task-phase` with TDD workflow
3. **Create PR** - Use `/pr --phase 1` after implementation

---

## 📚 Related Documents

- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md) - Architecture decision
- [Requirements](../../research/proj-cli-architecture/requirements.md) - Full requirements
- [Research Summary](../../research/proj-cli-architecture/research-summary.md) - Research findings
- [Exploration](../../explorations/proj-cli-architecture/exploration.md) - Initial design exploration

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Planning  
**Next:** Expand Phase 1 scaffolding


