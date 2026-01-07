# Fix Plan: PR #21 Batch MEDIUM MEDIUM - Batch 01

**PR:** #21
**Batch:** medium-medium-01
**Priority:** 🟡 MEDIUM
**Effort:** 🟡 MEDIUM
**Status:** 🔴 Not Started
**Created:** 2026-01-07
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR21-Overall-1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Centralize `VALID_PROJECT_TYPES` constant |
| PR21-Overall-2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Use custom exception for `project_type` validation |

---

## Overview

This batch contains 2 MEDIUM priority issues with MEDIUM effort. These issues are related to code quality and robustness improvements for the `project_type` validation.

**Estimated Time:** 1-2 hours
**Files Affected:**
- `src/proj/api_client.py`
- `src/proj/commands/projects.py`
- `src/proj/error_handler.py` (new exception)
- `tests/test_commands_projects.py`

---

## Issue Details

### Issue PR21-Overall-1: Centralize VALID_PROJECT_TYPES

**Location:** `src/proj/api_client.py:43`
**Sourcery Comment:** Overall Comment #1
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
The `VALID_PROJECT_TYPES` list is duplicated implicitly in the CLI help text and in the error message string; consider centralizing the allowed values (e.g., via an Enum or shared constant used by both the API client and CLI help/error messaging) to avoid drift if the set of types changes.

**Current Code:**

```python
# src/proj/api_client.py
class APIClient:
    VALID_PROJECT_TYPES = ['Work', 'Personal', 'Learning', 'Inactive']
    
    def list_projects(self, ..., project_type: Optional[str] = None, ...):
        if project_type and project_type not in self.VALID_PROJECT_TYPES:
            raise ValueError(
                f"Invalid project_type. Must be one of: {self.VALID_PROJECT_TYPES}"
            )

# src/proj/commands/projects.py
def list_projects(
    ...
    project_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Filter by project type (Work, Personal, Learning, Inactive)"  # Duplicated
    ),
    ...
):
```

**Proposed Solution:**

```python
# Option 1: Shared constant module (simpler)
# src/proj/constants.py
VALID_PROJECT_TYPES = ['Work', 'Personal', 'Learning', 'Inactive']
PROJECT_TYPE_HELP = f"Filter by project type ({', '.join(VALID_PROJECT_TYPES)})"

# Option 2: Enum (more robust)
# src/proj/constants.py
from enum import Enum

class ProjectType(str, Enum):
    WORK = 'Work'
    PERSONAL = 'Personal'
    LEARNING = 'Learning'
    INACTIVE = 'Inactive'
```

---

### Issue PR21-Overall-2: Custom Exception for Project Type Validation

**Location:** `src/proj/commands/projects.py:list_projects` exception handling
**Sourcery Comment:** Overall Comment #2
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
The `list_projects` command currently catches all `ValueError` exceptions and treats them as user-facing type errors; it would be safer to either narrow this to the specific validation error from `project_type` (e.g., a custom exception) or to ensure other `ValueError` sources aren't accidentally surfaced as generic CLI usage errors.

**Current Code:**

```python
# src/proj/commands/projects.py
def list_projects(...):
    try:
        client = get_client()
        projects = client.list_projects(...)
        ...
    except ValueError as e:  # Catches ALL ValueErrors
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
```

**Proposed Solution:**

```python
# src/proj/error_handler.py (add new exception)
class InvalidProjectTypeError(ValueError):
    """Raised when an invalid project type is provided."""
    pass

# src/proj/api_client.py (use custom exception)
from proj.error_handler import InvalidProjectTypeError

def list_projects(self, ..., project_type: Optional[str] = None, ...):
    if project_type and project_type not in self.VALID_PROJECT_TYPES:
        raise InvalidProjectTypeError(
            f"Invalid project_type. Must be one of: {self.VALID_PROJECT_TYPES}"
        )

# src/proj/commands/projects.py (catch specific exception)
from proj.error_handler import InvalidProjectTypeError

def list_projects(...):
    try:
        client = get_client()
        projects = client.list_projects(...)
        ...
    except InvalidProjectTypeError as e:  # Specific exception
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except (APIError, BackendConnectionError, TimeoutError) as e:
        handle_error(e, console)
        raise typer.Exit(1)
```

---

## Implementation Steps

1. **Create constants module:**
   - [ ] Create `src/proj/constants.py`
   - [ ] Add `VALID_PROJECT_TYPES` list or `ProjectType` enum
   - [ ] Add `PROJECT_TYPE_HELP` string

2. **Add custom exception:**
   - [ ] Add `InvalidProjectTypeError` to `src/proj/error_handler.py`
   - [ ] Inherit from `ValueError` for backward compatibility

3. **Update API client:**
   - [ ] Import from constants module
   - [ ] Use custom exception for validation

4. **Update CLI command:**
   - [ ] Import from constants module
   - [ ] Update help text to use constant
   - [ ] Catch `InvalidProjectTypeError` specifically

5. **Update tests:**
   - [ ] Update test to use/check `InvalidProjectTypeError`
   - [ ] Add test for other `ValueError` not being caught

---

## Testing

- [ ] All existing tests pass
- [ ] Test invalid project_type raises `InvalidProjectTypeError`
- [ ] Test other `ValueError` not caught as project type error
- [ ] Test help text includes all project types
- [ ] No regressions introduced

---

## Files to Modify

- `src/proj/constants.py` - New file for shared constants
- `src/proj/error_handler.py` - Add `InvalidProjectTypeError`
- `src/proj/api_client.py` - Use constants and custom exception
- `src/proj/commands/projects.py` - Use constants and catch specific exception
- `tests/test_commands_projects.py` - Update tests

---

## Definition of Done

- [ ] Constants centralized in single module
- [ ] Custom exception created and used
- [ ] CLI help text uses constant
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Both relate to `project_type` validation robustness
- Share similar MEDIUM priority and effort
- Should be implemented together for consistency
- Improve code quality and maintainability

---

**Last Updated:** 2026-01-07

