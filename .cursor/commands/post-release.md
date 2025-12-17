# Post Release Command

Handles post-release cleanup including merging main back to develop, cleaning up the release branch, and preparing for the next development cycle. Customized for work-prod's release workflow.

---

## Configuration

**Path Detection:**

- Releases Hub: `docs/maintainers/planning/releases/README.md`
- Per-Version: `docs/maintainers/planning/releases/[version]/`

**Version Format:** `vX.Y.Z` (e.g., `v0.2.0`)

---

## Workflow Overview

**When to use:**

- After release PR is merged to main
- After tag is created
- To clean up and prepare for next development cycle

**Workflow Position:**

```
/release-finalize vX.Y.Z
         │
         ▼
   /pr --release (merged)
         │
         ▼
   Tag created (git tag vX.Y.Z)
         │
         ▼
┌─────────────────────────────────────┐
│   /post-release vX.Y.Z              │  ◄── This command
│                                     │
│   1. Validate release complete      │
│   2. Merge main to develop          │
│   3. Clean up release branch        │
│   4. Update release documentation   │
│   5. Update releases hub            │
│   6. Prepare for next cycle         │
└─────────────────────────────────────┘
         │
         ▼
   Ready for next development cycle
```

---

## Usage

**Command:** `/post-release [version] [options]`

**Examples:**

- `/post-release v0.2.0` - Full post-release workflow
- `/post-release v0.2.0 --dry-run` - Preview changes
- `/post-release v0.2.0 --keep-branch` - Don't delete release branch

**Options:**

