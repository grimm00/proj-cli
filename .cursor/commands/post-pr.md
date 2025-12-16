# Post-PR Documentation Update Command

Use this command after a PR is merged to update all relevant documentation. This ensures phase completion status, feature milestones, and next steps are properly documented.

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns, matching `/task-phase` and `/pr`:

1. **Feature-Specific Structure (default):**
   - Phase paths: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Status document: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Fix paths: `docs/maintainers/planning/features/[feature-name]/fix/pr##/`
   - Manual testing: `docs/maintainers/planning/features/[feature-name]/manual-testing.md`

2. **Project-Wide Structure:**
   - Phase paths: `docs/maintainers/planning/phases/phase-N.md`
   - Status document: `docs/maintainers/planning/status-and-next-steps.md` (if exists)
   - Fix paths: `docs/maintainers/planning/fix/pr##/`
   - Manual testing: `docs/maintainers/planning/manual-testing.md` (if exists)

**Feature Detection:**

- Use `--feature` option if provided
- Otherwise, auto-detect using same logic as other commands:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for phase/fix structure in each
  - If no features exist, use project-wide structure

**Release Paths:**

- Release planning: `docs/maintainers/planning/releases/[version]/`
- Transition plan: `docs/maintainers/planning/releases/[version]/transition-plan.md`
- Release notes: `docs/maintainers/planning/releases/[version]/release-notes.md`

---

## Workflow Overview

**When to use:**

- After PR is merged to `develop`
- Before starting next phase
- To ensure documentation stays in sync with code

**Key principle:** Documentation updates happen in a separate `docs` branch, then merged directly to `develop` (no PR needed for docs-only changes).

---

## Usage

**Command:** `/post-pr [pr-number] [--phase|--fix|--release] [identifier] [options]`

**Examples:**

- `/post-pr 10 --phase 3` - Update docs after PR #10 (Phase 3) merge
- `/post-pr 11 --phase 4` - Update docs after PR #11 (Phase 4) merge
- `/post-pr 12 --fix pr12-batch-medium-low-01` - Update docs after fix PR merge
- `/post-pr 36 --release v0.1.0` - Update docs after release PR merge
- `/post-pr 10 --phase 3 --feature my-feature` - Specify feature name

**Options:**

- `--feature [name]` - Specify feature name (overrides auto-detection)

---

## Step-by-Step Process

### Mode Selection

**Determine mode:**

- `--phase` flag → Phase mode (default for backward compatibility)
- `--fix` flag → Fix mode
- `--release` flag → Release mode
- No flag with old format `[pr-number] [phase-number]` → Phase mode (backward compatibility)

**Checklist:**

- [ ] Mode determined
- [ ] Identifier provided (phase number, batch name, or version)
- [ ] PR number provided

---

### 1. Validate Inputs

**Check before proceeding:**

- [ ] PR number is valid (check GitHub)
- [ ] Identifier is valid (phase document, fix plan, or release transition plan exists)
- [ ] PR is merged to `develop` (or user confirms it will be merged)
- [ ] Current branch is `develop` (or can switch to it)

**Validation commands:**

```bash
# Check current branch
git branch --show-current

# Verify PR is merged (check GitHub or git log)
gh pr view [pr-number] --json merged
```

---

### 2. Create Docs Branch

**Branch naming:**

- Phase mode: `docs/post-pr##-phase##-complete`
- Fix mode: `docs/post-pr##-fix-[batch-name]-complete`
- Release mode: `docs/post-pr##-release-[version]-complete`

**Examples:**

- `docs/post-pr10-phase3-complete` (Phase mode)
- `docs/post-pr12-fix-pr12-batch-medium-low-01-complete` (Fix mode)
- `docs/post-pr36-release-v0.1.0-complete` (Release mode)

**Steps:**

```bash
# Ensure we're on develop
git checkout develop
git pull origin develop

# Create docs branch
git checkout -b docs/post-pr[##]-phase[##]-complete
```

**Checklist:**

- [ ] Branch created from `develop`
- [ ] Branch name follows convention
- [ ] Local `develop` is up-to-date with remote

---

### 3. Update Phase Document (Phase Mode)

**Detect feature name:**

