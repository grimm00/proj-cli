# Fix Plan: PR #8 Batch MEDIUM LOW - Batch 01

**PR:** #8  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-01-05  
**Issues:** 3 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR8-#1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | env_prefix confusion for TemplateConfig |
| PR8-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | env_prefix confusion for RegistryConfig |
| PR8-#4 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Missing env override test for PROJ_TEMPLATES__DEFAULT |

---

## Overview

This batch contains 3 MEDIUM priority issues with LOW effort. Issues #1 and #2 are related (env_prefix cleanup) and #4 is a missing test for documented functionality.

**Estimated Time:** 45 minutes  
**Files Affected:** `src/proj/config.py`, `tests/test_config.py`

---

## Issue Details

### Issue PR8-#1: env_prefix Confusion for TemplateConfig

**Location:** `src/proj/config.py:38`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
The `TemplateConfig` nested model has its own `env_prefix="PROJ_TEMPLATES_"` which may conflict with the parent `Config`'s `env_nested_delimiter="__"`. Tests prove `PROJ_TEMPLATES__SOURCE` works via the nested delimiter, so the explicit `env_prefix` is redundant and potentially confusing.

**Current Code:**

```python
class TemplateConfig(BaseSettings):
    """Template-related configuration."""

    model_config = SettingsConfigDict(
        env_prefix="PROJ_TEMPLATES_",  # May not be used
        extra="ignore",
    )
```

**Proposed Solution:**

```python
class TemplateConfig(BaseSettings):
    """Template-related configuration."""

    model_config = SettingsConfigDict(
        extra="ignore",
    )
```

---

### Issue PR8-#2: env_prefix Confusion for RegistryConfig

**Location:** `src/proj/config.py:59-62`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
Same issue as #1 - `RegistryConfig` has its own `env_prefix="PROJ_REGISTRY_"` that may conflict with nested delimiter pattern.

**Current Code:**

```python
class RegistryConfig(BaseSettings):
    """Local registry configuration."""

    model_config = SettingsConfigDict(
        env_prefix="PROJ_REGISTRY_",  # May not be used
        extra="ignore",
    )
```

**Proposed Solution:**

```python
class RegistryConfig(BaseSettings):
    """Local registry configuration."""

    model_config = SettingsConfigDict(
        extra="ignore",
    )
```

---

### Issue PR8-#4: Missing Test for PROJ_TEMPLATES__DEFAULT

**Location:** `tests/test_config.py:88-92`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
There's no env override test for `PROJ_TEMPLATES__DEFAULT` even though it's documented in the PR description. This is a gap in test coverage.

**Proposed Solution:**

```python
def test_config_templates_default_env_override(tmp_path, monkeypatch):
    """Test PROJ_TEMPLATES__DEFAULT environment variable."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("PROJ_TEMPLATES__DEFAULT", "learning-project")
    from proj.config import Config
    config = Config.load()
    assert config.templates.default == "learning-project"
```

---

## Implementation Steps

1. **Remove env_prefix from TemplateConfig (Issue #1):**
   - [ ] Open `src/proj/config.py`
   - [ ] Remove `env_prefix="PROJ_TEMPLATES_"` from TemplateConfig
   - [ ] Run tests to verify env overrides still work

2. **Remove env_prefix from RegistryConfig (Issue #2):**
   - [ ] Remove `env_prefix="PROJ_REGISTRY_"` from RegistryConfig
   - [ ] Run tests to verify env overrides still work

3. **Add missing test (Issue #4):**
   - [ ] Add `test_config_templates_default_env_override` to `tests/test_config.py`
   - [ ] Use XDG isolation (depends on batch-high-low-01)
   - [ ] Run test to verify it passes

4. **Run full test suite:**
   - [ ] `pytest tests/ -v`
   - [ ] Verify no regressions

---

## Testing

- [ ] All existing tests pass
- [ ] New test for PROJ_TEMPLATES__DEFAULT passes
- [ ] Env overrides work correctly after removing env_prefix
- [ ] No regressions introduced

---

## Files to Modify

- `src/proj/config.py` - Remove redundant env_prefix from nested models
- `tests/test_config.py` - Add missing env override test

---

## Definition of Done

- [ ] env_prefix removed from TemplateConfig
- [ ] env_prefix removed from RegistryConfig
- [ ] New test for PROJ_TEMPLATES__DEFAULT added
- [ ] All tests passing
- [ ] Ready for PR

---

**Batch Rationale:**
Issues #1 and #2 are directly related (same pattern in different classes). Issue #4 is a test that completes the env override coverage. All can be implemented together efficiently.

**Dependency:** Should implement after `batch-high-low-01` to ensure XDG isolation is in place for new test.

