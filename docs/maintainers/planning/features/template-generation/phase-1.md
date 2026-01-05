# Template Generation - Phase 1: Config Extension

**Phase:** 1 - Config Extension  
**Duration:** ~2 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** proj-cli foundation complete (Phases 1-4)

---

## 📋 Overview

Extend the existing Pydantic configuration with new fields for template source, registry path, and API enablement toggle. This provides the foundation for subsequent phases.

**Success Definition:** Configuration supports all new fields with proper defaults and environment variable overrides.

---

## 🎯 Goals

1. **Add `api_enabled` boolean toggle** - Control whether API integration is active
2. **Add `TemplateConfig` nested model** - Configure template source and default type
3. **Add `RegistryConfig` nested model** - Configure registry location
4. **Add `default_project_dir` field** - Default location for new projects
5. **Update `proj init`** - Handle new configuration fields

---

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan template-generation --expand --phase 1` to add detailed TDD tasks.

### Task Categories

- [ ] **Config Model Extension** - Add new fields and nested models to Config class
- [ ] **Environment Variable Support** - Ensure PROJ_* overrides work for nested fields
- [ ] **Init Command Update** - Update `proj init` to create config with new fields
- [ ] **Validation** - Add validation for paths (expand ~, check existence)
- [ ] **Tests** - Write tests for all new configuration

---

## ✅ Completion Criteria

- [ ] `api_enabled` field works with default `True`
- [ ] `templates.source` and `templates.default` fields accessible
- [ ] `registry.path` field defaults to XDG data directory
- [ ] `default_project_dir` defaults to `~/Projects`
- [ ] Environment variables override: `PROJ_API_ENABLED`, `PROJ_TEMPLATES__SOURCE`
- [ ] `proj init` creates valid config with new fields
- [ ] All tests pass

---

## 📦 Deliverables

- Updated `src/proj/config.py` with new configuration fields
- Tests in `tests/test_config.py` for new fields
- Updated `proj init` command

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-CONFIG-1 | api_enabled toggle | 🔴 Pending |
| FR-CONFIG-2 | templates.source path | 🔴 Pending |
| FR-CONFIG-3 | registry.path setting | 🔴 Pending |
| FR-CONFIG-4 | Environment overrides | 🔴 Pending |
| NFR-CONFIG-1 | XDG registry location | 🔴 Pending |
| NFR-CONFIG-2 | YAML format maintained | 🔴 Pending |

---

## 🔗 Dependencies

### Prerequisites

- proj-cli foundation complete (existing `Config` class works)
- Pydantic settings framework in place

### Blocks

- Phase 2 (registry.path configuration)
- Phase 3 (templates.source configuration)
- Phase 4 (api_enabled toggle)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Next Phase: Phase 2 - Local Registry](phase-2.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan template-generation --expand --phase 1`


