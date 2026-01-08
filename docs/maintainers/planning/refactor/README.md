# Refactoring Hub

**Purpose:** Code quality improvements and internal restructuring  
**Status:** ✅ Active  
**Last Updated:** 2026-01-07

---

## 📋 Quick Links

### Active Refactors

- **[code-structure-refactoring](code-structure-refactoring/README.md)** - Split large modules, organize tests (🔴 Scaffolding)

---

## 🎯 Overview

The refactor directory contains internal code quality improvements that:
- Don't add new user-facing functionality
- Don't require research/decision workflow
- Focus on maintainability, organization, and code health

### Refactor vs Feature vs CI/CD

| Category | Purpose | Workflow |
|----------|---------|----------|
| **Refactor** | Code quality, restructuring | Explore → Plan → Implement |
| **Feature** | New user functionality | Research → Decision → Plan → Implement |
| **CI/CD** | Pipeline, automation | Improvement plan → Implement |

---

## 📁 Directory Structure

```
refactor/
├── README.md                    # 📍 HUB - This file
└── [refactor-name]/             # Individual refactors
    ├── README.md                # Refactor hub
    ├── feature-plan.md          # Refactor plan (reuse feature template)
    ├── status-and-next-steps.md # Progress tracking
    ├── phase-1.md               # Phase details
    └── phase-N.md               # Additional phases
```

---

## 🔄 Refactor Workflow

### Simplified Workflow (vs Features)

```
Exploration (optional)
    ↓
/transition-plan --type refactor
    ↓
/task-phase [N]
    ↓
/pr --phase [N]
```

**Key Differences from Features:**
- No `/research` command needed
- No `/decision` or ADR required
- Exploration is optional (can start from proposal)
- Simpler documentation structure

### When to Use Refactor vs Feature

**Use Refactor for:**
- Splitting large modules
- Reorganizing directory structure
- Improving code organization
- Removing technical debt
- Internal restructuring

**Use Feature for:**
- New commands or flags
- New user-facing capabilities
- API changes
- Integration additions

---

## 📊 Status Overview

### 🟠 In Progress

| Refactor | Current Phase | Progress | Effort |
|----------|---------------|----------|--------|
| code-structure-refactoring | Scaffolding | 0% | ~4-5 hrs |

### ✅ Completed

| Refactor | Completed | Result |
|----------|-----------|--------|
| - | - | - |

---

## 🚀 Quick Start

### Starting a New Refactor

1. **Create from exploration** (if exists):
   ```
   /transition-plan [exploration-path] --type refactor
   ```

2. **Create from proposal** (direct):
   ```bash
   mkdir -p docs/maintainers/planning/refactor/[refactor-name]
   # Copy templates, define phases
   ```

3. **Implement phases**:
   ```
   /task-phase [N] --refactor [refactor-name]
   ```

---

## 📚 Related

- **[Features](../features/README.md)** - User-facing functionality
- **[CI/CD](../ci/README.md)** - Pipeline improvements
- **[Explorations](../../explorations/README.md)** - Research and discovery

---

**Last Updated:** 2026-01-07
