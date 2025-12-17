# PR Validation & Review Command

Use this command when a PR is already open to run manual testing, update documentation, and perform code review in one workflow.

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns, matching `/pr` and `/post-pr`:

1. **Feature-Specific Structure (default):**
   - Manual testing: `docs/maintainers/planning/features/[feature-name]/manual-testing.md`
   - Phase documents: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Sourcery reviews: `docs/maintainers/feedback/sourcery/pr##.md`

2. **Project-Wide Structure:**
   - Manual testing: `docs/maintainers/planning/manual-testing.md` (if exists)
   - Phase documents: `docs/maintainers/planning/phases/phase-N.md`
   - Sourcery reviews: `docs/maintainers/feedback/sourcery/pr##.md`

**Feature Detection:**

- Auto-detect from PR branch name or phase number
- Use `--feature` option if provided
- Otherwise, detect using same logic as other commands:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for phase/manual testing structure
  - If no features exist, use project-wide structure

**Sourcery Review:**

- Review tool: `dt-review` (REQUIRED - always run this tool)
- Review output: `docs/maintainers/feedback/sourcery/pr##.md`
- **IMPORTANT:** Always run `dt-review` explicitly - do NOT assume GitHub's Sourcery integration check is sufficient

---

## Workflow Overview

**When to use:**

- PR is already created and open
- Need to validate features with manual testing
- Need to run Sourcery review (dt-review, if available)
- Want to update manual testing guide with scenarios

**Key principle:** Combines manual testing execution, documentation updates, and code review into a single workflow.

---

## Usage

**Command:** `/pr-validation [pr-number] [phase-number] [options]`

**Examples:**

- `/pr-validation 12 4` - Validate PR #12 for Phase 4
- `/pr-validation 10 3` - Validate PR #10 for Phase 3
- `/pr-validation 12 4 --feature my-feature` - Specify feature name

**Options:**

- `--feature [name]` - Specify feature name (overrides auto-detection)
- `--skip-manual-testing` - Skip manual testing (auto-detected for non-feature PRs)
- `--force-manual-testing` - Force manual testing even for non-feature PRs

**Note:** There is no `--skip-review` option. Sourcery review via `dt-review` is REQUIRED.

---

## Step-by-Step Process

### 1. Verify PR Status

**Check PR exists and is open:**

```bash
gh pr view [pr-number] --json state,title,headRefName
```

**Expected:**

- PR state: `OPEN`
- PR title matches phase/fix/release
- Head branch exists

**Checklist:**

- [ ] PR exists and is open
- [ ] PR number is valid
- [ ] Head branch accessible

---

### 1a. Restore Unrelated Files (Cursor IDE Bug Fix)

**Issue:** Cursor IDE may modify unrelated files when opening them. These should be restored before proceeding.

**Process:**

1. **Check modified files:**
   ```bash
   git status --short
   ```

2. **Identify phase/fix-related files:**
   - Review what files should actually be modified for this PR
   - Keep only files that are part of the implementation

3. **Restore unrelated files:**
   ```bash
   # Restore all unrelated files (adjust paths as needed)
   git restore [unrelated-file-1] [unrelated-file-2] ...
   
   # Or restore all modified files except phase-specific ones
   git restore $(git diff --name-only | grep -v "phase-[N]\.md\|[relevant-files]")
   ```

4. **Verify only relevant files remain:**
   ```bash
   git status --short
   ```

**Common unrelated files to restore:**

- `__init__.py` files (often just whitespace changes)
- Documentation files unrelated to the PR
- Frontend files (if backend PR)
- Config files (`.gitignore`, `pytest.ini`, `requirements.txt`) unless actually changed

**After restoration:**

- [ ] Only PR-related files remain modified
- [ ] No accidental changes to unrelated code
- [ ] Ready to proceed with validation

---

### 1b. Status Validation (NEW)

**Purpose:** Verify that phase and feature status documents are current before proceeding with PR validation. This ensures status updates happen during work, not just at PR creation time.

**When to check:**
- Before proceeding with manual testing
- After PR is verified to be open
- As part of PR validation workflow

**Status Check Process:**

1. **Detect feature name:**
   - Use `--feature` option if provided
   - Otherwise, auto-detect from PR branch name or phase number:
     - Check if `docs/maintainers/planning/features/` exists
     - If single feature exists, use that feature name
     - If multiple features exist, search for phase documents
     - If no features exist, use project-wide structure

