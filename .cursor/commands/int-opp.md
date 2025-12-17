# Document Internal Opportunities

Capture learnings from projects to improve dev-infra template and other projects. Supports any project with automatic project discovery and command adaptation workflow.

---

## Configuration

**Path Detection:**

This command supports dev-infra's opportunity structure:

- **Internal Opportunities:** `admin/planning/opportunities/internal/[project-name]/`
- **Project Hub:** `admin/planning/opportunities/internal/[project-name]/README.md`
- **Learnings:** `admin/planning/opportunities/internal/[project-name]/learnings/`
- **Improvements:** `admin/planning/opportunities/internal/[project-name]/improvements/`
- **Command Adaptations:** `admin/planning/opportunities/internal/dev-infra/command-adaptations/` (if applicable)

**Project Detection:**

- Use `--new-project` flag for automatic project discovery
- Support multiple projects
- Auto-detect project information from various sources

---

## Workflow Overview

**When to use:**

- After completing a phase or significant work
- To capture learnings for improving dev-infra template
- To create project-specific opportunity directories
- To document command adaptations for dev-infra

**Key principle:** Capture learnings while fresh, organize by project, and create actionable improvement checklists.

---

## Usage

**Command:** `/int-opp [project-name] [options]`

**Examples:**

- `/int-opp` - Capture learnings for current project (default)
- `/int-opp work-prod` - Explicitly specify work-prod
- `/int-opp dev-infra` - Create opportunities directory for dev-infra
- `/int-opp inventory-tools --new-project` - Create new project directory and discover project info
- `/int-opp dev-infra --command-adaptation` - Document command adaptations for dev-infra
- `/int-opp [project] --phase N` - Capture phase-specific learnings
- `/int-opp [project] --phase N --feature [feature-name]` - Capture phase learnings grouped by feature

**Options:**

- `--new-project` - Create directory for new project and discover project information
- `--command-adaptation` - Document command adaptations for dev-infra (use with dev-infra project)
- `--phase N` - Capture learnings for specific phase (auto-detects feature if in feature branch/context)
- `--feature [name]` - Group phase learnings by feature name (creates `learnings/[feature-name]/` subdirectory)
- `--type TYPE` - Type of opportunity (`learnings`, `improvements`, `command-adaptation`)
- `--dry-run` - Show what would be created without creating files

---

## Step-by-Step Process

### 1. Identify Project

**Default behavior:**

- If no project specified, detect current project from context
- Check if project directory exists in `admin/planning/opportunities/internal/[project]/`
- Use project name from git remote or directory name

**New project discovery (`--new-project`):**

1. **Check if directory exists:**
   - Look for `admin/planning/opportunities/internal/[project]/`
   - If exists, project is known

2. **Search for project information:**
   - Check Projects API: `./proj list --search "[project-name]"` (if available)
   - Check GitHub: Search for repository with project name
   - Check local filesystem: Look for project directories in `~/Projects/` or `~/Learning/`
   - Check if project is mentioned in documentation

3. **Gather project context:**
   - Project type (application, tool, library, template)
   - Technology stack (if known)
   - Purpose/description
   - Current status

4. **Ask for clarification (if needed):**
   - If project info is ambiguous or missing
   - Request: project description, type, purpose
   - Confirm project name and directory structure

**Checklist:**

- [ ] Project identified (or using default)
- [ ] Project directory checked/created
- [ ] Project information gathered (if new project)
- [ ] Clarification obtained (if needed)

---

### 2. Create Project Directory Structure (if new project)

**If `--new-project` specified and directory doesn't exist:**

**Directory structure:**

```
admin/planning/opportunities/internal/[project-name]/
├── README.md                    # Project hub
├── learnings/                   # Learnings from this project
│   ├── README.md                # Learnings hub
│   └── [topic]-learnings.md    # Specific learnings documents
└── improvements/                # Improvements for dev-infra/other projects
    ├── README.md                # Improvements hub
    └── [topic]-improvements.md  # Specific improvement documents
```

**Create project hub:**

**File:** `admin/planning/opportunities/internal/[project-name]/README.md`

