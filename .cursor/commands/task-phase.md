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

**Note:** For CI/CD improvements, use `/task-improvement` command instead.

**Important:** 
- This command handles **one task group at a time** (typically RED+GREEN pair)
- After completing a task group, stop and wait for user to invoke again for next group
- Do NOT continue to next task group automatically
- Use `/pr --phase [N]` command when all tasks are complete to create PR

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

**Checklist:**

- [ ] Phase structure detected
- [ ] Phase document read and understood
- [ ] Prerequisites met (previous phase complete)
- [ ] Feature branch created (if first task)
- [ ] Current task identified and understood

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

**Commit after each logical unit:**

**Small commits are better:**

- One commit per test file
- One commit per implementation
- One commit per migration
- One commit per CLI command

**Commit message format:**

```
type(scope): brief description

Longer explanation if needed

Related: Phase N, Task M
```

**Types:**

- `test` - Adding tests
- `feat` - New feature/functionality
- `fix` - Bug fix
- `refactor` - Code improvement
- `docs` - Documentation only
- `chore` - Maintenance

**Examples:**

```bash
git commit -m "test(phase-3): add DELETE endpoint tests"
git commit -m "feat(phase-3): implement DELETE endpoint"
git commit -m "feat(phase-3): add proj delete CLI command"
```

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
- [ ] **STOP - Do NOT proceed to next task group**
- [ ] Present completion summary to user
- [ ] Indicate which tasks were completed (e.g., "Tasks 1-2 complete: Filter tests + implementation")
- [ ] Wait for user to invoke command again for next task group

**Important:** This command handles ONE task group at a time (typically RED+GREEN pair). The user will invoke the command again with the next task number when ready to continue.

---

### 6. Complete All Tasks - Create PR

**When ALL tasks in phase are done:**

**Pre-PR Checklist:**

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Coverage maintained/improved
- [ ] Manual testing complete (if applicable)
- [ ] Phase document updated (all tasks marked complete)
- [ ] README/docs updated (if needed)
- [ ] No linter errors

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
- [ ] PR created and reviewed
- [ ] Sourcery review completed (if available)
- [ ] CRITICAL/HIGH issues addressed
- [ ] PR merged to develop
- [ ] Phase document status updated to "✅ Complete"
- [ ] Feature status updated (if needed)

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

- `docs/maintainers/planning/features/[feature-name]/testing/manual-testing.md` (if exists)

**Workflow:**

- Git Flow: See workflow rules
- PR Review: See workflow rules (Pull Request Review Workflow section)

**Related Commands:**

- `/pr --phase [N]` - Create PR for completed phase
- `/fix-plan` - Create fix plans from reviews
- `/fix-implement` - Implement fixes from batches

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use to implement phase tasks following TDD workflow (supports feature-specific and project-wide phases)

