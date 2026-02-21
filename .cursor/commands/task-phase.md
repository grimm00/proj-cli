# Task Phase Command

Use this command to implement phase tasks step-by-step, following TDD workflow and creating PRs at the right time.

---

## Configuration

**Phase Path Detection:**

This command supports multiple phase organization patterns:

1. **Feature-Specific Phases (default):**

   - Path: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Feature name auto-detected from context or configuration
   - Example: `docs/maintainers/planning/features/my-feature/phase-1.md`

2. **Project-Wide Phases:**
   - Path: `docs/maintainers/planning/phases/phase-N.md`
   - Used when no feature structure exists
   - Example: `docs/maintainers/planning/phases/phase-1.md`

**Note:** For CI/CD improvements, use `/task-improvement` command instead. CI/CD improvements have different structure (no `status-and-next-steps.md`, process/documentation workflow vs. TDD).

**Feature Detection:**

- Use `--feature` option if provided
- Otherwise, auto-detect:
  - Check if `docs/maintainers/planning/features/` exists
  - If multiple features exist, use configuration or prompt user
  - If single feature exists, use that feature name
  - If no features exist, use project-wide structure

**Phase Structure Support:**

- Numbered phases: `phase-1.md`, `phase-2.md` (default)
- Named phases: `phase-[name].md` (if configured)
- Milestones: `milestone-N.md` (if configured)
- Sprints: `sprint-N.md` (if configured)

**Branch Naming:**

- Default format: `feat/phase-N-[description]`
- Configurable via project configuration
- Examples: `feat/phase-3-delete-archive`, `feat/my-feature-phase-1`

**Task Grouping:**

- Default: RED + GREEN tasks grouped together
- Configurable grouping rules via project configuration
- Auto-detect task relationships

---

## Pre-Task Branch Validation (BLOCKING)

**CRITICAL:** This validation MUST pass before any work begins. Do NOT proceed if validation fails.

### Validation Steps

1. **Check Current Branch:**
   ```bash
   git branch --show-current
   ```
   
2. **Expected Pattern:** `feat/[feature-name]-phase-N-*` or `feat/phase-N-*`

3. **Validation Logic:**
   - If on `develop` or `main` → **ERROR: Wrong branch**
   - If on different feature branch → **ERROR: Wrong feature**
   - If branch in worktree elsewhere → **ERROR: Worktree conflict**

### Error Handling

**Wrong Branch Error:**
```
❌ BLOCKING: Currently on 'develop', expected 'feat/[feature]-phase-N-*'
   
   Resolution:
   1. Check out the correct feature branch: git checkout feat/[feature]-phase-N-[desc]
   2. If branch exists in worktree, work from that worktree instead
   3. If starting new phase, create branch: git checkout -b feat/[feature]-phase-N-[desc]
```

**Worktree Conflict Error:**
```
❌ BLOCKING: Branch 'feat/...' is checked out in worktree at '/path/to/worktree'
   
   Resolution:
   1. Work from the worktree: cd /path/to/worktree
   2. Or delete the worktree: git worktree remove /path/to/worktree
   3. Then checkout: git checkout feat/...
```

### Enforcement

- This check runs at the START of every `/task-phase` invocation
- If validation fails, the command STOPS immediately
- No code changes should be made until validation passes

## Workflow Overview

**Pattern:**

1. Phase has multiple tasks (usually TDD: RED → GREEN cycles)
2. **Task Grouping:** RED + GREEN phases are grouped together (tightly coupled TDD cycle)
3. Implement the task group completely (RED → GREEN → REFACTOR)
4. Commit the work
5. Stop and wait for user to invoke command again for next task group
6. Create PR only after completing ALL tasks in phase (use `/pr --phase [N]` command)

**Task Grouping Rules:**

- **Group together:** RED test task + GREEN implementation task (e.g., Task 1 + Task 2)
- **Separate:** Different task types (e.g., API tasks vs CLI tasks)
- **Separate:** Large/complex tasks that benefit from review

**Examples:**

- Task 1 (Write Filter Tests - RED) + Task 2 (Implement Filtering - GREEN) = **One invocation**
- Task 3 (Write Search Tests - RED) + Task 4 (Implement Search - GREEN) = **One invocation**
- Task 5 (Enhance CLI) = **Separate invocation** (different component)

**When to create PR:**

- After completing the LAST task in the phase
- Use `/pr --phase [N]` command for complete PR workflow
- Before marking phase as complete
- After all tests pass
- After manual testing (if applicable)

