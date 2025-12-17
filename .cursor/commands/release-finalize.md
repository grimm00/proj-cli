# Release Finalize Command

Finalizes release preparation by merging CHANGELOG draft, completing release notes, and preparing for the release PR. Customized for work-prod's release workflow.

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

- After `/release-prep` has generated draft documents
- After reviewing and approving draft content
- Before creating the release PR

**Workflow Position:**

```
/release-prep vX.Y.Z
         │
         ▼
   Review Drafts (manual)
         │
         ▼
┌─────────────────────────────────────┐
│   /release-finalize vX.Y.Z          │  ◄── This command
│                                     │
│   1. Validate prerequisites         │
│   2. Merge CHANGELOG draft          │
│   3. Finalize release notes         │
│   4. Update release hub             │
│   5. Update checklist               │
│   6. Update releases hub            │
│   7. Commit to release branch       │
└─────────────────────────────────────┘
         │
         ▼
   /pr --release (create PR to main)
```

---

## Usage

**Command:** `/release-finalize [version] [options]`

**Examples:**

- `/release-finalize v0.2.0` - Full finalization
- `/release-finalize v0.2.0 --dry-run` - Preview changes
- `/release-finalize v0.2.0 --date 2025-12-20` - Set specific release date

**Options:**

- `--dry-run` - Show what would be done without executing
- `--date YYYY-MM-DD` - Set release date (default: today)
- `--skip-changelog` - Skip CHANGELOG merge (if not using root CHANGELOG)

---

## Step-by-Step Process

### 1. Validate Prerequisites

**Required files:**

```
docs/maintainers/planning/releases/vX.Y.Z/README.md
docs/maintainers/planning/releases/vX.Y.Z/checklist.md
docs/maintainers/planning/releases/vX.Y.Z/release-notes.md
docs/maintainers/planning/releases/vX.Y.Z/CHANGELOG-DRAFT.md
CHANGELOG.md (root - create if missing)
```

**Validation checks:**

- [ ] Release directory exists
- [ ] All required files exist
- [ ] Draft status is not already "Final" or "Released"
- [ ] On release branch (`release/vX.Y.Z`) or develop

**Error handling:**

```
❌ Missing required file: vX.Y.Z/release-notes.md
   Resolution: Run /release-prep vX.Y.Z first
```

**Checklist:**

- [ ] All required files found
- [ ] Status is Draft (not already finalized)
- [ ] Ready to proceed

---

### 2. Merge CHANGELOG Draft

**Read:** `docs/maintainers/planning/releases/vX.Y.Z/CHANGELOG-DRAFT.md`

**Update:** `CHANGELOG.md` (root)

**Process:**

1. Read CHANGELOG-DRAFT.md content
2. Set release date (today or `--date` option)
3. Insert version section into CHANGELOG.md after `## [Unreleased]`

**Example result:**

```markdown
## [Unreleased]

[Changes not yet released]

## [0.2.0] - 2025-12-20    ◄── Inserted

### Added

- [Feature from draft]

### Fixed

- [Fix from draft]

## [0.1.0] - 2025-12-07    ◄── Existing
```

**Update comparison links:**

```markdown
[Unreleased]: https://github.com/grimm00/work-prod/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/grimm00/work-prod/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/grimm00/work-prod/releases/tag/v0.1.0
```

**Checklist:**

- [ ] CHANGELOG-DRAFT.md read
- [ ] Version section inserted into CHANGELOG.md
- [ ] Release date set
- [ ] Comparison links updated

---

### 3. Finalize Release Notes

**File:** `docs/maintainers/planning/releases/vX.Y.Z/release-notes.md`

**Updates:**

```markdown
# Before
**Release Date:** YYYY-MM-DD
**Status:** 🔴 Draft

# After
**Release Date:** 2025-12-20
**Status:** ✅ Final
```

**Also update:**

- Last Updated field
- Any remaining placeholder text
- Ensure all sections are complete

**Checklist:**

- [ ] Status updated to Final
- [ ] Release date set
- [ ] Last Updated refreshed
- [ ] Content complete (no placeholders)

---

### 4. Update Release Hub

**File:** `docs/maintainers/planning/releases/vX.Y.Z/README.md`

**Updates:**

```markdown
# Before
**Status:** 🔴 Draft
**Target Date:** YYYY-MM-DD

# After
**Status:** 🟡 Ready for Release
**Release Date:** 2025-12-20
```

**Update checklist status section:**

```markdown
## ✅ Release Checklist Status

**Pre-Release:**
- [x] All tests passing
- [x] Test coverage > 80%
- [x] Release checklist complete
- [x] Release notes prepared

**Release:**
- [ ] Version tagged in git      ← Still pending (done during merge)
- [x] Release notes finalized
- [x] Documentation updated
```

**Checklist:**

- [ ] Status updated to Ready for Release
- [ ] Release date set
- [ ] Checklist status section updated
- [ ] Last Updated refreshed

---

### 5. Update Release Checklist

**File:** `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`

**Updates:**

