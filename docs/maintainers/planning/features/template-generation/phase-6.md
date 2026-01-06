# Template Generation - Phase 6: API Sync Enhancement

**Phase:** 6 - API Sync Enhancement  
**Duration:** ~2-3 hours (estimated)  
**Status:** 🔴 Not Started  
**Prerequisites:** Phase 4 complete, Phase 5 Tasks 1-4 complete  
**Last Updated:** 2026-01-06

---

## 📋 Overview

Add API synchronization to template creation flow. Currently, `proj create --template` only creates locally and registers in the local registry. This phase adds the ability to also create a corresponding record in the work-prod API, linking local and remote records.

**Gap Identified:** Template creation doesn't sync to work-prod API - users must manually create API records or use separate commands.

**Success Definition:** Template creation can optionally sync to API, with graceful handling of offline/API-unavailable scenarios.

---

## 🎯 Goals

1. **API Integration:** Call work-prod API after successful template creation
2. **Registry Linking:** Store `work_prod_id` in local registry entry
3. **Graceful Degradation:** Handle API errors without failing local creation
4. **User Control:** Respect `--local-only` flag and `api_enabled` config

---

## 📝 Tasks

### Task 1: API Sync Implementation (TDD)

**Purpose:** Add API call to template creation flow.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Test: Template creation calls API when `api_enabled=True`
   - [ ] Test: Template creation skips API when `--local-only`
   - [ ] Test: Template creation skips API when `api_enabled=False`
   - [ ] Test: API failure doesn't prevent local creation
   - [ ] Test: `work_prod_id` stored in registry on success

2. **GREEN - Implement:**

   - [ ] Add API call after successful `create_from_template()`
   - [ ] Pass project info to `APIClient.create_project()`
   - [ ] Update registry entry with `work_prod_id`
   - [ ] Handle API errors gracefully (warn, don't fail)

3. **REFACTOR:**

   - [ ] Extract API sync logic to helper function
   - [ ] Ensure clean separation of concerns

**Checklist:**

- [ ] Tests written and passing
- [ ] API sync works when enabled
- [ ] Local-only mode skips API
- [ ] API errors handled gracefully
- [ ] Registry stores work_prod_id

---

### Task 2: Behavior Configuration

**Purpose:** Ensure behavior is intuitive and configurable.

**Implementation:**

1. **Default Behavior:**

   - [ ] If `api_enabled=True` (default): Sync to API
   - [ ] If `api_enabled=False`: Skip API (config-level disable)
   - [ ] If `--local-only`: Skip API (command-level override)

2. **Error Handling:**

   - [ ] API unreachable: Warn user, continue with local creation
   - [ ] API returns error: Warn user, continue with local creation
   - [ ] Show clear message about what was/wasn't synced

3. **Optional Enhancements:**

   - [ ] Consider `--offline` as alias for `--local-only` (more intuitive?)
   - [ ] Consider `--no-api` flag for explicit API skip

**Checklist:**

- [ ] Default behavior documented
- [ ] Error messages are clear
- [ ] User has control over sync behavior

---

### Task 3: Documentation & Testing Update

**Purpose:** Update docs and manual testing for new capability.

**Updates:**

1. **README.md:**

   - [ ] Document API sync behavior
   - [ ] Update create command options
   - [ ] Add examples showing sync vs local-only

2. **Manual Testing Guide:**

   - [ ] Add scenario: Template + API sync
   - [ ] Add scenario: Template + API offline/error
   - [ ] Update existing scenarios as needed

3. **Requirements:**

   - [ ] Add new requirements if needed
   - [ ] Update requirements.md

**Checklist:**

- [ ] README updated
- [ ] Manual testing guide updated
- [ ] Requirements documented

---

## ✅ Completion Criteria

- [ ] Template creation syncs to API by default (when enabled)
- [ ] `--local-only` skips API sync
- [ ] API errors don't break local creation
- [ ] `work_prod_id` stored in registry
- [ ] All tests passing
- [ ] Documentation updated
- [ ] PR reviewed and merged

---

## 📦 Deliverables

- Updated `src/proj/commands/projects.py` with API sync
- Updated `src/proj/registry.py` if needed
- New tests for API sync behavior
- Updated README.md
- Updated manual-testing.md

---

## 🔗 Dependencies

### Prerequisites

- Phase 4 complete (template creation working)
- Phase 5 Tasks 1-4 complete (bug fixes, coverage, docs, requirements)

### Blocks

- Phase 5 Tasks 5-6 (manual testing requires Phase 6 complete)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 5 - Testing & Polish](phase-5.md) (paused pending this phase)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2026-01-06  
**Status:** 🔴 Not Started  
**Next:** Expand with `/transition-plan --expand --phase 6` when ready

