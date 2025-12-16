# Task Release Command

Implements release tasks following TDD workflow. Similar to `/task-phase` but focused on release preparation tasks. Ensures release tasks are implemented with proper testing and documentation.

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns:

1. **Release-Specific Structure (default):**
   - Release transition plan: `docs/maintainers/planning/releases/[version]/transition-plan.md`
   - Release checklist: `docs/maintainers/planning/releases/[version]/checklist.md`
   - Release notes: `docs/maintainers/planning/releases/[version]/release-notes.md`

2. **Project-Wide Structure:**
   - Release planning: `docs/maintainers/planning/releases/[version]/` (if exists)

**Version Detection:**

- Extract version from current branch (e.g., `release/v1.0.0`)
- Or use `--version` option to specify version
- Or auto-detect from release directory structure

---

## Workflow Overview

**When to use:**

- When implementing release preparation tasks
- After transition plan is created
- To implement release checklist items
- Following TDD workflow for release tasks

**Key principle:** Implement release tasks with TDD discipline, ensuring each task is tested and documented before moving to the next.

---

## Usage

**Command:** `/task-release [task-number] [options]`

**Examples:**

- `/task-release 1` - Implement release task 1
- `/task-release 2 --version v1.0.0` - Implement task 2 for specific version
- `/task-release 3 --checklist-only` - Only update checklist, don't implement
- `/task-release 1 --dry-run` - Show what would be done without implementing

**Options:**

- `--task NUMBER` - Task number to implement (required)
- `--version VERSION` - Specify version (e.g., v1.0.0)
- `--checklist-only` - Only update checklist, don't implement
- `--dry-run` - Show implementation plan without executing

---

## Step-by-Step Process

### 1. Identify Release Information

**Detect version:**

- Extract from current branch: `release/v1.0.0` → `v1.0.0`
- Or use `--version` option
- Or find latest release directory: `docs/maintainers/planning/releases/v*/`

**Load release documents:**

- Transition plan: `docs/maintainers/planning/releases/[version]/transition-plan.md`
- Checklist: `docs/maintainers/planning/releases/[version]/checklist.md`
- Release notes: `docs/maintainers/planning/releases/[version]/release-notes.md`

**Verify documents exist:**

```bash
# Check transition plan
ls docs/maintainers/planning/releases/[version]/transition-plan.md

# Check checklist
ls docs/maintainers/planning/releases/[version]/checklist.md
```

**Checklist:**

- [ ] Version identified
- [ ] Release documents found
- [ ] Documents are readable
- [ ] Current branch is release branch (if applicable)

---

### 2. Load Release Task

**Parse transition plan:**

- Extract task from transition plan
- Identify task number
- Read task description
- Identify task dependencies
- Check task status

**Task format in transition plan:**

```markdown
## Transition Steps

1. **Step 1: [Task Name]**
   - [ ] Task 1
   - [ ] Task 2
   - Estimated: [X] hours
```

**Checklist:**

- [ ] Task identified
- [ ] Task description clear
- [ ] Dependencies checked
- [ ] Task is ready to implement

---

### 3. Implement Task (TDD Workflow)

**Follow TDD discipline:**

1. **RED:** Write failing test
   - Create test for task functionality
   - Ensure test fails (RED)
   - Commit test

2. **GREEN:** Implement minimum code
   - Implement just enough to pass test
   - Ensure test passes (GREEN)
   - Commit implementation

3. **REFACTOR:** Improve code
   - Refactor if needed
   - Ensure tests still pass
   - Commit refactoring

**For release tasks, tests may include:**

- Version validation tests
- Release checklist validation
- Release notes format validation
- Tag validation
- Distribution validation

**Checklist:**

- [ ] Test written (RED)
- [ ] Test fails as expected
- [ ] Implementation complete (GREEN)
- [ ] Test passes
- [ ] Code refactored (if needed)
- [ ] All tests passing

---

### 4. Update Release Checklist

**Mark task complete:**

- Update checklist: `- [x]` instead of `- [ ]`
- Add completion notes if needed
- Document any issues encountered

**Checklist location:**

- `docs/maintainers/planning/releases/[version]/checklist.md`

**Update format:**

```markdown
## Release Preparation

- [x] Task 1: [Description] ✅ Completed YYYY-MM-DD
- [ ] Task 2: [Description]
```

