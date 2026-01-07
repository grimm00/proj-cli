# Release Checklist - v0.3.1

**Version:** v0.3.1
**Status:** 🟡 Ready for Release
**Created:** 2026-01-07
**Type:** Patch Release

---

## Pre-Release

### Code Quality

- [x] All tests passing
- [x] Test coverage > 80%
- [x] 0 linting errors maintained
- [x] All HIGH priority issues addressed (PR #23)
- [x] Critical bugs fixed

### Documentation

- [x] Documentation reviewed and accurate
- [x] Fix tracking updated
- [x] Sourcery review issues marked as fixed

### Release Preparation

- [x] Release directory structure created ✅
- [x] Release checklist complete (this file) ✅
- [x] Release notes prepared ✅
- [x] Version number determined (v0.3.1) ✅
- [x] CHANGELOG updated ✅ Finalized 2026-01-07

---

## Release

### Version Management

- [ ] Version tagged in git (`git tag v0.3.1`)
- [ ] Tag pushed to remote (`git push origin v0.3.1`)
- [ ] Version number updated in `src/proj/__init__.py`
- [ ] Version number updated in `pyproject.toml`

### Release Documentation

- [x] Release notes finalized ✅ Finalized 2026-01-07
- [x] CHANGELOG merged ✅
- [x] Documentation updated with version number ✅

### Release Artifacts

- [ ] GitHub release created
- [ ] Release notes published

---

## Post-Release

### Git Cleanup

- [ ] Main merged to develop
- [ ] Release branch deleted (local)
- [ ] Release branch deleted (remote)

### Follow-up

- [ ] Post-release verification complete
- [ ] Next release planned

---

## Release Summary

**Version:** v0.3.1 - Code Quality Improvements
**Release Date:** TBD
**Status:** 🔴 Draft

**Key Improvements:**

- Centralized project type constants
- Custom exception for type validation
- Improved test assertions

**Related:**

- Source: PR #21 Sourcery review
- PRs: PR #23

---

**Last Updated:** 2026-01-07

