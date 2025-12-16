# proj-cli

**Purpose:** Project Management Client for managing projects and inventory  
**Version:** v0.1.0  
**Last Updated:** 2025-12-16  
**Status:** 🟡 In Development

---

## ⚠️ Experimental Template

This template includes **experimental/evolving commands** that are not yet stable enough for the standard template.

### Stability Levels

| Indicator | Level | Meaning |
| --------- | ----- | ------- |
| 🟢 | Stable | Production-ready, included in standard template |
| 🟠 | Experimental | May change, included only in experimental template |
| 🔴 | Deprecated | Being removed, migration guide available |

📖 **Learn More:** [Stability Levels Documentation](docs/STABILITY-LEVELS.md)

### What Experimental Means

- 🟠 May change without notice
- 🟠 May have incomplete documentation
- 🟠 May be removed or significantly modified
- 🟠 Provide early access to new features

### When to Use This Template

**Use experimental-project if:**

- You want early access to new commands
- You're comfortable with potential breaking changes
- You can provide feedback on evolving features

**Use standard-project if:**

- You need maximum stability
- You're building production systems
- You prefer proven, stable commands

### Experimental Commands

| Command | Status | Description |
| ------- | ------ | ----------- |
| `/status` | 🟠 Experimental | Project status tracking and sync |

### Graduation Process

Commands graduate from Experimental (🟠) to Stable (🟢) when they meet the graduation criteria:

- ≥1 release cycle in experimental
- No major changes in 2+ weeks  
- Documentation 100% complete
- Demonstrated successful use

📖 **Full Criteria:** [Graduation Checklist](docs/GRADUATION-CHECKLIST.md)

### 💬 Provide Feedback

Your feedback helps experimental features improve and graduate to stable!

- **Report issues or suggestions:** [Create Feedback Issue](.github/ISSUE_TEMPLATE/experimental-feedback.yml)
- **Share your experience** with experimental commands
- **Vote on graduation readiness** in feedback issues

**We especially want to know:**

- What works well?
- What needs improvement?
- Is the feature ready to graduate?

---

## 🎯 Quick Start

### Prerequisites

- [List any prerequisites]
- [Development environment requirements]

### Setup

```bash
# Clone and setup
git clone [repository-url]
cd [project-name]

# Install dependencies
[installation commands]

# Start development environment
[development commands]
```

### First Steps

1. [First step]
2. [Second step]
3. [Third step]

---

## 📁 Project Structure

This project follows a **hub-and-spoke documentation pattern**:

- **Hub Files** (README.md) serve as entry points and navigation guides
- **Spoke Directories** contain detailed implementation and specialized documentation
- **Maintainers Directory** manages project planning, feedback, and decision tracking

### Key Directories

- **`docs/maintainers/`** - Project management hub ([Maintainers Guide](docs/maintainers/README.md))
- **`backend/`** - Backend application ([Backend Guide](backend/README.md))
- **`frontend/`** - Frontend application ([Frontend Guide](frontend/README.md))
- **`tests/`** - Centralized testing ([Testing Guide](tests/README.md))
- **`scripts/`** - Automation scripts ([Scripts Guide](scripts/README.md))
- **`docs/`** - User documentation ([Documentation Guide](docs/README.md))

---

## 🚀 Development Workflow

### Git Flow

- **`main`** - Production releases only
- **`develop`** - Ongoing development
- **`feat/*`** - Feature branches (require PRs)
- **`fix/*`** - Bug fixes (require PRs)
- **`docs/*`** - Documentation (can push directly)
- **`chore/*`** - Maintenance (can push directly)

### Branch Requirements

- Feature branches: Full testing, linting, external reviews
- Documentation branches: Minimal validation
- Release branches: Full validation + external reviews

---

## 🤖 Workflow Automation Commands

This project includes workflow automation commands to streamline development, planning, and project management. All commands are located in `.cursor/commands/` and can be used directly in Cursor IDE.

### Quick Reference

