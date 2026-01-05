# Fix Tracking - PR #8 (Phase 1: Config Extension)

**PR:** #8 - feat: Config Extension for Template Generation (Phase 1)  
**Merged:** 2025-01-05  
**Phase:** Phase 1: Config Extension  
**Status:** ✅ Merged

---

## 📋 Deferred Issues

**Date:** 2025-01-05  
**Review:** PR #8 (Phase 1) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

### Issue Summary

| # | Description | Priority | Effort | Action |
|---|-------------|----------|--------|--------|
| #1 | env_prefix confusion for TemplateConfig | 🟡 MEDIUM | 🟢 LOW | Defer |
| #2 | env_prefix confusion for RegistryConfig | 🟡 MEDIUM | 🟢 LOW | Defer |
| #3 | Test isolation for XDG_CONFIG_HOME | 🟠 HIGH | 🟢 LOW | Defer |
| #4 | Missing test for PROJ_TEMPLATES__DEFAULT | 🟡 MEDIUM | 🟢 LOW | Defer |
| #5 | Strengthen save() test with type assertions | 🟢 LOW | 🟢 LOW | Defer |
| #6 | Extend YAML load test coverage | 🟢 LOW | 🟢 LOW | Defer |
| #7 | CLI init test should validate loaded config | 🟢 LOW | 🟢 LOW | Defer |
| #8 | Documentation count mismatch (PORT requirements) | 🟢 LOW | 🟢 LOW | Defer |

---

### Issue Details

#### PR8-#1: env_prefix Confusion for TemplateConfig

**Location:** `src/proj/config.py:38`  
**Type:** question (bug_risk)  
**Priority:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:** The `TemplateConfig` nested model has its own `env_prefix="PROJ_TEMPLATES_"` which may conflict with the parent `Config`'s `env_nested_delimiter="__"`. Tests prove `PROJ_TEMPLATES__SOURCE` works, but having two mechanisms is confusing.

**Action:** Defer - Consider removing `env_prefix` from nested models in future cleanup.

---

#### PR8-#2: env_prefix Confusion for RegistryConfig

**Location:** `src/proj/config.py:59-62`  
**Type:** suggestion  
**Priority:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:** Same issue as #1 - `RegistryConfig` has its own `env_prefix` that may conflict with nested delimiter pattern.

**Action:** Defer - Batch with #1 if fixing.

---

#### PR8-#3: Test Isolation for XDG_CONFIG_HOME

**Location:** `tests/test_config.py:52-61`  
**Type:** issue (testing)  
**Priority:** 🟠 HIGH | **Effort:** 🟢 LOW

**Description:** Config tests don't isolate `XDG_CONFIG_HOME`, so they may be flaky if developer has a local config file with non-default values.

**Action:** Defer - Add `monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))` to affected tests.

---

#### PR8-#4: Missing Test for PROJ_TEMPLATES__DEFAULT

**Location:** `tests/test_config.py:88-92`  
**Type:** suggestion (testing)  
**Priority:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:** No env override test for `PROJ_TEMPLATES__DEFAULT` even though it's documented in PR description.

**Action:** Defer - Add test for completeness.

---

#### PR8-#5: Strengthen save() Test

**Location:** `tests/test_config.py:150-159`  
**Type:** suggestion (testing)  
**Priority:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:** Test only checks keys exist, doesn't verify correct serialization types.

**Action:** Defer - Add type assertions for completeness.

---

#### PR8-#6: Extend YAML Load Test

**Location:** `tests/test_config.py:169-178`  
**Type:** suggestion (testing)  
**Priority:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:** Test should also assert `registry.path` and `default_project_dir` fields.

**Action:** Defer - Add assertions for completeness.

---

#### PR8-#7: CLI Init Test Should Validate Loaded Config

**Location:** `tests/test_cli_integration.py:175-184`  
**Type:** suggestion (testing)  
**Priority:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:** Test only checks YAML keys, should also validate `Config.load()` yields expected defaults.

**Action:** Defer - Add Config.load() validation.

---

#### PR8-#8: Documentation Count Mismatch

**Location:** `docs/maintainers/planning/features/template-generation/feature-plan.md:64`  
**Type:** issue (bug_risk)  
**Priority:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:** PORT requirements row shows count of 4 but label says PORT-1 to PORT-7.

**Action:** Defer - Fix documentation count.

---

## 📊 Overall Summary

- **Total Issues:** 8
- **CRITICAL:** 0
- **HIGH:** 1 (#3 - test isolation)
- **MEDIUM:** 3 (#1, #2, #4)
- **LOW:** 4 (#5, #6, #7, #8)

**Recommendation:** All issues can be deferred. Consider creating a fix batch when starting Phase 2 or handling opportunistically during future phases.

---

## 📋 Quick Links

- [Sourcery Review](../../../../feedback/sourcery/pr8.md)
- [Phase 1 Document](../../phase-1.md)
- [Feature Status](../../status-and-next-steps.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🟡 Deferred  
**Next:** Handle opportunistically or create fix batch

