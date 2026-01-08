# Fix Plan: PR #26 Batch LOW LOW - Batch 01

**PR:** #26  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-08  
**Completed:** 2026-01-08  
**PR:** Pending  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR26-Overall-#1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Consolidate `_get_client()` with `helpers.get_client()` |

---

## Overview

This batch contains 1 LOW priority issue with LOW effort. The issue addresses minor code duplication where `create.py` has a `_get_client()` function that duplicates the behavior of `helpers.get_client()`.

**Estimated Time:** ~10-15 minutes  
**Files Affected:**
- `src/proj/commands/projects/create.py`

---

## Issue Details

### Issue PR26-Overall-#1: Consolidate _get_client() with helpers.get_client()

**Location:** `src/proj/commands/projects/create.py`  
**Sourcery Comment:** Overall Comment #1  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
In `create.py`, `_get_client()` duplicates the behavior of `helpers.get_client()`. This creates potential for divergence if the client construction logic changes. Consider reusing the shared helper.

**Current Code:**
```python
# In create.py
def _get_client():
    """Get configured API client."""
    pkg = get_package_imports()
    return pkg.APIClient(pkg.Config.load())
```

**helpers.get_client():**
```python
# In helpers.py
def get_client() -> APIClient:
    """Get configured API client."""
    return _APIClient(_Config.load())
```

**Proposed Solution:**
Remove `_get_client()` from `create.py` and use `get_client` from the package imports:
```python
# In create.py - replace _get_client() calls with:
pkg = get_package_imports()
client = pkg.get_client()
```

Or simply import from helpers:
```python
from .helpers import get_client
# Then use get_client() directly
```

---

## Implementation Steps

1. **Issue PR26-Overall-#1**
   - [ ] Open `src/proj/commands/projects/create.py`
   - [ ] Find all uses of `_get_client()`
   - [ ] Replace with `pkg.get_client()` (using package imports)
   - [ ] Remove the `_get_client()` function definition
   - [ ] Run tests to verify no regressions

---

## Testing

- [ ] All existing tests pass
- [ ] `create` command still works correctly
- [ ] Test patching still works (via package-level imports)
- [ ] No regressions introduced

---

## Files to Modify

- `src/proj/commands/projects/create.py` - Remove `_get_client()`, use `pkg.get_client()`

---

## Definition of Done

- [x] `_get_client()` removed from create.py
- [x] Function was unused (no calls found)
- [x] All 238+ tests passing (4 pre-existing failures unrelated)
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This issue is in its own batch because:
- Single issue with clear scope
- Quick fix (remove duplication)
- Can be done independently or combined with other LOW priority fixes

---

**Last Updated:** 2026-01-08
