# Fix Plan: PR #12 Batch LOW HIGH - 01

**PR:** #12  
**Batch:** low-high-01  
**Priority:** 🟢 LOW  
**Effort:** 🟠 HIGH  
**Status:** 🔴 Not Started  
**Created:** 2026-01-06  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-Overall-2 | 🟢 LOW | 🟡 MEDIUM | 🟠 HIGH | Refactor large create_project function |

---

## Overview

This batch contains 1 LOW priority issue with HIGH effort. This is a major refactoring task that should be done when there's dedicated time.

**Estimated Time:** 3-4 hours  
**Files Affected:** `src/proj/commands/projects.py`, possibly new helper files

---

## Issue Details

### Issue PR12-Overall-2: Refactor create_project Function

**Location:** `src/proj/commands/projects.py` - `create_project` function  
**Sourcery Comment:** Overall Comment #1  
**Priority:** 🟢 LOW | **Impact:** 🟡 MEDIUM | **Effort:** 🟠 HIGH

**Description:**
The `create_project` function has become quite large and branchy (dry-run, interactive, template, local-only, API-only, fallback), and would be easier to maintain if the major flows were split into smaller helpers that encapsulate each mode's logic.

**Current Structure (pseudo):**

```python
def create_project(...):
    # Config loading
    # Dry-run check
    # Interactive prompting
    # Mode detection
    # Template flow (local creation)
    # API-only flow
    # Local-only flow
    # Fallback API flow
```

**Proposed Refactoring:**

```python
def create_project(...):
    config = Config.load()
    
    if dry_run:
        return _handle_dry_run(...)
    
    if interactive:
        options = _prompt_for_options(config)
        return _execute_create(**options)
    
    mode = detect_create_mode(...)
    
    handlers = {
        "template": _create_from_template,
        "api-only": _create_api_only,
        "local-only": _create_local_only,
    }
    return handlers[mode](...)


def _handle_dry_run(...):
    """Handle dry-run preview."""
    pass


def _create_from_template(...):
    """Create project from template."""
    pass


def _create_api_only(...):
    """Create project via API only."""
    pass


def _create_local_only(...):
    """Create local-only project without API."""
    pass
```

---

## Implementation Steps

1. **Analysis Phase**
   - [ ] Map all current flows in create_project
   - [ ] Identify shared logic vs mode-specific logic
   - [ ] Design helper function signatures

2. **Extract Helpers**
   - [ ] Extract `_handle_dry_run()` helper
   - [ ] Extract `_create_from_template()` helper
   - [ ] Extract `_create_api_only()` helper
   - [ ] Consider `_create_local_only()` helper

3. **Refactor Main Function**
   - [ ] Replace inline code with helper calls
   - [ ] Ensure all tests still pass
   - [ ] Add docstrings to new helpers

4. **Testing**
   - [ ] Run full test suite after each extraction
   - [ ] Add any missing tests for edge cases
   - [ ] Manual testing of all flows

---

## Testing

- [ ] All existing tests pass (must not break anything)
- [ ] Each helper function tested in isolation
- [ ] Integration tests still pass
- [ ] Manual testing of all create modes

---

## Files to Modify

- `src/proj/commands/projects.py` - Main refactoring
- `tests/test_commands_projects.py` - May need updates

---

## Definition of Done

- [ ] `create_project` function is more maintainable
- [ ] Each mode encapsulated in helper
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

## Notes

**Why This is LOW Priority:**
- Current code works correctly
- Refactoring is for maintainability, not functionality
- No user-facing impact

**When to Do This:**
- During a dedicated refactoring sprint
- When adding new create modes
- When significant changes needed anyway

---

**Batch Rationale:**
HIGH effort refactoring should be its own batch. This is a "nice to have" improvement that can wait until there's dedicated time for code quality work.