**Checklist:**

- [ ] Checklist updated
- [ ] Task marked complete
- [ ] Completion date added
- [ ] Notes added (if needed)

---

### 5. Update Release Notes (if applicable)

**If task affects release notes:**

- Update release notes with task completion
- Add relevant information
- Update version information

**Release notes location:**

- `docs/maintainers/planning/releases/[version]/release-notes.md`

**Checklist:**

- [ ] Release notes updated (if applicable)
- [ ] Information added
- [ ] Version information current

---

### 6. Commit Changes

**Commit strategy:**

- Commit test first: `test(release): add test for [task description]`
- Commit implementation: `feat(release): implement [task description]`
- Commit checklist update: `docs(release): update checklist for [task description]`

**Branch:**

- Work on release branch: `release/[version]`
- Or feature branch if needed: `feat/release-[version]-[task]`

**Checklist:**

- [ ] Changes committed
- [ ] Commit messages descriptive
- [ ] Commits follow project conventions
- [ ] Branch is correct

---

### 7. Stop After Task Completion

**After completing a task:**

- [ ] Task fully implemented and tested
- [ ] All commits made to release branch
- [ ] Tests passing
- [ ] Checklist updated
- [ ] **STOP - Do NOT proceed to next task**
- [ ] Present completion summary to user
- [ ] Indicate which task was completed
- [ ] Wait for user to invoke command again for next task

**Important:** This command handles ONE task at a time. The user will invoke the command again with the next task number when ready to continue.

---

### 8. Complete All Tasks - Finalize Release

**When ALL release tasks are done:**

**Pre-Release Checklist:**

- [ ] All tasks completed
- [ ] All tests passing
- [ ] Release checklist complete
- [ ] Release notes finalized
- [ ] Version tagged
- [ ] Documentation updated
- [ ] No linter errors

**Create Release PR:**

1. Push final commits to release branch
2. Run Sourcery review: `dt-review` from dev-toolkit (if available)
3. Fill out priority matrix in `docs/maintainers/feedback/sourcery/pr##.md` (if review available)
4. Address any CRITICAL/HIGH issues before PR
5. Create PR with comprehensive description

**PR Title Format:**

```
chore: Release [version]
```

**PR Description Template:**

```markdown
## Release [version]

[Brief description of release]

---

## Release Preparation Complete

### Checklist Items Completed
- [x] Task 1: [Description]
- [x] Task 2: [Description]
- [x] Task 3: [Description]

### Release Notes
- Release notes finalized
- Version information updated
- Documentation updated

### Verification
- All tests passing ([N] tests)
- Release checklist complete
- Release notes finalized
- Version tagged: [version]

### Next Steps
1. Review PR
2. Merge to main
3. Create GitHub release
4. Distribute release
```

**Checklist:**

- [ ] All tasks complete
- [ ] Release PR created
- [ ] PR description comprehensive
- [ ] Ready for review

---

## Common Issues

### Issue: Release Documents Missing

**Solution:**

- Create release directory structure
- Use `/transition-plan` to create transition plan first
- Create checklist template
- Create release notes template

### Issue: Task Not Found

**Solution:**

- Check task number
- Verify transition plan exists
- Check task format in transition plan
- Ensure task is not already complete

### Issue: Tests Failing

**Solution:**

- Review test implementation
- Check test data
- Verify test environment
- Fix implementation to pass tests

---

## Tips

### Before Starting

- Ensure transition plan exists
- Review release checklist
- Understand task requirements
- Check dependencies

### During Implementation

- Follow TDD workflow strictly
- Write tests first
- Implement minimum code
- Refactor as needed

### After Completion

- Update checklist immediately
- Document any issues
- Commit changes promptly
- Present summary to user

---

## Reference

**Release Documents:**

- Transition plan: `docs/maintainers/planning/releases/[version]/transition-plan.md`
- Checklist: `docs/maintainers/planning/releases/[version]/checklist.md`
- Release notes: `docs/maintainers/planning/releases/[version]/release-notes.md`

**Related Commands:**

- `/transition-plan` - Create release transition plans
- `/pr` - Create release PRs
- `/task-phase` - Similar workflow for phase tasks

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use to implement release preparation tasks following TDD workflow

