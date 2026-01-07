# Fix Plan: PR #21 Batch LOW LOW - Batch 01

**PR:** #21
**Batch:** low-low-01
**Priority:** 🟢 LOW
**Effort:** 🟢 LOW
**Status:** 🔴 Not Started
**Created:** 2026-01-07
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR21-#1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Strengthen invalid-type test with error formatting assertion |

---

## Overview

This batch contains 1 LOW priority issue with LOW effort. This is a minor test improvement.

**Estimated Time:** 15-30 minutes
**Files Affected:**
- `tests/test_commands_projects.py`

---

## Issue Details

### Issue PR21-#1: Strengthen Invalid-Type Test

**Location:** `tests/test_commands_projects.py:219-228`
**Sourcery Comment:** Comment #1
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
This already asserts the `ValueError` and message substring, but to fully cover the new CLI error path, please also assert on the Rich-formatted prefix (e.g. red `"Error:"`) to confirm the specific `ValueError` handling is used rather than the generic `handle_error` branch.

**Current Code:**

```python
@patch('proj.commands.projects.get_client')
def test_list_projects_with_invalid_type(mock_get_client):
    """Test proj list --type Invalid shows error."""
    mock_client = MagicMock()
    mock_client.list_projects.side_effect = ValueError(
        "Invalid project_type. Must be one of: ['Work', 'Personal', 'Learning', 'Inactive']"
    )
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list", "--type", "Invalid"])

    assert result.exit_code == 1
    assert "Invalid project_type" in result.output
```

**Proposed Solution:**

```python
@patch('proj.commands.projects.get_client')
def test_list_projects_with_invalid_type(mock_get_client):
    """Test proj list --type Invalid shows error with proper formatting."""
    mock_client = MagicMock()
    mock_client.list_projects.side_effect = ValueError(
        "Invalid project_type. Must be one of: ['Work', 'Personal', 'Learning', 'Inactive']"
    )
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list", "--type", "Invalid"])

    assert result.exit_code == 1
    assert "Invalid project_type" in result.output
    # Verify specific ValueError handling (not generic handle_error)
    assert "Error:" in result.output  # Rich-formatted error prefix
```

---

## Implementation Steps

1. **Update test assertion:**
   - [ ] Add assertion for "Error:" prefix in output
   - [ ] Verify test still passes

---

## Testing

- [ ] Test passes with new assertion
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_commands_projects.py` - Add assertion for error formatting

---

## Definition of Done

- [ ] Test assertion added
- [ ] Test passing
- [ ] Ready for PR

---

**Batch Rationale:**
This is a standalone LOW priority, LOW effort issue that can be implemented quickly.

---

**Last Updated:** 2026-01-07

