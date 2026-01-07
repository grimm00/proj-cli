# Template Generation Extension - Transition Plan

**Feature:** Template Generation Extension  
**Status:** 🔴 Not Started  
**Created:** 2025-01-05  
**Source:** [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)  
**Type:** Feature

---

## 📋 Overview

This transition plan implements ADR-0008's decision to extend `proj create` with template generation capabilities from dev-infra. The implementation follows a phased approach to minimize risk while delivering incremental value.

### Source Documents

- **ADR:** [ADR-0008-template-generation-extension.md](../../decisions/ADR-0008-template-generation-extension.md)
- **Requirements:** [requirements.md](../../research/proj-cli-architecture/requirements.md)
- **Research:** [research-summary.md](../../research/proj-cli-architecture/research-summary.md)

### Key Decisions (from ADR-0008)

| Decision Point | Choice | Rationale |
|----------------|--------|-----------|
| **Command** | Extend `proj create` | Single mental model, backward compatible |
| **Default Mode** | Interactive | Matches new-project.sh UX |
| **Template Source** | Local path reference | Simple, offline, user has dev-infra |
| **Registry Location** | `~/.local/share/proj/registry.json` | XDG-compliant |
| **API Integration** | Config-driven, optional | Supports offline workflows |

---

## 🎯 Transition Goals

From ADR-0008 and requirements:

1. **Unified Workflow:** Single command for all project creation scenarios
2. **Interactive-First:** Default behavior matches `new-project.sh`
3. **Backward Compatible:** Existing `proj create` usage must work unchanged
4. **Offline Support:** Works without API when configured
5. **Local Tracking:** Registry enables future sync feature
6. **Config-Driven:** Behavior controlled by configuration

---

## ✅ Pre-Transition Checklist

- [x] ADR-0008 created and reviewed
- [x] Requirements documented (19 FR + 8 NFR)
- [x] Research completed and summarized
- [x] Phase structure defined
- [ ] Phase scaffolding expanded with TDD tasks
- [ ] Development environment ready

---

## 📅 Transition Phases

### Phase 1: Config Extension (~2 hours)

**Goal:** Extend configuration with template and registry settings

**Estimated Effort:** ~2 hours

**Prerequisites:**
- [x] proj-cli foundation (Phase 1-4 complete)
- [x] Pydantic settings framework in place

**Key Deliverables:**
- Updated `src/proj/config.py` with new fields
- Tests for config extension
- `proj init` handles new configuration

**Requirements Addressed:**
- FR-CONFIG-1: api_enabled toggle
- FR-CONFIG-2: templates.source path
- FR-CONFIG-3: registry.path setting
- FR-CONFIG-4: Environment overrides

**Definition of Done:**
- [ ] All config tests pass
- [ ] `proj init` creates valid config with new fields
- [ ] Environment variable overrides work

**Details:** [phase-1.md](phase-1.md)

---

### Phase 2: Local Registry (~2 hours)

**Goal:** Create local registry module for project tracking

**Estimated Effort:** ~2 hours

**Prerequisites:**
- [ ] Phase 1 complete (registry.path in config)

**Key Deliverables:**
- New `src/proj/registry.py` module
- Registry read/write functions
- Project lookup by path/name
- Tests for registry operations

**Requirements Addressed:**
- FR-REG-1: Project tracking
- FR-REG-2: Project path
- FR-REG-3: Template info
- FR-REG-4: API linkage
- NFR-REG-1: Human-readable (JSON)
- NFR-REG-2: XDG location

**Definition of Done:**
- [ ] Registry module tests pass
- [ ] Can add/remove/lookup projects
- [ ] Registry file is valid JSON
- [ ] XDG data directory used

**Details:** [phase-2.md](phase-2.md)

---

### Phase 3: Template Copying (~3 hours)

**Goal:** Port template operations from new-project.sh

**Estimated Effort:** ~3 hours

**Prerequisites:**
- [ ] Phase 1 complete (templates.source in config)

**Key Deliverables:**
- New `src/proj/templates.py` module
- Name validation logic
- Directory validation
- Template copying with hidden files
- Placeholder replacement
- Tests for template operations

**Requirements Addressed:**
- FR-TMPL-1: Local template source
- FR-TMPL-2: Template validation
- FR-TMPL-3: Template types (standard/learning)
- FR-PORT-1: Name validation
- FR-PORT-2: Directory validation
- FR-PORT-3: Template copying
- FR-PORT-4: Placeholder replacement
- NFR-TMPL-1: Offline operation
- NFR-TMPL-2: Clear errors

**Definition of Done:**
- [ ] Template module tests pass
- [ ] Can copy template to target directory
- [ ] Hidden files (.gitignore, .cursor/) included
- [ ] Placeholders replaced in README.md, start.txt
- [ ] Clear error messages for invalid paths

**Details:** [phase-3.md](phase-3.md)

