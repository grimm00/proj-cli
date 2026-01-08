# Release Checklist - v0.3.2

**Version:** v0.3.2  
**Status:** 🔴 Not Started  
**Created:** 2026-01-08  
**Type:** Patch Release

---

## Pre-Release

### Code Quality

- [ ] All tests passing (238+ expected, 4 pre-existing failures)
- [ ] Test coverage maintained (~92%)
- [ ] 0 linting errors maintained
- [ ] All Sourcery review issues addressed (PRs #27, #28, #29)

### Documentation

- [ ] README.md accurate
- [ ] Test README updated with new structure
- [ ] Release notes prepared

### Release Preparation

- [x] Release directory structure created
- [x] Release checklist complete (this file)
- [ ] Release notes prepared
- [ ] CHANGELOG draft prepared
- [ ] Version number confirmed (v0.3.2)

---

## Release

### Version Management

- [ ] Version bumped in `pyproject.toml` (0.3.1 → 0.3.2)
- [ ] Version bumped in `src/proj/__init__.py` (0.3.1 → 0.3.2)
- [ ] Version tagged in git (`git tag v0.3.2`)
- [ ] Tag pushed to remote (`git push origin v0.3.2`)

### Release Documentation

- [ ] Release notes finalized
- [ ] CHANGELOG.md updated
- [ ] Release hub status updated to ✅ Released

---

## Post-Release

### Git Cleanup

- [ ] Release branch merged to main (if used)
- [ ] Main merged back to develop
- [ ] Release branch deleted (if used)

### Follow-up

- [ ] Next release planned (v0.4.0 - Work-Prod Integration?)

---

## Release Summary

**Version:** v0.3.2 - Code Structure Refactoring  
**Release Date:** 2026-01-08  
**Status:** 🔴 Draft

**Changes:**

- **Refactoring:** Split `projects.py` into 5 focused modules (PR #25)
- **Refactoring:** Reorganized test structure into 4 categories (PR #26)
- **Bug Fix:** Fixed blank "path" field in inventory export (BUG-001)
- **Code Quality:** Test improvements (PRs #27, #28, #29)

**PRs Included:**

- PR #25: refactor: Split projects.py into focused modules (Phase 1)
- PR #26: refactor: Test Structure Reorganization (Phase 2)
- PR #27: fix: Test regression coverage improvements
- PR #28: fix: Remove unused _get_client() function
- PR #29: fix: Parametrize command-existence tests
- Direct: fix(inventory): use 'path' field name to match work-prod API (BUG-001)

---

**Last Updated:** 2026-01-08
