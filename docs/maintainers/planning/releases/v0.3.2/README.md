# Release v0.3.2 - Code Structure Refactoring

**Version:** v0.3.2  
**Status:** 🔴 Draft  
**Target Date:** 2026-01-08  
**Created:** 2026-01-08  
**Source:** Code Structure Refactoring feature + BUG-001 fix  
**Type:** Patch Release

---

## 📋 Quick Links

- **[Release Checklist](checklist.md)** - Release preparation checklist
- **[Release Notes](release-notes.md)** - Release notes and changelog
- **[CHANGELOG Draft](CHANGELOG-DRAFT.md)** - CHANGELOG entry draft

---

## 📊 Release Summary

**Version:** v0.3.2  
**Target Date:** 2026-01-08  
**Status:** 🔴 Draft

**Key Changes:**

- **Code Refactoring:** Split `projects.py` (943 lines) into focused modules
- **Test Reorganization:** Hierarchical test structure (`unit/`, `integration/`, `commands/`, `create/`)
- **Bug Fix:** Fixed blank "path" field in inventory export (BUG-001)
- **Code Quality:** Removed dead code, added test helper, improved test coverage

**Development:**

- PRs: 5 total (#25, #26, #27, #28, #29) + 1 direct fix
- Phases: 2 (Code Structure Refactoring)
- Source: Code Structure Refactoring exploration

---

## ✅ Release Checklist Status

**Pre-Release:**

- [ ] All tests passing
- [ ] Test coverage maintained
- [ ] 0 linting errors
- [ ] Documentation reviewed
- [ ] Release checklist complete
- [ ] Release notes prepared

**Release:**

- [ ] Version bumped in pyproject.toml
- [ ] Version bumped in `__init__.py`
- [ ] Version tagged in git
- [ ] Release notes finalized
- [ ] CHANGELOG updated

**Post-Release:**

- [ ] Main merged to develop
- [ ] Release branch cleaned up
- [ ] Release docs updated

---

## 🔗 Related

- **Release Checklist:** [checklist.md](checklist.md)
- **Release Notes:** [release-notes.md](release-notes.md)
- **Feature Status:** [Code Structure Refactoring](../../refactor/code-structure-refactoring/status-and-next-steps.md)
- **Bug Fix:** BUG-001 in [research-topics.md](../../../explorations/work-prod-integration/research-topics.md)

---

**Last Updated:** 2026-01-08
