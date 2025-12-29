# Project Type Support - Feature Hub

**Purpose:** Add `project_type` parameter support to proj-cli  
**Status:** 🟡 Ready to Start  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-29  
**Owner:** proj-cli  
**Dependency:** ✅ work-prod `project-type-field` complete (PR #42, 2025-12-29)

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

- **[work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)** - API implementation ✅ **COMPLETE** (PR #42, 2025-12-29)

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

## ✅ Dependency Satisfied

~~This feature **MUST** wait for work-prod to complete:~~
- ~~Phase 1: Schema Migration~~ ✅ PR #40 (2025-12-29)
- ~~Phase 2: Data Backfill~~ ✅ PR #41 (2025-12-29)
- ~~Phase 3: API Updates~~ ✅ PR #42 (2025-12-29)

**Status:** work-prod `project-type-field` feature is **COMPLETE**. This feature can now be implemented.

---

## 🚀 Next Steps

1. ~~Wait for work-prod `project-type-field` Phase 3 completion~~ ✅ **DONE**
2. Review transition plan
3. Begin Phase 1: Client Update
4. Use `/task-phase 1 --feature project-type-support` to implement Phase 1

---

## 📋 Handoff from work-prod

**Date:** 2025-12-29  
**From:** work-prod  
**To:** proj-cli

**work-prod Deliverables (Complete):**
- ✅ `project_type` enum column (Work, Personal, Learning, Inactive)
- ✅ GET `/api/projects?project_type=Work` filtering works
- ✅ Invalid `project_type` returns 400 with error message
- ✅ Response includes `project_type` field in all project objects
- ✅ OpenAPI spec updated (`backend/openapi.yaml`)

**API Contract:**
- **Endpoint:** `GET /api/projects`
- **Parameter:** `project_type` (optional, query string)
- **Valid Values:** `Work`, `Personal`, `Learning`, `Inactive` (case-sensitive)
- **Error:** 400 with `{"error": "Invalid project_type. Must be one of: ['Work', 'Personal', 'Learning', 'Inactive']"}`

**Reference:** [work-prod OpenAPI Spec](../../../../../work-prod/backend/openapi.yaml)

---

**Last Updated:** 2025-12-29

