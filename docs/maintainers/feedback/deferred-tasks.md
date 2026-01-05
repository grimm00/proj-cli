# Deferred Tasks

**Purpose:** Centralize deferred issues (MEDIUM/LOW priority) from PR reviews for future addressing.  
**Last Updated:** 2025-01-05  
**Status:** ✅ Active

---

## 📊 Summary

| Priority | Count |
|----------|-------|
| 🟡 MEDIUM | 1 |
| 🟢 LOW | 1 |
| **Total** | **2** |

---

## 🟡 Medium Priority Tasks

### Test Infrastructure

#### Task 1: Add XDG isolation to env override tests

- **Source:** PR #9 - Sourcery Comment #1
- **Location:** `tests/test_config.py` - env override tests
- **Priority:** 🟡 MEDIUM
- **Impact:** 🟡 MEDIUM
- **Effort:** 🟢 LOW
- **Description:** Add `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))` to env override tests (`test_config_env_override`, `test_config_api_enabled_env_override`, `test_config_templates_source_env_override`, `test_config_registry_path_env_override`, etc.) for full isolation.
- **Status:** ⏸️ Deferred

---

## 🟢 Low Priority Tasks

### Code Quality

#### Task 2: Extract shared XDG isolation fixture

- **Source:** PR #9 - Sourcery Overall Comment #1
- **Location:** `tests/test_config.py` - fixture extraction
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟢 LOW
- **Description:** Extract a shared fixture (e.g., `isolated_config_home`) to replace duplicated `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))` setup across tests.
- **Status:** ⏸️ Deferred

---

## PR Additions Log

### PR #9 Additions (2025-01-05)

- Task 1: Add XDG isolation to env override tests (MEDIUM priority, LOW effort)
- Task 2: Extract shared XDG isolation fixture (LOW priority, LOW effort)

---

**Last Updated:** 2025-01-05

