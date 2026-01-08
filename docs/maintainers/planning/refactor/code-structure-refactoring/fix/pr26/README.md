# Fix Tracking - PR #26

**PR:** #26 - refactor: Test Structure Reorganization (Phase 2)  
**Phase:** Phase 2  
**Merged:** 2026-01-08  
**Status:** 🟡 Planned  
**Last Updated:** 2026-01-08

---

## 📋 Quick Links

### Fix Batches

- **[batch-medium-low-01.md](batch-medium-low-01.md)** - Test regression coverage (🟡 MEDIUM, 🟢 LOW, 2 issues)
- **[batch-low-low-01.md](batch-low-low-01.md)** - Code consolidation (🟢 LOW, 🟢 LOW, 1 issue)
- **[batch-low-medium-01.md](batch-low-medium-01.md)** - Test parametrization (🟢 LOW, 🟡 MEDIUM, 1 issue)

---

## 📊 Summary

**Total Issues:** 4  
**Batches:** 3  
**Status:** 🟡 Planned

**Priority Breakdown:**
- 🟡 MEDIUM: 2 issues (1 batch)
- 🟢 LOW: 2 issues (2 batches)

---

## 📋 Deferred Issues

**Date:** 2026-01-08
**Review:** PR #26 Sourcery feedback
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled opportunistically

**Deferred Issues:**

### Individual Comments

- **PR26-#1:** Strengthen prompt_for_create_options regression coverage (MEDIUM priority, LOW effort)
  - Add assertion checks for helper interactions (`get_templates_source`, `list_templates`)
  - Location: `tests/commands/projects/test_create.py:100-109`

- **PR26-#2:** Add regression test for `get_package_imports` patching (MEDIUM priority, LOW effort)
  - Add test to verify patching `proj.commands.projects.*` affects submodules
  - Location: `tests/commands/projects/test_list.py:104-107`

### Overall Comments

- **PR26-Overall-#1:** Consolidate `_get_client()` with `helpers.get_client()` (LOW priority, LOW effort)
  - `_get_client()` in `create.py` duplicates behavior of `helpers.get_client()`
  - Consider reusing shared helper to avoid divergence

- **PR26-Overall-#2:** Parametrize command-existence tests (LOW priority, MEDIUM effort)
  - Command-existence tests use nearly identical patterns across files
  - Extract helper or parametrized test to reduce repetition

**Action Plan:** These can be handled opportunistically during future work or in a dedicated test improvement PR. All are testing/code quality improvements with no user impact.

---

## 🔗 Related Documents

- [Sourcery Review](../../../../feedback/sourcery/pr26.md)
- [Phase 2](../../phase-2.md)
- [Fix Hub](../README.md)

---

**Last Updated:** 2026-01-08
