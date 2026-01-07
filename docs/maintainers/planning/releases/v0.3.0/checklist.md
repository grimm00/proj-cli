# Release Checklist - v0.3.0

**Version:** v0.3.0
**Status:** 🔴 Not Started
**Created:** 2026-01-07
**Type:** Minor Release

---

## Pre-Release

### Code Quality

- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] 0 linting errors maintained
- [ ] All HIGH priority issues addressed
- [ ] Critical bugs fixed

### Documentation

- [x] Documentation reviewed and accurate
- [x] README updated with `--type` filter examples
- [x] CLI help includes `--type` option
- [x] All examples verified and working

### Production Readiness

- [ ] All integration tests passing against work-prod API

### Release Preparation

- [x] Release directory structure created
- [ ] Release checklist complete (this file)
- [ ] Release notes prepared
- [ ] Version number determined (v0.3.0)
- [ ] CHANGELOG updated

---

## Release

### Version Management

- [ ] Version tagged in git (`git tag v0.3.0`)
- [ ] Tag pushed to remote (`git push origin v0.3.0`)
- [ ] Version number updated in `src/proj/__init__.py`
- [ ] Version number updated in `pyproject.toml`

### Release Documentation

- [ ] Release notes finalized
- [ ] CHANGELOG merged
- [ ] Documentation updated with version number

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

**Version:** v0.3.0 - Project Type Support
**Release Date:** TBD
**Status:** 🔴 Draft

**Key Features:**

- Project type filtering (`--type` option)
- Combined filter support
- Enhanced error handling

**Related:**

- Source: project-type-support feature
- PRs: PR #21 (Phase 1)

---

**Last Updated:** 2026-01-07

