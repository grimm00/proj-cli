# Project Type Support - Feature Hub

**Purpose:** Add `project_type` parameter support to proj-cli  
**Status:** 🔴 Not Started  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Owner:** proj-cli

---

## 📋 Quick Links

- **[Feature Plan](feature-plan.md)** - Feature overview and goals
- **[Transition Plan](transition-plan.md)** - Implementation transition plan
- **[Phase 1: Client Update](phase-1.md)** - API client and CLI changes
- **[Phase 2: Integration Testing](phase-2.md)** - Testing against work-prod API

### Related ADRs (dev-infra)

- **[ADR-001: Tier 1 API Validation](../../../../../dev-infra/admin/decisions/project-model-definition/adr-001-tier-1-api-validation.md)** - API readiness confirmed
- **[ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)** - Decision to add field

### Related work-prod Feature

- **[work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)** - API implementation (dependency)

---

## 🎯 Feature Overview

Update proj-cli to support filtering projects by `project_type` when work-prod implements the new field.

**Dependency:** This feature depends on work-prod completing the `project-type-field` feature first.

---

## 📊 Feature Status

| Phase | Name | Status | Effort |
|-------|------|--------|--------|
| Phase 1 | Client Update | 🔴 Not Started | ~2 hours |
| Phase 2 | Integration Testing | 🔴 Not Started | ~1 hour |

**Total Estimated Effort:** ~3 hours

---

## 🏢 Ownership

| Arm | Role | Responsibilities |
|-----|------|------------------|
| **work-prod** | API Provider | Implements `project_type` field and filtering |
| **proj-cli** | Consumer | Consumes `project_type` parameter in CLI |

---

## ⚠️ Dependency

This feature **MUST** wait for work-prod to complete:
- Phase 1: Schema Migration
- Phase 3: API Updates (specifically the query parameter)

**Recommended:** Start this feature after work-prod Phase 3 is complete.

---

## 🚀 Next Steps

1. Wait for work-prod `project-type-field` Phase 3 completion
2. Review transition plan
3. Begin Phase 1: Client Update
4. Use `/task-phase 1` to implement Phase 1

---

**Last Updated:** 2025-12-23