**Key Principle:** Group related TDD cycles (RED+GREEN), but separate different components. Complete the task group, commit it, then stop. User will invoke command again for the next task group.

---

## Usage

**Command:** `/task-phase [phase-number] [task-number] [options]`

**Examples:**

- `/task-phase 4 1` - Implement Phase 4, Tasks 1-2 (RED + GREEN for filtering)
- `/task-phase 4 3` - Implement Phase 4, Tasks 3-4 (RED + GREEN for search)
- `/task-phase 4 5` - Implement Phase 4, Task 5 (CLI enhancement)
- `/task-phase 4 1 --feature my-feature` - Specify feature name
- `/task-phase 4 1 --project-wide` - Use project-wide phase structure

**Task Grouping:**

- When you specify a RED task (e.g., Task 1), automatically include the next GREEN task (Task 2)
- Different task types (API vs CLI) are separate invocations
- Check phase document to identify natural groupings

**Options:**

- `--feature [name]` - Specify feature name (overrides auto-detection)
- `--project-wide` - Use project-wide phase structure
- `--phase-type [type]` - Specify phase type (phase, milestone, sprint)
- `--force-pr` - Force PR creation even for docs-only phases (overrides auto-detection)

**Note:** To address pre-phase review gaps before implementation, use `/address-review` command first.

**Note:** For CI/CD improvements, use `/task-improvement` command instead.

**Docs-Only Detection:**

This command automatically detects if a phase is documentation-only and uses a direct merge workflow (no PR) to preserve Sourcery review quota for code changes.

**Detection Criteria:**

A phase is considered "docs-only" if:

- Only documentation files are modified (`.md`, `.txt`, `.yml`, `.yaml`, `.json` config files)
- Only copying existing files (no code modifications)
- Creating new documentation/README files
- Template work that involves copying files and creating documentation

A phase requires PR if:

- Any code files are modified (`.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`, `.cpp`, `.sh`, `.bash`, etc.)
- Scripts are modified (even if they generate docs)
- CI/CD workflows are modified (`.yml` in `.github/workflows/`)
- Mixed changes (code + docs) → Use PR workflow

**Workflow:**

- **Docs-Only Phase:** Feature branch → Commit → Merge directly to develop → Update status docs
- **Code Phase:** Feature branch → Commit → Create PR → Review → Merge → Update status docs

**Important:**

- This command handles **one task group at a time** (typically RED+GREEN pair)
- After completing a task group, stop and wait for user to invoke again for next group
- Do NOT continue to next task group automatically
- Use `/pr --phase [N]` command when all tasks are complete to create PR (for code phases)
- Docs-only phases merge directly to develop (no PR needed)

---

## Pre-Phase Review Workflow

**Before starting implementation**, ensure phase plan is complete:

1. **Run `/pre-phase-review [N]`** to identify gaps
2. **Run `/address-review [review-path]`** to address gaps (if any found)
3. **Run `/task-phase [N] [task]`** to start implementation (this command)

**Separation of Concerns:**

- **`/pre-phase-review`** - Identifies issues (creates review document)
- **`/address-review`** - Addresses issues (updates phase document)
- **`/task-phase`** - Implements work (writes code/tests)

This keeps planning/documentation updates separate from implementation.

---

## Step-by-Step Process

### 1. Start a Phase Task

**What to do:**

1. **Detect phase structure:**

   - Use `--feature` option if provided
   - Otherwise, auto-detect using same logic as other commands:
     - Check if `docs/maintainers/planning/features/` exists
     - If single feature exists, use that feature name
     - If multiple features exist, search for phase documents in each
     - If no features exist, use project-wide structure

2. **Read the phase document:**
   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`
   - Support alternative structures: `milestone-N.md`, `sprint-N.md` (if configured)

**Note:** If CI/CD improvement detected, suggest using `/task-improvement` command instead.

3. **Identify the current task** (numbered in the document)

4. **Check prerequisites** (previous tasks, phase status)

5. **Create feature branch if starting phase:**
   - Default: `feat/phase-N-[description]`
   - Feature-specific: `feat/[feature-name]-phase-N-[description]` (if configured)
   - Configurable via project configuration

**Branch naming:**

- First task: `feat/phase-N-[description]` (e.g., `feat/phase-3-delete-archive`)
- Feature-specific: `feat/[feature-name]-phase-N-[description]` (if configured)
- Subsequent tasks: Use same branch

**Status Update (Start of Phase):**

**Note:** For authoritative status update requirements, see [PR Status Update Requirements](../../docs/PR-STATUS-UPDATE-REQUIREMENTS.md). Examples below use placeholder dates (e.g., `2025-12-07`) and phase numbers (e.g., `Phase 3`) for illustration.

**Auto-Update Phase Status:**

When starting a phase (first task of the phase), automatically update status:

1. **Read phase document:**

   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`

