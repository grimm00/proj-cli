# Feature Development Workflow

**Purpose:** Guide for planning and implementing features
**Status:** ✅ Active
**Last Updated:** [Date]

---

## 📋 Quick Links

- **[Workflow Overview](WORKFLOW-OVERVIEW.md)** - All available workflows
- **[Planning Hub](planning/README.md)** - Feature planning overview
- **[Feature Planning](planning/features/README.md)** - Feature development process

### Example Documents

- **[Example Feature Plan](examples/example-feature-plan.md)** - Sample feature plan

---

## 🎯 Overview

The Feature Development workflow guides you through planning, implementing, and delivering features. This workflow uses phase-based development with TDD (Test-Driven Development) and integrates with workflow automation commands.

### Workflow Sequence

```
Feature Plan → Phase Planning → Implementation → PR → Merge
     ↓              ↓                ↓           ↓      ↓
  Create      /task-phase      /task-phase   /pr   /post-pr
```

### When to Use

- **New features** - When implementing new functionality
- **Feature enhancements** - When extending existing features
- **Structured development** - When you want organized, phased implementation

---

## 🚀 Quick Start

### Step 1: Create Feature Plan

Create a feature plan document:

**File:** `planning/features/[feature-name]/feature-plan.md`

**Key sections:**
- Feature overview
- Success criteria
- Implementation phases
- Dependencies

### Step 2: Create Phase Documents

Break feature into phases:

**File:** `planning/features/[feature-name]/phase-N.md`

**Each phase includes:**
- Phase goals
- Tasks (TDD: RED → GREEN cycles)
- Completion criteria

### Step 3: Implement Phases

Use `/task-phase` command to implement phases:

```bash
/task-phase [phase-number] [task-number]
```

**Example:**
```bash
/task-phase 1 1
```

**Output:**
- Tasks implemented following TDD
- Status automatically updated
- Commits made to feature branch

### Step 4: Create PR

After completing all tasks in a phase:

```bash
/pr --phase [phase-number]
```

**Example:**
```bash
/pr --phase 1
```

**Output:**
- PR created with comprehensive description
- Status validation performed
- Ready for review

### Step 5: Post-Merge Updates

After PR is merged:

```bash
/post-pr [pr-number] --phase [phase-number]
```

**Example:**
```bash
/post-pr 42 --phase 1
```

**Output:**
- Status documents updated
- Phase marked complete
- Feature progress updated

---

## 📖 Detailed Workflow

### Phase 1: Feature Planning

**Purpose:** Plan feature structure, phases, and approach

**Activities:**

1. **Create feature plan**
   - File: `planning/features/[feature-name]/feature-plan.md`
   - Document feature overview
   - Define success criteria
   - Break into phases

2. **Create phase documents**
   - File: `planning/features/[feature-name]/phase-N.md`
   - Define phase goals
   - List tasks (TDD cycles)
   - Set completion criteria

3. **Create status document**
   - File: `planning/features/[feature-name]/status-and-next-steps.md`
   - Track overall progress
   - Track phase completion
   - Document next steps

**Key principles:**
- Break work into manageable phases
- Use TDD (RED → GREEN cycles)
- Define clear success criteria
- Plan dependencies

**Next step:** Begin implementation with `/task-phase`

---

### Phase 2: Implementation

**Purpose:** Implement feature phases using TDD workflow

**Command:** `/task-phase [phase-number] [task-number]`

**Workflow:**

1. **Start phase**
   ```bash
   /task-phase 1 1
   ```
   - Creates feature branch (if first task)
   - Updates status to "In Progress"
   - Implements task group (RED + GREEN)

2. **Continue with next task group**
   ```bash
   /task-phase 1 3
   ```
   - Implements next task group
   - Commits work
   - Updates phase document

3. **Complete phase**
   - All tasks completed
   - Status auto-updated to "Complete"
   - Ready for PR creation

**Task Grouping:**

- **RED + GREEN** tasks grouped together (TDD cycle)
- Different components separated
- Complete task group before moving to next

**TDD Pattern:**

- **RED:** Write failing tests
- **GREEN:** Implement to pass tests
- **REFACTOR:** Improve code (if needed)

**Status Updates:**

- Status updated automatically at phase start
- Status updated automatically at phase completion
- Phase document updated as tasks complete

**Next step:** Create PR with `/pr --phase`

---

### Phase 3: Pull Request

**Purpose:** Create PR for completed phase

**Command:** `/pr --phase [phase-number]`

**Workflow:**

1. **Create PR**
   ```bash
   /pr --phase 1
   ```
   - Validates status updates
   - Creates PR description
   - Pushes branch and creates PR

2. **Review Process**
   - External review (if available)
   - Address CRITICAL/HIGH issues
   - Get approval

3. **Merge**
   - Merge PR to develop
   - Run `/post-pr` to update status

**PR Description Includes:**