---

### Phase 4: Create Command Extension (~3 hours)

**Goal:** Extend `proj create` with template modes

**Estimated Effort:** ~3 hours

**Prerequisites:**
- [ ] Phase 2 complete (registry module)
- [ ] Phase 3 complete (templates module)

**Key Deliverables:**
- Extended `proj create` command
- `--template` flag
- `--api-only` and `--local-only` flags
- Interactive prompts
- Integration with registry and templates
- Tests for all modes

**Requirements Addressed:**
- FR-CREATE-1: Interactive mode
- FR-CREATE-2: Template-based creation
- FR-CREATE-3: API-only mode
- FR-CREATE-4: Local-only mode
- FR-PORT-5: Git initialization
- FR-PORT-6: Interactive prompts
- FR-PORT-7: Non-interactive mode
- NFR-CREATE-1: Backward compatibility

**Definition of Done:**
- [ ] `proj create` interactive works
- [ ] `proj create --template standard` works
- [ ] `proj create --api-only` works (backward compat)
- [ ] `proj create --local-only` works
- [ ] Project registered in local registry
- [ ] All tests pass

**Details:** [phase-4.md](phase-4.md)

---

### Phase 5: Testing & Polish (~2 hours)

**Goal:** Comprehensive testing and documentation

**Estimated Effort:** ~2 hours

**Prerequisites:**
- [ ] Phase 4 complete (all functionality)

**Key Deliverables:**
- Integration tests for all create modes
- Documentation updates
- Manual testing complete
- Edge case coverage

**Requirements Addressed:**
- All NFR requirements verified
- Quality criteria met

**Definition of Done:**
- [ ] >80% test coverage
- [ ] README updated with new options
- [ ] Manual testing scenarios pass
- [ ] No linting errors
- [ ] PR ready for review

**Details:** [phase-5.md](phase-5.md)

---

## 📊 Requirements Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| FR-CREATE-1: Interactive mode | 4 | 🔴 |
| FR-CREATE-2: Template-based creation | 4 | 🔴 |
| FR-CREATE-3: API-only mode | 4 | 🔴 |
| FR-CREATE-4: Local-only mode | 4 | 🔴 |
| FR-CONFIG-1: api_enabled toggle | 1 | 🔴 |
| FR-CONFIG-2: templates.source path | 1 | 🔴 |
| FR-CONFIG-3: registry.path setting | 1 | 🔴 |
| FR-CONFIG-4: Environment overrides | 1 | 🔴 |
| FR-TMPL-1: Local template source | 3 | 🔴 |
| FR-TMPL-2: Template validation | 3 | 🔴 |
| FR-TMPL-3: Template types | 3 | 🔴 |
| FR-REG-1: Project tracking | 2 | 🔴 |
| FR-REG-2: Project path | 2 | 🔴 |
| FR-REG-3: Template info | 2 | 🔴 |
| FR-REG-4: API linkage | 2 | 🔴 |
| FR-PORT-1: Name validation | 3 | 🔴 |
| FR-PORT-2: Directory validation | 3 | 🔴 |
| FR-PORT-3: Template copying | 3 | 🔴 |
| FR-PORT-4: Placeholder replacement | 3 | 🔴 |
| FR-PORT-5: Git initialization | 4 | 🔴 |
| FR-PORT-6: Interactive prompts | 4 | 🔴 |
| FR-PORT-7: Non-interactive mode | 4 | 🔴 |
| NFR-CREATE-1: Backward compatibility | 4,5 | 🔴 |
| NFR-CONFIG-1: XDG registry location | 1,2 | 🔴 |
| NFR-CONFIG-2: YAML format | 1 | 🔴 |
| NFR-TMPL-1: Offline operation | 3 | 🔴 |
| NFR-TMPL-2: Clear errors | 3 | 🔴 |
| NFR-REG-1: Human-readable | 2 | 🔴 |
| NFR-REG-2: XDG location | 2 | 🔴 |
| NFR-PORT-1: Name sanitization | 3 | 🔴 |

---

## 🔄 Post-Transition

After all phases complete:

- [ ] All tests pass (>80% coverage)
- [ ] Documentation updated
- [ ] Feature complete and working
- [ ] Backward compatibility verified
- [ ] PR merged to develop

### Future Enhancements (Phase 2 - Deferred)

From ADR-0008:
- `proj sync` command - Sync template updates
- HTTP template download - Fetch from dev-infra releases
- GitHub repo creation - Auto-create repository

---

## 📚 Related Documents

- [Feature Hub](README.md) - Feature overview
- [Feature Plan](feature-plan.md) - Success criteria
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md) - Architecture decision
- [Requirements](../../research/proj-cli-architecture/requirements.md) - Full requirements

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Scaffolding  
**Next:** Expand Phase 1 with `/transition-plan template-generation --expand --phase 1`


