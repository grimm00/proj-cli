# Fix Plan: PR #11 Batch MEDIUM LOW - Batch 01

**PR:** #11  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-05  
**Completed:** 2026-01-06  
**Merged:** PR #16 (Fix PR #2)  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR11-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Add non-writable directory test |

---

## Overview

This batch contains 1 MEDIUM priority issue with LOW effort. The issue addresses test coverage for the `DirectoryNotWritableError` exception path in `validate_target_directory`.

**Estimated Time:** 30 minutes  
**Files Affected:** `tests/test_templates.py`

---

## Issue Details

### Issue PR11-#2: Add Non-Writable Directory Test

**Location:** `tests/test_templates.py:192-194`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`validate_target_directory` has a dedicated `DirectoryNotWritableError` branch via `os.access(path, os.W_OK)`, but current tests don't hit it. Add a test that makes a directory non-writable and asserts that `DirectoryNotWritableError` is raised.

**Current Code:**
The `validate_target_directory` function checks writability but this path is not tested:

```python
if not os.access(path, os.W_OK):
    raise DirectoryNotWritableError(
        f"Target directory is not writable: {path}"
    )
```

**Proposed Solution:**
Add a test using `monkeypatch` to mock `os.access` returning `False`:

```python
def test_non_writable_directory_raises_error(self, tmp_path, monkeypatch):
    """Test non-writable directory raises DirectoryNotWritableError."""
    # Make os.access return False for write check
    original_access = os.access
    def mock_access(path, mode):
        if mode == os.W_OK:
            return False
        return original_access(path, mode)
    
    monkeypatch.setattr(os, "access", mock_access)
    
    with pytest.raises(DirectoryNotWritableError) as exc:
        validate_target_directory(tmp_path)
    assert "not writable" in str(exc.value)
```

---

## Implementation Steps

1. **Issue PR11-#2: Non-writable directory test**
   - [ ] Add test to `TestValidateTargetDirectory` class
   - [ ] Use `monkeypatch` to mock `os.access`
   - [ ] Assert `DirectoryNotWritableError` is raised
   - [ ] Assert error message contains expected text
   - [ ] Run tests to verify coverage improved

---

## Testing

- [ ] All existing tests pass
- [ ] New test added for non-writable directory
- [ ] Coverage for `validate_target_directory` improved
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_templates.py` - Add non-writable directory test to `TestValidateTargetDirectory`

---

## Definition of Done

- [ ] Issue fixed
- [ ] Test passing
- [ ] Coverage improved for exception path
- [ ] Ready for PR

---

**Batch Rationale:**
This issue is in its own batch because it's MEDIUM priority (higher than other deferred issues) and should be addressed first for better test coverage of exception handling.