| Command | Purpose | Common Use Case |
|---------|---------|----------------|
| `/task-phase` | Implement feature phase tasks | Daily development work |
| `/task-improvement` | Implement CI/CD improvement tasks | Process improvements |
| `/task-release` | Implement release tasks | Release preparation |
| `/pr` | Create pull requests | After completing work |
| `/pr-validation` | Validate and review PRs | PR review workflow |
| `/post-pr` | Update docs after PR merge | Post-merge cleanup |
| `/explore` | Start exploration cycles | New ideas/concepts |
| `/research` | Conduct structured research | Before decisions |
| `/decision` | Make architecture decisions | After research |
| `/transition-plan` | Create transition plans | Planning next steps |
| `/reflect` | Analyze project state | After milestones |
| `/reflection-artifacts` | Extract planning artifacts | From reflections |
| `/fix-plan` | Create fix plans from reviews | After code review |
| `/fix-implement` | Implement fixes | Fix batch work |
| `/fix-review` | Review deferred issues | Issue prioritization |
| `/pre-phase-review` | Review phase plans | Before implementation |
| `/int-opp` | Document internal opportunities | Capture learnings |
| `/cursor-rules` | Manage cursor rules | Update AI config |

### Core Workflow Commands

#### Feature Development

- **`/task-phase [N]`** - Implement phase tasks following TDD workflow
  - Reads from `docs/maintainers/planning/features/[feature-name]/phase-N.md`
  - Groups RED+GREEN tasks together
  - Creates commits after each task group
  - Use `/pr --phase [N]` when phase complete

- **`/pr --phase [N]`** - Create PR for completed phase
  - Validates phase completion
  - Creates comprehensive PR description
  - Includes status updates

- **`/post-pr`** - Update documentation after PR merge
  - Updates phase status
  - Updates feature status
  - Updates planning documents

#### CI/CD Improvements

- **`/task-improvement [N]`** - Implement CI/CD improvement tasks
  - Reads from `docs/maintainers/planning/ci/[improvement-name]/phase-N.md`
  - Focuses on process/documentation workflow
  - Similar to `/task-phase` but for CI/CD improvements

#### Exploration → Research → Decision → Planning

- **`/explore [topic]`** - Start exploration cycle
  - Creates exploration documents
  - Identifies research topics
  - Output: `docs/maintainers/planning/explorations/[topic]/`

- **`/research [topic] --from-explore [topic]`** - Conduct research
  - Reads research topics from exploration
  - Creates research documents
  - Extracts requirements
  - Output: `docs/maintainers/research/[topic]/` + `requirements.md`

- **`/decision [topic] --from-research`** - Make decisions
  - Reads research documents
  - Creates ADR documents
  - Output: `docs/maintainers/decisions/[topic]/` + ADRs

- **`/transition-plan --from-adr`** - Transition to planning
  - Reads ADR documents
  - Creates feature plan and phases
  - Output: Feature plan + phase documents

#### Reflection and Learning

- **`/reflect`** - Analyze project state
  - Reviews recent work
  - Identifies opportunities
  - Provides actionable suggestions

- **`/reflection-artifacts --type [type]`** - Extract planning artifacts
  - Creates feature plans, release checklists, CI/CD improvements
  - From reflection documents
  - Ready for implementation

- **`/int-opp`** - Document internal opportunities
  - Captures learnings from projects
  - Creates opportunity documents
  - Supports template evolution

#### Code Review and Fixes

- **`/fix-plan`** - Create fix plans from reviews
  - Analyzes Sourcery reviews
  - Batches issues by priority
  - Creates fix plans ready for implementation

- **`/fix-implement [batch]`** - Implement fixes
  - Reads fix plan batch
  - Implements fixes following TDD
  - Creates PR when batch complete

- **`/fix-review`** - Review deferred issues
  - Identifies candidates for addressing
  - Helps prioritize old issues

#### Release Management

- **`/task-release`** - Implement release tasks
  - Reads release transition plan
  - Implements release preparation tasks
  - Similar to `/task-phase` but for releases

