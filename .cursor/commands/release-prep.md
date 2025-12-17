# Release Prep Command

Orchestrates release preparation by creating documentation drafts and optionally creating the release branch. Customized for work-prod's release workflow.

---

## Configuration

**Path Detection:**

- Releases Hub: `docs/maintainers/planning/releases/README.md`
- Per-Version: `docs/maintainers/planning/releases/[version]/`
- CHANGELOG: `CHANGELOG.md` (root)

**Version Format:** `vX.Y.Z` (e.g., `v0.2.0`)

---

## Workflow Overview

**When to use:**

- When starting release preparation
- After feature development is complete for a milestone
- To generate all release documentation

**Workflow Position:**

```
Feature Development Complete
         │
         ▼
┌─────────────────────────────────────┐
│   /release-prep vX.Y.Z              │  ◄── This command
│                                     │
│   1. Create release directory       │
│   2. Create per-version hub         │
│   3. Create checklist               │
│   4. Create release notes draft     │
│   5. Create CHANGELOG draft         │
│   6. Create transition plan (opt)   │
│   7. Create release branch (opt)    │
└─────────────────────────────────────┘
         │
         ▼
   Manual review of drafts
         │
         ▼
   /release-finalize vX.Y.Z
```

---

## Usage

**Command:** `/release-prep [version] [options]`

**Examples:**

- `/release-prep v0.2.0` - Full release preparation
- `/release-prep v0.2.0 --dry-run` - Show what would be done
- `/release-prep v0.2.0 --skip-branch` - Prepare but don't create branch
- `/release-prep v0.2.0 --skip-transition` - Skip transition plan (for minor releases)
- `/release-prep v0.2.0 --from-reflection [path]` - Use reflection as source

**Options:**

- `--dry-run` - Show what would be done without executing
- `--skip-branch` - Skip release branch creation
- `--skip-transition` - Skip transition plan (for patch releases)
- `--from-reflection [path]` - Use reflection document as source for content
- `--force` - Continue despite warnings

---

## Step-by-Step Process

### 1. Gather Release Information

**Determine version type:**

- **Major (vX.0.0):** Breaking changes, major features
- **Minor (v0.X.0):** New features, backward compatible
- **Patch (v0.0.X):** Bug fixes only

**Gather from context:**

```bash
# Get commits since last tag
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "")..HEAD --oneline

# Get merged PRs (if gh available)
gh pr list --state merged --limit 50 --json number,title,mergedAt 2>/dev/null || echo "No gh CLI"

# Check for reflection document
ls docs/maintainers/planning/notes/reflections/reflection-*.md 2>/dev/null | tail -1
```

**Read related documents:**

- Feature status: `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`
- Recent reflections: `docs/maintainers/planning/notes/reflections/`
- MVP roadmap: `docs/maintainers/planning/mvp-roadmap.md`

**Checklist:**

- [ ] Version number determined
- [ ] Version type identified (major/minor/patch)
- [ ] Changes gathered (commits, PRs, features)
- [ ] Related documents identified

---

### 2. Create Release Directory

```bash
mkdir -p docs/maintainers/planning/releases/vX.Y.Z/
```

---

### 3. Create Per-Version Hub

**File:** `docs/maintainers/planning/releases/vX.Y.Z/README.md`

```markdown
# Release vX.Y.Z - [Release Name]

**Version:** vX.Y.Z  
**Status:** 🔴 Draft  
**Target Date:** YYYY-MM-DD  
**Created:** YYYY-MM-DD  
**Source:** [reflection-YYYY-MM-DD-description.md or "feature development"]  
**Type:** [Major/Minor/Patch] Release

---

## 📋 Quick Links

- **[Release Checklist](checklist.md)** - Release preparation checklist
- **[Release Notes](release-notes.md)** - Release notes and changelog
- **[Transition Plan](transition-plan.md)** - Release transition planning document (if applicable)

---

## 📊 Release Summary

**Version:** vX.Y.Z  
**Target Date:** YYYY-MM-DD  
**Status:** 🔴 Draft

**Key Features:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Development:**
- Phases: [X/Y complete]
- PRs: [N] total
- Source: [Reflection or feature planning document]

---

## ✅ Release Checklist Status

**Pre-Release:**
- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] 0 linting errors maintained
- [ ] Documentation reviewed
- [ ] Release checklist complete
- [ ] Release notes prepared

**Release:**
- [ ] Version tagged in git
- [ ] Release notes finalized
- [ ] Documentation updated

**Post-Release:**
- [ ] Main merged to develop
- [ ] Release branch cleaned up
- [ ] Release docs updated

---

## 🔗 Related

- **Release Checklist:** [checklist.md](checklist.md)
- **Release Notes:** [release-notes.md](release-notes.md)
- **Transition Plan:** [transition-plan.md](transition-plan.md)
- **Feature Status:** `docs/maintainers/planning/features/[feature]/status-and-next-steps.md`

---

**Last Updated:** YYYY-MM-DD
```

