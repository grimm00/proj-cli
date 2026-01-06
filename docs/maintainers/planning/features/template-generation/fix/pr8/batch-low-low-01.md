# Fix Plan: PR #8 Batch LOW LOW - Batch 01

**PR:** #8  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2025-01-05  
**Completed:** 2026-01-06  
**Merged:** PR #[pending]  
**Issues:** 4 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR8-#5 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Strengthen save() test with type assertions |
| PR8-#6 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Extend YAML load test to cover more fields |
| PR8-#7 | 🟢 LOW | 🟡 MEDIUM | 🟢 LOW | CLI init test should validate loaded Config values |
| PR8-#8 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Documentation count mismatch |

---

## Overview

This batch contains 4 LOW priority issues with LOW effort. These are test improvements and a documentation fix that improve code quality but are not blocking.

**Estimated Time:** 30-45 minutes  
**Files Affected:** `tests/test_config.py`, `tests/test_cli_integration.py`, `docs/maintainers/planning/features/template-generation/feature-plan.md`

---

## Issue Details

### Issue PR8-#5: Strengthen save() Test

**Location:** `tests/test_config.py:150-159`  
**Sourcery Comment:** Comment #5  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The test only checks that new keys exist; it doesn't verify correct serialization (e.g. `Path` → `str`, booleans staying `bool`, nested structures shaped correctly).

**Proposed Solution:**
Add type assertions to `test_config_save_includes_new_fields`:

```python
def test_config_save_includes_new_fields(tmp_path, monkeypatch):
    """Test that save() includes new configuration fields."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    from proj.config import Config, get_config_file
    config = Config.load()
    config.save()

    config_file = get_config_file()
    with open(config_file) as f:
        saved = yaml.safe_load(f)

    # Check keys exist
    assert 'api_enabled' in saved
    assert 'templates' in saved
    assert 'registry' in saved
    assert 'default_project_dir' in saved

    # Check types (NEW)
    assert isinstance(saved['api_enabled'], bool)
    assert isinstance(saved['templates'], dict)
    assert isinstance(saved['registry'], dict)
    assert isinstance(saved['default_project_dir'], str)

    # Check nested structure (NEW)
    assert 'source' in saved['templates']
    assert 'default' in saved['templates']
    assert 'path' in saved['registry']
```

---

### Issue PR8-#6: Extend YAML Load Test

**Location:** `tests/test_config.py:169-178`  
**Sourcery Comment:** Comment #6  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The test sets `registry.path` and `default_project_dir` in the YAML but doesn't assert those fields are loaded correctly.

**Proposed Solution:**
Add assertions to `test_config_load_nested_from_yaml`:

```python
def test_config_load_nested_from_yaml(tmp_path, monkeypatch):
    """Test loading nested config from YAML file."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # ... existing setup code ...

    config = Config.load()
    assert config.api_enabled is False
    assert str(config.templates.source) == '/custom/templates'
    assert config.templates.default == 'learning-project'
    
    # Add assertions for registry and default_project_dir (NEW)
    assert str(config.registry.path) == '/custom/registry.json'
    assert str(config.default_project_dir) == '/custom/projects'
```

---

### Issue PR8-#7: CLI Init Test Should Validate Loaded Config

**Location:** `tests/test_cli_integration.py:175-184`  
**Sourcery Comment:** Comment #7  
**Priority:** 🟢 LOW | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The test only checks that new keys exist in the generated YAML. It should also validate that `Config.load()` yields expected defaults.

**Proposed Solution:**
Extend `test_init_creates_config_with_new_fields`:

```python
def test_init_creates_config_with_new_fields(tmp_path, monkeypatch):
    """Test that proj init creates config with new fields."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    result = subprocess.run(
        [sys.executable, "-m", "proj", "init"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0

    from proj.config import get_config_file, Config
    config_file = get_config_file()
    assert config_file.exists()

    # Check YAML keys exist
    with open(config_file) as f:
        saved = yaml.safe_load(f)
    assert 'api_enabled' in saved
    assert 'templates' in saved
    assert 'registry' in saved
    assert 'default_project_dir' in saved

    # Validate loaded Config values (NEW)
    config = Config.load()
    assert config.api_enabled is True
    assert config.templates.default == 'standard-project'
    assert config.templates.source is None
```

---

### Issue PR8-#8: Documentation Count Mismatch

**Location:** `docs/maintainers/planning/features/template-generation/feature-plan.md:64`  
**Sourcery Comment:** Comment #8  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The PORT requirements row shows count of 4 but label says PORT-1 to PORT-7.

**Current Documentation:**

```markdown
| Port (PORT-1 to PORT-7) | 4 | 🔴 Pending |
```

**Proposed Solution:**
Fix the count or the label to match:

```markdown
| Port (PORT-1 to PORT-4) | 4 | 🔴 Pending |
```

---

## Implementation Steps

1. **Strengthen save() test (Issue #5):**
   - [ ] Add type assertions to `test_config_save_includes_new_fields`
   - [ ] Add nested structure assertions
   - [ ] Run test to verify

2. **Extend YAML load test (Issue #6):**
   - [ ] Add assertions for `registry.path` and `default_project_dir`
   - [ ] Run test to verify

3. **Validate loaded Config in CLI init test (Issue #7):**
   - [ ] Add `Config.load()` validation
   - [ ] Assert expected default values
   - [ ] Run test to verify

4. **Fix documentation count (Issue #8):**
   - [ ] Update `feature-plan.md` with correct PORT count
   - [ ] Verify count matches actual requirements

---

## Testing

- [ ] All existing tests pass
- [ ] New assertions in tests pass
- [ ] No regressions introduced

---

## Files to Modify

- `tests/test_config.py` - Strengthen save() and YAML load tests
- `tests/test_cli_integration.py` - Validate loaded Config values
- `docs/maintainers/planning/features/template-generation/feature-plan.md` - Fix PORT count

---

## Definition of Done

- [x] Test assertions strengthened in save() test
- [x] YAML load test extended with missing assertions
- [x] CLI init test validates loaded Config values
- [x] Documentation count fixed
- [x] All tests passing
- [x] Ready for PR

---

**Batch Rationale:**
These are all LOW priority, LOW effort issues that improve test quality and documentation accuracy. They can be implemented together as a code quality cleanup.

**Dependency:** Should implement after `batch-high-low-01` to ensure XDG isolation is in place for test modifications.