#### Project Management

- **`/pre-phase-review`** - Review phase plans
  - Validates phase completeness
  - Checks dependencies
  - Ensures ready for implementation

- **`/pr-validation`** - Validate and review PRs
  - Manual testing workflow
  - Documentation updates
  - Code review integration

- **`/cursor-rules`** - Manage cursor rules
  - Updates AI assistant configuration
  - Creates new rule files
  - Maintains rule documentation

### Command Documentation

All commands have detailed documentation in `.cursor/commands/`. Each command includes:

- Configuration and path detection
- Workflow overview
- Step-by-step process
- Usage examples
- Common patterns
- Integration with other commands

### Getting Started

1. **Start with exploration:** Use `/explore [topic]` for new ideas
2. **Research before decisions:** Use `/research [topic]` to investigate
3. **Make decisions:** Use `/decision [topic]` to document decisions
4. **Plan implementation:** Use `/transition-plan --from-adr` to create plans
5. **Implement features:** Use `/task-phase [N]` for development work
6. **Create PRs:** Use `/pr --phase [N]` when work is complete
7. **Reflect and learn:** Use `/reflect` and `/int-opp` to capture learnings

### Workflow Examples

**Feature Development:**
```
/explore new-feature
  → /research new-feature --from-explore new-feature
  → /decision new-feature --from-research
  → /transition-plan --from-adr
  → /task-phase 1
  → /pr --phase 1
```

**CI/CD Improvement:**
```
/reflect
  → /reflection-artifacts --type ci-cd
  → /task-improvement 1
  → /pr --ci-improvement [name] --phase 1
```

**Fix Implementation:**
```
/fix-plan
  → /fix-implement batch-1
  → /pr --fix batch-1
```

---

## 📚 Documentation

## 🛠️ Technology Stack

### Backend

- [Technology 1]
- [Technology 2]
- [Technology 3]

### Frontend

- [Technology 1]
- [Technology 2]
- [Technology 3]

### DevOps

- [Technology 1]
- [Technology 2]
- [Technology 3]

---

## 📊 Project Status

### ✅ Completed

- [Completed feature 1]
- [Completed feature 2]

### 🟠 In Progress

- [Current feature 1]
- [Current feature 2]

### 🟡 Planned

- [Planned feature 1]
- [Planned feature 2]

---

## 📚 Documentation

### Quick References

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Contributing Guide](CONTRIBUTING.md)

### Planning Documents

- [Project Roadmap](docs/maintainers/planning/roadmap.md)
- [Feature Plans](docs/maintainers/planning/features/)
- [CI/CD Improvements](docs/maintainers/planning/ci/)
- [Release History](docs/maintainers/planning/releases/)

---

## 🔄 CI/CD Improvements

This project supports CI/CD improvements for process enhancements, workflow automation, and infrastructure improvements.

### CI/CD Improvement Structure

**Location:** `docs/maintainers/planning/ci/[improvement-name]/`

**Key Files:**
- `README.md` - Improvement hub
- `improvement-plan.md` - Improvement plan
- `phase-N.md` - Phase documents

**Key Differences from Features:**
- Uses `improvement-plan.md` instead of `feature-plan.md`
- No `status-and-next-steps.md` file (status tracked in README.md)
- Similar phase structure to features
- Use `/task-improvement` command instead of `/task-phase`

### Creating CI/CD Improvements

1. **Create improvement directory:**
   ```bash
   mkdir -p docs/maintainers/planning/ci/[improvement-name]
   ```

2. **Create improvement plan:**
   - Copy `docs/maintainers/planning/ci/improvement-plan-template.md` as `improvement-plan.md`
   - Fill in improvement details
   - Define implementation steps

3. **Create phase documents:**
   - Create `phase-1.md`, `phase-2.md`, etc.
   - Define tasks and deliverables

4. **Implement improvements:**
   - Use `/task-improvement [N]` to implement phases
   - Use `/pr --ci-improvement [name]` to create PRs

