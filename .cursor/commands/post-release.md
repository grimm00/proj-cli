# Post-Release Command

Handles all post-merge release tasks: tagging, merging main→develop, creating GitHub release, and cleanup.

---

## Configuration

**Path Detection:**

- Releases Hub: `docs/maintainers/planning/releases/README.md`
- Per-Version: `docs/maintainers/planning/releases/[version]/`

**Version Format:** `vX.Y.Z` (e.g., `v0.1.0`)

---

## Workflow Overview

**When to use:**

- After release PR is merged to `main`
- To complete the release process with tagging and cleanup

**Workflow Position:**

```
/release-prep vX.Y.Z
         │
         ▼
/release-finalize vX.Y.Z
         │
         ▼
/pr --release vX.Y.Z
         │
         ▼
   [Merge PR to main]
         │
         ▼
┌─────────────────────────────────────┐
│   /post-release vX.Y.Z              │  ◄── This command
│                                     │
│   1. Validate PR merged             │
│   2. Tag release                    │
│   3. Merge main → develop           │
│   4. Create GitHub release          │
│   5. Clean up release branch        │
│   6. Update release documentation   │
└─────────────────────────────────────┘
```

---

## Usage

**Command:** `/post-release [version] [options]`

**Examples:**

- `/post-release v0.1.0` - Full post-release workflow
- `/post-release v0.1.0 --skip-github-release` - Skip GitHub release creation
- `/post-release v0.1.0 --dry-run` - Preview changes without executing

**Options:**

- `--dry-run` - Show what would be done without executing
- `--skip-github-release` - Skip GitHub release creation
- `--skip-cleanup` - Skip release branch cleanup
- `--pr [number]` - Specify PR number (auto-detects if not provided)

---

## Step-by-Step Process

### 1. Validate Prerequisites

**Check PR is merged:**

```bash
# Find release PR
gh pr list --state merged --head release/vX.Y.Z --json number,mergedAt

# Or if PR number provided
gh pr view [number] --json state,mergedAt
```

**Verify on correct branch:**

```bash
git branch --show-current
# Should be on release/vX.Y.Z or main
```

**Update local main:**

```bash
git checkout main
git pull origin main
```

**Validation checks:**

- [ ] Release PR is merged
- [ ] Local main is up-to-date
- [ ] Tag doesn't already exist

**Error handling:**

```
❌ Release PR not found or not merged
   Resolution: Merge PR #[number] first, then re-run /post-release

❌ Tag vX.Y.Z already exists
   Resolution: Tag already created. Skip to next step or use --force
```

**Checklist:**

- [ ] PR merged verified
- [ ] On main branch
- [ ] Local main updated
- [ ] Ready to proceed

---

### 2. Tag the Release

**Create annotated tag:**

```bash
git checkout main
git pull origin main

# Create annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z"

# Verify tag
git tag -l vX.Y.Z
git show vX.Y.Z
```

**Push tag:**

```bash
git push origin vX.Y.Z
```

**Checklist:**

- [ ] Tag created locally
- [ ] Tag message set
- [ ] Tag pushed to remote

---

### 3. Merge Main to Develop

**Purpose:** Ensure develop has all release changes.

```bash
git checkout develop
git pull origin develop

# Merge main into develop
git merge main --no-edit

# Push develop
git push origin develop
```

**Handle conflicts (if any):**

- Release changes should merge cleanly
- If conflicts exist, resolve favoring main (release) changes
- Document any manual conflict resolution

**Checklist:**

- [ ] Switched to develop
- [ ] Merged main into develop
- [ ] Pushed develop

---

### 4. Create GitHub Release (Optional)

**Skip if:** `--skip-github-release` option provided

**Create release using GitHub CLI:**

```bash
# Read release notes
RELEASE_NOTES=$(cat docs/maintainers/planning/releases/vX.Y.Z/release-notes.md)

# Create GitHub release
gh release create vX.Y.Z \
  --title "vX.Y.Z - [Release Name]" \
  --notes-file docs/maintainers/planning/releases/vX.Y.Z/release-notes.md
```

**Alternative: Manual creation**

1. Go to: `https://github.com/[owner]/[repo]/releases/new`
2. Select tag: `vX.Y.Z`
3. Title: `vX.Y.Z - [Release Name]`
4. Copy content from `release-notes.md`
5. Publish release

**Checklist:**

- [ ] GitHub release created (or skipped)
- [ ] Release notes included
- [ ] Release published

---

### 5. Clean Up Release Branch

**Skip if:** `--skip-cleanup` option provided

**Delete local branch:**

```bash
git branch -d release/vX.Y.Z
```

**Delete remote branch:**

```bash
git push origin --delete release/vX.Y.Z
```

**Error handling:**

```
⚠️ Cannot delete release/vX.Y.Z - currently checked out
   Resolution: Switch to main or develop first

⚠️ Remote branch already deleted
   Resolution: Skip remote deletion (already cleaned up)
```

**Checklist:**

- [ ] Local branch deleted
- [ ] Remote branch deleted

---

### 6. Update Release Documentation

**File:** `docs/maintainers/planning/releases/vX.Y.Z/README.md`

**Update status:**

