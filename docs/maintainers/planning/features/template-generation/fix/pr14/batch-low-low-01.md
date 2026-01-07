# Fix Plan: PR #14 Batch LOW LOW - 01

**PR:** #14  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2026-01-06  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR14-#2 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Assert CLI output for sync message |
| PR14-#3 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Assert CLI output for skip messages |

---

## Overview

This batch contains 2 LOW priority test improvements with LOW effort. These add output assertions to existing tests.

**Estimated Time:** 30 minutes  
**Files Affected:** `tests/test_create_api_sync.py`

---

## Issue Details

### Issue PR14-#2: Assert Sync Message Output

**Location:** `tests/test_create_api_sync.py:128-137`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Test confirms `APIClient.create_project` is called, but not the user-visible message. Assert that the expected sync message (e.g. `"Synced to API (ID: 99)"`) appears in `result.stdout`.

**Proposed Change:**

```python
def test_template_create_syncs_to_api(tmp_path, monkeypatch):
    # ... existing setup and invoke ...
    
    assert result.exit_code == 0
    mock_instance.create_project.assert_called_once()
    # Add output assertion
    assert "Synced to API" in result.output or "ID:" in result.output
```

---

### Issue PR14-#3: Assert Skip Message Output

**Location:** `tests/test_create_api_sync.py:182-178`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Assert on `result.stdout` for the expected messages (e.g. `"Skipped API sync (--local-only)"` and `"Skipped API sync (api_enabled=False)"`).

**Proposed Changes:**

```python
def test_template_create_skips_api_when_local_only(tmp_path, monkeypatch):
    # ... existing setup and invoke ...
    
    assert result.exit_code == 0
    mock_instance.create_project.assert_not_called()
    # Add output assertion
    assert "local-only" in result.output.lower() or "skipped" in result.output.lower()


def test_template_create_skips_api_when_disabled(tmp_path, monkeypatch):
    # ... existing setup and invoke ...
    
    assert result.exit_code == 0
    mock_instance.create_project.assert_not_called()
    # Add output assertion
    assert "api_enabled" in result.output.lower() or "skipped" in result.output.lower()
```

---

## Implementation Steps

1. **PR14-#2: Sync Message Assertion**
   - [ ] Find `test_template_create_syncs_to_api` test
   - [ ] Add assertion for sync success message in output

2. **PR14-#3: Skip Message Assertions**
   - [ ] Find `test_template_create_skips_api_when_local_only` test
   - [ ] Add assertion for skip message
   - [ ] Find `test_template_create_skips_api_when_disabled` test
   - [ ] Add assertion for skip message

---

## Testing

- [ ] All existing tests pass
- [ ] Output assertions validate user-facing messages
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_create_api_sync.py` - Add output assertions to existing tests

---

## Definition of Done

- [ ] Both tests have output assertions
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
Two simple LOW/LOW test improvements that can be done quickly together.

