# Fix Plan: Cross-PR Quick Wins 02 - Technical Fixes

**Batch:** quick-wins-02  
**Priority:** 🟠 HIGH / 🟡 MEDIUM / 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-18  
**Source:** fix-review-report-2025-12-18.md  
**Issues:** 9 issues from 2 PRs

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|-----|----------|--------|--------|-------------|
| PR5-#3 | #5 | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | Fix broad exception handling in integration tests |
| PR5-#1 | #5 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Centralize status_emoji constant |
| PR4-#2 | #4 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Delete corrupted inventory file |
| PR4-#3 | #4 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Handle PackageNotFoundError gracefully |
| PR5-#4 | #5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Add exit code assertion in test |
| PR5-#6 | #5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Assert config file created after load |
| PR5-#8 | #5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Fix typo in docs (PR reference) |
| PR5-OC2 | #5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Fix URL consistency in docs |
| PR4-OC2 | #4 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Add JSON error logging |

---

## Overview

This batch contains 9 LOW effort issues from PRs #4 and #5, focusing on:
1. **Test reliability** (HIGH priority) - Fix broad exception handling
2. **Code quality** - Centralize duplicated code, improve UX
3. **Documentation** - Fix typos and URL consistency

**Estimated Time:** ~1.5-2 hours  
**Files Affected:**
- `tests/test_api_client_integration.py`
- `src/proj/commands/projects.py`
- `src/proj/commands/inventory.py`
- `tests/test_package.py`
- `tests/test_cli_integration.py`
- `tests/test_config_integration.py`
- `docs/maintainers/planning/features/proj-cli/phase-4.md`
- `README.md`

**Source PRs:**
- PR #4: Fix: Quick Wins Batch
- PR #5: Phase 4: Polish & Cleanup

---

## Issue Details

### Issue PR5-#3: Fix broad exception handling in integration tests (HIGH)

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `tests/test_api_client_integration.py:5-14`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟠 HIGH | **Impact:** 🟠 HIGH | **Effort:** 🟢 LOW

**Description:**
Wrapping both the HTTP call and assertions in `try/except Exception` means `AssertionError` and other real failures will be turned into skips. This hides test failures and reduces test reliability.

**Current Code:**

```python
@pytest.mark.integration
def test_list_projects_integration():
    """Test listing projects against real API."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        projects = client.list_projects()
        assert isinstance(projects, list)
    except Exception as e:
        pytest.skip(f"API not available: {e}")
```

**Proposed Solution:**
Catch only specific connectivity exceptions:

```python
import requests

@pytest.mark.integration
def test_list_projects_integration():
    """Test listing projects against real API."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        projects = client.list_projects()
    except (requests.ConnectionError, requests.Timeout) as e:
        pytest.skip(f"API not available: {e}")
    
    # Assertions are outside try/except so failures are caught
    assert isinstance(projects, list)
```

---

### Issue PR5-#1: Centralize status_emoji constant

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `src/proj/commands/projects.py:74-75`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The `status_emoji` dict is duplicated in `list_projects`, `get_project`, and `search_projects`. Extract to shared constant.

**Current Code (duplicated 3 times):**

```python
status_emoji = {
    "active": "🟢",
    "inactive": "⚪",
    "archived": "📦",
    "completed": "✅",
}
```

**Proposed Solution:**
Add constant at module level:

```python
# At top of file, after imports
STATUS_EMOJI = {
    "active": "🟢",
    "inactive": "⚪",
    "archived": "📦",
    "completed": "✅",
}

# In functions, replace local dict with:
emoji = STATUS_EMOJI.get(project.get("status", "").lower(), "")
```

---

### Issue PR4-#2: Delete corrupted inventory file

**Source PR:** #4 - Fix: Quick Wins Batch  
**Location:** `src/proj/commands/inventory.py:62-69`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
On `JSONDecodeError`, the corrupted file is left in place, causing repeated warnings. Consider backing up or deleting the bad file.

**Current Code:**

```python
except json.JSONDecodeError:
    console.print(
        "[yellow]Warning: inventory.json is corrupted. "
        "Starting with empty inventory.[/yellow]"
    )
    return []
```