```markdown
# Before
**Status:** ✅ Ready for Release

# After
**Status:** ✅ Released
**Released:** YYYY-MM-DD
```

**File:** `docs/maintainers/planning/releases/vX.Y.Z/checklist.md`

**Mark post-release items complete:**

```markdown
## Post-Release

- [x] Version tagged in git ✅
- [x] Main merged to develop ✅
- [x] Release branch cleaned up ✅
- [x] GitHub release created ✅ (or N/A)
- [x] Release documentation updated ✅
```

**Update status:**

```markdown
**Status:** ✅ Released
```

**File:** `docs/maintainers/planning/releases/README.md`

**Update releases hub:**

```markdown
### Releases

- **[vX.Y.Z](vX.Y.Z/README.md)** - [Release Name] (✅ Released YYYY-MM-DD)
```

**Update timeline:**

```markdown
| vX.Y.Z | ✅ Released | YYYY-MM-DD | [Type] | [Description] |
```

**Checklist:**

- [ ] Release hub updated (status → Released)
- [ ] Checklist updated (post-release items)
- [ ] Releases hub updated

---

### 7. Commit Documentation Updates

**Stage and commit:**

```bash
git checkout develop
git add docs/maintainers/planning/releases/
git commit -m "docs(release): mark vX.Y.Z as released

- Updated release hub status to Released
- Marked post-release checklist items complete
- Updated releases hub with release date

Release: vX.Y.Z"
```

**Push:**

```bash
git push origin develop
```

**Checklist:**

- [ ] Documentation changes committed
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
| Tag created | ✅ vX.Y.Z |
| Tag pushed | ✅ origin/vX.Y.Z |
| Main → Develop | ✅ Merged |
| GitHub Release | ✅ Created (or ⏭️ Skipped) |
| Branch cleanup | ✅ Deleted (or ⏭️ Skipped) |
| Documentation | ✅ Updated |

### Links

- **Tag:** https://github.com/[owner]/[repo]/releases/tag/vX.Y.Z
- **GitHub Release:** https://github.com/[owner]/[repo]/releases/vX.Y.Z
- **Release Notes:** docs/maintainers/planning/releases/vX.Y.Z/release-notes.md

### What's Next

- Monitor for any post-release issues
- Begin planning for vX.Y.Z+1 (if applicable)
- Update project roadmap (if applicable)

---

🎉 **Release vX.Y.Z is complete!**
```

---

## Common Issues

### Issue: Tag Already Exists

**Cause:** Tag was created manually or in a previous attempt.

**Solution:**

```bash
# Verify tag exists
git tag -l vX.Y.Z

# If tag is correct, skip tagging step
# If tag needs to be recreated:
git tag -d vX.Y.Z           # Delete local
git push origin :vX.Y.Z     # Delete remote
# Then re-run /post-release
```

---

### Issue: Merge Conflicts (Main → Develop)

**Cause:** Develop has changes that conflict with main.

**Solution:**

```bash
# Check conflict files
git status

# Resolve conflicts (favor main/release changes)
git checkout --theirs [conflicting-file]  # Use main version
# OR manually resolve

git add [resolved-files]
git commit
git push origin develop
```

---

### Issue: Cannot Delete Branch (In Use)

**Cause:** Currently on the release branch.

**Solution:**

```bash
git checkout main  # Or develop
git branch -d release/vX.Y.Z
```

---

### Issue: GitHub Release Creation Failed

**Cause:** Permissions, network, or CLI issues.

**Solution:**

1. **Manual creation:**
   - Go to: `https://github.com/[owner]/[repo]/releases/new`
   - Select existing tag: `vX.Y.Z`
   - Add title and release notes
   - Publish

2. **Retry with CLI:**
   ```bash
   gh auth status  # Verify authentication
   gh release create vX.Y.Z --title "vX.Y.Z" --notes "Release notes..."
   ```

---

## Tips

### Before Running

- Ensure release PR is merged
- Have write access to repository
- Verify `gh` CLI is authenticated

### During Execution

- Watch for merge conflicts
- Verify tag creation before pushing
- Check GitHub release preview before publishing

### After Completion

- Verify tag appears in GitHub
- Check release notes render correctly
- Monitor for any immediate issues

---

## Integration with Other Commands

### Complete Release Workflow

```
1. /release-prep vX.Y.Z      - Create draft documents
2. [Review drafts]
3. /release-finalize vX.Y.Z  - Finalize documents
4. /pr --release vX.Y.Z      - Create PR to main
5. [Review and merge PR]
6. /post-release vX.Y.Z      - Tag, merge, release, cleanup  ◄── This command
```

### Related Commands

- **`/release-prep`** - Create release draft documents
- **`/release-finalize`** - Finalize release documents
- **`/pr --release`** - Create release PR to main

---

## Quick Reference

**Minimal usage:**

```bash
/post-release v0.1.0
```

**Skip GitHub release:**

```bash
/post-release v0.1.0 --skip-github-release
```

**Preview only:**

```bash
/post-release v0.1.0 --dry-run
```

**With specific PR:**

```bash
/post-release v0.1.0 --pr 7
```

---

**Last Updated:** 2025-12-18  
**Status:** ✅ Active  
**Next:** Use after merging release PR to main
