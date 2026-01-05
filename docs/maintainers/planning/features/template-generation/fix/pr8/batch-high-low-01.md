# Fix Plan: PR #8 Batch HIGH LOW - Batch 01

**PR:** #8  
**Batch:** high-low-01  
**Priority:** 🟠 HIGH  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-01-05  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR8-#3 | 🟠 HIGH | 🟠 HIGH | 🟢 LOW | Test isolation for XDG_CONFIG_HOME |

---

## Overview

This batch contains 1 HIGH priority issue with LOW effort. This issue addresses test flakiness that can occur when developers have local config files.

**Estimated Time:** 30 minutes  
**Files Affected:** `tests/test_config.py`

---

## Issue Details

### Issue PR8-#3: Test Isolation for XDG_CONFIG_HOME

**Location:** `tests/test_config.py:52-61`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟠 HIGH | **Impact:** 🟠 HIGH | **Effort:** 🟢 LOW

**Description:**
The `Config.load()` tests (e.g. `test_config_has_api_enabled`, `test_config_api_enabled_default_true`, and other default-value checks) currently depend on there being no real `config.yaml` under the user's XDG config/home dirs. If a developer has a local config with non-default values, the tests can fail or become flaky.

**Solution:**
Isolate tests by pointing `XDG_CONFIG_HOME` at a temporary directory via `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))`.

**Current Code (affected tests):**

```python
def test_config_has_api_enabled():
    """Test that config has api_enabled setting."""
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'api_enabled')
```

**Proposed Solution:**

```python
def test_config_has_api_enabled(tmp_path, monkeypatch):
    """Test that config has api_enabled setting."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'api_enabled')
```

---

## Implementation Steps

1. **Identify affected tests:**
   - [ ] Find all tests that call `Config.load()` without XDG isolation
   - [ ] List: `test_config_has_api_enabled`, `test_config_api_enabled_default_true`, etc.

2. **Add fixtures:**
   - [ ] Add `tmp_path` and `monkeypatch` fixtures to affected tests
   - [ ] Add `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))` at start

3. **Verify tests still pass:**
   - [ ] Run `pytest tests/test_config.py -v`
   - [ ] Verify all tests pass with isolation

4. **Test with local config:**
   - [ ] Create a local config file with non-default values
   - [ ] Verify tests still pass (proving isolation works)

---

## Testing

- [ ] All existing tests pass
- [ ] Tests pass when developer has local config
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_config.py` - Add XDG isolation to affected tests

---

## Definition of Done

- [ ] All affected tests have XDG isolation
- [ ] Tests pass in CI
- [ ] Tests pass with local config present
- [ ] Ready for PR

---

**Batch Rationale:**
This issue is batched alone because it's HIGH priority and affects test reliability. It should be addressed before other issues to ensure test suite is stable.

