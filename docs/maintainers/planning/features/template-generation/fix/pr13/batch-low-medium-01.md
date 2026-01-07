# Fix Plan: PR #13 Batch LOW MEDIUM - 01

**PR:** #13  
**Batch:** low-medium-01  
**Priority:** 🟢 LOW  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2026-01-06  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR13-Overall-#3 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Centralize placeholders in mapping/dictionary |

---

## Overview

This batch contains 1 LOW priority issue with MEDIUM effort. This is a nice-to-have refactoring to make `replace_placeholders()` more maintainable.

**Estimated Time:** 1-1.5 hours  
**Files Affected:** `src/proj/templates.py`

---

## Issue Details

### Issue PR13-Overall-#3: Centralize Placeholders

**Location:** `src/proj/templates.py` - `replace_placeholders()` function  
**Sourcery Comment:** Overall Comment #3  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
As `replace_placeholders()` continues to grow (now handling both `[Project Name]` and `[Learning Project Name]`), you might consider centralizing placeholders into a mapping/dictionary and looping over it, which would make future additions or renames less error-prone than multiple hard-coded `replace` calls.

**Current Code Pattern:**

```python
def replace_placeholders(content: str, project_name: str) -> str:
    """Replace placeholders in content."""
    content = content.replace("[Project Name]", project_name)
    content = content.replace("[Learning Project Name]", project_name)
    # More replace calls as placeholders grow...
    return content
```

**Proposed Solution:**

```python
# Define placeholders as a mapping
PLACEHOLDERS = {
    "[Project Name]": lambda name: name,
    "[Learning Project Name]": lambda name: name,
    # Easy to add more:
    # "[Project Description]": lambda name: f"Description for {name}",
}


def replace_placeholders(content: str, project_name: str) -> str:
    """Replace placeholders in content using centralized mapping."""
    for placeholder, resolver in PLACEHOLDERS.items():
        content = content.replace(placeholder, resolver(project_name))
    return content
```

---

## Implementation Steps

1. **Create Placeholder Mapping**
   - [ ] Define `PLACEHOLDERS` dict at module level
   - [ ] Map each placeholder to its replacement logic
   - [ ] Consider using lambdas or simple functions

2. **Refactor replace_placeholders()**
   - [ ] Replace hard-coded replace calls with loop
   - [ ] Ensure all existing placeholders are covered
   - [ ] Add docstring explaining the mapping

3. **Update Tests**
   - [ ] Ensure existing tests still pass
   - [ ] Add test for new placeholder (verify extensibility)
   - [ ] Test edge cases (placeholder not in content)

---

## Testing

- [ ] All existing tests pass
- [ ] New placeholder easily addable (verify pattern)
- [ ] No regressions in template generation
- [ ] Manual test: create project, verify placeholders replaced

---

## Files to Modify

- `src/proj/templates.py` - Refactor `replace_placeholders()`
- `tests/test_templates.py` - Update/add tests

---

## Definition of Done

- [ ] Placeholders centralized in mapping
- [ ] Loop replaces hard-coded calls
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
Single LOW/MEDIUM issue - nice refactoring but not urgent. Can be done during code quality improvement time.