- Use `--feature` option if provided
- Otherwise, auto-detect using same logic as `/task-phase`:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for phase documents in each
  - If no features exist, use project-wide structure

**File:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

**Updates to make:**

1. **Status Field**
   - Change from current status to: `**Status:** ✅ Complete`
   - If already marked complete, verify it's correct

2. **Completion Date**
   - Add completion date if not present
   - Format: `**Completed:** YYYY-MM-DD`
   - Use today's date

3. **Verify Tasks**
   - Check all task checkboxes are marked: `- [x]`
   - If any are incomplete, note them (shouldn't happen if PR merged)

4. **Last Updated**
   - Update `**Last Updated:**` field to today's date

**Example updates:**

```markdown
**Phase:** 3 - Projects API - Delete & Archive (Backend + CLI)  
**Duration:** 1 day  
**Status:** ✅ Complete  
**Completed:** 2025-12-04
**Prerequisites:** Phase 2 complete
```

**Checklist:**

- [ ] Feature name detected or specified
- [ ] Phase document found
- [ ] Status marked as complete
- [ ] Completion date added
- [ ] All tasks verified complete
- [ ] Last Updated date refreshed

---

### 4. Update Feature Status Document (Phase Mode)

**File:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
- Project-wide: `docs/maintainers/planning/status-and-next-steps.md` (if exists)

**Updates to make:**

1. **Current Phase Field**
   - Update to reflect completed phase
   - Example: `**Current Phase:** Phase 3 Complete`

2. **Overall Progress**
   - Calculate new percentage
   - Format: `X/[total] phases complete (XX%)`
   - Example: `3/8 phases complete (37.5%)`

3. **Completed Milestones Section**
   - Add new entry for completed phase
   - Include PR number
   - Include completion date
   - Brief summary of what was accomplished

4. **What's Happening Now**
   - Update to reflect current state
   - Mark completed phase with ✅
   - Update next phase status

5. **Immediate Next Steps**
   - Update to next phase
   - Remove completed phase items
   - Add next phase tasks

6. **Progress Tracking Table**
   - Update phase row status to "✅ Complete"
   - Add end date
   - Calculate duration

7. **Last Updated**
   - Update to today's date

**Example milestone entry:**

```markdown
- ✅ **Phase 3: Delete & Archive Complete** (2025-12-04)
  - DELETE /api/projects/<id> endpoint implemented
  - PUT /api/projects/<id>/archive endpoint implemented
  - CLI `proj delete` and `proj archive` commands added
  - 49 tests passing with 92% coverage
  - Merged via PR #10
```

**Checklist:**

- [ ] Current phase updated
- [ ] Progress percentage calculated
- [ ] Milestone entry added
- [ ] Next steps updated
- [ ] Progress table updated
- [ ] Last Updated refreshed

---

### 5. Document Deferred Issues (Phase Mode)

**IMPORTANT:** Always check for deferred issues, even if none exist. This ensures tracking is complete.

**Detect feature name:**

- Use same feature detection as phase document update

**Process:**

1. **Check Sourcery Review File**
   - Location: `docs/maintainers/feedback/sourcery/pr##.md`
   - Review priority matrix for all comments
   - Identify MEDIUM/LOW priority issues that were deferred

2. **Create/Update PR Directory**
   - Create PR directory if it doesn't exist:
     - Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/pr##/`
     - Project-wide: `docs/maintainers/planning/fix/pr##/`
   - Create or update PR hub:
     - Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/pr##/README.md`
     - Project-wide: `docs/maintainers/planning/fix/pr##/README.md`

3. **If Deferred Issues Exist:**
   - Add deferred issues section to PR hub README.md
   - Include date, review source, and status
   - List each deferred issue with:
     - Comment number (e.g., PR12-#1)
     - Brief description
     - Priority and effort levels
     - Action plan (deferred to next phase, future PR, etc.)
   - Update main fix tracking README.md to link to PR hub

4. **If No Deferred Issues:**
   - Note in PR hub that review was checked
   - All issues were CRITICAL/HIGH and addressed, or no issues found
   - Update main fix tracking README.md

**PR Hub Entry (with deferred issues):**

**File:** `docs/maintainers/planning/features/[feature-name]/fix/pr##/README.md`  
**OR:** `docs/maintainers/planning/fix/pr##/README.md` (project-wide)

```markdown
## 📋 Deferred Issues

**Date:** 2025-12-04  
**Review:** PR #12 (Phase 4) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

**Deferred Issues:**

- **PR12-#1:** Use `click.Choice` for CLI validation (MEDIUM priority, LOW effort) - Improves UX by catching invalid values early
- **PR12-#2:** Tighten test expectations for invalid status (MEDIUM priority, LOW effort) - Test quality improvement
- **PR12-#3:** Avoid conditionals in tests (MEDIUM priority, MEDIUM effort) - Code quality improvement, requires test refactoring
- **PR12-#4:** Use named expression (LOW priority, LOW effort) - Minor code quality improvement
- **PR12-#5:** Raise from previous error (LOW priority, LOW effort) - Minor code quality improvement

**Action Plan:** These can be handled opportunistically during future phases or in a dedicated code quality improvement PR.
```

**PR Hub Entry (no deferred issues):**

```markdown
## 📋 Deferred Issues

**Date:** YYYY-MM-DD  
**Review:** PR #N (Phase N) Sourcery feedback  
**Status:** ✅ **NONE** - All issues were CRITICAL/HIGH priority and addressed in PR, or no issues found
```

**Update Main Fix Tracking:**

**File:** 
- Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/README.md`
- Project-wide: `docs/maintainers/planning/fix/README.md`

Add PR to active PRs section (if not already there):

```markdown
### Active PRs

- **[PR ##](pr##/README.md)** - [PR Title] ([Status])
```

**Checklist:**

- [ ] Feature name detected or specified
- [ ] PR directory created (if needed)
- [ ] PR hub README.md created/updated
- [ ] Sourcery review file checked for deferred issues
- [ ] Deferred issues section added to PR hub (if issues exist)
- [ ] Each issue documented with priority, effort, and action plan
- [ ] No deferred issues noted in PR hub (if none exist)
- [ ] Main fix tracking README.md updated with PR link

---

### 6. Update Fix Plan Status (Fix Mode)

**Detect feature name:**

- Use `--feature` option if provided
- Otherwise, auto-detect using same logic as `/fix-implement`:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for fix structure in each
  - If no features exist, use project-wide structure

**For PR-Specific Batches:**

**File:** 
- Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/pr##/[batch-name].md`
- Project-wide: `docs/maintainers/planning/fix/pr##/[batch-name].md`

**Updates:**

- Mark batch as complete
- Add completion date
- Add PR number reference

**For Cross-PR Batches:**

**File:**
- Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/cross-pr/[batch-name].md`
- Project-wide: `docs/maintainers/planning/fix/cross-pr/[batch-name].md`

**Updates:**

- Mark batch as complete
- Add completion date
- Add PR number reference
- Update source PR review files

**Checklist:**

- [ ] Feature name detected or specified
- [ ] Fix plan found
- [ ] Batch marked as complete
- [ ] Completion date added
- [ ] PR number referenced

---

### 7. Update Release Documentation (Release Mode)

**File:** `docs/maintainers/planning/releases/[version]/transition-plan.md`

**Updates:**

- Mark release steps as complete
- Update release status
- Add completion date
- Update release notes status

**Checklist:**

- [ ] Transition plan found
- [ ] Release steps marked complete
- [ ] Release status updated
- [ ] Completion date added

---

### 8. Commit Changes

**Commit message format:**

**Phase Mode:**

```
docs(phase-N): update post-merge documentation

Post-PR #N documentation updates:
- Mark Phase N as complete with date
- Update feature status milestones
- Update progress to X/[total] phases (XX%)
- Update next steps to Phase N+1
- Document deferred issues (if any)

Related: PR #N
```

**Fix Mode:**

```
docs(fix): update post-merge documentation

Post-PR #N documentation updates:
- Mark fix batch [batch-name] as complete
- Update fix tracking status
- Document completion date

Related: PR #N
```

**Release Mode:**

```
docs(release): update post-merge documentation

Post-PR #N documentation updates:
- Mark release [version] steps as complete
- Update release status
- Document completion date

Related: PR #N
```

**Steps:**

```bash
# Stage all documentation changes
git add docs/

# Commit with proper message
git commit -m "docs(phase-N): update post-merge documentation

Post-PR #N documentation updates:
- Mark Phase N as complete with date
- Update feature status milestones
- Update progress to X/[total] phases (XX%)
- Update next steps to Phase N+1
- Document deferred issues (if any)

Related: PR #N"
```

**Checklist:**

- [ ] All relevant files staged
- [ ] Commit message follows conventional format
- [ ] PR number included in commit body

---

### 9. Merge Directly to Develop

**Since this is documentation-only, merge directly to develop (no PR needed):**

```bash
# Switch to develop
git checkout develop
git pull origin develop

# Merge docs branch
git merge docs/post-pr[##]-phase[##]-complete --no-edit

# Push to remote
git push origin develop

# Clean up local branch
git branch -d docs/post-pr[##]-phase[##]-complete

# Clean up remote branch
git push origin --delete docs/post-pr[##]-phase[##]-complete
```

**Checklist:**

- [ ] Merged to `develop` locally
- [ ] Pushed to remote `develop`
- [ ] Local branch deleted
- [ ] Remote branch deleted

**Note:** Documentation-only changes can be merged directly to `develop` without a PR, following Git Flow pattern for `docs/*` branches.

---

### 10. Clean Up Merged PR Branch

**IMPORTANT:** Clean up the merged PR branch (both local and remote) to keep repository clean.

**Process:**

1. **Verify PR is merged:**
   ```bash
   gh pr view [pr-number] --json state,mergedAt
   ```
   - Should show `state: "MERGED"` and `mergedAt` timestamp

2. **Check if branch exists locally:**
   ```bash
   git branch --list [branch-name]
   ```

3. **Check if branch exists remotely:**
   ```bash
   git branch -r --list origin/[branch-name]
   ```

4. **Delete local branch (if exists):**
   ```bash
   # Try normal delete first (only works if merged locally)
   git branch -d [branch-name]
   
   # If that fails (branch merged via GitHub, not locally), force delete
   # This is safe if PR is confirmed merged on GitHub
   git branch -D [branch-name]
   ```
   
   **Note:** If branch was merged via GitHub PR (not locally), `git branch -d` may fail even though the branch is merged. Use `git branch -D` in this case, but only after confirming PR is merged on GitHub.

5. **Delete remote branch (if exists):**
   ```bash
   git push origin --delete [branch-name]
   ```

**Branch naming patterns:**

- Feature branches: `feat/phase-N-[description]` or `feat/[feature-name]-phase-N-[description]`
- Fix branches: `fix/[description]` or `fix/[batch-name]`
- Docs branches: `docs/[description]`

**Example cleanup:**

```bash
# For PR #12 (feat/phase-4-search-filter)
git branch -d feat/phase-4-search-filter
git push origin --delete feat/phase-4-search-filter

# For PR #13 (fix/pr12-batch-medium-medium-01)
git branch -d fix/pr12-batch-medium-medium-01
git push origin --delete fix/pr12-batch-medium-medium-01
```

**Safety checks:**

- Only delete branches that are merged
- Verify branch name matches PR head branch
- Check that branch is not currently checked out
- Confirm deletion before proceeding

**Checklist:**

- [ ] PR verified as merged
- [ ] Local branch deleted (if existed)
- [ ] Remote branch deleted (if existed)
- [ ] No errors during cleanup

---

## Auto-Detection Features

### Detect Next Phase

**Logic:**

- Current phase number + 1
- Check if phase document exists:
  - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
  - Project-wide: `docs/maintainers/planning/phases/phase-N.md`
- If last phase, note completion

**Example:**

- Phase 3 complete → Next: Phase 4
- Phase 8 complete → Next: MVP Complete

### Calculate Progress

**Formula:**

- Completed phases / Total phases × 100
- Total phases: Count from feature plan or phase documents
- Round to 1 decimal place

**Example:**

- 3 phases complete, 8 total → 3/8 = 37.5%
- 5 phases complete, 8 total → 5/8 = 62.5%

### Find Phase Document

**Path pattern:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`
- Verify file exists before updating

---

## Validation Checks

### Before Starting

- [ ] PR number is valid (exists in GitHub)
- [ ] Phase/fix/release identifier is valid (document exists)
- [ ] PR is merged (or user confirms merge)
- [ ] Current branch is `develop` or can switch

### During Updates

- [ ] Phase/fix/release document exists and is readable
- [ ] Status document exists and is readable (if applicable)
- [ ] Fix tracking document exists and is readable (if applicable)
- [ ] Sourcery review file checked for deferred issues
- [ ] All required fields can be updated
- [ ] No conflicting changes in files

### After Updates

- [ ] All files updated correctly
- [ ] Dates are correct (today's date)
- [ ] Progress percentage is accurate
- [ ] Next phase is correct (if applicable)
- [ ] Commit message is proper
- [ ] Merged PR branch cleaned up (local and remote)

---

## Error Handling

### Missing Files

**If phase document doesn't exist:**

- Error: "Phase N document not found at [path]"
- Suggest: Check phase number or create document first

**If status document doesn't exist:**

- Error: "Status document not found at [path]"
- Suggest: Check feature directory structure or create document

### Invalid PR Number

**If PR doesn't exist:**

- Error: "PR #N not found"
- Suggest: Verify PR number or check if merged

### Branch Conflicts

**If branch already exists:**

- Error: "Branch docs/post-pr##-phase##-complete already exists"
- Options:
  - Use existing branch
  - Delete and recreate
  - Use different branch name

### Merge Conflicts

**If conflicts when merging:**

- Resolve conflicts manually
- Re-commit resolved files
- Continue with merge

---

## Integration with Other Commands

### Command Sequence

**Complete workflow:**

1. `/task-phase` - Implement phase tasks
2. `/pr --phase [N]` - Complete phase and create PR
3. PR merged (manual GitHub action)
4. `/post-pr --phase [N]` - Update documentation ← **You are here**
5. `/int-opp` - Capture phase learnings (optional)

### Related Commands

- **`/task-phase`** - Phase task implementation
- **`/pr --phase [N]`** - Phase completion and PR workflow
- **`/pr --fix [batch-name]`** - Fix batch PR workflow
- **`/pr --release [version]`** - Release PR workflow
- **`/post-pr`** - Post-merge documentation updates (this command)
- **`/int-opp`** - Document phase learnings (run after post-pr)

---

## Common Scenarios

### Scenario 1: Standard Phase Completion

**Situation:** Phase 3 complete, PR #10 merged

**Steps:**

1. Run `/post-pr 10 --phase 3`
2. Updates phase-3.md (mark complete, add date)
3. Updates status-and-next-steps.md (milestone, progress, next steps)
4. Creates docs branch and commits
5. Merge docs branch to develop
6. Clean up merged PR branch

**Result:** Documentation reflects Phase 3 completion, ready for Phase 4

---

### Scenario 2: Phase with Deferred Issues

**Situation:** Phase 4 complete, PR #12 had deferred MEDIUM/LOW issues

**Steps:**

1. Run `/post-pr 12 --phase 4`
2. Updates phase and status documents
3. Checks Sourcery review file (`pr12.md`)
4. Updates fix tracking with deferred issues section
5. Documents all deferred issues with priority/effort
6. Notes action plan (opportunistic handling)

**Result:** Documentation complete, deferred issues tracked for future handling

---

### Scenario 3: Fix Batch Completion

**Situation:** Fix batch complete, PR #15 merged

**Steps:**

1. Run `/post-pr 15 --fix pr12-batch-medium-low-01`
2. Updates fix plan status
3. Marks batch as complete
4. Updates fix tracking hubs

**Result:** Fix batch documentation complete

---

## Status Update Behavior

**What `/post-pr` Updates:**

### Phase Mode Status Updates

**Phase Document:**
- Updates status field to "✅ Complete"
- Adds completion date if not present
- Verifies all task checkboxes are marked complete
- Updates "Last Updated" field

**Feature Status Document:**
- Updates current phase field
- Calculates and updates overall progress percentage
- Adds completed milestone entry with PR number and date
- Updates "What's Happening Now" section
- Updates "Immediate Next Steps" section
- Updates progress tracking table (phase row status, end date, duration)
- Updates "Last Updated" field

### Fix Mode Status Updates

**Fix Plan:**
- Updates fix plan status
- Marks batch as complete
- Updates fix tracking hubs

### Release Mode Status Updates

**Release Documentation:**
- Updates release status
- Updates release notes status

**When `/post-pr` Updates Status:**

- **After PR Merge:** `/post-pr` should be run immediately after PR is merged to `develop`
- **Before Next Phase:** Run `/post-pr` before starting the next phase to ensure documentation is current
- **As Part of Workflow:** `/post-pr` is part of the standard PR workflow (see step 8 in PR Review Workflow)

**Status Update Examples:**

**Example 1: Phase Completion**
```bash
# After PR #10 (Phase 3) is merged
/post-pr 10 --phase 3

# Updates:
# - phase-3.md: Status → "✅ Complete", Completed → "2025-12-07"
# - status-and-next-steps.md: Phase 3 marked complete, progress updated
```

**Example 2: Feature Status Update**
```markdown
# Before /post-pr:
**Current Phase:** Phase 3 - Documentation & Examples
**Progress:** 50% (2 of 4 phases complete)

# After /post-pr:
**Current Phase:** Phase 3 Complete
**Progress:** 75% (3 of 4 phases complete)

**Completed Milestones:**
- Phase 3: Documentation & Examples ✅ (PR #10, 2025-12-07)
```

**Example 3: Progress Tracking Update**
```markdown
# Before /post-pr:
| Phase | Status | Start Date | End Date | Duration |
|-------|--------|------------|----------|----------|
| Phase 3 | 🟠 In Progress | 2025-12-06 | - | - |

# After /post-pr:
| Phase | Status | Start Date | End Date | Duration |
|-------|--------|------------|----------|----------|
| Phase 3 | ✅ Complete | 2025-12-06 | 2025-12-07 | 1 day |
```

**Consistency Requirements:**

- **Always Run After PR Merge:** `/post-pr` should be run consistently after every PR merge
- **Before Next Phase:** Ensure `/post-pr` is run before starting the next phase
- **Part of Standard Workflow:** `/post-pr` is step 8 in the PR Review Workflow (see workflow rules)

**See Also:**
- [Status Update Workflow](../../docs/STATUS-UPDATE-WORKFLOW.md) - Complete status update guide
- [Status Update Checklist](../../docs/STATUS-UPDATE-CHECKLIST.md) - Checklist for status updates
- [Status Update Timing](../../docs/STATUS-UPDATE-TIMING.md) - Timing and frequency guide

---

## Tips

### Before Running Command

- Verify PR is actually merged (check GitHub)
- Ensure `develop` branch is up-to-date
- Have PR number and identifier ready
- Check if any special updates needed (deferred issues, etc.)

### During Updates

- Review each file change before committing
- Verify dates are correct (today's date)
- Double-check progress percentage calculation
- Ensure next phase number is correct
- Check Sourcery review for deferred issues
- Document deferred issues even if none exist (note "NONE")

### After Updates

- Review commit message before committing
- Verify all files updated correctly
- Check that next phase is ready to start
- Clean up merged PR branch (local and remote)
- Consider running `/int-opp` to capture learnings

---

## Reference

**Phase Documents:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

**Feature Planning:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
- Feature-specific: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
- Project-wide: `docs/maintainers/planning/status-and-next-steps.md` (if exists)

**Fix Tracking:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/fix/README.md`
- Project-wide: `docs/maintainers/planning/fix/README.md`

**Release Planning:**

- `docs/maintainers/planning/releases/[version]/transition-plan.md`
- `docs/maintainers/planning/releases/[version]/release-notes.md`

**Related Commands:**

- `/task-phase` - Phase task implementation
- `/pr --phase [N]` - Phase completion and PR workflow
- `/pr --fix [batch-name]` - Fix batch PR workflow
- `/pr --release [version]` - Release PR workflow
- `/post-pr` - Post-merge documentation updates (this command)
- `/int-opp` - Document phase learnings

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use after each PR merge to keep documentation current (supports phase, fix, and release modes, feature-specific and project-wide structures)