**Proposed Solution:**
Rename corrupted file to backup:

```python
except json.JSONDecodeError:
    # Rename corrupted file to backup
    backup_file = inv_file.with_suffix('.json.corrupt')
    inv_file.rename(backup_file)
    console.print(
        f"[yellow]Warning: inventory.json was corrupted. "
        f"Backed up to {backup_file.name}. Starting fresh.[/yellow]"
    )
    return []
```

---

### Issue PR4-#3: Handle PackageNotFoundError gracefully

**Source PR:** #4 - Fix: Quick Wins Batch  
**Location:** `tests/test_package.py:18-22`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Test assumes metadata is installed. Skip gracefully when not available.

**Current Code:**

```python
def test_version_matches_metadata():
    """Test that __version__ matches installed package metadata."""
    try:
        from proj import __version__
        metadata_version = importlib.metadata.version("proj-cli")
        assert __version__ == metadata_version
    except importlib.metadata.PackageNotFoundError:
        pytest.skip("Package metadata not available")
```

**Note:** This was partially addressed in Phase 4. Verify the skip is in place and test works correctly.

---

### Issue PR5-#4: Add exit code assertion in test

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `tests/test_cli_integration.py:28-32`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
`test_cli_no_args_shows_help` only asserts on stdout. Add exit code assertion.

**Current Code:**

```python
def test_cli_no_args_shows_help():
    """Test that no args shows help."""
    result = runner.invoke(app, [])
    # Typer with no_args_is_help=True shows help
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()
```

**Proposed Solution:**

```python
def test_cli_no_args_shows_help():
    """Test that no args shows help."""
    result = runner.invoke(app, [])
    # Typer with no_args_is_help=True shows help and exits 0
    assert result.exit_code == 0
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()
```

---

### Issue PR5-#6: Assert config file created after load

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `tests/test_config_integration.py:8-17`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Test should verify config file is created on disk after `Config.load()`.

**Proposed Solution:**
Add assertion at end of test:

```python
def test_config_creates_default_on_first_run(mock_xdg_dirs):
    """Test that default config is created on first run."""
    from proj.config import Config, get_config_file
    
    config_file = get_config_file()
    assert not config_file.exists()
    
    config = Config.load()
    assert config.api_url == "http://localhost:5000"
    
    # After loading, config file should exist
    # Note: This depends on Config.load() behavior - verify if it creates file
    # If Config.load() doesn't create file, this assertion may not apply
```

**Note:** Verify if `Config.load()` actually creates the file on first run. If it only loads defaults without writing, this may not be applicable.

---

### Issue PR5-#8: Fix typo in docs (PR reference)

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `docs/maintainers/planning/features/proj-cli/phase-4.md:41`  
**Sourcery Comment:** Comment #8  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The `PR #2 #2` formatting is confusing. Fix to `PR #2-#2` or `PR #2 Issue #2`.

**Current Code:**

```markdown
- PR #2 #2: Add CliRunner tests for actual command behavior (HIGH value)
```

**Proposed Solution:**

```markdown
- PR #2-#2: Add CliRunner tests for actual command behavior (HIGH value)
```

---

### Issue PR5-OC2: Fix URL consistency in docs

**Source PR:** #5 - Phase 4: Polish & Cleanup  
**Location:** `README.md`  
**Sourcery Comment:** Overall Comment 2  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Repository references mix `grimm00` and `yourusername` in GitHub URLs.

**Proposed Solution:**
Search and replace `yourusername` with `grimm00` throughout documentation.

---

### Issue PR4-OC2: Add JSON error logging

**Source PR:** #4 - Fix: Quick Wins Batch  
**Location:** `src/proj/commands/inventory.py:62-69`  
**Sourcery Comment:** Overall Comment  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Log exception message for debugging when `json.JSONDecodeError` occurs.

**Proposed Solution:**

```python
import logging

logger = logging.getLogger(__name__)

# In load_inventory():
except json.JSONDecodeError as e:
    logger.debug(f"Failed to parse inventory.json: {e}")
    # ... rest of handler
```

