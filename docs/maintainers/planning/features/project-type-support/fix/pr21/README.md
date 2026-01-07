# Fix Tracking - PR #21 (Phase 1: Client Update)

**PR:** #21
**Phase:** Phase 1 - Client Update
**Merged:** 2026-01-07
**Status:** 🟡 Deferred Issues

---

## 📋 Deferred Issues

**Date:** 2026-01-07
**Review:** PR #21 (Phase 1) Sourcery feedback
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

### Individual Comments

| # | Description | Priority | Effort | Status |
|---|-------------|----------|--------|--------|
| #1 | Strengthen invalid-type test with error formatting assertion | 🟢 LOW | 🟢 LOW | Deferred |

### Overall Comments

| # | Description | Priority | Effort | Status |
|---|-------------|----------|--------|--------|
| Overall #1 | Centralize `VALID_PROJECT_TYPES` constant (avoid duplication) | 🟡 MEDIUM | 🟡 MEDIUM | Deferred |
| Overall #2 | Use custom exception for `project_type` validation | 🟡 MEDIUM | 🟡 MEDIUM | Deferred |

---

## 📝 Issue Details

### PR21-#1: Strengthen Invalid-Type Test

**Priority:** 🟢 LOW  
**Impact:** 🟢 LOW  
**Effort:** 🟢 LOW

**Description:** Test already asserts `ValueError` and message substring, but could also assert on Rich-formatted prefix (e.g., red `"Error:"`) to confirm specific `ValueError` handling.

**Action:** Deferred - test covers core behavior, formatting assertion is minor improvement.

---

### PR21-Overall-1: Centralize VALID_PROJECT_TYPES

**Priority:** 🟡 MEDIUM  
**Impact:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM

**Description:** The `VALID_PROJECT_TYPES` list is duplicated implicitly in CLI help text and error message. Consider using Enum or shared constant.

**Action:** Deferred - good suggestion for future refactoring. Can be addressed when adding new project types.

---

### PR21-Overall-2: Custom Exception for Project Type Validation

**Priority:** 🟡 MEDIUM  
**Impact:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM

**Description:** `list_projects` catches all `ValueError` exceptions; safer to use custom exception for `project_type` validation.

**Action:** Deferred - valid concern, can be addressed in future robustness improvement.

---

## 📊 Action Plan

These issues can be handled opportunistically:
- During Phase 2 integration testing
- In a future code quality PR
- When adding new project types

---

## 🔗 Related

- [Sourcery Review](../../../../../feedback/sourcery/pr21.md)
- [Phase 1](../../phase-1.md)
- [Feature Status](../../status-and-next-steps.md)

---

**Last Updated:** 2026-01-07

