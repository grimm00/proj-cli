# PR #31 Fix Tracking - expected_skills Validation

**PR:** #31 — `feat(skill-template-separation): expected_skills warn-not-error validation`  
**Feature:** Template Generation Extension (cross-project ADR-001 companion)  
**Review:** Sourcery (3 comments: 1 individual + 2 overall)  
**Last Updated:** 2026-06-09  
**Status:** 🟠 Partial (2/3 fixed in-line, 1 deferred)

---

## 📋 Review Summary

| Comment | Priority | Impact | Effort | Status |
|---------|----------|--------|--------|--------|
| #1 — empty `skill_roots` falsy bug | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | ✅ Fixed in-line (`ff362d4`) |
| Overall-1 — catch `yaml.YAMLError` | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | ✅ Fixed in-line (`ff362d4`) |
| Overall-2 — double-read `.dev-infra.yml` | 🟢 LOW | 🟢 LOW | 🟢 LOW | ⏸️ Deferred |

---

## 📋 Deferred Issues

**Date:** 2026-06-09  
**Review:** PR #31 Sourcery feedback  
**Status:** 🟢 **1 LOW deferred** — cosmetic optimization, no user impact

### PR31-Overall-2: Avoid double-read of `.dev-infra.yml`

- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟢 LOW
- **Location:** `src/proj/skills.py` — `warn_missing_expected_skills` function
- **Description:** `warn_missing_expected_skills` calls `load_expected_skills` directly (line 72) and then `find_missing_skills` (line 76) which calls `load_expected_skills` again internally. The manifest file is read and parsed twice per invocation. Refactor to pass the already-loaded list into `find_missing_skills` or inline the logic.
- **Action:** Deferred — cosmetic. File is tiny YAML. No measurable user impact.

---

**Last Updated:** 2026-06-09