---

### 4. Create Release Checklist

**File:** `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`

```markdown
# Release Checklist - vX.Y.Z

**Version:** vX.Y.Z  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Type:** [Major/Minor/Patch] Release

---

## Pre-Release

### Code Quality

- [ ] All tests passing
- [ ] Test coverage > 80%
- [ ] 0 linting errors maintained
- [ ] All HIGH priority issues addressed
- [ ] Critical bugs fixed

### Documentation

- [ ] Documentation reviewed and accurate
- [ ] API specification accurate (if changed)
- [ ] User documentation updated (README.md)
- [ ] All examples verified and working

### Production Readiness

- [ ] Production configuration verified (if applicable)
- [ ] Database migrations documented (if applicable)
- [ ] Performance verified (if applicable)

### Release Preparation

- [ ] Release directory structure created ✅
- [ ] Release checklist complete (this file)
- [ ] Release notes prepared
- [ ] Version number determined (vX.Y.Z)
- [ ] CHANGELOG updated

---

## Release

### Version Management

- [ ] Version tagged in git (`git tag vX.Y.Z`)
- [ ] Tag pushed to remote (`git push origin vX.Y.Z`)
- [ ] Version number updated in documentation

### Release Documentation

- [ ] Release notes finalized
- [ ] CHANGELOG merged
- [ ] Documentation updated with version number

### Release Artifacts

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

- [ ] Post-release monitoring active (if applicable)
- [ ] Issues tracked (if any)
- [ ] Next release planned

---

## Release Summary

**Version:** vX.Y.Z - [Release Name]  
**Release Date:** YYYY-MM-DD  
**Status:** 🔴 Draft

**Key Features:**
- [Feature 1]
- [Feature 2]

**Related:**
- Source: [reflection or feature document]
- PRs: [List key PRs]

---

**Last Updated:** YYYY-MM-DD
```

---

### 5. Create Release Notes Draft

**File:** `docs/maintainers/planning/releases/vX.Y.Z/release-notes.md`

```markdown
# Release Notes - vX.Y.Z

**Release Date:** YYYY-MM-DD  
**Status:** 🔴 Draft  
**Type:** [Major/Minor/Patch] Release

---

## What's New

### [Feature Category 1]

**[Feature Name]:**
- [Description]
- [Key capability]

### [Feature Category 2]

**[Feature Name]:**
- [Description]

---

## Improvements

### [Improvement Category]

- **[Improvement]:** [Description]
- **[Improvement]:** [Description]

---

## Bug Fixes

### [Fix Category]

- **[Fix]:** [Description] (PR #XX)

---

## Breaking Changes

[None in this release / List breaking changes]

---

## Migration Guide

### [Migration Section if needed]

[Migration instructions]

---

## Technical Details

### Changes Summary

- **Files Changed:** [N]
- **Tests Added:** [N]
- **Coverage:** [X]%

### Key PRs

- PR #XX: [Description]
- PR #XX: [Description]

---

## Known Issues

[List any known issues or planned improvements]

---

**Last Updated:** YYYY-MM-DD  
**Next Release:** TBD
```

---

### 6. Create CHANGELOG Draft

**File:** `docs/maintainers/planning/releases/vX.Y.Z/CHANGELOG-DRAFT.md`

