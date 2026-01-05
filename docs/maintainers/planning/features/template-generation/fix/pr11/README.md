# PR #11 Fix Tracking - Phase 3: Template Copying

**PR:** #11  
**Phase:** Phase 3: Template Copying  
**Date:** 2026-01-05  
**Status:** 🟡 Deferred Issues

---

## 📋 Overview

PR #11 implemented Phase 3 (Template Copying) with all 8 TDD tasks. Sourcery review found 5 comments, 1 was fixed before merge, 4 are deferred.

---

## 📊 Issue Summary

| Total | Fixed | Deferred | CRITICAL/HIGH | MEDIUM | LOW |
|-------|-------|----------|---------------|--------|-----|
| 5 | 1 | 4 | 0 | 1 | 3 |

---

## 📋 Deferred Issues

**Date:** 2026-01-05  
**Review:** PR #11 (Phase 3) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All LOW/MEDIUM priority, can be handled opportunistically

### Deferred Issues:

- **PR11-#1:** Add whitespace strip test (LOW priority, LOW effort)
  - Location: `tests/test_templates.py:42-47`
  - Description: Add test for `validate_project_name` to verify whitespace stripping
  - Action: Opportunistic handling in future PR

- **PR11-#2:** Add non-writable directory test (MEDIUM priority, LOW effort)
  - Location: `tests/test_templates.py:192-194`
  - Description: Add test for `DirectoryNotWritableError` path coverage
  - Action: Opportunistic handling in future PR

- **PR11-#3:** Strengthen default description test (LOW priority, LOW effort)
  - Location: `tests/test_templates.py:463-401`
  - Description: Assert actual replacement value in default description test
  - Action: Opportunistic handling in future PR

- **PR11-#4:** Add ProjectExistsError test for create_from_template (LOW priority, LOW effort)
  - Location: `tests/test_templates.py:545-502`
  - Description: Add test to verify `create_from_template` surfaces `ProjectExistsError`
  - Action: Opportunistic handling in future PR

### Fixed Before Merge:

- **PR11-#5:** Progress table out of sync (MEDIUM priority, LOW effort) ✅
  - Location: `phase-3.md:1373-1382`
  - Description: Progress tracking table showed tasks as "Not Started" when complete
  - Action: Fixed in PR #11 before merge

---

## 📋 Action Plan

These issues are all test improvements (LOW/MEDIUM priority, LOW effort). They can be:
- Handled opportunistically during future phases
- Bundled into a dedicated test improvement PR
- Added to cross-PR batch if similar issues accumulate

---

## 📚 Quick Links

- [Sourcery Review PR #11](../../../../feedback/sourcery/pr11.md)
- [Phase 3 Document](../../phase-3.md)
- [Fix Hub](../README.md)

---

**Last Updated:** 2026-01-05  
**Status:** 🟡 Deferred  
**Next:** Handle opportunistically or in future test improvement batch

