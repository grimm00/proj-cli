# Status Command

**Status:** 🟠 Evolving  
**Stability:** Experimental - may change without notice  
**Feedback:** [Provide feedback](../../.github/ISSUE_TEMPLATE/experimental-feedback.yml)

> ⚠️ **Experimental Command**: This command is under active development and may change significantly between releases. Use in production with caution and please [provide feedback](../../.github/ISSUE_TEMPLATE/experimental-feedback.yml)!

Use this command to view, update, and sync project status tracking across features and phases.

---

## 🎯 Purpose

Centralized status management that:
- Shows current progress at a glance
- Updates status documents consistently
- Syncs status with actual git history
- Validates status accuracy

**Philosophy:** Status tracking should be separate from implementation commands. Other commands (`/task-phase`, `/pr`, `/post-pr`) should delegate status updates to `/status`.

---

## Configuration

**Status Document Locations:**

1. **Feature-Specific (default):**
   - Phase docs: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Status doc: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`

2. **Project-Wide:**
   - Phase docs: `docs/maintainers/planning/phases/phase-N.md`
   - Status doc: `docs/maintainers/planning/status-and-next-steps.md`

3. **CI/CD Improvements:**
   - Phase docs: `docs/maintainers/planning/ci/[improvement-name]/phase-N.md`
   - No status-and-next-steps.md (CI improvements use different tracking)

4. **Legacy/Alternative (dev-infra specific):**
   - Phase docs: `admin/planning/features/[feature-name]/phase-N.md`
   - Status doc: `admin/planning/features/[feature-name]/status-and-next-steps.md`

**Feature Detection:**
- Auto-detect from current branch name (e.g., `feat/release-readiness-phase-3`)
- Or specify with `--feature [name]`

---

## Usage

### View Status

```bash
# Show all features status (dashboard)
/status

# Show specific feature status
/status --feature release-readiness

# Show specific phase status
/status --feature release-readiness --phase 3

# Show verbose (include task details)
/status --verbose
/status -v
```

### Update Status

```bash
# Mark a task complete
/status --task-complete [phase] [task]
/status --task-complete 3 2              # Phase 3, Task 2

# Mark a phase as started
/status --phase-start [phase]
/status --phase-start 3

# Mark a phase complete
/status --phase-complete [phase]
/status --phase-complete 3

# Update progress percentage
/status --update-progress [phase] [percent]
/status --update-progress 3 66
```

### Sync & Validate

```bash
# Validate status accuracy (check docs vs reality)
/status --validate

# Sync status from git history (auto-fix mismatches)
/status --sync

# Dry-run sync (show what would change)
/status --sync --dry-run
```

### Options

| Option | Description |
|--------|-------------|
| `--feature [name]` | Specify feature name |
| `--phase [N]` | Specify phase number |
| `--verbose`, `-v` | Show detailed task breakdown |
| `--dry-run` | Show changes without applying |
| `--commit` | Auto-commit status changes |
| `--no-commit` | Don't commit (manual commit later) |

---

## Output Format

### Dashboard View (`/status`)

```
📊 Project Status Dashboard

