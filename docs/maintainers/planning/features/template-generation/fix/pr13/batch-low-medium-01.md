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
| PR13-Overall-#3 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Centralize placeholders in mapping |

---

## Overview

This batch contains 1 LOW priority issue with MEDIUM effort. This is a code quality refactoring to centralize placeholder handling.

**Estimated Time:** 1-1.5 hours  
**Files Affected:** `src/proj/templates.py`

---

## Issue Details

### Issue PR13-Overall-#3: Centralize Placeholders

**Location:** `src/proj/templates.py` - `replace_placeholders()` function  
**Sourcery Comment:** Overall Comment #3  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
As `replace_placeholders()` continues to grow (now handling both `[Project Name]` and `[Learning Project Name]`), consider centralizing placeholders into a mapping/dictionary and looping over it, which would make future additions or renames less error-prone than multiple hard-coded `replace` calls.

**Current Code (approximate):**

```python
def replace_placeholders(content: str, project_name: str) -> str:
    """Replace placeholders in template content."""
    content = content.replace("[Project Name]", project_name)
    content = content.replace("[Learning Project Name]", project_name)
    # ... more replace calls as placeholders are added
    return content
```

**Proposed Solution:**

```python
# Define placeholder mapping (could be moved to config)
PLACEHOLDERS = {
    "[Project Name]": lambda name: name,
    "[Learning Project Name]": lambda name: name,
    "[project-name]": lambda name: name.lower().replace(" ", "-"),
    "[PROJECT_NAME]": lambda name: name.upper().replace(" ", "_"),
    # Easy to add more in the future
}

def replace_placeholders(content: str, project_name: str) -> str:
    """Replace placeholders in template content.
    
    Placeholders are defined in PLACEHOLDERS mapping for maintainability.
    """
    for placeholder, transform in PLACEHOLDERS.items():
        content = content.replace(placeholder, transform(project_name))
    return content
```

**Benefits:**
- Single place to add/modify placeholders
- Supports placeholder-specific transformations
- Easier to test exhaustively
- Self-documenting (mapping shows all supported placeholders)

---

## Implementation Steps

1. **Define Placeholder Mapping**
   - [ ] Create `PLACEHOLDERS` constant/mapping
   - [ ] Include all existing placeholders
   - [ ] Add transformation functions where needed

2. **Refactor Function**
   - [ ] Replace hard-coded calls with loop
   - [ ] Ensure all tests still pass
   - [ ] Add docstring explaining mapping

3. **Testing**
   - [ ] Add test for each placeholder
   - [ ] Test with content containing multiple placeholders
   - [ ] Test edge cases (no placeholders, unknown placeholders)

---

## Testing

- [ ] All existing tests pass
- [ ] New tests for each placeholder transformation
- [ ] No regressions in template generation

---

## Files to Modify

- `src/proj/templates.py` - Add mapping, refactor function
- `tests/test_templates.py` - Add comprehensive placeholder tests

---

## Definition of Done

- [ ] Placeholders centralized in mapping
- [ ] Function refactored to use mapping
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This is a "nice to have" refactoring that improves maintainability. MEDIUM effort because it requires careful refactoring and comprehensive testing to ensure no regressions.

**When to Do This:**
- When adding new placeholders (good opportunity to refactor)
- During a code quality sprint
- When template functionality is being extended