```markdown
# CHANGELOG Draft - vX.Y.Z

**Draft Created:** YYYY-MM-DD  
**Status:** 🔴 Draft - Needs Review

---

## [X.Y.Z] - YYYY-MM-DD

### Added

- **[Feature]** - Description (PR #XX)

### Changed

- **[Change]** - Description (PR #XX)

### Fixed

- **[Fix]** - Description (PR #XX)

### Removed

- [If any removals]

---

## Review Checklist

- [ ] All PRs listed
- [ ] Categorization correct (Added/Changed/Fixed/Removed)
- [ ] PR numbers accurate
- [ ] Descriptions clear and user-facing
- [ ] Ready to merge into CHANGELOG.md

---

**Ready for merge:** [ ] Yes / [x] No - Needs review
```

---

### 7. Create Transition Plan (Optional)

**File:** `docs/maintainers/planning/releases/vX.Y.Z/transition-plan.md`

**Skip if:** `--skip-transition` flag used (for patch releases)

```markdown
# Transition Plan - vX.Y.Z

**Version:** vX.Y.Z  
**Status:** 🔴 Draft  
**Created:** YYYY-MM-DD

---

## 📋 Overview

[Brief description of what this release transitions from/to]

---

## 🎯 Goals

1. [Goal 1]
2. [Goal 2]

---

## 📝 Pre-Release Tasks

- [ ] [Task 1]
- [ ] [Task 2]

---

## 🚀 Release Tasks

- [ ] [Task 1]
- [ ] [Task 2]

---

## 📦 Post-Release Tasks

- [ ] [Task 1]
- [ ] [Task 2]

---

## ⚠️ Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Mitigation] |

---

**Last Updated:** YYYY-MM-DD
```

---

### 8. Create Release Branch (Optional)

**Skip if:** `--skip-branch` flag used

```bash
git checkout develop
git pull origin develop
git checkout -b release/vX.Y.Z

git add docs/maintainers/planning/releases/vX.Y.Z/
git commit -m "docs(release): initialize vX.Y.Z release preparation

- Created release directory structure
- Added release hub (README.md)
- Added release checklist
- Added release notes draft
- Added CHANGELOG draft
- Added transition plan (if applicable)

Ready for review and finalization."
```

---

### 9. Update Releases Hub

**File:** `docs/maintainers/planning/releases/README.md`

**Add to Quick Links:**

```markdown
- **[vX.Y.Z](vX.Y.Z/README.md)** - [Release Name] (🔴 Draft)
```

**Add to Release Timeline:**

```markdown
| vX.Y.Z | 🔴 Draft | YYYY-MM-DD | [Type] | [Description] |
```

---

### 10. Summary Report

```markdown
## ✅ Release Preparation Complete

**Version:** vX.Y.Z

### Documents Created

| File | Status |
|------|--------|
| `vX.Y.Z/README.md` | ✅ Created |
| `vX.Y.Z/checklist.md` | ✅ Created |
| `vX.Y.Z/release-notes.md` | ✅ Created |
| `vX.Y.Z/CHANGELOG-DRAFT.md` | ✅ Created |
| `vX.Y.Z/transition-plan.md` | ✅ Created / ⏭️ Skipped |

### Branch

- **Branch:** `release/vX.Y.Z` (created / skipped)

### Next Steps

1. Review all draft documents
2. Fill in specific content (features, fixes, changes)
3. Run `/release-finalize vX.Y.Z` when ready
```

---

## Work-Prod Specific Customizations

### Root CHANGELOG.md

If `CHANGELOG.md` doesn't exist at root, create it:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

[Changes not yet released]

## [0.1.0] - 2025-12-07

### Added

- Full CRUD API (GET, POST, PATCH, DELETE, Archive)
- Search and filter capabilities
- Bulk import functionality
- CLI tool with all commands
- Production configuration and deployment guides

### Fixed

- Environment variable loading robustness
- Database migration always-run pattern

---

[Unreleased]: https://github.com/grimm00/work-prod/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/grimm00/work-prod/releases/tag/v0.1.0
```

---

## Integration with Other Commands

### Command Sequence

```
1. Feature development complete
2. /release-prep vX.Y.Z          ← This command
3. Review and edit drafts
4. /release-finalize vX.Y.Z
5. /pr --release
6. Merge to main, tag
7. /post-release vX.Y.Z
```

### Related Commands

- **`/release-finalize`** - Finalize release documents
- **`/post-release`** - Post-release cleanup
- **`/reflect`** - Create reflection (often source for release)

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active - Customized for work-prod
