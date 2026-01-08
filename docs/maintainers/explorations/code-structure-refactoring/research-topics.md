# Research Topics - Code Structure Refactoring

**Purpose:** List of research topics/questions to investigate  
**Status:** 🟡 Partial (sufficient for decision)  
**Created:** 2025-01-05  
**Last Updated:** 2026-01-07

---

## 📋 Research Topics

This document lists research topics and questions identified during exploration. Topics are marked as addressed, deferred, or pending.

---

## Part A: Source Code Refactoring

### Research Topic A1: Module Size Best Practices

**Question:** When is a Python module too large, and how should it be split?

**Why:** Need guidance on when/how to split `projects.py` (943 lines).

**Areas to Research:**
- Python module size guidelines
- Single responsibility principle in practice
- Package vs module trade-offs

**Priority:** High

**Status:** ✅ Addressed (via analysis)

**Resolution:** 
- 943 lines with 4 create modes and 14 functions is clearly too large
- Convert to package with single-responsibility modules
- See `implementation-plan.md` for target structure

---

### Research Topic A2: Package Structure Patterns

**Question:** What's the best way to structure a commands package with multiple subcommands?

**Why:** Need to ensure the refactored structure follows Python best practices.

**Areas to Research:**
- Typer/Click command organization patterns
- Re-export patterns in `__init__.py`
- Import path implications

**Priority:** High

**Status:** ✅ Addressed (via analysis)

**Resolution:**
- Use `__init__.py` for re-exports (maintains backward compatibility)
- Group by functionality: helpers, list, crud, create, import_export
- See `implementation-plan.md` for module breakdown

---

## Part B: Test Structure

### Research Topic B1: Python CLI Test Organization Best Practices

**Question:** What is the recommended test organization for Python CLI projects using pytest?

**Why:** Need to understand community best practices before deviating from them.

**Areas to Research:**
- pytest official documentation recommendations
- Popular CLI tools (Typer, Click, Rich) test structures
- Python packaging best practices (src/ layout implications)

**Priority:** High

**Status:** ✅ Addressed (via ecosystem analysis)

**Resolution:**
- pytest supports both flat and subdirectory structures
- Subdirectories are preferred for larger projects
- src/ layout works well with subdirectory tests

---

### Research Topic B2: Ecosystem Consistency Analysis

**Question:** What test structure should we adopt to maintain consistency across dev-infra, work-prod, and proj-cli?

**Why:** Consistency reduces cognitive load when switching between projects.

**Areas to Research:**
- Compare dev-infra structure (unit/, integration/, regression/, smoke/)
- Compare work-prod structure (unit/, integration/, performance/)
- Identify common patterns and differences
- Determine what makes sense for Python CLI vs Flask API vs Bash scripts

**Priority:** High

**Status:** ✅ Addressed (via exploration.md)

**Resolution:**
- Both sibling projects use subdirectory structure
- Common pattern: `unit/`, `integration/`, with optional specialized dirs
- Adopting `unit/`, `integration/`, `commands/`, `create/` structure
- See `exploration.md` Option B for analysis

---

### Research Topic B3: pytest Configuration for Subdirectories

**Question:** What pytest configuration is needed to properly support subdirectory organization?

**Why:** Need to ensure tests run correctly after reorganization.

**Areas to Research:**
- pytest.ini or pyproject.toml test configuration
- conftest.py placement and fixture scoping
- Test discovery with subdirectories
- Import path handling with src/ layout

**Priority:** Medium

**Status:** 🟡 Deferred (address during implementation)

**Notes:**
- Basic configuration outlined in `implementation-plan.md`
- May need refinement during PR #5 (test reorganization)
- Current `conftest.py` should work with subdirectories

---

### Research Topic B4: Test Markers vs Directory Separation

**Question:** Should we rely on pytest markers (`@pytest.mark.integration`) or directory separation, or both?

**Why:** Both approaches have trade-offs; need to decide on primary organization method.

**Areas to Research:**
- Marker-based filtering (`pytest -m "not integration"`)
- Directory-based filtering (`pytest tests/unit/`)
- Combining both approaches
- CI/CD implications

**Priority:** Medium

**Status:** ✅ Addressed (decision: use both)

**Resolution:**
- Use directory structure as primary organization
- Keep existing markers (`@pytest.mark.integration`) for flexibility
- Both work together: `pytest tests/unit/ -m "not slow"`

---

### Research Topic B5: Source Structure Mirroring

**Question:** Should test directories mirror the source structure (e.g., `src/proj/commands/` → `tests/commands/`)?

**Why:** Mirroring makes it easy to find tests for a specific module, but may not always make sense.

**Areas to Research:**
- Flat test files vs nested structure
- When mirroring makes sense vs when it doesn't
- Balance between navigation and simplicity

**Priority:** Medium

**Status:** ✅ Addressed (decision: partial mirroring)

**Resolution:**
- Mirror for `commands/` directory (matches source structure)
- Separate `create/` directory for detailed create mode tests (10 files)
- Don't over-mirror - balance navigation with simplicity

---

### Research Topic B6: Migration Strategy

**Question:** What is the safest migration path from flat to subdirectory structure?

**Why:** Need to minimize risk and disruption during reorganization.

**Areas to Research:**
- Git history preservation during file moves
- Import path updates required
- CI/CD changes needed
- Rollback strategy if issues arise

**Priority:** Low (after decision made)

**Status:** ✅ Addressed (via implementation-plan.md)

**Resolution:**
- Source refactor first (PRs 1-4), then tests (PRs 5-6)
- Use `git mv` for history preservation
- All tests must pass after each PR
- No import path changes needed (tests import from `proj.*`)

---

### Research Topic B7: Template Update for dev-infra

**Question:** Should we update the dev-infra standard-project template's test README?

**Why:** The current template README describes directories that generated projects may not use.

**Areas to Research:**
- Current template test README content
- Whether templates should include test subdirectories
- How to handle different testing patterns (pytest vs bats)

**Priority:** Low

**Status:** 🟡 Deferred (separate effort)

**Notes:**
- Out of scope for proj-cli refactoring
- Should be tracked as dev-infra improvement opportunity
- Can be addressed after proj-cli implementation proves the pattern

---

## 📊 Research Status Summary

| Topic | Priority | Status |
|-------|----------|--------|
| **Source Code** | | |
| A1: Module Size Best Practices | High | ✅ Addressed |
| A2: Package Structure Patterns | High | ✅ Addressed |
| **Test Structure** | | |
| B1: Python CLI Test Best Practices | High | ✅ Addressed |
| B2: Ecosystem Consistency | High | ✅ Addressed |
| B3: pytest Configuration | Medium | 🟡 Deferred |
| B4: Markers vs Directories | Medium | ✅ Addressed |
| B5: Source Structure Mirroring | Medium | ✅ Addressed |
| B6: Migration Strategy | Low | ✅ Addressed |
| B7: dev-infra Template Update | Low | 🟡 Deferred |

**Summary:** 7/9 topics addressed, 2 deferred (will address during/after implementation)

---

## 🎯 Next Steps

Research is sufficient to proceed. Decision has been made (see `exploration.md`).

**Workflow completed:**
1. ✅ `/explore` - Exploration complete
2. ✅ Research - Sufficient analysis done inline
3. ✅ Decision - Option B selected (subdirectories)
4. 🔴 Implementation - Ready to begin

**Next command:** Begin implementation per `implementation-plan.md`

---

**Last Updated:** 2026-01-07