```markdown
# [Project Name] Opportunities

**Purpose:** [Project description]  
**Type:** [Application/Tool/Library/Template]  
**Status:** ✅ Active  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Learnings

- **[Learnings Hub](learnings/README.md)** - Learnings from [project name]

### Improvements

- **[Improvements Hub](improvements/README.md)** - Improvements for dev-infra/other projects

---

## 🎯 Overview

[Project description and purpose]

**Project Context:**
- **Type:** [Application/Tool/Library/Template]
- **Technology Stack:** [If known]
- **Purpose:** [What this project does]
- **Status:** [Current status]

---

## 📊 Summary

**Learnings Documents:** [N]  
**Improvement Documents:** [M]  
**Status:** ✅ Active

---

**Last Updated:** YYYY-MM-DD
```

**Create learnings hub:**

**File:** `admin/planning/opportunities/internal/[project-name]/learnings/README.md`

```markdown
# [Project Name] Learnings

**Purpose:** Learnings from [project name] implementation  
**Target:** Inform dev-infra template and other projects  
**Status:** ✅ Active  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Learning Documents

- **[Learning Document 1]([topic]-learnings.md)** - [Description]

### Feature-Specific Learnings

- **[Feature Name Learnings]([feature-name]/README.md)** - Learnings from [feature name] ([N] phases)

---

## 🎯 Purpose

This directory contains learnings from [project name] that can inform:

- Dev-infra template improvements
- Future project patterns
- Best practices documentation

**Organization:**

- Phase learnings grouped by feature: `[feature-name]/phase-N-learnings.md`
- General learnings in root: `[topic]-learnings.md`

---

## 📊 Summary

**Total Learning Documents:** [N]  
**Feature-Specific Learnings:** [M] features  
**Status:** ✅ Active

---

**Last Updated:** YYYY-MM-DD
```

**Create feature learnings hub (if feature grouping used):**

**File:** `admin/planning/opportunities/internal/[project-name]/learnings/[feature-name]/README.md`

```markdown
# [Feature Name] Learnings

**Purpose:** Phase learnings from [feature name] implementation  
**Target:** Inform dev-infra template and other projects  
**Status:** ✅ Active  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Phase Learnings

- **[Phase 1](phase-1-learnings.md)** - [Phase description]
- **[Phase 2](phase-2-learnings.md)** - [Phase description]
- **[Phase N](phase-N-learnings.md)** - [Phase description]

---

## 🎯 Purpose

This directory contains phase-specific learnings from [feature name] implementation.

---

## 📊 Summary

**Total Phase Learnings:** [N]  
**Status:** ✅ Active

---

**Last Updated:** YYYY-MM-DD
```

**Create improvements hub:**

**File:** `admin/planning/opportunities/internal/[project-name]/improvements/README.md`