Mark items complete:

```markdown
### Release Preparation

- [x] Release directory structure created ✅
- [x] Release checklist complete (this file) ✅
- [x] Release notes prepared ✅
- [x] Version number determined (vX.Y.Z) ✅
- [x] CHANGELOG updated ✅
```

```markdown
### Release Documentation

- [x] Release notes finalized ✅ Finalized YYYY-MM-DD
- [x] CHANGELOG merged ✅
- [ ] Documentation updated with version number (pending release)
```

**Update header:**

```markdown
**Status:** 🟡 Ready for Release
```

**Checklist:**

- [ ] Pre-release items marked complete
- [ ] Release documentation items marked complete
- [ ] Status updated
- [ ] Last Updated refreshed

---

### 6. Update Releases Hub

**File:** `docs/maintainers/planning/releases/README.md`

**Update Quick Links:**

```markdown
### Releases

- **[vX.Y.Z](vX.Y.Z/README.md)** - [Release Name] (🟡 Ready for Release)
- **[v0.1.0](v0.1.0/README.md)** - MVP Release (✅ Released 2025-12-07)
```

**Update Release Timeline:**

```markdown
| vX.Y.Z | 🟡 Ready | YYYY-MM-DD | [Type] | [Description] |
| v0.1.0 | ✅ Released | 2025-12-07 | MVP | Backend MVP Release |
```

**Update Summary:**

```markdown
**Total Releases:** 1 released, 1 pending  
**Latest Release:** v0.1.0 (MVP) - Released 2025-12-07  
**Next Release:** vX.Y.Z - Ready for release
```

**Checklist:**

- [ ] Quick Links updated
- [ ] Release Timeline updated
- [ ] Summary updated
- [ ] Last Updated refreshed

---

### 7. Commit Changes

**Ensure on release branch:**

```bash
git branch --show-current  # Should be release/vX.Y.Z or develop
```

**Stage and commit:**

```bash
git add CHANGELOG.md
git add docs/maintainers/planning/releases/vX.Y.Z/
git add docs/maintainers/planning/releases/README.md

git commit -m "docs(release): finalize vX.Y.Z release documents

- Merged CHANGELOG draft into CHANGELOG.md
- Finalized release notes (status: Final)
- Updated release hub (status: Ready for Release)
- Updated release checklist
- Updated releases hub with new version

Ready for release PR to main."
```

**Push if on release branch:**

```bash
git push origin release/vX.Y.Z
```

**Checklist:**

- [ ] All files staged
- [ ] Commit created
- [ ] Pushed (if on release branch)

---

### 8. Summary Report

```markdown
## ✅ Release Finalization Complete

**Version:** vX.Y.Z
**Date:** YYYY-MM-DD

### Documents Updated

| File | Change |
|------|--------|
| `CHANGELOG.md` | Version section added |
| `vX.Y.Z/README.md` | Status → Ready for Release |
| `vX.Y.Z/release-notes.md` | Status → Final |
| `vX.Y.Z/checklist.md` | Items marked complete |
| `releases/README.md` | New version added |

### Status Summary

- **Release Notes:** ✅ Final
- **CHANGELOG:** ✅ Merged
- **Checklist:** ✅ Updated
- **Releases Hub:** ✅ Updated

### Next Steps

1. Create release PR: `/pr --release vX.Y.Z`
2. Get review and approval
3. Merge to main
4. Tag version: `git tag vX.Y.Z && git push origin vX.Y.Z`
5. Run: `/post-release vX.Y.Z`
```

---

## Common Issues

### Issue: CHANGELOG.md Doesn't Exist

**Solution:**

```bash
# Create CHANGELOG.md with initial content
# See /release-prep for template
```

### Issue: Already Finalized

**Solution:**

```bash
# Check status
grep "Status:" docs/maintainers/planning/releases/vX.Y.Z/README.md

# If already "Ready for Release" or "Released", no action needed
# Use --force to re-finalize if needed
```

### Issue: Missing Draft Files

**Solution:**

```bash
# Run release-prep first
/release-prep vX.Y.Z
```

---

## Tips

### Before Finalizing

- Review all draft content thoroughly
- Ensure all features/fixes are documented
- Verify PR numbers are correct
- Check for placeholder text

### During Finalization

- Use `--dry-run` first to preview changes
- Verify dates are correct
- Check comparison links in CHANGELOG

### After Finalization

- Review the commit diff
- Verify CHANGELOG.md looks correct
- Proceed to create release PR

---

## Integration with Other Commands

### Command Sequence

```
1. /release-prep vX.Y.Z          - Create drafts
2. Manual review and editing
3. /release-finalize vX.Y.Z      ← This command
4. /pr --release                 - Create PR to main
5. Merge and tag
6. /post-release vX.Y.Z          - Cleanup
```

### Related Commands

- **`/release-prep`** - Create release drafts (run first)
- **`/post-release`** - Post-release cleanup (run after merge)
- **`/pr --release`** - Create release PR

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active - Customized for work-prod
