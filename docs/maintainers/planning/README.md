# Planning Hub

**Purpose:** Central coordination for project planning and roadmap management
**Status:** ✅ Active
**Last Updated:** 2026-01-07

---

## 📋 Quick Links

### Core Planning

- **[Features](features/README.md)** - Feature-based planning and tracking
- **[Refactor](refactor/README.md)** - Code quality and restructuring (NEW)
- **[Explorations](../explorations/README.md)** - Early-stage explorations and proof of concepts
- **[Releases](releases/README.md)** - Release management and versioning
- **[Phases](phases/README.md)** - Development phase tracking
- **[Notes](notes/README.md)** - Planning insights and decisions

### CI/CD Planning

- **[CI/CD](ci/README.md)** - Continuous integration and deployment planning

---

## 🎯 Overview

The planning directory organizes all project planning activities using a hub-and-spoke documentation pattern. Each planning area has its own directory with focused documentation.

### Planning Philosophy

1. **Feature-Based Planning** - Organize work around user-facing features
2. **Hub-and-Spoke Documentation** - Clear entry points with detailed spoke documents
3. **Progressive Disclosure** - Overview → Plan → Phases → Analysis
4. **Status Tracking** - Consistent indicators and progress monitoring
5. **Decision Documentation** - Rationale and context preservation

---

## 📁 Directory Structure

```
planning/
├── features/                   # 📡 SPOKE - Feature planning
│   └── [feature-name]/        # Individual feature directories
│       ├── README.md          # Feature hub
│       ├── feature-plan.md    # High-level plan
│       ├── status-and-next-steps.md # Current status
│       ├── quick-start.md     # Implementation guide
│       ├── phase-*.md         # Phase details
│       └── fix/               # Troubleshooting docs
├── explorations/              # 📡 SPOKE - Early explorations
│   └── [topic]/               # Topic-specific exploration
│       ├── README.md          # Exploration hub
│       ├── exploration.md     # Main exploration doc
│       └── research-topics.md # Research questions
├── releases/                  # 📡 SPOKE - Release management
│   ├── README.md              # Release hub
│   ├── history.md             # Release timeline
│   └── vX.Y.Z/                # Version-specific
│       ├── checklist.md       # Release checklist
│       └── release-notes.md   # Release notes
├── phases/                    # 📡 SPOKE - Development phases
│   └── *.md                   # Phase documentation
├── notes/                     # 📡 SPOKE - Planning insights
│   ├── opportunities/         # Feature opportunities
│   └── *.md                   # Planning notes
└── ci/                        # 📡 SPOKE - CI/CD planning
    └── [project-name]/        # CI project directories
```

---

## 🎨 Planning Patterns

### Feature Development Lifecycle

1. **Discovery** - Identify feature opportunity
2. **Planning** - Create feature-plan.md with phases
3. **Implementation** - Execute phases with status tracking
4. **Completion** - Document results and lessons learned

### Release Management

1. **Planning** - Create release directory with checklist
2. **Preparation** - Complete checklist items
3. **Release** - Deploy and document
4. **Post-Release** - Update history and roadmap

### Phase Tracking

1. **Definition** - Clear phase boundaries and deliverables
2. **Execution** - Status tracking and progress updates
3. **Completion** - Results documentation and handoff
4. **Review** - Lessons learned and process improvement

---

## 📊 Current Status

### ✅ Active Planning

- **[Code Structure Refactoring](refactor/code-structure-refactoring/)** - Split large modules and organize tests (🔴 Scaffolding)
- **[Work-Prod Integration](../explorations/work-prod-integration/)** - API integration patterns (🔴 Exploration)

### 🟡 Planned Items

- v0.4.0 - Code quality improvements (refactoring)
- v0.5.0 - Work-prod integration features

### 📈 Planning Metrics

- **Features Completed:** 3 (proj-cli, template-generation, project-type-support)
- **Current Version:** v0.3.1

---

## 🚀 Quick Start

### Starting a New Feature

1. Create feature directory: `features/[feature-name]/`
2. Copy templates from this guide
3. Create README.md with quick links
4. Write feature-plan.md with overview
5. Create phase-1.md with first phase details

### Planning a Release

1. Create release directory: `releases/vX.Y.Z/`
2. Add checklist.md with release steps
3. Write release-notes.md
4. Update history.md and roadmap.md

### Documenting Decisions

1. Create note in `notes/` directory
2. Document options and rationale
3. Link to related planning documents
4. Update status as decisions are made

---

## 📚 Related Documents

### Planning Guides

- [Feature Planning](features/README.md) - Feature development process
- [Release Process](releases/README.md) - Release management guide
- [Phase Management](phases/README.md) - Development phase tracking

### External References

- [Hub-and-Spoke Best Practices](../../../../docs/BEST-PRACTICES.md) - See hub-and-spoke documentation patterns

---

**Last Updated:** 2026-01-07
**Status:** ✅ Active
**Next:** Begin code structure refactoring (v0.4.0)