```markdown
# [Project Name] Improvements

**Purpose:** Actionable improvements based on [project name] learnings  
**Target:** Dev-infra template and other projects  
**Status:** ✅ Active  
**Last Updated:** YYYY-MM-DD

---

## 📋 Quick Links

### Improvement Documents

- **[Improvement Document 1]([topic]-improvements.md)** - [Description]

---

## 🎯 Purpose

This directory contains actionable improvement checklists based on learnings from [project name].

---

## 📊 Summary

**Total Improvement Documents:** [N]  
**Status:** ✅ Active

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Project directory created (if new project)
- [ ] Project hub README created
- [ ] Learnings directory and hub created
- [ ] Improvements directory and hub created
- [ ] Project information documented

---

### 3. Detect Feature Name (if --phase specified)

**When `--phase N` is used:**

1. **Auto-detect feature name:**

   - Check git branch name (e.g., `feat/templates-enhancement-phase-5` → `templates-enhancement`)
   - Check current directory context (if in `admin/planning/features/[feature-name]/`)
   - Check recent commits for feature name
   - Check phase document location (if exists)

2. **If `--feature [name]` provided:**

   - Use provided feature name
   - Validate feature name format (kebab-case recommended)

3. **If feature not detected:**
   - Ask user for feature name
   - Suggest feature name based on context
   - Confirm feature name before proceeding

**Feature grouping:**

- Phase learnings grouped by feature: `learnings/[feature-name]/phase-N-learnings.md`
- Non-phase learnings remain in root: `learnings/[topic]-learnings.md`

**Checklist:**

- [ ] Feature name detected or provided
- [ ] Feature name validated
- [ ] Feature subdirectory structure determined

---

### 4. Determine Opportunity Type

**Types:**

1. **Learnings** (default):
   - What worked well
   - What needs improvement
   - Unexpected discoveries
   - Time investment analysis

2. **Improvements** (for dev-infra):
   - Actionable checklists
   - Template updates needed
   - Pattern documentation

3. **Command Adaptation** (for dev-infra):
   - How to adapt commands for dev-infra
   - Command modifications needed
   - Workflow adaptations

**Auto-detection:**

- If project is `dev-infra` and `--command-adaptation` → Command Adaptation
- If project is `dev-infra` → Improvements
- Otherwise → Learnings (or ask user)

**Checklist:**

- [ ] Opportunity type determined
- [ ] Type is appropriate for project
- [ ] Type matches user intent

---

### 5. Create Opportunity Documents

#### For Learnings (Default)

**Location:** `admin/planning/opportunities/internal/[project]/learnings/`

**File naming:**

- **Phase learnings with feature:** `[feature-name]/phase-N-learnings.md` (e.g., `templates-enhancement/phase-5-learnings.md`)
- **Phase learnings without feature:** `phase-N-learnings.md` (legacy format, still supported)
- **General learnings:** `[topic]-learnings.md` (e.g., `fix-management-learnings.md`)
- **General learnings with date:** `[project]-learnings-[date].md`

**Feature grouping:**

- When `--phase N` and feature detected/provided, create feature subdirectory
- Structure: `learnings/[feature-name]/phase-N-learnings.md`
- Keeps learnings organized by feature, preventing crowding in root directory

**Learnings Template:**

```markdown
# [Project Name] Learnings - [Topic]

**Project:** [Project Name]  
**Topic:** [Topic/Phase Name]  
**Date:** YYYY-MM-DD  
**Status:** ✅ Complete  
**Last Updated:** YYYY-MM-DD

---

## 📋 Overview

[Summary of what was learned]

---

## ✅ What Worked Exceptionally Well

### [Pattern/Category]

**Why it worked:**
[Explanation]

**What made it successful:**
[Details]

**Template implications:**
[What to template]

**Key examples:**
[Code/documentation examples]

**Benefits:**
- Benefit 1
- Benefit 2

---

## 🟡 What Needs Improvement

### [Issue/Category]

**What the problem was:**
[Description]

**Why it occurred:**
[Root cause]

**Impact:**
[How it affected development]

**How to prevent:**
[Prevention strategies]

**Template changes needed:**
[Specific changes]

---

## 💡 Unexpected Discoveries

### [Discovery]

**Finding:**
[What was discovered]

**Why it's valuable:**
[Value explanation]

**How to leverage:**
[How to use this]

---

## ⏱️ Time Investment Analysis

**Breakdown:**
- [Activity]: [Time]
- [Activity]: [Time]

**What took longer:**
- [Activity]: [Reason]

**What was faster:**
- [Activity]: [Reason]

**Estimation lessons:**
- Lesson 1
- Lesson 2

---

## 📊 Metrics & Impact

**Code metrics:**
- Lines of code: [N]
- Test coverage: [X]% (if applicable)
- Files created/modified: [N]

**Quality metrics:**
- Bugs found/fixed: [N]
- External review feedback: [Summary]

**Developer experience:**
- Improvement 1
- Improvement 2

---

**Last Updated:** YYYY-MM-DD
```

---

#### For Improvements (Dev-Infra)

**Location:** `admin/planning/opportunities/internal/[project]/improvements/`

**File naming:**
- Format: `[project]-improvements-[topic].md` (e.g., `dev-infra-improvements-phaseN.md`)

**Improvements Template:**

```markdown
# [Project Name] Improvements - [Topic]

**Source:** [Project Name] - [Topic/Phase]  
**Target:** Dev-infra template  
**Status:** ✅ Complete  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Overview

[Summary of improvements]

---

## 🎯 Improvement Categories

### [Category Name]

- [ ] **Improvement Title**
  - **Location:** [File path in template]
  - **Action:** [What to do]
  - **Prevents/Enables:** [Problem solved or capability added]
  - **Content/Example:** [Code or content to add]
  - **Expected Impact:** [Benefit statement]
  - **Priority:** CRITICAL/HIGH/MEDIUM/LOW
  - **Effort:** LOW/MEDIUM/HIGH

