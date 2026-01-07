# Project Type Support - Feature Plan

**Feature:** Add `project_type` parameter support
**Status:** ✅ Complete
**Completed:** 2026-01-07
**Created:** 2025-12-23
**Last Updated:** 2026-01-07
**Owner:** proj-cli
**Dependency:** ✅ Satisfied (work-prod PR #42, 2025-12-29)

---

## 📋 Overview

Update proj-cli to support filtering projects by the new `project_type` field in work-prod API.

**Problem Statement:**

The work-prod API is adding a `project_type` field (Work, Personal, Learning, Inactive) to enable filtering projects by type. proj-cli needs to support this new parameter to provide users with filtering capabilities.

**Solution:**

Add `--type` option to `proj list` command that passes `project_type` parameter to the API.

---

## 🎯 Success Criteria

- [x] API client supports `project_type` parameter ✅ (PR #21)
- [x] `proj list --type Work` filters to Work projects only ✅
- [x] `proj list --type Personal` filters to Personal projects only ✅
- [x] `proj list --type Learning` filters to Learning projects only ✅
- [x] `proj list --type Inactive` filters to Inactive projects only ✅
- [x] Invalid type values show helpful error message ✅
- [x] Project output includes `project_type` field ✅
- [x] All tests pass ✅

---

## 📅 Implementation Phases

### Phase 1: Client Update (~2 hours)

**Goal:** Add `project_type` support to API client and CLI

**Tasks:**

- Add `project_type` parameter to `list_projects()` in API client
- Add `--type` option to `proj list` command
- Update output formatting to show project_type
- Add unit tests

**Deliverables:**

- Updated `api_client.py`
- Updated `commands/projects.py`
- Unit tests

---

### Phase 2: Integration Testing (~1 hour)

**Goal:** Verify integration with work-prod API

**Tasks:**

- Test against running work-prod instance
- Verify filtering works correctly
- Update documentation

**Deliverables:**

- Integration tests passing
- Updated CLI documentation

---

## 📋 Requirements Addressed

| Requirement | Description                   | Phase   |
| ----------- | ----------------------------- | ------- |
| FR-2d       | API Filtering by Project Type | Phase 1 |
| NFR-1       | API Client Consistency        | Phase 1 |

---

## ✅ Dependencies

**Blocking Dependency:** ✅ **SATISFIED**

- ~~work-prod `project-type-field` Phase 3 must be complete~~ ✅ Complete (PR #42, 2025-12-29)

**API Ready:**

- `GET /api/projects?project_type=Work` filtering works
- Invalid values return 400 error
- OpenAPI spec updated

---

## ⚠️ Risks and Mitigations

| Risk                        | Impact           | Mitigation            |
| --------------------------- | ---------------- | --------------------- |
| ~~work-prod API not ready~~ | ~~Cannot test~~  | ✅ work-prod complete |
| API contract changes        | Breaking changes | Follow OpenAPI spec   |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)
- [work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)

---

**Last Updated:** 2025-12-29