- Phase summary
- What's included
- Testing information
- Related documents

**Status Validation:**

- Verifies phase status is current
- Checks feature status updates
- Ensures progress tracking accurate

**Next step:** Post-merge updates with `/post-pr`

---

### Phase 4: Post-Merge Updates

**Purpose:** Update status documents after PR merge

**Command:** `/post-pr [pr-number] --phase [phase-number]`

**Workflow:**

1. **Update status**
   ```bash
   /post-pr 42 --phase 1
   ```
   - Updates phase document with PR number
   - Updates feature status document
   - Updates progress tracking

2. **Continue to next phase**
   - Start next phase with `/task-phase`
   - Repeat implementation → PR → merge cycle

**Status Updates:**

- Phase marked complete with PR number
- Feature progress updated
- Next steps documented

**Next step:** Continue with next phase or complete feature

---

## 💡 Best Practices

### Feature Planning

- **Break into phases** - Manageable chunks of work
- **Use TDD** - Test-driven development ensures quality
- **Define success criteria** - Clear goals for each phase
- **Plan dependencies** - Understand phase relationships

### Implementation

- **One task group at a time** - Focus on current work
- **Complete TDD cycles** - RED → GREEN → REFACTOR
- **Commit frequently** - Small, logical commits
- **Update status** - Keep status documents current

### Pull Requests

- **Complete phase before PR** - All tasks done
- **Validate status** - Ensure status is current
- **Comprehensive description** - Document what's included
- **Address feedback** - Fix CRITICAL/HIGH issues

### Status Updates

- **Automatic updates** - Commands handle status updates
- **Manual updates** - Update during work if needed
- **Post-merge updates** - Use `/post-pr` after merge
- **Keep current** - Status should reflect reality

---

## 🔄 Workflow Integration

### Integration with Exploration/Research/Decision

Feature development often follows exploration/research/decision:

```
Exploration → Research → Decision → Feature Development
     ↓           ↓          ↓              ↓
  /explore   /research  /decision    /task-phase
```

### Integration with Commands

All phases integrate with Cursor commands:

- **`/task-phase`** - Implements phases with TDD
- **`/pr`** - Creates PRs for completed phases
- **`/post-pr`** - Updates status after merge

### Document Organization

Documents follow hub-and-spoke pattern:

- **Hub files** - `README.md` files provide navigation
- **Spoke documents** - Phase documents focus on specific work
- **Status tracking** - Consistent status indicators

---

## 📊 Workflow Diagram

```
┌─────────────┐
│Feature Plan │
└──────┬──────┘
       │
       ▼
┌─────────────┐     /task-phase
│ Phase 1     │ ────────────────────┐
└──────┬──────┘                     │
       │                             │
       ▼                             │
┌─────────────┐     /pr              │
│   PR #42    │ ────────────────────┤
└──────┬──────┘                     │
       │                             │
       ▼                             │
┌─────────────┐     /post-pr          │
│   Merge     │ ────────────────────┤
└──────┬──────┘                     │
       │                             │
       ▼                             │
┌─────────────┐     /task-phase      │
│ Phase 2     │ ────────────────────┤
└──────┬──────┘                     │
       │                             │
       ▼                             │
┌─────────────┐
│  Complete   │
└─────────────┘
```

---

## ❓ Common Questions

### How do I start a new feature?

1. Create feature plan: `planning/features/[feature-name]/feature-plan.md`
2. Create phase documents: `planning/features/[feature-name]/phase-N.md`
3. Start implementation: `/task-phase 1 1`

### How do I group tasks?

- **Group together:** RED + GREEN tasks (TDD cycle)
- **Separate:** Different components (API vs CLI)
- **Complete task group** before moving to next

### When do I create a PR?

- After completing **all tasks** in a phase
- Use `/pr --phase [N]` command
- Status must be current before PR

### How do I update status?

- **Automatic:** Commands update status automatically
- **Manual:** Update during work if needed
- **Post-merge:** Use `/post-pr` after merge

### Can I skip phases?

- Phases should be completed in order
- Dependencies may require sequential completion
- Some phases can be parallelized if independent

---

## 🔗 Related Documentation

### Workflow Guides

- [Workflow Overview](WORKFLOW-OVERVIEW.md) - All workflows
- [Exploration/Research/Decision Workflow](WORKFLOW-EXPLORATION-RESEARCH-DECISION.md) - Discovery workflow
- [CI/CD Improvement Workflow](WORKFLOW-CICD-IMPROVEMENT.md) - Process improvements

### Command Documentation

- `/task-phase` - Phase implementation command
- `/pr` - PR creation command
- `/post-pr` - Post-merge status updates

### Example Documents

- [Example Feature Plan](examples/example-feature-plan.md)

---

**Last Updated:** [Date]
**Status:** ✅ Active
**Next:** Create feature plan and start with `/task-phase 1 1`