2. **Check current status:**

   - If status is "🔴 Not Started" or missing, update to "🟠 In Progress"
   - If status is already "🟠 In Progress", leave as is (may be resuming)
   - If status is "✅ Complete", warn user (shouldn't happen)

3. **Update phase document:**

   - Change `**Status:** 🔴 Not Started` to `**Status:** 🟠 In Progress`
   - Update `**Last Updated:**` field to today's date
   - Example:
     ```markdown
     **Status:** 🟠 In Progress
     **Last Updated:** 2025-12-07
     ```

4. **Update feature status document (if first phase):**

   - File: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Update `**Status:**` to "🟠 In Progress" if still "🔴 Not Started"
   - Update `**Current Phase:**` to reflect starting phase
   - Update `**Last Updated:**` field

5. **Commit status updates:**
   - Commit message: `docs(phase-N): update phase status to In Progress`
   - Include both phase document and feature status document if updated
   - Commit immediately after updating (before starting work)

**Note:** Status updates are committed immediately at phase start to ensure status is current from the beginning.

**Checklist:**

- [ ] Phase structure detected
- [ ] Phase document read and understood
- [ ] Prerequisites met (previous phase complete)
- [ ] Feature branch created (if first task)
- [ ] Current task identified and understood
- [ ] Phase status auto-updated to "🟠 In Progress" (if starting phase)
- [ ] Feature status auto-updated (if first phase)
- [ ] Status updates committed

---

### 2. Implement Task Group Following TDD

**TDD Pattern (RED → GREEN → REFACTOR):**

**If task group includes RED + GREEN:**

#### RED Phase (Write Tests First)

- [ ] Write failing tests for the task
- [ ] Run tests to confirm they fail
- [ ] Commit: `test(phase-N): add tests for [task description]`

#### GREEN Phase (Implement to Pass)

- [ ] Implement minimum code to pass tests
- [ ] Run tests to confirm they pass
- [ ] Commit: `feat(phase-N): implement [task description]`

#### REFACTOR Phase (Improve Code)

- [ ] Refactor if needed (with tests still passing)
- [ ] Commit: `refactor(phase-N): improve [task description]` (if needed)

**If task group is standalone (e.g., CLI task):**

- [ ] Implement the task completely
- [ ] Test manually
- [ ] Commit: `feat(phase-N): implement [task description]`

**Task-specific patterns:**

**Model Changes:**

1. Write model tests (RED)
2. Update model (GREEN)
3. Create migration: `flask db migrate -m "Description"` (or project-specific migration command)
4. Apply migration: `flask db upgrade` (or project-specific command)
5. Run tests (should pass)

**API Endpoints:**

1. Write integration tests (RED)
2. Implement endpoint (GREEN)
3. Test with curl/CLI manually
4. Run full test suite

**CLI Commands:**

1. Write CLI tests (if applicable)
2. Implement command
3. Test manually
4. Update CLI README

**Frontend Components:**

1. Write component tests (RED)
2. Implement component (GREEN)
3. Test manually
4. Run test suite

---

### 3. Commit Strategy

**IMPORTANT:** Always commit work before stopping or moving to next task group.

**Reference:** [Commit Workflow](../../docs/COMMIT-WORKFLOW.md) - Central commit workflow documentation

**For code changes (tests, implementation, refactoring):**

Use `/review` to review changes before committing. This forces a deliberate pause to verify agentic code changes.

```
[AI implements task]
    ↓
/review [task-description]   ← Review in a separate prompt
    ↓ human review
/commit                      ← Commit reviewed changes
```

**For documentation-only changes (status updates, phase markers):**

Direct commit is fine -- no review pause needed.

```bash
git commit -m "docs(phase-N): mark Task M complete"
```

**Commit Message Format:**

- Follow standard format: `type(scope): brief description`
- Include "Related:" line for context
- See [Commit Workflow](../../docs/COMMIT-WORKFLOW.md#commit-message-format) for complete format

**Examples:**

```bash
# Code changes -- use /review + /commit
# test(phase-3): add DELETE endpoint tests
# feat(phase-3): implement DELETE endpoint

# Doc changes -- direct commit is fine
git commit -m "docs(phase-3): update status checkboxes"
```

**Before Stopping:**

- [ ] Check `git status` for uncommitted changes
- [ ] Use `/review` for code changes, direct commit for docs-only
- [ ] Push to remote if on feature branch
- [ ] Verify no uncommitted changes remain

---

### 4. Check Task Completion

**After implementing a task:**

- [ ] All tests for this task pass
- [ ] Code follows project patterns
- [ ] No linter errors
- [ ] Manual testing done (if applicable)
- [ ] Task checklist items completed
- [ ] Committed to feature branch

**Update phase document:**

- Mark task items as complete: `- [x]` instead of `- [ ]`
- Don't commit phase doc changes until phase complete

**Phase document location:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

---

### 5. Stop After Task Group Completion

**After completing a task group:**

- [ ] Task group fully implemented and tested
- [ ] All commits made to feature branch
- [ ] Tests passing

**Auto-Status Update (MANDATORY):**

After task implementation is complete, AUTOMATICALLY:

1. **Update Phase Document:**
   ```bash
   # Mark task checkboxes as complete
   # Change: - [ ] **RED:** ... → - [x] **RED:** ...
   # Change: - [ ] **GREEN:** ... → - [x] **GREEN:** ...
   # Update Last Updated field
   ```

2. **Commit Status Update:**
   ```bash
   git add [phase-document]
   git commit -m "docs(phase-N): mark Task M complete"
   ```

3. **Verify Commit Location:**
   ```bash
   # Confirm commit is on feature branch, NOT develop
   git branch --show-current  # Should be feat/...
   git log --oneline -1       # Should show status commit
   ```

**Then STOP:**

- [ ] **STOP - Do NOT proceed to next task group**
- [ ] Present completion summary to user
- [ ] Indicate which tasks were completed (e.g., "Tasks 1-2 complete: Filter tests + implementation")
- [ ] Remind user: "Use `/review` to review code changes before committing"
- [ ] Wait for user to invoke command again for next task group

**Important:** This command handles ONE task group at a time (typically RED+GREEN pair). The user will invoke `/review` to review and commit, then invoke this command again with the next task number when ready to continue.

---

### 6. Complete All Tasks - Determine Workflow

**When ALL tasks in phase are done:**

**First, detect phase type (docs-only vs code):**

1. **Analyze modified files:**

   - Check git diff for files that will be modified
   - Check phase document tasks for file patterns mentioned
   - Look for code file extensions vs docs-only extensions

2. **Detection logic:**

   ```bash
   # Check for code files in changes
   git diff --name-only develop...HEAD | grep -E '\.(py|js|ts|go|rs|java|cpp|c|h|sh|bash)$'
   # If found → Code phase (use PR workflow)
   # If not found → Docs-only phase (use direct merge)
   ```

3. **Special cases:**
   - Template generation scripts (`.sh` in `scripts/`) → Code phase
   - CI/CD workflows (`.yml` in `.github/workflows/`) → Code phase
   - Mixed changes (code + docs) → Code phase (use PR workflow)
   - User override: `--force-pr` flag forces PR workflow

**Pre-Completion Checklist:**

- [ ] All tasks completed
- [ ] All tests passing (if applicable)
- [ ] Coverage maintained/improved (if applicable)
- [ ] Manual testing complete (if applicable)
- [ ] Phase document updated (all tasks marked complete)
- [ ] README/docs updated (if needed)
- [ ] No linter errors (if applicable)
- [ ] Phase type detected (docs-only vs code)

**Status Update (Phase Completion):**

**Auto-Update Phase Status:**

When all tasks in phase are complete, automatically update status:

1. **Read phase document:**

   - Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Project-wide: `docs/maintainers/planning/phases/phase-N.md`

2. **Verify all tasks complete:**

   - Check all task checkboxes are marked `- [x]`
   - Verify no incomplete tasks remain
   - If tasks incomplete, warn user before updating status

3. **Update phase document:**

   - Change `**Status:** 🟠 In Progress` to `**Status:** ✅ Complete`
   - Add `**Completed:** YYYY-MM-DD` field if not present
   - Update `**Last Updated:**` field to today's date
   - Example:
     ```markdown
     **Status:** ✅ Complete
     **Completed:** 2025-12-07
     **Last Updated:** 2025-12-07
     ```

4. **Update feature status document:**

   - File: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`
   - Update `**Current Phase:**` to reflect completed phase
   - Update `**Progress:**` percentage (calculate based on completed phases)
   - Add completed milestone entry:
     ```markdown
     - **Phase N:** [Phase Name] ✅ (2025-12-07) - [Brief summary]
     ```
   - Update `**Last Updated:**` field

5. **Commit status updates:**
   - Commit message: `docs(phase-N): update phase status to Complete`
   - Include both phase document and feature status document
   - Commit before creating PR (for code phases) or before direct merge (for docs-only phases)

**Note:** Status updates are committed before PR creation (code phases) or direct merge (docs-only phases) to ensure status is current.

**Checklist:**

- [ ] Phase status auto-updated to "✅ Complete"
- [ ] Completion date added to phase document
- [ ] Feature status document updated with phase completion
- [ ] Progress tracking updated
- [ ] Status updates committed

---

### 6a. Docs-Only Phase: Direct Merge Workflow

**If phase is detected as docs-only (and `--force-pr` not used):**

1. **Push feature branch to remote:**

   ```bash
   git push origin feat/phase-N-[description]
   ```

2. **Merge directly to develop:**

   ```bash
   git checkout develop
   git pull origin develop
   git merge feat/phase-N-[description] --no-edit
   git push origin develop
   ```

3. **Update post-merge documentation:**

   - Run `/post-pr --direct --phase N` to update status documents
   - This updates phase and feature status without PR number

4. **Clean up branch:**
   ```bash
   git branch -d feat/phase-N-[description]
   git push origin --delete feat/phase-N-[description]
   ```

**Checklist:**

- [ ] Feature branch pushed
- [ ] Merged directly to develop
- [ ] Post-merge documentation updated (`/post-pr --direct --phase N`)
- [ ] Branch cleaned up (local and remote)

**Note:** Docs-only phases skip PR creation to preserve Sourcery review quota for code changes. Status documents are still updated via `/post-pr --direct`.

---

### 6b. Code Phase: PR Workflow

**If phase contains code changes (or `--force-pr` used):**

**Create PR:**

1. Push final commits to feature branch
2. Run Sourcery review: `dt-review` from dev-toolkit (if available)
3. Fill out priority matrix in `docs/maintainers/feedback/sourcery/pr##.md` (if review available)
4. Address any CRITICAL/HIGH issues before PR
5. Create PR with comprehensive description

**PR Title Format:**

```
feat: [Phase N Description] (Phase N)
```

**PR Description Template:**

```markdown
## Phase N: [Phase Name]

[Brief description of what was implemented]

---

## What's Included

### [Component 1]

- Feature/change description
- Tests added
- Files modified

### [Component 2]

- Feature/change description
- Tests added
- Files modified

---

## Testing

- [ ] All automated tests passing
- [ ] Coverage: [X]%
- [ ] Manual testing complete (if applicable)
- [ ] Sourcery review completed (if applicable)

---

## Related

- **Phase Plan:** `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- **Feature Plan:** `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
```

**After PR Created:**

- [ ] Present PR link to user (DO NOT auto-merge)
- [ ] Wait for external review (dt-review, if available)
- [ ] Address CRITICAL/HIGH issues
- [ ] Get user approval before merge
- [ ] After merge, run `/post-pr [pr-number] --phase N` to update documentation

---

## Task Detection Logic

**How to identify tasks:**

Tasks are typically numbered in phase documents:

- `#### 1. Write DELETE Endpoint Tests (TDD - RED)`
- `#### 2. Implement DELETE Endpoint (TDD - GREEN)`
- `#### 3. Write Archive Tests (TDD - RED)`
- etc.

**Task boundaries:**

- Each numbered section is a task
- Tasks may have sub-items (checkboxes)
- Complete all sub-items before moving to next task

**Last task detection:**

- Check if there are more numbered tasks after current
- Look for "Completion Criteria" section (comes after all tasks)
- If no more tasks, it's time to create PR

---

## Common Patterns

### Pattern 1: Model Extension Task

**Task:** "Extend Project Model"

**Steps:**

1. Write model tests (RED)
2. Update model file
3. Create migration: `flask db migrate -m "Description"` (or project-specific command)
4. Apply migration: `flask db upgrade` (or project-specific command)
5. Update `to_dict()` method (if applicable)
6. Run tests (GREEN)
7. Commit

**Files typically modified:**

- `backend/tests/unit/models/test_project.py` (or project-specific test structure)
- `backend/app/models/project.py` (or project-specific model structure)
- `backend/migrations/versions/XXX_*.py` (new, if using Flask-Migrate)

### Pattern 2: API Endpoint Task

**Task:** "Implement DELETE Endpoint"

**Steps:**

1. Write integration tests (RED)
2. Add route to API file (project-specific structure)
3. Implement handler function
4. Add error handling
5. Run tests (GREEN)
6. Test manually with curl
7. Commit

**Files typically modified:**

- `backend/tests/integration/api/test_projects.py` (or project-specific test structure)
- `backend/app/api/projects.py` (or project-specific API structure)
- `backend/README.md` (update API docs, if applicable)

### Pattern 3: CLI Command Task

**Task:** "Add proj delete command"

**Steps:**

1. Create command file (project-specific structure)
2. Implement command with CLI framework (Click, argparse, etc.)
3. Add formatting (Rich, etc.)
4. Register command
5. Test manually
6. Update CLI README
7. Commit

**Files typically modified:**

- `scripts/project_cli/commands/delete_cmd.py` (new, project-specific)
- `scripts/project_cli/proj` (or project-specific CLI entry point)
- `scripts/project_cli/README.md` (or project-specific CLI docs)

### Pattern 4: Frontend Component Task

**Task:** "Add Filter Component"

**Steps:**

1. Write component tests (RED)
2. Create component file
3. Implement component (GREEN)
4. Add styling
5. Test manually
6. Run test suite
7. Commit

**Files typically modified:**

- `frontend/tests/components/Filter.test.tsx` (or project-specific test structure)
- `frontend/src/components/Filter.tsx` (or project-specific component structure)
- `frontend/src/components/index.ts` (export, if applicable)

---

## Error Handling

**If tests fail:**

- Debug the failure
- Fix the issue
- Re-run tests
- Don't move to next task until tests pass

**If migration fails:**

- Check migration file
- May need to reset database (project-specific)
- Re-run migration (project-specific command)

**If linter errors:**

- Fix linter issues
- Re-run linter
- Don't commit until clean

**If phase document not found:**

- Check feature detection logic
- Verify phase structure (numbered vs named)
- Use `--feature` option to specify feature name
- Use `--project-wide` option for project-wide phases

---

## Phase Completion Checklist

**Before marking phase complete:**

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Coverage maintained
- [ ] Manual testing done
- [ ] Documentation updated
- [ ] Phase status auto-updated to "✅ Complete" (automatic)
- [ ] Feature status auto-updated (automatic)
- [ ] Status updates committed (automatic)
- [ ] PR created and reviewed
- [ ] Sourcery review completed (if available)
- [ ] CRITICAL/HIGH issues addressed
- [ ] PR merged to develop
- [ ] Post-merge status updates handled by `/post-pr` command (automatic)

---

## Tips

**While implementing:**

- Focus on ONE task group (typically RED+GREEN pair)
- Keep phase document open for reference
- Check off items as you complete them
- Don't skip tests (TDD discipline)
- Commit frequently (small commits)
- Push to branch regularly

**Task grouping:**

- RED + GREEN phases naturally belong together
- Complete the full TDD cycle before stopping
- Different components (API vs CLI) are separate

**After completing task group:**

- **STOP - Do NOT continue to next task group**
- Present summary of what was accomplished
- Indicate which tasks were completed (e.g., "Tasks 1-2 complete")
- Wait for user to invoke command again

**Important reminders:**

- One task group per invocation (typically RED+GREEN pair)
- Complete task group fully before stopping
- Don't proceed to next task group automatically
- Use `/pr --phase [N]` when all tasks done

---

## Reference

**Phase Documents:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`
- Alternative structures: `milestone-N.md`, `sprint-N.md` (if configured)

**Note:** For CI/CD improvements, use `/task-improvement` command which reads from `docs/maintainers/planning/ci/[improvement-name]/phase-N.md`.

**Feature Planning:**

- `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
- `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`

**Testing:**

- `docs/maintainers/planning/features/[feature-name]/manual-testing.md` (if exists)

**Workflow:**

- Git Flow: See workflow rules
- PR Review: See workflow rules (Pull Request Review Workflow section)

**Related Commands:**

- `/pre-phase-review [N]` - Review phase plan before implementation
- `/address-review [path]` - Address pre-phase review gaps (run before task-phase)
- `/pr --phase [N]` - Create PR for completed phase
- `/fix-plan` - Create fix plans from reviews
- `/fix-implement` - Implement fixes from batches

---

**Last Updated:** 2025-12-10  
**Status:** ✅ Active  
**Next:** Use to implement phase tasks following TDD workflow (supports feature-specific and project-wide phases, now with pre-phase review integration)