---

**Last Updated:** YYYY-MM-DD
```

---

#### For Command Adaptation (Dev-Infra)

**Location:** `admin/planning/opportunities/internal/dev-infra/command-adaptations/`

**File naming:**
- Format: `[command-name]-adaptation.md` (e.g., `int-opp-adaptation.md`, `reflect-adaptation.md`)

**Command Adaptation Template:**

```markdown
# Command Adaptation: [Command Name] for Dev-Infra

**Source Command:** [Command name from source project]  
**Target:** Dev-infra template  
**Status:** 🔴 Not Started  
**Created:** YYYY-MM-DD  
**Last Updated:** YYYY-MM-DD

---

## 📋 Overview

[Description of command and how it should be adapted for dev-infra]

---

## 🎯 Original Command

**Command:** `/[command-name]`  
**Purpose:** [Original purpose]  
**Location:** `.cursor/commands/[command-name].md`

**Key Features:**
- Feature 1
- Feature 2

---

## 🔄 Adaptations Needed

### [Adaptation Category]

**Change:** [What needs to change]  
**Reason:** [Why this change is needed]  
**Impact:** [How this affects dev-infra usage]

**Original:**
[Original code/pattern]

**Adapted:**
[Adapted code/pattern]

**Files to modify:**
- `[file1]` - [reason]
- `[file2]` - [reason]

---

## 📝 Implementation Steps

1. **Step 1: [Name]**
   - [ ] Task 1
   - [ ] Task 2

2. **Step 2: [Name]**
   - [ ] Task 1
   - [ ] Task 2

---

## ✅ Definition of Done

- [ ] Command adapted for dev-infra
- [ ] Documentation updated
- [ ] Tests updated (if applicable)
- [ ] Ready for use in dev-infra

---

**Last Updated:** YYYY-MM-DD
```

---

### 6. Update Project Hubs

**Update project hub:**

- Add new document to Quick Links
- Update summary statistics
- Update "Last Updated" date

**Update learnings hub:**

- If feature grouping: Add link to feature learnings hub (if first phase for feature)
- If no feature grouping: Add document link directly
- Update summary statistics
- Update "Last Updated" date

**Update feature learnings hub (if feature grouping):**

- Add phase learnings link
- Update phase count
- Update "Last Updated" date

**Checklist:**

- [ ] Project hub updated
- [ ] Learnings hub updated
- [ ] Feature learnings hub updated (if feature grouping)
- [ ] Quick links added
- [ ] Summary statistics updated

---

### 7. Update Main Internal Opportunities Hub

**File:** `admin/planning/opportunities/internal/README.md`

**Add project entry:**

```markdown
### [Project Name] Opportunities

- **[Project Hub]([project-name]/README.md)** - [Project description]
  - Learnings: [N] documents
  - Improvements: [M] documents
```

**Update completion tracking:**

```markdown
| Project | Learnings | Improvements | Status |
|---------|-----------|--------------|--------|
| work-prod | [N] | [M] | ✅ Active |
| dev-infra | [N] | [M] | ✅ Active |
| [project] | [N] | [M] | ✅ Active |
```

**Checklist:**

- [ ] Main hub updated with project entry
- [ ] Completion tracking updated
- [ ] Quick links updated
- [ ] "Last Updated" date updated

---

### 8. Commit and Push Changes

**IMPORTANT:** Always commit work before completing command.

**Reference:** [Commit Workflow](../../docs/COMMIT-WORKFLOW.md) - Central commit workflow documentation, especially [Documentation/Chore Branches](../../docs/COMMIT-WORKFLOW.md#documentationchore-branches) section

**Since learnings/improvements are documentation-only, use docs-only workflow:**

**Branch naming:**

- Format: `docs/int-opp-[project]-[topic]` (e.g., `docs/int-opp-dev-infra-phase-4`)
- Or: `docs/int-opp-[project]-learnings` (for general learnings)

**Steps:**

1. **Check current branch:**

   ```bash
   git branch --show-current
   ```

2. **Create docs branch (if not already on one):**

   ```bash
   git checkout -b docs/int-opp-[project]-[topic]
   ```

3. **Stage all changes:**

   ```bash
   git add admin/planning/opportunities/internal/
   ```

4. **Commit with proper message:**

   ```bash
   git commit -m "docs(learnings): capture [project] learnings - [topic]

   Created learnings document:
   - [Brief summary of learnings]
   - Updated project hub
   - Updated learnings hub
   - Updated main opportunities hub

   Related: [Phase N or topic]"
   ```

5. **Push branch:**

   ```bash
   git push origin docs/int-opp-[project]-[topic]
   ```

6. **Merge directly to develop (docs-only, no PR needed):**

   ```bash
   git checkout develop
   git pull origin develop
   git merge docs/int-opp-[project]-[topic] --no-edit
   git push origin develop
   ```

7. **Clean up branch:**

   ```bash
   git branch -d docs/int-opp-[project]-[topic]
   git push origin --delete docs/int-opp-[project]-[topic]
   ```

8. **Verify no uncommitted changes:**
   ```bash
   git status --short
   ```

**Commit message examples:**

**For phase learnings:**

```bash
git commit -m "docs(learnings): capture dev-infra learnings - Phase 4

