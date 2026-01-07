# CHANGELOG Draft - v0.3.1

**Draft Created:** 2026-01-07
**Status:** 🔴 Draft - Needs Review

---

## [0.3.1] - 2026-01-07

### Changed

- **Centralized project type constants:** Created `constants.py` with `VALID_PROJECT_TYPES` and `PROJECT_TYPE_HELP` to avoid duplication (PR #23)
- **Custom exception for type validation:** Added `InvalidProjectTypeError` for safer error handling instead of catching all `ValueError` (PR #23)
- **Improved test assertions:** Strengthened invalid project type test with specific error format verification (PR #23)

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct (Added/Changed/Fixed/Removed)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing
- [ ] Ready to merge into CHANGELOG.md

---

**Ready for merge:** [ ] Yes / [x] No - Needs review