### CI/CD vs Feature Structure

| Aspect | Features | CI/CD Improvements |
|--------|----------|-------------------|
| Plan File | `feature-plan.md` | `improvement-plan.md` |
| Status File | `status-and-next-steps.md` | Status in `README.md` |
| Command | `/task-phase` | `/task-improvement` |
| Phase Structure | Similar | Similar |
| Purpose | User-facing features | Process/infrastructure improvements |

---

## 🔍 Exploration/Research/Decision Workflows

This project supports structured workflows for exploring ideas, conducting research, and making architectural decisions before transitioning to feature planning.

### Directory Structure

**Hub Directories:**
- `docs/maintainers/planning/explorations/` - Exploration hub (created by template)
- `docs/maintainers/research/` - Research hub (created by template)
- `docs/maintainers/decisions/` - Decisions hub (created by template)

**Topic-Specific Directories:**
- Commands (`/explore`, `/research`, `/decision`) create topic-specific directories automatically
- Example: `/explore my-topic` creates `docs/maintainers/planning/explorations/my-topic/`
- Example: `/research my-topic` creates `docs/maintainers/research/my-topic/`
- Example: `/decision my-topic` creates `docs/maintainers/decisions/my-topic/`

### Workflow: Exploration → Research → Decision → Planning

1. **Exploration** (`/explore [topic]`)
   - Organize abstract ideas and proof of concepts
   - Identify research topics
   - Creates: `docs/maintainers/planning/explorations/[topic]/`

2. **Research** (`/research [topic]`)
   - Conduct structured research on identified topics
   - Extract functional and non-functional requirements
   - Creates: `docs/maintainers/research/[topic]/` + `requirements.md`

3. **Decision** (`/decision [topic]`)
   - Make architectural decisions based on research
   - Create Architecture Decision Records (ADRs)
   - Creates: `docs/maintainers/decisions/[topic]/` + ADRs

4. **Transition** (`/transition-plan --from-adr`)
   - Transition from decisions to feature planning
   - Creates feature plan and phase documents
   - Ready for implementation with `/task-phase`

### Hub vs Topic-Specific Directories

**Hub Directories:**
- Created by templates (already present in new projects)
- Contain `README.md` files that serve as navigation hubs
- Provide overview and workflow documentation
- List active explorations/research/decisions

**Topic-Specific Directories:**
- Created by commands (`/explore`, `/research`, `/decision`)
- Contain topic-specific documents
- Automatically organized under hub directories
- Commands populate these directories with structured content

### Getting Started

1. **Start exploration:** Use `/explore [topic]` for new ideas
2. **Conduct research:** Use `/research [topic]` to investigate
3. **Make decisions:** Use `/decision [topic]` to document decisions
4. **Plan implementation:** Use `/transition-plan --from-adr` to create plans

### Example Workflow

```
/explore new-feature
  → Creates: docs/maintainers/planning/explorations/new-feature/
  → Identifies research topics

/research new-feature --from-explore new-feature
  → Creates: docs/maintainers/research/new-feature/
  → Extracts requirements

/decision new-feature --from-research
  → Creates: docs/maintainers/decisions/new-feature/
  → Creates ADRs

/transition-plan --from-adr docs/maintainers/decisions/new-feature/adr-001-*.md
  → Creates: docs/maintainers/planning/features/new-feature/
  → Ready for /task-phase
```

---

## 🔧 Development Commands

```bash
# Development
[dev command]

# Testing
[test command]

# Building
[build command]

# Deployment
[deploy command]
```

---

## 📈 Metrics

- [Key metric 1]
- [Key metric 2]
- [Key metric 3]

---

## 🎊 Key Achievements

1. [Achievement 1]
2. [Achievement 2]
3. [Achievement 3]

---

## 📞 Support

- [Documentation](docs/)
- [Issues]([issues-url])
- [Discussions]([discussions-url])

---

**Last Updated:** 2025-12-16  
**Status:** [Status]  
**Next:** [Next milestone]
