# Deferred Tasks

**Purpose:** Centralize deferred issues (MEDIUM/LOW priority) from PR reviews for future addressing.  
**Last Updated:** 2025-01-05  
**Status:** ✅ Active

---

## 📊 Summary

| Priority | Count |
|----------|-------|
| 🟡 MEDIUM | 1 |
| 🟢 LOW | 2 |
| **Total** | **3** |

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

#### Task 3: Avoid double-read of `.dev-infra.yml` in skills validation

- **Source:** PR #31 - Sourcery Overall Comment #2
- **Location:** `src/proj/skills.py` - `warn_missing_expected_skills` function
- **Priority:** 🟢 LOW
- **Impact:** 🟢 LOW
- **Effort:** 🟢 LOW
- **Description:** `warn_missing_expected_skills` calls `load_expected_skills` directly and then `find_missing_skills` which calls it again internally. Refactor to pass the already-loaded list or inline the logic to avoid parsing the manifest twice.
- **Status:** ⏸️ Deferred

---

## PR Additions Log

### PR #9 Additions (2025-01-05)

- Task 1: Add XDG isolation to env override tests (MEDIUM priority, LOW effort)
- Task 2: Extract shared XDG isolation fixture (LOW priority, LOW effort)

### PR #31 Additions (2026-06-09)

- Task 3: Avoid double-read of `.dev-infra.yml` in skills validation (LOW priority, LOW effort)

---

**Last Updated:** 2026-06-09

