# Fix Plan: PR #12 Batch LOW LOW - 01

**PR:** #12  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-06  
**Completed:** 2026-01-07  
**Merged:** PR #19  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-#3 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | Add precedence tests |
| PR12-#4 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | Add dry-run prompt test |
| PR12-#5 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | Add implicit API test |
| PR12-Overall-1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Remove unused config param |

---

## Overview

This batch contains 4 LOW priority issues with LOW effort. These are test improvements and a minor code cleanup.

**Estimated Time:** 1-1.5 hours  
**Files Affected:** `src/proj/commands/projects.py`, `tests/test_commands_projects.py`, `tests/test_create_dry_run.py`, `tests/test_create_integration.py`

---

## Issue Details

### Issue PR12-#3: Add Precedence Tests

**Location:** `tests/test_commands_projects.py:130-137`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟢 LOW | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add tests for `detect_create_mode` when both a template and an explicit mode flag are provided, to document precedence behavior.

**Proposed Tests:**

```python
def test_detect_mode_template_with_api_only_flag():
    """Explicit api_only flag takes precedence over template."""
    config = MagicMock()
    mode = detect_create_mode(
        config=config,
        template="standard-project",
        api_only=True,
        local_only=False,
    )
    assert mode == "api-only"


def test_detect_mode_template_with_local_only_flag():
    """Explicit local_only flag takes precedence over template."""
    config = MagicMock()
    mode = detect_create_mode(
        config=config,
        template="standard-project",
        api_only=False,
        local_only=True,
    )
    assert mode == "local-only"
```

---

### Issue PR12-#4: Add Dry-Run Prompt Test

**Location:** `tests/test_create_dry_run.py:24-33`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add a test that patches `proj.commands.projects.Prompt`, runs `proj create --dry-run` without `name`/`--template`, and asserts `Prompt.ask` is never called. This protects the expectation that dry-run stays non-interactive.

**Proposed Test:**

```python
@patch('proj.commands.projects.Prompt')
@patch('proj.commands.projects.Config.load')
def test_create_dry_run_interactive_does_not_prompt(
    mock_config_load, mock_prompt, tmp_path
):
    """Dry-run should not trigger interactive prompts."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config_load.return_value = mock_config

    result = runner.invoke(app, ["create", "--dry-run"])

    # Dry-run should not call any prompts
    mock_prompt.ask.assert_not_called()
```

---

### Issue PR12-#5: Add Implicit API Test

**Location:** `tests/test_create_integration.py:60-90`  
**Sourcery Comment:** Comment #5  
**Priority:** 🟢 LOW | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Add integration test that runs `proj create "My Application"` with no mode flags and asserts `get_client().create_project` is called, covering backward-compatible behavior.

**Proposed Test:**

```python
@patch('proj.commands.projects.get_client')
@patch('proj.commands.projects.Config.load')
def test_create_name_only_falls_back_to_api(
    mock_config_load, mock_get_client, tmp_path
):
    """Providing only a name falls back to API (backward compatible)."""
    mock_config = MagicMock()
    mock_config.api_enabled = True
    mock_config_load.return_value = mock_config

    mock_client = MagicMock()
    mock_client.create_project.return_value = {
        "id": 456,
        "name": "My Application",
        "status": "active",
    }
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["create", "My Application"])

    assert result.exit_code == 0
    mock_client.create_project.assert_called_once()
    assert "Created project" in result.output
```

---

### Issue PR12-Overall-1: Remove Unused Config Param

**Location:** `src/proj/commands/projects.py` - `detect_create_mode` function  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
`detect_create_mode` takes a `config` argument but does not use it. Either remove the unused parameter or incorporate config-driven behavior.

**Current Code:**

```python
def detect_create_mode(config, template, api_only, local_only):
    # config is never used
```

**Proposed Solution:**
Remove unused parameter (simplest fix):

```python
def detect_create_mode(template, api_only, local_only):
    """Detect create mode based on arguments."""
```

Update all callers to not pass `config`.

---

## Implementation Steps

1. **PR12-#3: Precedence Tests**
   - [x] Add `test_detect_mode_template_with_api_only_flag`
   - [x] Add `test_detect_mode_template_with_local_only_flag`

2. **PR12-#4: Dry-Run Prompt Test**
   - [x] Add `test_create_dry_run_interactive_does_not_prompt`

3. **PR12-#5: Implicit API Test**
   - [x] Add `test_create_name_only_falls_back_to_api`

4. **PR12-Overall-1: Config Cleanup**
   - [x] Remove `config` param from `detect_create_mode`
   - [x] Update all callers (search for `detect_create_mode`)
   - [x] Update existing tests

---

## Testing

- [x] All existing tests pass
- [x] 4 new tests added
- [x] No regressions introduced

---

## Files to Modify

- `src/proj/commands/projects.py` - Remove unused config param
- `tests/test_commands_projects.py` - Add precedence tests
- `tests/test_create_dry_run.py` - Add prompt test
- `tests/test_create_integration.py` - Add implicit API test

---

## Definition of Done

- [x] All 4 issues addressed
- [x] Tests passing
- [x] Code reviewed
- [x] Ready for PR

---

**Batch Rationale:**
These 4 LOW priority, LOW effort issues are all quick improvements that can be done together efficiently. Three are test additions and one is a simple code cleanup.

