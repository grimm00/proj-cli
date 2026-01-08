# Fix Plan: PR #26 Batch MEDIUM LOW - Batch 01

**PR:** #26  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2026-01-08  
**Issues:** 2 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR26-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Add assertions for helper interactions in prompt test |
| PR26-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Add regression test for `get_package_imports` patching |

---

## Overview

This batch contains 2 MEDIUM priority issues with LOW effort. Both issues improve test regression coverage for the refactored code structure, ensuring the late-binding pattern via `get_package_imports()` is properly tested.

**Estimated Time:** ~30-45 minutes  
**Files Affected:**
- `tests/commands/projects/test_create.py`
- `tests/commands/projects/test_list.py`

---

## Issue Details

### Issue PR26-#1: Strengthen prompt_for_create_options Test

**Location:** `tests/commands/projects/test_create.py:100-109`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The `test_prompt_for_create_options_no_templates_available` test relies on late-bound imports via `get_package_imports()`. Add assertions to verify that `get_templates_source` and `list_templates` are called with expected arguments, validating the wiring to the helper layer.

**Current Test:**
```python
def test_prompt_for_create_options_no_templates_available(tmp_path):
    """Test prompt when no templates available."""
    # ... test code that patches functions but doesn't assert they were called
```

**Proposed Solution:**
Add explicit assertions:
```python
def test_prompt_for_create_options_no_templates_available(tmp_path):
    """Test prompt when no templates available."""
    # ... existing setup ...
    
    # Assert helper functions were called with expected arguments
    mock_get_templates_source.assert_called_once_with(mock_config)
    mock_list_templates.assert_called_once_with(expected_templates_source)
```

---

### Issue PR26-#2: Add Regression Test for get_package_imports Patching

**Location:** `tests/commands/projects/test_list.py:104-107`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add a regression test that explicitly verifies patching `proj.commands.projects.*` affects submodules that use `get_package_imports()`. This documents the patching pattern and protects against regressions.

**Proposed Solution:**
```python
@patch('proj.commands.projects.get_client')
def test_list_projects_uses_patched_get_client_via_package_imports(mock_get_client):
    """Regression test: patching proj.commands.projects.get_client affects submodules using get_package_imports."""
    mock_client = MagicMock()
    mock_client.list_projects.return_value = []

    # When get_client is patched at package level, commands that use get_package_imports
    # (such as `list`) should still see the patched version.
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    mock_get_client.assert_called_once()
    mock_client.list_projects.assert_called_once()
```

---

## Implementation Steps

1. **Issue PR26-#1**
   - [ ] Open `tests/commands/projects/test_create.py`
   - [ ] Find `test_prompt_for_create_options_no_templates_available`
   - [ ] Add `assert_called_once_with()` assertions for mocked functions
   - [ ] Run test to verify it passes

2. **Issue PR26-#2**
   - [ ] Open `tests/commands/projects/test_list.py`
   - [ ] Add new test function `test_list_projects_uses_patched_get_client_via_package_imports`
   - [ ] Run test to verify it passes
   - [ ] Add docstring explaining the regression test purpose

---

## Testing

- [ ] All existing tests pass
- [ ] New assertions don't break existing test logic
- [ ] Regression test correctly verifies patching behavior
- [ ] No regressions introduced

---

## Files to Modify

- `tests/commands/projects/test_create.py` - Add assertions to existing test
- `tests/commands/projects/test_list.py` - Add new regression test

---

## Definition of Done

- [ ] PR26-#1 assertions added
- [ ] PR26-#2 regression test added
- [ ] All 242+ tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Both improve test regression coverage
- Both validate the `get_package_imports()` late-binding pattern
- Both are MEDIUM priority with LOW effort
- Can be implemented together in a single test improvement PR

---

**Last Updated:** 2026-01-08
