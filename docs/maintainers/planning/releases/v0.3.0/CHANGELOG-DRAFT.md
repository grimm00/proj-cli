# CHANGELOG Draft - v0.3.0

**Draft Created:** 2026-01-07
**Status:** 🔴 Draft - Needs Review

---

## [0.3.0] - YYYY-MM-DD

### Added

- **Project Type Filtering:** Filter projects by type using `proj list --type` (PR #21)
  - `--type Work` - Show only Work projects
  - `--type Personal` - Show only Personal projects
  - `--type Learning` - Show only Learning projects
  - `--type Inactive` - Show only Inactive projects

- **Combined Filters:** Type filtering works with other filters (PR #21)
  - Type + classification: `proj list --type Work --class primary`
  - Type + search: `proj list --type Personal --search "python"`

- **Type Column:** Project type shown in table output (PR #21)

- **Documentation:** Added "Filtering Projects" section to README

### Changed

- **Error Messages:** Invalid type values show clear error with list of valid options

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct (Added/Changed/Fixed/Removed)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing
- [ ] Ready to merge into CHANGELOG.md

---

**Ready for merge:** [ ] Yes / [x] No - Needs review

