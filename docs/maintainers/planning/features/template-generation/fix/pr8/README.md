# PR #8 Fix Tracking

**PR:** #8 - feat: Config Extension for Template Generation (Phase 1)  
**Merged:** 2025-01-05  
**Phase:** Phase 1: Config Extension  
**Status:** 🟡 Planned  
**Last Updated:** 2025-01-05

---

## 📋 Quick Links

### Fix Batches

- **[batch-high-low-01.md](batch-high-low-01.md)** - Test isolation (🟠 HIGH, 🟢 LOW, 1 issue)
- **[batch-medium-low-01.md](batch-medium-low-01.md)** - Config cleanup + test (🟡 MEDIUM, 🟢 LOW, 3 issues)
- **[batch-low-low-01.md](batch-low-low-01.md)** - Test improvements + docs (🟢 LOW, 🟢 LOW, 4 issues)

---

## 📊 Summary

**Total Issues:** 8  
**Batches:** 3  
**Status:** 🟡 Planned

**Priority Breakdown:**

| Priority | Count | Batch |
|----------|-------|-------|
| 🟠 HIGH | 1 | batch-high-low-01 |
| 🟡 MEDIUM | 3 | batch-medium-low-01 |
| 🟢 LOW | 4 | batch-low-low-01 |

**Recommended Order:**
1. `batch-high-low-01` - Fix test isolation first (blocking)
2. `batch-medium-low-01` - Config cleanup and missing test
3. `batch-low-low-01` - Test improvements and docs fix

---

## 🟠 HIGH Priority Batch

### batch-high-low-01: Test Isolation

- **Status:** 🔴 Not Started
- **Issues:** 1
- **Estimated:** 30 minutes
- **File:** [batch-high-low-01.md](batch-high-low-01.md)

**Issue:**
- PR8-#3: Test isolation for XDG_CONFIG_HOME

---

## 🟡 MEDIUM Priority Batch

### batch-medium-low-01: Config Cleanup + Test

- **Status:** 🔴 Not Started
- **Issues:** 3
- **Estimated:** 45 minutes
- **File:** [batch-medium-low-01.md](batch-medium-low-01.md)

**Issues:**
- PR8-#1: env_prefix confusion for TemplateConfig
- PR8-#2: env_prefix confusion for RegistryConfig
- PR8-#4: Missing env override test for PROJ_TEMPLATES__DEFAULT

---

## 🟢 LOW Priority Batch

### batch-low-low-01: Test Improvements + Docs

- **Status:** 🔴 Not Started
- **Issues:** 4
- **Estimated:** 30-45 minutes
- **File:** [batch-low-low-01.md](batch-low-low-01.md)

**Issues:**
- PR8-#5: Strengthen save() test with type assertions
- PR8-#6: Extend YAML load test to cover more fields
- PR8-#7: CLI init test should validate loaded Config values
- PR8-#8: Documentation count mismatch

---

## 📋 Quick Links

- [Sourcery Review](../../../../feedback/sourcery/pr8.md)
- [Phase 1 Document](../../phase-1.md)
- [Feature Status](../../status-and-next-steps.md)
- [Fix Tracking Hub](../README.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🟡 Planned  
**Next:** Implement batches using `/fix-implement`