┌─────────────────────────────────────────────────────────────┐
│ Feature: release-readiness                                  │
├─────────────────────────────────────────────────────────────┤
│ Overall: 47% complete                                       │
│                                                             │
│ Phase 1: Criteria Standardization    ✅ 100%  (PR #32)     │
│ Phase 2: Automation Approach         ✅ 100%  (PR #32)     │
│ Phase 3: Assessment Structure        🟠  66%  (2/3 tasks)  │
│ Phase 4: Process Integration         🔴   0%               │
│ Phase 5: Historical Tracking         🔴   0%               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Feature: templates-enhancement                              │
├─────────────────────────────────────────────────────────────┤
│ Overall: 80% complete                                       │
│ ...                                                         │
└─────────────────────────────────────────────────────────────┘
```

### Verbose View (`/status --feature release-readiness -v`)

```
📊 Feature: release-readiness

Overall Progress: 47% (2.66 of 5 phases)
Current Phase: Phase 3: Assessment Structure
Last Updated: 2025-12-09

─────────────────────────────────────────────

Phase 1: Criteria Standardization ✅ 100%
  Completed: 2025-12-08 (PR #32)
  └─ All tasks complete

Phase 2: Automation Approach ✅ 100%
  Completed: 2025-12-08 (PR #32)
  └─ All tasks complete

Phase 3: Assessment Structure 🟠 66%
  Status: In Progress
  ├─ ✅ Task 1: Assessment Generator (TDD)
  ├─ ✅ Task 2: Summary Calculation (TDD)
  └─ 🔴 Task 3: Evidence Sections (TDD)

Phase 4: Process Integration 🔴 0%
  Status: Not Started
  └─ 0 of 3 tasks complete

Phase 5: Historical Tracking 🔴 0%
  Status: Not Started
  └─ 0 of 2 tasks complete

─────────────────────────────────────────────

Next Action: Complete Phase 3, Task 3
```

### Validation Output (`/status --validate`)

```
🔍 Status Validation Report

Feature: release-readiness

✅ Phase 1: Status matches git history
✅ Phase 2: Status matches git history
⚠️  Phase 3: MISMATCH DETECTED
   - phase-3.md shows Task 2 incomplete
   - Git log shows: "feat(phase-3): implement summary calculation (Task 2 complete)"
   - Recommendation: Run `/status --sync` to fix

Summary: 1 mismatch found
Run `/status --sync` to auto-fix
```

---

## Step-by-Step Process

### 1. View Status (Default)

**What to do:**

1. **Detect all features:**
   - Scan `docs/maintainers/planning/features/` (or alternative paths)
   - List all features with phase documents

2. **For each feature:**
   - Read `status-and-next-steps.md` for overall status
   - Read each `phase-N.md` for phase details
   - Calculate completion percentages

3. **Display dashboard:**
   - Show feature name, overall progress, phase breakdown
   - Highlight current phase
   - Show any warnings/issues

---

### 2. Update Task Status (`--task-complete`)

**What to do:**

1. **Locate phase document:**
   - Find `phase-N.md` for specified phase
   - Parse task structure

2. **Update task checkboxes:**
   - Find task N section
   - Change `- [ ]` to `- [x]` for all sub-items
   - Update `**Last Updated:**` field

3. **Calculate new progress:**
   - Count completed tasks vs total tasks
   - Update phase progress percentage

4. **Update status document:**
   - Find `status-and-next-steps.md`
   - Update phase progress entry
   - Update `**Last Updated:**` field

5. **Commit (if --commit):**
   - Commit message: `docs(status): mark phase N task M complete`

**Example:**

```bash
/status --task-complete 3 2 --commit
```

Updates:
- `phase-3.md`: Task 2 checkboxes → `[x]`
- `status-and-next-steps.md`: Phase 3 progress → 66%
- Commit: `docs(status): mark phase 3 task 2 complete`

---

### 3. Update Phase Status (`--phase-start`, `--phase-complete`)

**Phase Start (`--phase-start`):**

1. Update phase document:
   - `**Status:** 🔴 Not Started` → `**Status:** 🟠 In Progress`
   - Update `**Last Updated:**`

2. Update status document:
   - Phase entry: `🔴 Not Started` → `🟠 In Progress`
   - `**Current Phase:**` → Phase N

**Phase Complete (`--phase-complete`):**

1. Verify all tasks complete:
   - Check all `- [x]` in phase document
   - Warn if incomplete tasks found

2. Update phase document:
   - `**Status:** 🟠 In Progress` → `**Status:** ✅ Complete`
   - Add `**Completed:** YYYY-MM-DD`

3. Update status document:
   - Phase entry: `🟠 In Progress` → `✅ Complete`
   - Add completion date
   - Update overall progress percentage
   - Update `**Current Phase:**` to next phase

---

### 4. Validate Status (`--validate`)

**What to do:**

1. **Parse phase documents:**
   - Extract task checkboxes status
   - Extract phase status

2. **Parse git history:**
   - Find commits mentioning tasks/phases
   - Look for patterns: `Task N complete`, `phase-N`, etc.

3. **Compare:**
   - For each task, check if git says complete but doc says incomplete
   - For each phase, check status consistency

4. **Report mismatches:**
   - List all discrepancies
   - Provide recommendations

---

### 5. Sync Status (`--sync`)

**What to do:**

1. **Run validation** (same as --validate)

2. **For each mismatch:**
   - Determine correct status from git history
   - Update document to match

3. **Apply updates:**
   - Update phase documents
   - Update status documents
   - Recalculate percentages

4. **Commit (if --commit):**
   - Commit message: `docs(status): sync status from git history`

5. **Report changes:**
   - List all updates made
   - Show before/after

---

## Integration with Other Commands

### Commands That Should Call `/status`

| Command | When to Call `/status` | What to Call |
|---------|------------------------|--------------|
| `/task-phase` | Starting phase | `/status --phase-start N` |
| `/task-phase` | Completing task | `/status --task-complete N M` |
| `/task-phase` | Completing phase | `/status --phase-complete N` |
| `/pr` | Before PR creation | `/status --validate` |
| `/post-pr` | After PR merge | `/status --phase-complete N --commit` |
| `/fix-implement` | After fix batch | (fix-specific, not phase tracking) |

### Decoupling Strategy

**Current State:** Commands inline status updates (error-prone, inconsistent)

**Target State:** Commands delegate to `/status` (centralized, consistent)

**Example - `/task-phase` Integration:**

```markdown
# Instead of inline status updates in /task-phase:

## After Task Complete
1. Complete task implementation
2. Commit code changes
3. **Delegate:** Run `/status --task-complete [phase] [task] --commit`
4. Stop and wait for next invocation

## After Phase Complete
1. Complete all tasks
2. **Delegate:** Run `/status --phase-complete [phase] --commit`
3. Proceed to PR creation
```

---

## Status Indicators

| Indicator | Meaning |
|-----------|---------|
| 🔴 | Not Started (0%) |
| 🟠 | In Progress (1-99%) |
| ✅ | Complete (100%) |
| ⚠️ | Warning/Issue detected |

---

## Progress Calculation

### Phase Progress

```
Phase Progress = (Completed Tasks / Total Tasks) × 100%
```

### Overall Feature Progress

```
Overall Progress = Σ(Phase Progress × Phase Weight) / Total Phases

Where Phase Weight:
- Completed phase = 1.0
- In Progress phase = (Task Progress / 100)
- Not Started phase = 0.0
```

**Example:**
- Phase 1: ✅ 100% → Weight 1.0
- Phase 2: ✅ 100% → Weight 1.0
- Phase 3: 🟠 66% → Weight 0.66
- Phase 4: 🔴 0% → Weight 0.0
- Phase 5: 🔴 0% → Weight 0.0

Overall = (1.0 + 1.0 + 0.66 + 0.0 + 0.0) / 5 = 53%

---

## Error Handling

**Phase document not found:**
```
❌ Error: Phase document not found
   Looking for: docs/maintainers/planning/features/release-readiness/phase-3.md
   Suggestion: Check feature name and phase number
```

**Status document not found:**
```
⚠️ Warning: Status document not found
   Looking for: docs/maintainers/planning/features/release-readiness/status-and-next-steps.md
   Continuing with phase documents only...
```

**Invalid task number:**
```
❌ Error: Task 5 not found in Phase 3
   Phase 3 has 3 tasks (1-3)
```

**Uncommitted changes:**
```
⚠️ Warning: Uncommitted changes detected
   Status updates will be added to existing changes
   Use --commit to commit all, or commit manually
```

---

## Examples

### Example 1: Quick Status Check

```bash
/status
```

Shows dashboard of all features with progress.

### Example 2: Mark Task Complete

```bash
/status --task-complete 3 2 --feature release-readiness --commit
```

Output:
```
✅ Updated Phase 3, Task 2 to complete
   - phase-3.md: Task 2 checkboxes updated
   - status-and-next-steps.md: Phase 3 progress → 66%
   - Committed: docs(status): mark phase 3 task 2 complete
```

### Example 3: Sync After Finding Mismatch

```bash
/status --validate --feature release-readiness

# Output shows mismatch...

/status --sync --feature release-readiness --commit
```

Output:
```
🔄 Syncing status for release-readiness...

Changes:
  - phase-3.md: Task 2 marked complete (was incomplete)
  - status-and-next-steps.md: Phase 3 progress 0% → 66%

✅ Committed: docs(status): sync status from git history
```

---

## Related Commands

- `/task-phase` - Implement phase tasks (delegates status to `/status`)
- `/pr` - Create PR (validates status via `/status --validate`)
- `/post-pr` - Post-merge updates (delegates to `/status --phase-complete`)
- `/reflect` - Reflection workflow (can include status summary)

---

**Last Updated:** 2025-12-09  
**Status:** ✅ Active  
**Next:** Integrate with other commands for decoupled status tracking

