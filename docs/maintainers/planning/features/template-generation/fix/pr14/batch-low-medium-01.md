# Fix Plan: PR #14 Batch LOW MEDIUM - 01

**PR:** #14  
**Batch:** low-medium-01  
**Priority:** 🟢 LOW  
**Effort:** 🟡 MEDIUM  
**Status:** 🔴 Not Started  
**Created:** 2026-01-06  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR14-Overall-#2 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Extract shared test fixtures |

---

## Overview

This batch contains 1 LOW priority test refactoring issue with MEDIUM effort. This is a DRY improvement for test maintainability.

**Estimated Time:** 1-1.5 hours  
**Files Affected:** `tests/test_create_api_sync.py`, possibly `tests/conftest.py`

---

## Issue Details

### Issue PR14-Overall-#2: Extract Shared Test Fixtures

**Location:** `tests/test_create_api_sync.py`  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
The integration tests repeat a fair amount of setup (env vars, template dirs, config YAML, target dirs); extracting this into shared fixtures or helper functions would reduce duplication and make future test changes easier.

**Current Pattern (repeated in multiple tests):**

```python
def test_something(tmp_path, monkeypatch):
    # XDG setup
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    
    # Template setup
    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    
    # Config setup
    config_dir = tmp_path / "proj"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text(f"""
api_url: http://localhost:5000
api_enabled: true
templates:
  source: {templates}
""")
    
    # Target dir setup
    projects = tmp_path / "projects"
    projects.mkdir()
    # ... test logic ...
```

**Proposed Solution:**

```python
# In tests/conftest.py or tests/test_create_api_sync.py

@pytest.fixture
def api_sync_test_env(tmp_path, monkeypatch):
    """Standard test environment for API sync tests."""
    # XDG setup
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    
    # Template setup
    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    
    # Config setup
    config_dir = tmp_path / "proj"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text(f"""
api_url: http://localhost:5000
api_enabled: true
templates:
  source: {templates}
""")
    
    # Target dir setup
    projects = tmp_path / "projects"
    projects.mkdir()
    
    return {
        "tmp_path": tmp_path,
        "templates": templates,
        "config_dir": config_dir,
        "config_file": config_file,
        "projects": projects,
    }


# Usage in tests:
def test_something(api_sync_test_env):
    projects = api_sync_test_env["projects"]
    # ... test logic using shared setup ...
```

---

## Implementation Steps

1. **Analyze Existing Tests**
   - [ ] Identify all tests with repeated setup
   - [ ] Document common setup patterns
   - [ ] Identify variations between tests

2. **Create Shared Fixtures**
   - [ ] Create `api_sync_test_env` fixture
   - [ ] Consider parameterized fixtures for variations
   - [ ] Place in `conftest.py` or test file

3. **Refactor Tests**
   - [ ] Update each test to use shared fixture
   - [ ] Remove duplicate setup code
   - [ ] Verify tests still pass after each change

4. **Review**
   - [ ] Ensure DRY improvement is significant
   - [ ] Verify no test isolation issues
   - [ ] Document fixture usage

---

## Testing

- [ ] All existing tests pass after refactoring
- [ ] No test isolation issues
- [ ] Fixture provides necessary flexibility
- [ ] Future tests easier to write

---

## Files to Modify

- `tests/test_create_api_sync.py` - Refactor to use fixtures
- `tests/conftest.py` - Add shared fixtures (optional)

---

## Definition of Done

- [ ] Shared fixtures created
- [ ] Tests refactored to use fixtures
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
Single LOW/MEDIUM refactoring task. Should be done when there's time for careful test refactoring to avoid breaking tests.

