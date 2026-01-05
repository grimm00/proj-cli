# Research Topics - Test Structure Standardization

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** 2025-01-05  
**Last Updated:** 2025-01-05

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before making decisions.

---

### Research Topic 1: Python CLI Test Organization Best Practices

**Question:** What is the recommended test organization for Python CLI projects using pytest?

**Why:** Need to understand community best practices before deviating from them.

**Areas to Research:**
- pytest official documentation recommendations
- Popular CLI tools (Typer, Click, Rich) test structures
- Python packaging best practices (src/ layout implications)

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 2: Ecosystem Consistency Analysis

**Question:** What test structure should we adopt to maintain consistency across dev-infra, work-prod, and proj-cli?

**Why:** Consistency reduces cognitive load when switching between projects.

**Areas to Research:**
- Compare dev-infra structure (unit/, integration/, regression/, smoke/)
- Compare work-prod structure (unit/, integration/, performance/)
- Identify common patterns and differences
- Determine what makes sense for Python CLI vs Flask API vs Bash scripts

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 3: pytest Configuration for Subdirectories

**Question:** What pytest configuration is needed to properly support subdirectory organization?

**Why:** Need to ensure tests run correctly after reorganization.

**Areas to Research:**
- pytest.ini or pyproject.toml test configuration
- conftest.py placement and fixture scoping
- Test discovery with subdirectories
- Import path handling with src/ layout

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 4: Test Markers vs Directory Separation

**Question:** Should we rely on pytest markers (`@pytest.mark.integration`) or directory separation, or both?

**Why:** Both approaches have trade-offs; need to decide on primary organization method.

**Areas to Research:**
- Marker-based filtering (`pytest -m "not integration"`)
- Directory-based filtering (`pytest tests/unit/`)
- Combining both approaches
- CI/CD implications

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 5: Source Structure Mirroring

**Question:** Should test directories mirror the source structure (e.g., `src/proj/commands/` → `tests/unit/commands/`)?

**Why:** Mirroring makes it easy to find tests for a specific module, but may not always make sense.

**Areas to Research:**
- Flat test files vs nested structure
- When mirroring makes sense vs when it doesn't
- Balance between navigation and simplicity

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 6: Migration Strategy

**Question:** What is the safest migration path from flat to subdirectory structure?

**Why:** Need to minimize risk and disruption during reorganization.

**Areas to Research:**
- Git history preservation during file moves
- Import path updates required
- CI/CD changes needed
- Rollback strategy if issues arise

**Priority:** Low (after decision made)

**Status:** 🔴 Not Started

---

### Research Topic 7: Template Update for dev-infra

**Question:** Should we update the dev-infra standard-project template's test README?

**Why:** The current template README describes directories that generated projects may not use.

**Areas to Research:**
- Current template test README content
- Whether templates should include test subdirectories
- How to handle different testing patterns (pytest vs bats)

**Priority:** Low

**Status:** 🔴 Not Started

---

## 🎯 Research Workflow

1. Use `/research test-structure-standardization --from-explore test-structure-standardization` to conduct research
2. Research will create documents in `docs/maintainers/research/test-structure-standardization/`
3. After research complete, use `/decision test-structure-standardization --from-research` to make decisions

---

## 📊 Research Priority Summary

| Topic | Priority | Status |
|-------|----------|--------|
| Python CLI Test Best Practices | High | 🔴 Not Started |
| Ecosystem Consistency Analysis | High | 🔴 Not Started |
| pytest Configuration | Medium | 🔴 Not Started |
| Markers vs Directories | Medium | 🔴 Not Started |
| Source Structure Mirroring | Medium | 🔴 Not Started |
| Migration Strategy | Low | 🔴 Not Started |
| Template Update for dev-infra | Low | 🔴 Not Started |

---

**Last Updated:** 2025-01-05