---

## Implementation Steps

### 1. PR5-#3: Fix broad exception handling (HIGH PRIORITY)

- [ ] Open `tests/test_api_client_integration.py`
- [ ] Import `requests` module
- [ ] Change `except Exception` to `except (requests.ConnectionError, requests.Timeout)`
- [ ] Move assertions outside try/except block
- [ ] Apply to all integration test functions
- [ ] Run tests to verify

### 2. PR5-#1: Centralize status_emoji

- [ ] Open `src/proj/commands/projects.py`
- [ ] Add `STATUS_EMOJI` constant at module level (after imports)
- [ ] Remove local `status_emoji` dict from `list_projects`
- [ ] Remove local `status_emoji` dict from `get_project`
- [ ] Remove local `status_emoji` dict from `search_projects`
- [ ] Update all references to use `STATUS_EMOJI`
- [ ] Run tests to verify

### 3. PR4-#2: Delete corrupted inventory file

- [ ] Open `src/proj/commands/inventory.py`
- [ ] Update `load_inventory()` JSONDecodeError handler
- [ ] Rename corrupted file to `.json.corrupt` backup
- [ ] Update warning message
- [ ] Run tests to verify

### 4. PR4-#3: Verify PackageNotFoundError handling

- [ ] Open `tests/test_package.py`
- [ ] Verify `test_version_matches_metadata` has proper skip
- [ ] Run test in environment without package metadata
- [ ] Confirm skip works correctly

### 5. PR5-#4: Add exit code assertion

- [ ] Open `tests/test_cli_integration.py`
- [ ] Add `assert result.exit_code == 0` to `test_cli_no_args_shows_help`
- [ ] Run tests to verify

### 6. PR5-#6: Assert config file created (if applicable)

- [ ] Check if `Config.load()` creates file on first run
- [ ] If yes, add assertion to `test_config_creates_default_on_first_run`
- [ ] If no, skip this issue (not applicable)
- [ ] Run tests to verify

### 7. PR5-#8: Fix typo in docs

- [ ] Open `docs/maintainers/planning/features/proj-cli/phase-4.md`
- [ ] Change `PR #2 #2` to `PR #2-#2`
- [ ] Check for similar typos

### 8. PR5-OC2: Fix URL consistency

- [ ] Search for `yourusername` in all documentation
- [ ] Replace with `grimm00`
- [ ] Verify links work

### 9. PR4-OC2: Add JSON error logging

- [ ] Open `src/proj/commands/inventory.py`
- [ ] Add `import logging` and `logger = logging.getLogger(__name__)`
- [ ] Add `logger.debug()` call in JSONDecodeError handler
- [ ] Run tests to verify

---

## Testing

- [ ] All existing tests pass (49+ tests)
- [ ] Integration tests properly skip when API unavailable
- [ ] Integration tests properly fail on assertion errors
- [ ] Status emoji displays correctly
- [ ] Corrupted inventory file is backed up
- [ ] No regressions introduced

---

## Files to Modify

| File | Changes |
|------|---------|
| `tests/test_api_client_integration.py` | Catch specific exceptions only |
| `src/proj/commands/projects.py` | Centralize STATUS_EMOJI constant |
| `src/proj/commands/inventory.py` | Backup corrupted file, add logging |
| `tests/test_package.py` | Verify PackageNotFoundError handling |
| `tests/test_cli_integration.py` | Add exit code assertion |
| `tests/test_config_integration.py` | Assert config file created (if applicable) |
| `docs/.../phase-4.md` | Fix PR reference typo |
| `README.md` | Fix URL consistency |

---

## Definition of Done

- [ ] All 9 issues addressed (or documented as N/A)
- [ ] Tests passing
- [ ] Linting clean
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This batch was created from fix-review-report-2025-12-18.md. These issues are batched together because they:
- Include 1 HIGH priority test reliability issue
- Are all LOW effort (~10-15 minutes each)
- Focus on technical improvements (tests, code quality, docs)
- Can be implemented together efficiently (~1.5-2 hours)

---

**Last Updated:** 2025-12-18