Created learnings document for Phase 4:
- What worked well: Requirements template pattern replication
- What needs improvement: Template generation testing
- Unexpected discoveries: Commands already support template structure
- Time analysis: ~20 minutes (faster than estimated)

Updated learnings hub with new document link.

Related: Phase 4"
```

**For general learnings:**

```bash
git commit -m "docs(learnings): capture work-prod learnings - Fix Management

Created learnings document:
- What worked well: Batch-based fix planning
- What needs improvement: Priority assessment timing
- Unexpected discoveries: Automated fix detection patterns

Updated project hub and learnings hub.

Related: Fix Management Workflow"
```

**Checklist:**

- [ ] Docs branch created
- [ ] All changes staged
- [ ] Commit message follows conventional format
- [ ] Branch pushed to remote
- [ ] Merged directly to develop
- [ ] Branch cleaned up (local and remote)

**Note:** Learnings/improvements are documentation-only, so they can be merged directly to `develop` without a PR, following Git Flow pattern for `docs/*` branches.

---

## Project Discovery Process (--new-project)

### 1. Check Existing Projects

**Search locations:**

1. **Projects API:**
   ```bash
   ./proj list --search "[project-name]"  # If available
   ```

2. **GitHub:**
   ```bash
   gh repo list --search "[project-name]"
   ```

3. **Local filesystem:**
   ```bash
   find ~/Projects ~/Learning -type d -name "*[project-name]*" 2>/dev/null
   ```

4. **Documentation:**
   - Search README files
   - Check exploration documents
   - Check research documents

**Checklist:**

- [ ] Projects API searched (if available)
- [ ] GitHub searched
- [ ] Local filesystem searched
- [ ] Documentation searched

---

### 2. Gather Project Information

**If project found:**

- Extract: name, description, type, technology stack, status
- Verify: project path, repository URL, current state

**If project not found:**

- Ask user for:
  - Project name (confirm spelling)
  - Project type (application, tool, library, template)
  - Project purpose/description
  - Technology stack (if known)
  - Current status
  - Project location (if exists)

**Checklist:**

- [ ] Project information gathered
- [ ] Project details verified
- [ ] Missing information requested from user

---

### 3. Create Project Directory

**After gathering information:**

1. Create project directory structure
2. Create project hub with gathered information
3. Create learnings and improvements directories
4. Document project context in hub

**Checklist:**

- [ ] Project directory created
- [ ] Project hub created with information
- [ ] Directory structure complete
- [ ] Project context documented

---

## Command Adaptation Workflow (--command-adaptation)

### When to Use

**Use with dev-infra project:**

- When adapting commands for dev-infra template
- When documenting how commands should work in dev-infra
- When creating adaptation guides for command porting

**Example:**

```bash
/int-opp dev-infra --command-adaptation
```

---

### 1. Identify Commands to Adapt

**Source commands:**

- List commands in `.cursor/commands/` directory
- Identify commands that should be adapted for dev-infra
- Prioritize by usage and importance

**Common commands to adapt:**

- `/int-opp` - This command itself
- `/reflect` - Reflection workflow
- `/fix-plan` - Fix planning workflow
- `/transition-plan` - Transition planning
- `/task-phase` - Phase implementation workflow

**Checklist:**

- [ ] Commands identified
- [ ] Priority assigned
- [ ] Adaptation order determined

---

### 2. Analyze Command for Adaptation

**For each command:**

1. **Read command documentation:**
   - Understand original purpose
   - Identify key features
   - Note project-specific assumptions

2. **Identify adaptations needed:**
   - What's project-specific?
   - What should be generic?
   - What paths need to change?
   - What assumptions need updating?

3. **Document adaptations:**
   - Create adaptation document
   - Document changes needed
   - Provide examples

**Checklist:**

- [ ] Command analyzed
- [ ] Adaptations identified
- [ ] Adaptation document created

---

### 3. Create Command Adaptation Document

**Location:** `admin/planning/opportunities/internal/dev-infra/command-adaptations/`

**File naming:**
- Format: `[command-name]-adaptation.md`

**Template:** See "Command Adaptation Template" above

**Checklist:**

- [ ] Adaptation document created
- [ ] Adaptations documented
- [ ] Examples provided
- [ ] Implementation steps outlined

---

### 4. Update Dev-Infra Hub

**File:** `admin/planning/opportunities/internal/dev-infra/README.md`

**Add command adaptations section:**

```markdown
### Command Adaptations

- **[Command Adaptations Hub](command-adaptations/README.md)** - How to adapt commands for dev-infra
```

**Checklist:**

- [ ] Dev-infra hub updated
- [ ] Command adaptations section added
- [ ] Links to adaptation documents added

---

## Common Scenarios

### Scenario 1: Capture Phase Learnings

**Command:** `/int-opp [project] --phase N` or `/int-opp [project] --phase N --feature [feature-name]`

**Process:**

1. Identify project
2. Detect feature name (from git branch, context, or `--feature` flag)
3. Create feature subdirectory if needed: `learnings/[feature-name]/`
4. Create phase learnings document: `learnings/[feature-name]/phase-N-learnings.md`
5. Create/update feature learnings hub: `learnings/[feature-name]/README.md`
6. Update main learnings hub
7. Update project hub

---

### Scenario 2: Create New Project Directory

**Command:** `/int-opp inventory-tools --new-project`

**Process:**
1. Search for inventory-tools project
2. Gather project information
3. Ask for clarification if needed
4. Create project directory structure
5. Create project hub with information

---

### Scenario 3: Document Command Adaptation

**Command:** `/int-opp dev-infra --command-adaptation`

**Process:**
1. Identify commands to adapt
2. Analyze each command
3. Create adaptation documents
4. Update dev-infra hub

---

## Tips

### For New Projects

- Search thoroughly before asking user
- Gather as much information as possible automatically
- Only ask for clarification when information is ambiguous
- Document project context clearly in hub

### For Command Adaptations

- Focus on making commands generic/reusable
- Document project-specific assumptions
- Provide clear examples
- Think about how dev-infra will use the command

### For Learnings

- Capture while fresh (right after phase/work)
- Be specific with examples
- Focus on actionable items
- Think about template implications

---

## Reference

**Project Directories:**

- `admin/planning/opportunities/internal/[project-name]/`

**Command Files:**

- `.cursor/commands/[command-name].md`

**Related Commands:**

- `/reflect` - Create reflection documents (if available)
- `/transition-plan` - Create transition plans (if available)
- `/fix-plan` - Create fix plans (if available)

---

## 📊 Log Usage (Final Step)

**After successful command completion, update the usage tracker:**

1. **Update:** `admin/planning/commands/usage-tracker.md`
2. **Add entry to "Recent Usage" table:**
   ```markdown
   | YYYY-MM-DD | `/int-opp` | [Context] | ✅ Success | [Evidence] |
   ```
3. **Increment usage count** in summary table
4. **Commit with message:**
   ```
   docs(commands): update usage tracker - /int-opp
   ```

**Why:** Tracks command maturity for graduation decisions per [ADR-004](../admin/decisions/dev-infra-identity-and-focus/adr-004-graduation-process.md).

---

**Last Updated:** 2025-12-17  
**Status:** ✅ Active  
**Next:** Use to capture learnings, create project directories, or document command adaptations (supports any project with automatic discovery, feature-grouped phase learnings)
