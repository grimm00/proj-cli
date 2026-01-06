# Fix Plan: PR #14 Batch MEDIUM LOW - 01

**PR:** #14  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2026-01-06  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR14-#4 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Test for missing/None id response |
| PR14-Overall-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Narrow except clause in sync_to_api |

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW effort. One is a test improvement for edge case coverage, the other is code quality for exception handling.

**Estimated Time:** 45 minutes  
**Files Affected:** `src/proj/commands/projects.py`, `tests/test_create_api_sync.py`

---

## Issue Details

### Issue PR14-#4: Test Missing ID Response

**Location:** `tests/test_create_api_sync.py:339-348`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add a test for the case where the API call succeeds but returns no `id` (or `id=None`), since `sync_to_api` would then return `None` and the registry should not be updated.

**Proposed Test:**

```python
def test_sync_to_api_missing_id_response(monkeypatch):
    """Test sync_to_api handles response without id."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {}  # No id field
    
    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )
    
    assert result is None  # Should return None when no id


def test_sync_to_api_none_id_response(monkeypatch):
    """Test sync_to_api handles response with None id."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {"id": None}
    
    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )
    
    assert result is None  # Should return None when id is None
```

---

### Issue PR14-Overall-#1: Narrow Except Clause

**Location:** `src/proj/commands/projects.py` - `sync_to_api` function  
**Sourcery Comment:** Overall Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Consider narrowing the `except` clause to the specific timeout/HTTP exceptions your `APIClient` actually raises rather than catching the built-in `TimeoutError`, which can mask unrelated issues.

**Current Code:**

```python
except (APIError, BackendConnectionError, TimeoutError) as e:
```

**Proposed Solution:**

```python
# Import specific timeout from requests or define custom
from requests.exceptions import Timeout as RequestsTimeout

except (APIError, BackendConnectionError, RequestsTimeout) as e:
```

Or define a custom exception in api_client.py:

```python
class APITimeoutError(APIError):
    """Raised when API request times out."""
    pass
```

---

## Implementation Steps

1. **PR14-#4: Missing ID Tests**
   - [ ] Add `test_sync_to_api_missing_id_response`
   - [ ] Add `test_sync_to_api_none_id_response`
   - [ ] Verify tests pass (may need to fix implementation)

2. **PR14-Overall-#1: Narrow Except**
   - [ ] Check what exceptions APIClient actually raises
   - [ ] Replace `TimeoutError` with specific exception
   - [ ] Update imports as needed
   - [ ] Run tests to verify no regressions

---

## Testing

- [ ] All existing tests pass
- [ ] 2 new edge case tests added
- [ ] Exception handling still works correctly
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_create_api_sync.py` - Add missing id tests
- `src/proj/commands/projects.py` - Narrow except clause
- `src/proj/api_client.py` - May need custom timeout exception

---

## Definition of Done

- [ ] Both issues addressed
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
Two MEDIUM/LOW issues that improve code quality and test coverage. Can be done together efficiently.

