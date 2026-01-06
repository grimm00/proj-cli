# Fix Plan: PR #9 Batch MEDIUM LOW - Batch 01

**PR:** #9  
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
| PR9-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Add XDG isolation to env override tests |
| PR9-Overall-#1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Extract shared XDG isolation fixture |

---

## Overview

This batch contains 2 test infrastructure improvement issues with LOW effort. Both issues relate to XDG environment isolation in config tests and should be implemented together for consistency.

**Estimated Time:** 30-45 minutes  
**Files Affected:** `tests/test_config.py`

**Theme:** Test infrastructure - XDG isolation consistency

---

## Issue Details

### Issue PR9-#1: Add XDG Isolation to Env Override Tests

**Location:** `tests/test_config.py:116-119`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
PR #9 fixed `test_config_registry_path_xdg_default` to isolate XDG directories, but other `Config.load()` tests that rely on env overrides still use the real XDG environment. These tests should also set `XDG_CONFIG_HOME` and `XDG_DATA_HOME` via `monkeypatch` to avoid flakiness from local user config files.

**Tests needing isolation:**
- `test_config_env_override`
- `test_config_api_enabled_env_override`
- `test_config_templates_source_env_override`
- `test_config_registry_path_env_override`
- Other tests calling `Config.load()`

**Current Code Pattern:**
```python
def test_config_env_override(monkeypatch):
    """Test environment variable override."""
    monkeypatch.setenv("PROJ_API_URL", "http://test.example.com")
    from proj.config import Config
    config = Config.load()
    # Test relies on real XDG directories - flaky!
```

**Proposed Solution:**
```python
def test_config_env_override(tmp_path, monkeypatch):
    """Test environment variable override."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("PROJ_API_URL", "http://test.example.com")
    from proj.config import Config
    config = Config.load()
    # Test now uses isolated XDG directories
```

---

### Issue PR9-Overall-#1: Extract Shared XDG Isolation Fixture

**Location:** `tests/test_config.py` (throughout)  
**Sourcery Comment:** Overall Comment #1  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
All updated tests duplicate the same `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))` setup. Consider extracting a small fixture (e.g., `isolated_config_home`) so the isolation behavior is defined in one place and reused across tests.

**Current Code Pattern (duplicated):**
```python
def test_something(tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    # ... rest of test
```

**Proposed Solution:**
```python
@pytest.fixture
def isolated_xdg(tmp_path, monkeypatch):
    """Fixture to isolate XDG directories for config tests."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    return tmp_path

def test_something(isolated_xdg):
    """Test with isolated XDG directories."""
    from proj.config import Config
    config = Config.load()
    # Uses isolated XDG directories via fixture
```

---

## Implementation Steps

1. **Create Shared Fixture (PR9-Overall-#1)**
   - [ ] Add `isolated_xdg` fixture to `tests/test_config.py` or `tests/conftest.py`
   - [ ] Fixture should set both `XDG_CONFIG_HOME` and `XDG_DATA_HOME`
   - [ ] Return `tmp_path` for tests that need to access the directory

2. **Update Existing Isolated Tests**
   - [ ] Refactor `test_config_registry_path_xdg_default` to use new fixture
   - [ ] Remove duplicated monkeypatch calls

3. **Add Isolation to Env Override Tests (PR9-#1)**
   - [ ] Update `test_config_env_override` to use `isolated_xdg` fixture
   - [ ] Update `test_config_api_enabled_env_override` to use `isolated_xdg` fixture
   - [ ] Update `test_config_templates_source_env_override` to use `isolated_xdg` fixture
   - [ ] Update `test_config_registry_path_env_override` to use `isolated_xdg` fixture
   - [ ] Review other tests for similar issues

4. **Verify All Tests Pass**
   - [ ] Run `pytest tests/test_config.py -v`
   - [ ] Verify no flakiness
   - [ ] Verify tests work in CI environment

---

## Testing

- [ ] All existing tests pass
- [ ] No test flakiness when running multiple times
- [ ] Tests pass in CI environment
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_config.py` - Add fixture and update tests
- `tests/conftest.py` - Alternative location for shared fixture (if preferred)

---

## Definition of Done

- [ ] `isolated_xdg` fixture created
- [ ] All env override tests use fixture
- [ ] No duplicated XDG setup code
- [ ] Tests passing locally and in CI
- [ ] Code reviewed
- [ ] Ready for PR

---

## Batch Rationale

These issues are batched together because they:
- Both relate to XDG test isolation
- PR9-Overall-#1 (fixture) should be implemented before PR9-#1 (use fixture)
- Combined effort is still LOW
- Creates consistent test infrastructure

---

**Last Updated:** 2026-01-06