2. **Read phase document:**
   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`
   - Check status field at top of document
   - Verify all task checkboxes are marked complete
   - Verify status matches actual work completed

3. **Read feature status document (if applicable):**
   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Project-wide: `docs/maintainers/planning/status-and-next-steps.md` (if exists)
   - Check phase completion status
   - Verify progress tracking is current
   - Verify next steps are accurate

4. **Validate consistency:**
   - Phase document status matches feature status
   - Progress percentages are accurate
   - No discrepancies between documents

**Status Validation Checklist:**

- [ ] Phase document status is current
  - Location: `docs/maintainers/planning/features/[feature-name]/phase-N.md` or `docs/maintainers/planning/phases/phase-N.md`
  - Verify: Status reflects actual completion state
  - Expected: `**Status:** ✅ Complete` (if phase is complete) or `**Status:** 🟠 In Progress` (if still in progress)
- [ ] Feature status document is current (if applicable)
  - Location: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
  - Verify: Phase marked appropriately, progress updated
  - Expected: Phase status matches phase document
- [ ] Progress tracking is accurate
  - Verify: Progress percentages reflect actual completion
  - Verify: Task checkboxes match completed work
  - Verify: No outdated status indicators

**Status Check Examples:**

**Phase Document:**
```markdown
**Status:** ✅ Complete  # Should match actual completion state
```

**Feature Status Document:**
```markdown
**Phase 3: Documentation & Examples**
- [x] Dependency sections added ✅ (2025-12-07)
- [x] Dependency documentation created ✅ (2025-12-07)
- Status: ✅ Complete
```

**If status is not current:**

**Warning (Lenient Approach):**
- ⚠️ **Warning:** Status documents may be outdated
- ⚠️ **Recommendation:** Update status documents before proceeding
- ⚠️ **Note:** This is a warning, not a blocker - validation can continue
- Document the warning in the summary report
- Suggest updating status documents

**Action Items (if status outdated):**
- [ ] Update phase document status if needed
- [ ] Update feature status document if needed
- [ ] Commit status updates if made
- [ ] Note status update in PR description

**Note:** This validation uses a **lenient approach** (warnings, not blockers) to start. Validation strictness can be tightened based on feedback from real PR usage.

**Checklist:**

- [ ] Feature name detected or specified
- [ ] Phase document found and read
- [ ] Feature status document found and read (if applicable)
- [ ] Status documents validated
- [ ] Warnings documented if status outdated
- [ ] Ready to proceed with validation

---

### 1c. Check GitHub Actions/CI-CD Status (NEW)

**Purpose:** Verify that all GitHub Actions workflows and CI/CD jobs are passing before proceeding with PR validation.

**Process:**

1. **Check GitHub Actions status for PR:**

   ```bash
   gh pr checks [pr-number]
   ```

2. **Get detailed check information:**

   ```bash
   gh pr checks [pr-number] --json name,state,url
   ```

3. **Check required checks:**

   ```bash
   gh pr view [pr-number] --json mergeable,mergeStateStatus
   ```

**CI/CD Status Validation:**

- [ ] All GitHub Actions checks passing
- [ ] No failed CI/CD jobs
- [ ] Required checks passing

**If checks are failing:**

- ⚠️ **Warning:** Some CI/CD checks are failing
- ⚠️ **Recommendation:** Address failing checks before merge
- Document the warning in the summary report
- List failed checks and their URLs

---

### 1d. Determine Manual Testing Applicability (NEW)

**Purpose:** Automatically determine if this PR requires manual testing based on PR type, branch name, and file changes.

**When manual testing IS required:**

| PR Type | Branch Pattern | Requires Manual Testing |
|---------|----------------|------------------------|
| Feature (new functionality) | `feat/*` | ✅ Yes |
| Feature (phase work) | `feat/*-phase-*` | ✅ Yes |
| Fix (user-facing) | `fix/*` with UI/API changes | ✅ Yes |
| Script/Command changes | Any with `scripts/` changes | ✅ Yes |

**When manual testing is NOT required:**

| PR Type | Branch Pattern | Requires Manual Testing |
|---------|----------------|------------------------|
| Documentation only | `docs/*` | ❌ No |
| Chore/maintenance | `chore/*` | ❌ No |
| CI/CD changes | `ci/*` | ❌ No |
| Refactoring | `refactor/*` | ❌ No |

**Detection Process:**

1. **Extract branch type from PR head branch:**
   ```bash
   gh pr view [pr-number] --json headRefName --jq '.headRefName'
   ```

2. **Identify branch type:**
   - `feat/*` → Feature PR (requires testing)
   - `fix/*` → Fix PR (check file changes)
   - `docs/*` → Documentation PR (skip testing)
   - `chore/*` → Chore PR (skip testing)
   - `ci/*` → CI/CD PR (skip testing)

3. **Make determination:**
   - **Requires manual testing:** Proceed to Step 2
   - **Does NOT require manual testing:** Skip to Step 4 (Sourcery Review)

**Checklist:**

- [ ] Branch type identified
- [ ] File changes analyzed (if feat/fix)
- [ ] Manual testing determination made
- [ ] User informed of determination

---

### 2. Update Manual Testing Guide (CONDITIONAL)

**Applicability:** This step is **conditional** based on Step 1d determination.

- **If manual testing required:** Proceed with this step
- **If manual testing NOT required:** Skip to Step 4 (Sourcery Review)
- **If `--force-manual-testing` provided:** Proceed regardless
- **If `--skip-manual-testing` provided:** Skip to Step 4

---

#### ⚠️ IMPORTANT: Manual Testing Guides Are for HUMAN Users

**Manual testing guides are written for HUMAN team members to follow, NOT for the AI agent to run tests locally.**

**Purpose of manual testing guides:**
- 📖 **Documentation for humans** - Step-by-step instructions anyone can follow
- 🔍 **User verification** - Allows humans to manually verify features work as expected
- 📝 **Reference material** - Persists in the repo as a testing reference
- 🎓 **Knowledge transfer** - New team members can understand how to test

**Manual testing guides are NOT:**
- ❌ Tests the AI agent runs during PR validation
- ❌ A checklist only the AI uses internally
- ❌ Automated test scripts (those go in `tests/`)

---

#### 2a. Check if Manual Testing Guide Exists

**File locations:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/manual-testing.md`
- Project-wide: `docs/maintainers/planning/manual-testing.md` (if exists)

**Check if guide exists:**

```bash
ls docs/maintainers/planning/features/[feature-name]/manual-testing.md
```

**If guide does NOT exist:**

1. **STOP and create the guide first** - A feature PR with user-facing changes MUST have a manual testing guide
2. **Create the guide using the template below** (Section 2b)
3. **Add scenarios for ALL phases completed so far**
4. **Commit the guide to the feature branch** before proceeding

**If guide exists:**

- Proceed to Section 2c (Add scenarios for current phase)

---

#### 2b. Create Manual Testing Guide (If Missing)

**When to create:** When manual testing is required but no guide exists.

**Template:**

```markdown
# Manual Testing Guide - [Feature Name]

**Feature:** [Feature Name]  
**Phases Covered:** [List phases]  
**Last Updated:** [YYYY-MM-DD]  
**Status:** ✅ Active

---

## 📋 Overview

This guide provides step-by-step instructions for manually verifying the [feature name] feature.

**Purpose:**
- Verify user-facing functionality works as expected
- Test edge cases and error handling
- Validate documentation and user experience

**Prerequisites:**
- [List prerequisites]

---

## 🧪 Phase N: [Phase Name]

### Scenario N.1: [Scenario Name]

**Objective:** [What this test verifies]

**Steps:**

1. [Step 1]
2. [Step 2]

**Expected Result:** ✅ [What success looks like]

---

## ✅ Acceptance Criteria Checklist

- [ ] Scenario N.1 passes
- [ ] Scenario N.2 passes

---

**Last Updated:** [YYYY-MM-DD]
```

**Key principles for the guide:**

1. **Write for humans** - Clear, step-by-step instructions
2. **Include context** - Explain what each scenario verifies
3. **Provide cleanup** - Show how to reset after testing
4. **Cover all phases** - Include scenarios for ALL completed phases
5. **Be specific** - Include exact commands and expected outputs

---

#### 2c. Add Scenarios for Current Phase

**Process:**

1. **Review PR changes to identify new features:**
   - Check what endpoints/commands were added/modified
   - Identify all user-facing functionality

2. **Check if scenarios exist:**
   - Search manual testing guide for relevant scenarios
   - Check if all new features are covered

3. **Add missing scenarios:**
   - Use the scenario template below
   - For phase PRs: Add scenarios for all new functionality
   - For fix PRs: Add scenarios if behavior changed

4. **Update header:**
   - Update "Last Updated" date
   - Note which scenarios were added

**Scenario Template:**

````markdown
### Scenario N: [Feature Name] - [Test Type]

**Test:** [Brief description]

**Prerequisites:** [Any setup needed]

**[API/CLI] Test:**

```bash
[Command or curl example]
# Expected: [Expected result]
```

**Verification:**

```bash
[Verification command]
# Expected: [What to verify]
```

**Expected Result:** ✅ [Success criteria]
````

**After updating:**

- [ ] Scenarios added for all new functionality
- [ ] Header updated with date
- [ ] Acceptance criteria updated
- [ ] Scenarios committed to PR branch

---

### 3. Run Manual Testing Scenarios (CONDITIONAL)

**Applicability:** This step is **conditional** - only runs if Step 2 was executed.

- **If manual testing required:** Proceed with this step
- **If manual testing NOT required:** Skip to Step 4 (Sourcery Review)

**Location:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/manual-testing.md`
- Project-wide: `docs/maintainers/planning/manual-testing.md` (if exists)

**Prerequisites:**

- Backend server running (project-specific command)
  - Example: `cd backend && python run.py`
  - Example: `npm start` or project-specific command
- Server accessible (project-specific URL)
  - Example: `http://localhost:5000`
  - Health check: `curl http://localhost:5000/api/health` (or project-specific)

**Process:**

1. **Identify scenarios to test:**
   - Review manual testing guide
   - Find scenarios for this phase/fix
   - Note scenario numbers (e.g., "Scenarios 16-28 for Phase 4")

2. **Run scenarios in order:**
   - Some scenarios depend on previous state
   - Run each scenario completely
   - Document results (✅ pass / ❌ fail)

3. **For each scenario:**

   **API Tests:**
   ```bash
   # Run curl command from scenario
   curl [endpoint] [options]
   
   # Verify response matches expected
   # Check status code, JSON structure, values
   ```

   **CLI Tests:**
   ```bash
   # Navigate to CLI directory (project-specific)
   cd [cli-directory]
   
   # Run CLI command from scenario
   [project-cli] [command] [options]
   
   # Verify output matches expected
   # Check formatting, values, error messages
   ```

4. **Document results and check off scenarios:**
   - For each scenario that passes, check off its checkboxes in the manual testing guide
   - Change `- [ ]` to `- [x]` for each verification item that passes
   - Mark "Expected Result:" line with ✅ if all checks pass
   - Note any failures or issues (keep checkboxes unchecked if scenario fails)
   - Update acceptance criteria checklist at the end of the guide

**Common Issues:**

- **Database state:** If scenarios fail due to missing data, check prerequisites
- **Server not running:** Ensure backend is running before testing
- **Port conflicts:** Verify port is available (project-specific)
- **CLI path:** Ensure you're in the correct directory for CLI commands

**After manual testing:**

- [ ] All scenarios passed
- [ ] Checkboxes checked off (`- [ ]` → `- [x]`) for passing scenarios
- [ ] Expected Result lines marked with ✅ for passing scenarios
- [ ] Any failures documented (keep checkboxes unchecked)
- [ ] Acceptance criteria updated
- [ ] Results committed to PR branch

---

### 4. Run Sourcery Review (dt-review) - REQUIRED

**IMPORTANT:** This step is REQUIRED. Always run `dt-review` explicitly.

- Do NOT assume GitHub's Sourcery integration check is sufficient
- The GitHub check only indicates if Sourcery found issues, it does NOT generate the review file
- You MUST run `dt-review` to create the review file and fill out the priority matrix

**Process:**

1. **Navigate to project directory:**

   ```bash
   cd [project-directory]
   ```

2. **Ensure output directory exists:**

   ```bash
   mkdir -p docs/maintainers/feedback/sourcery
   ```

3. **Run review with custom path (ALWAYS RUN THIS):**

   ```bash
   dt-review [pr-number] docs/maintainers/feedback/sourcery/pr##.md
   ```

   **Example:**

   ```bash
   dt-review 19 docs/maintainers/feedback/sourcery/pr19.md
   ```

   **Note:** The `dt-review` command should be available in PATH. If not found, check if dev-toolkit is installed.

4. **Review will be saved directly to:**
   `docs/maintainers/feedback/sourcery/pr##.md`

**Expected:**

- Review file created/updated
- Contains Sourcery comments and suggestions
- Organized by file/line number
- Ready for priority matrix assessment

**If `dt-review` fails:**

- Check if dev-toolkit is installed: `which dt-review`
- Verify PR number is correct
- Check network connectivity
- Document the failure and investigate before proceeding

**Checklist:**

- [ ] `dt-review` command executed (REQUIRED)
- [ ] Review file created
- [ ] Review file committed to PR branch (if on PR branch)

---

### 5. Fill Out Priority Matrix - REQUIRED

**File:** `docs/maintainers/feedback/sourcery/pr##.md`

**IMPORTANT:** This step is REQUIRED after running `dt-review`. Fill out the priority matrix for all comments.

**For each Sourcery comment:**

Add priority assessment after the comment:

```markdown
**Priority:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
**Impact:** CRITICAL 🔴 / HIGH 🟠 / MEDIUM 🟡 / LOW 🟢
**Effort:** LOW 🟢 / MEDIUM 🟡 / HIGH 🟠 / VERY_HIGH 🔴
**Action:** Fix now / Defer to next PR / Document for future
```

**Priority Guidelines:**

**CRITICAL 🔴:**
- Security vulnerabilities
- Data loss risks
- Breaking API changes
- Test failures

**HIGH 🟠:**
- Performance issues
- Code quality problems
- Maintainability concerns
- Missing error handling

**MEDIUM 🟡:**
- Code style improvements
- Refactoring opportunities
- Documentation gaps
- Minor optimizations

**LOW 🟢:**
- Naming suggestions
- Style preferences
- Minor readability improvements
- Optional enhancements

**After priority matrix:**

- [ ] All comments assessed
- [ ] CRITICAL/HIGH items identified
- [ ] Action plan documented
- [ ] Matrix committed to PR branch

---

### 6. Address Critical Issues (If Any)

**If CRITICAL 🔴 or HIGH 🟠 issues found:**

1. **Create fix branch (if not already on PR branch):**
   ```bash
   git checkout [pr-branch-name]
   ```

2. **Implement fixes:**
   - Follow fix plans (if available)
   - Write tests for fixes
   - Run full test suite
   - Commit fixes

3. **Update PR:**
   - Push fixes to PR branch
   - Update PR description with fixes
   - Re-run manual testing if needed

**If only LOW/MEDIUM issues:**

- Document in fix tracking
- Can be deferred to future PR
- Proceed with merge approval

---

### 7. Update PR Description (If Needed)

**If manual testing or review revealed issues:**

Update PR description to include:

- Manual testing results
- Sourcery review summary (if available)
- Critical issues addressed
- Deferred issues documented

**PR Description Updates:**

```markdown
## Testing

- [x] All automated tests passing ([N] tests)
- [x] Coverage: [X]% (maintained/improved)
- [x] Manual testing complete ([N] scenarios)
- [x] Sourcery review complete ([N] comments) (if available)

## Review Summary

**Sourcery Review:** (if available)
- Total comments: [N]
- CRITICAL: [N] (all addressed)
- HIGH: [N] (all addressed)
- MEDIUM: [N] (deferred to next PR)
- LOW: [N] (documented for future)

**Manual Testing:**
- Scenarios tested: [N]
- All scenarios passed: ✅
- Checkboxes checked off: ✅ (all passing scenarios marked)
- Expected Result lines marked: ✅ (all passing scenarios)
- Issues found: [None / List issues]
```

---

### 8. Summary Report

**Present to user:**

```markdown
## PR Validation Complete

**PR:** #[pr-number] - [PR Title]
**PR Type:** [feat/fix/docs/chore/ci]
**Branch:** [branch-name]

### Manual Testing

[If manual testing was required:]
- ✅ Scenarios tested: [N]
- ✅ All scenarios passed
- ✅ Checkboxes checked off for passing scenarios
- ✅ Expected Result lines marked with ✅
- ⚠️ Issues found: [None / List]

[If manual testing was NOT required:]
- ⏭️ Skipped - No new user-facing functionality
- **PR Type:** [docs/chore/ci/refactor]
- **Reason:** [explanation from Step 1d]
- **To test manually:** Re-run with `--force-manual-testing`

### Code Review (Sourcery - REQUIRED)
- ✅ `dt-review` executed
- ✅ Review file created: `docs/maintainers/feedback/sourcery/pr##.md`
- ✅ Priority matrix filled out
- ⚠️ Critical/High issues: [N] (all addressed)
- ⚠️ Deferred issues (Medium/Low): [N]

### Status Validation
- ✅ Status documents validated (or ⚠️ Status warnings documented)
- ✅ Phase status current (or ⚠️ Status update recommended)
- ✅ Feature status current (or ⚠️ Status update recommended)

### Next Steps
- [ ] User review PR changes
- [ ] User approve merge (if ready)
- [ ] Merge PR
- [ ] Run `/post-pr` command for documentation updates
```

---

## Common Issues

### Issue: Manual Testing Scenarios Missing

**Solution:**

- Review PR changes to identify features
- Add scenarios using template from this command
- Ensure scenarios cover all new functionality
- Test at least one scenario to verify format

### Issue: Backend Server Not Running

**Solution:**

```bash
# Project-specific command to start server
# Example: cd backend && python run.py
# Example: npm start
```

Verify with health check (project-specific):

```bash
# Example: curl http://localhost:5000/api/health
```

### Issue: dt-review Not Found

**Solution:**

- The `dt-review` command should be available in PATH
- Try calling it directly: `dt-review [pr-number] [output-path]`
- Verify it's in PATH: `which dt-review`
- If not found, check if dev-toolkit is installed
- **Note:** Missing review is acceptable - workflow continues

### Issue: Sourcery Review File Not Created

**Solution:**

- **This is acceptable** - some PRs may not have reviews available
- Check if review completed successfully
- Verify PR number is correct
- Ensure output directory exists: `mkdir -p docs/maintainers/feedback/sourcery`
- Verify the path parameter is correct: `docs/maintainers/feedback/sourcery/pr##.md`
- Check that you're running from the project directory
- **If review is not available:** Continue without review - this is acceptable for the workflow

### Issue: Manual Testing Fails

**Solution:**

- Check database state (may need to reset, project-specific)
- Verify prerequisites for scenarios
- Check server logs for errors
- Ensure all dependencies installed
- Document failures and fix before proceeding

---

## Checklist Summary

**Before running command:**

- [ ] PR is open and accessible
- [ ] GitHub Actions checks reviewed (NEW)
- [ ] Backend server is running (if applicable, for feat/fix PRs)
- [ ] dev-toolkit is available (REQUIRED for Sourcery review - `which dt-review`)
- [ ] Status documents are current (checked during validation)

**During execution:**

- [ ] GitHub Actions/CI-CD status checked (NEW)
- [ ] Failed checks identified and documented (if any)
- [ ] Status documents validated
- [ ] Status warnings documented (if status outdated)
- [ ] **Manual testing applicability determined (NEW)**
  - [ ] Branch type identified (feat/fix/docs/chore/ci)
  - [ ] File changes analyzed
  - [ ] Determination: Required / Not Required / Skipped
- [ ] Manual testing guide updated with scenarios (IF REQUIRED)
- [ ] All scenarios tested and passed (IF REQUIRED)
- [ ] Checkboxes checked off (`- [ ]` → `- [x]`) for passing scenarios (IF REQUIRED)
- [ ] Expected Result lines marked with ✅ for passing scenarios (IF REQUIRED)
- [ ] `dt-review` executed (REQUIRED)
- [ ] Priority matrix filled out (REQUIRED)
- [ ] Critical issues addressed (if any)

**After execution:**

- [ ] Results documented
- [ ] PR description updated (if needed)
- [ ] Summary presented to user
- [ ] Ready for user review/approval

---

## Tips

**Manual Testing:**

- Run scenarios in order (some depend on previous state)
- Document results immediately
- Take screenshots if helpful
- Note any unexpected behavior

**Code Review (Sourcery - REQUIRED):**

- ALWAYS run `dt-review` - do NOT assume GitHub's Sourcery check is sufficient
- Be thorough with priority assessment for all comments
- Don't skip LOW priority items (document them)
- Address CRITICAL items before merge
- Document deferred items clearly

**Workflow:**

- This command combines multiple steps for efficiency
- Can be run multiple times if PR is updated
- Always verify results before proceeding
- Present clear summary to user

---

## Reference

**Manual Testing:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/manual-testing.md`
- Project-wide: `docs/maintainers/planning/manual-testing.md` (if exists)

**Code Review:**

- `docs/maintainers/feedback/sourcery/pr##.md`

**PR Management:**

- GitHub CLI: `gh pr view [number]`
- PR description updates

**Related Commands:**

- `/pr --phase [N]` - Create PR and initial validation
- `/post-pr` - Post-merge documentation updates
- `/int-opp` - Document phase learnings

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Active  
**Next:** Use when PR is open to validate features, run reviews, and update documentation (supports conditional manual testing based on PR type, enforces manual testing guide creation for human users)