- `--dry-run` - Show what would be done without executing
- `--keep-branch` - Keep release branch (don't delete)
- `--skip-merge` - Skip merging main to develop (if already done)

---

## Step-by-Step Process

### 1. Validate Release Complete

**Verify tag exists:**

```bash
git fetch --tags
git tag -l "vX.Y.Z"
```

**Verify main has release:**

```bash
git log main --oneline -5
# Should show release merge commit
```

**Checklist:**

- [ ] Tag vX.Y.Z exists
- [ ] Main branch has release changes
- [ ] Release PR merged

**Error handling:**

```
❌ Tag vX.Y.Z not found
   Resolution: Create tag first: git tag vX.Y.Z && git push origin vX.Y.Z

❌ Release changes not in main
   Resolution: Ensure release PR was merged to main
```

---

### 2. Merge Main to Develop

**Sync develop with main:**

```bash
git checkout develop
git pull origin develop
git fetch origin main
git merge origin/main --no-edit -m "Merge main into develop after vX.Y.Z release"
```

**Handle conflicts (if any):**

- Resolve in favor of main for release-specific changes
- Keep develop changes for ongoing work
- Common conflict areas:
  - CHANGELOG.md (accept main's version)
  - Version numbers (accept main's version)

**Push updated develop:**

```bash
git push origin develop
```

**Checklist:**

- [ ] Switched to develop branch
- [ ] Pulled latest develop
- [ ] Merged main into develop
- [ ] Conflicts resolved (if any)
- [ ] Pushed to origin

---

### 3. Clean Up Release Branch

**Skip if:** `--keep-branch` flag used

**Delete local release branch:**

```bash
git branch -d release/vX.Y.Z
```

**Delete remote release branch:**

```bash
git push origin --delete release/vX.Y.Z
```

**Prune stale references:**

```bash
git remote prune origin
```

**Checklist:**

- [ ] Local branch deleted
- [ ] Remote branch deleted
- [ ] Stale references pruned

---

### 4. Update Release Documentation

**File:** `docs/maintainers/planning/releases/vX.Y.Z/README.md`

**Update status:**

```markdown
# Before
**Status:** 🟡 Ready for Release

# After
**Status:** ✅ Released
**Released:** YYYY-MM-DD
**Merged:** PR #XX (to main)
```

**Update checklist status section:**

```markdown
## ✅ Release Checklist Status

**Pre-Release:**
- [x] All tests passing
- [x] Release checklist complete
- [x] Release notes prepared

**Release:**
- [x] Version tagged in git ✅ Tagged vX.Y.Z
- [x] Release notes finalized ✅ Finalized YYYY-MM-DD
- [x] Documentation updated ✅

**Post-Release:**
- [x] Main merged to develop ✅
- [x] Release branch cleaned up ✅
- [x] Release docs updated ✅
```

**Checklist:**

- [ ] Status updated to Released
- [ ] Release date added
- [ ] Merged PR number added
- [ ] Post-release checklist items marked complete

---

### 5. Update Release Checklist

**File:** `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`

**Mark post-release items complete:**

```markdown
## Post-Release

### Git Cleanup

- [x] Main merged to develop ✅
- [x] Release branch deleted (local) ✅
- [x] Release branch deleted (remote) ✅

### Communication

- [x] Release notes published ✅ (if applicable)

### Follow-up

- [x] Post-release complete ✅
```

**Update status:**

```markdown
**Status:** ✅ Complete
```

**Checklist:**

- [ ] Post-release items marked complete
- [ ] Status updated to Complete

---

### 6. Update Releases Hub

**File:** `docs/maintainers/planning/releases/README.md`

**Update Quick Links:**

```markdown
### Releases

- **[vX.Y.Z](vX.Y.Z/README.md)** - [Release Name] (✅ Released YYYY-MM-DD)
- **[v0.1.0](v0.1.0/README.md)** - MVP Release (✅ Released 2025-12-07)
```

**Update Release Timeline:**

```markdown
| vX.Y.Z | ✅ Released | YYYY-MM-DD | [Type] | [Description] |
| v0.1.0 | ✅ Released | 2025-12-07 | MVP | Backend MVP Release |
```

**Update Summary:**

```markdown
**Total Releases:** 2 released  
**Latest Release:** vX.Y.Z - Released YYYY-MM-DD  
**Status:** ✅ Released
```

**Add to Release History:**

```markdown
## 📝 Release History

### vX.Y.Z - [Release Name] (YYYY-MM-DD)

**Status:** ✅ Released  
**PR:** #XX  
**Type:** [Type]

**Key Features:**
- [Feature 1]
- [Feature 2]

**Release Notes:** [vX.Y.Z/release-notes.md](vX.Y.Z/release-notes.md)
```

**Update "Next Release" section:**

```markdown
## 🚀 Next Release

No release currently planned. Start planning with:
- `/release-prep vX.Y+1.0` for next minor release
- `/release-prep vX.Y.Z+1` for patch release
```

**Checklist:**

- [ ] Quick Links updated (status → Released)
- [ ] Release Timeline updated
- [ ] Summary updated
- [ ] Release History entry added
- [ ] Next Release section updated
- [ ] Last Updated refreshed

---

### 7. Commit Documentation Updates

**Stage and commit:**

```bash
git add docs/maintainers/planning/releases/vX.Y.Z/
git add docs/maintainers/planning/releases/README.md

git commit -m "docs(release): mark vX.Y.Z as released

- Updated release hub status to Released
- Updated checklist (all items complete)
- Updated releases hub with release history
- Post-release cleanup complete

Released: vX.Y.Z on YYYY-MM-DD"
```

**Push to develop:**

```bash
git push origin develop
```

**Checklist:**

- [ ] Documentation changes staged
- [ ] Commit created
- [ ] Pushed to develop

---

### 8. Summary Report

```markdown
## ✅ Post-Release Complete

**Version:** vX.Y.Z
**Released:** YYYY-MM-DD

### Actions Completed

| Action | Status |
|--------|--------|
| Tag verified | ✅ |
| Main merged to develop | ✅ |
| Release branch deleted | ✅ / ⏭️ Kept |
| Release hub updated | ✅ |
| Checklist updated | ✅ |
| Releases hub updated | ✅ |
| Documentation committed | ✅ |

### Branch Status

- **develop:** Up to date with main
- **release/vX.Y.Z:** Deleted / Kept
- **main:** Release tagged

### Next Steps

1. Start next development cycle
2. Create feature branches from develop
3. Plan next release when ready:
   - Minor: `/release-prep vX.Y+1.0`
   - Patch: `/release-prep vX.Y.Z+1`
```

---

## Common Issues

### Issue: Tag Not Found

**Solution:**

```bash
# Create and push tag
git checkout main
git tag vX.Y.Z
git push origin vX.Y.Z
```

### Issue: Merge Conflicts

**Solution:**

```bash
# Common resolution
git checkout --theirs CHANGELOG.md  # Accept main's CHANGELOG
git add CHANGELOG.md
git commit
```

### Issue: Branch Already Deleted

**Solution:**

```bash
# Check if branch exists
git branch -a | grep release/vX.Y.Z

# If not found, skip deletion steps
# Prune stale references
git remote prune origin
```

---

## Tips

### Before Running

- Ensure release PR was merged to main
- Ensure tag was created
- Verify you're on develop (or will switch)

### During Execution

- Watch for merge conflicts
- Use `--keep-branch` if you need the branch for hotfixes

### After Completion

- Verify develop is up to date with main
- Check releases hub looks correct
- Ready to start new development

---

## Integration with Other Commands

### Full Release Workflow

```
1. /release-prep vX.Y.Z          - Create drafts
2. Review and edit drafts
3. /release-finalize vX.Y.Z      - Finalize documents
4. /pr --release                 - Create PR to main
5. Review, approve, merge PR
6. git tag vX.Y.Z && git push origin vX.Y.Z
7. /post-release vX.Y.Z          ← This command
```

### Related Commands

- **`/release-prep`** - Create release drafts
- **`/release-finalize`** - Finalize release documents
- **`/pr --release`** - Create release PR

---

## Work-Prod Specific Notes

### Version History

| Version | Released | Notes |
|---------|----------|-------|
| v0.1.0 | 2025-12-07 | MVP Release |

### Typical Release Cadence

- **Minor releases:** After completing feature phases
- **Patch releases:** For critical bug fixes

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active - Customized for work-prod
