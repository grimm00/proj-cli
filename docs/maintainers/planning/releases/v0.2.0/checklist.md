# Release Checklist - v0.2.0

**Version:** v0.2.0  
**Status:** 🔴 Not Started  
**Created:** 2026-01-07  
**Type:** Minor Release

---

## Pre-Release

### Code Quality

- [ ] All tests passing
- [ ] Test coverage > 80% (current: >90% for core modules)
- [ ] 0 linting errors maintained
- [ ] All HIGH priority issues addressed (✅ 2 fixed in Fix PR #1)
- [ ] All MEDIUM priority issues addressed (✅ 10 fixed in Fix PR #2)
- [ ] Critical bugs fixed

### Documentation

- [ ] Documentation reviewed and accurate
- [ ] README.md updated with template generation docs
- [ ] All examples verified and working
- [ ] Manual testing guide complete

### Production Readiness

- [ ] All 30 requirements verified
- [ ] All 17 manual testing scenarios pass
- [ ] API sync graceful degradation tested

### Release Preparation

- [x] Release directory structure created ✅
- [x] Release checklist created (this file)
- [x] Release notes prepared
- [ ] Version number updated (0.1.0 → 0.2.0)
- [ ] CHANGELOG updated

---

## Release

### Version Management

- [ ] Version updated in `src/proj/__init__.py`
- [ ] Version tagged in git (`git tag v0.2.0`)
- [ ] Tag pushed to remote (`git push origin v0.2.0`)

### Release Documentation

- [ ] Release notes finalized
- [ ] CHANGELOG merged to root
- [ ] Documentation updated with version number

### Release Artifacts

- [ ] GitHub release created
- [ ] Release notes published
- [ ] Documentation links verified

---

## Post-Release

### Git Cleanup

- [ ] Main merged to develop
- [ ] Release branch deleted (local)
- [ ] Release branch deleted (remote)

### Communication

- [ ] Release notes published
- [ ] Team notified (if applicable)

### Follow-up

- [ ] Post-release monitoring active
- [ ] Issues tracked (if any)
- [ ] Next release planned (v0.3.0 - Project Type Support)

---

## Release Summary

**Version:** v0.2.0 - Template Generation Extension  
**Release Date:** 2026-01-07  
**Status:** 🔴 Draft

**Key Features:**

- Template Generation from `standard-project` and `learning-project`
- Local Registry for project tracking
- API Sync with graceful degradation
- Enhanced `proj create` command

**Related PRs:**

| PR | Title | Type |
|----|-------|------|
| #8 | Config Extension (Phase 1) | feat |
| #9 | Test isolation fix | fix |
| #10 | Local Registry (Phase 2) | feat |
| #11 | Template Copying (Phase 3) | feat |
| #12 | Create Command Extension (Phase 4) | feat |
| #13 | Testing & Polish (Phase 5 Partial) | feat |
| #14 | API Sync Enhancement (Phase 6) | feat |
| #15 | HIGH priority fixes (Fix PR #1) | fix |
| #16 | MEDIUM priority fixes (Fix PR #2) | fix |
| #17 | Test improvements (pr8-batch-low-low-01) | fix |
| #18 | Test improvements (pr11-batch-low-low-01) | fix |
| #19 | Test improvements (pr12-batch-low-low-01) | fix |

---

**Last Updated:** 2026-01-07

