# PR #2 - Deferred Issues

**PR:** #2 - feat: Migrate Project Commands (Phase 2)  
**Merged:** 2025-12-17  
**Status:** 🟡 Deferred to Phase 4

---

## 📋 Deferred Issues

**Date:** 2025-12-17  
**Review:** PR #2 (Phase 2) Sourcery feedback  
**Status:** 🟡 **DEFERRED** - All MEDIUM/LOW priority, can be handled in Phase 4

### Individual Comments

| # | Description | Priority | Effort | Action |
|---|-------------|----------|--------|--------|
| PR2-#2 | Add CliRunner tests for actual command behavior | 🟡 MEDIUM | 🟡 MEDIUM | Defer to Phase 4 |

### Overall Comments

| # | Description | Priority | Effort | Action |
|---|-------------|----------|--------|--------|
| OC-1 | API URL validation in APIClient constructor | 🟡 MEDIUM | 🟢 LOW | Defer to Phase 4 |
| OC-2 | Format option validation with typer.Choice | 🟢 LOW | 🟢 LOW | Defer to Phase 4 |
| OC-3 | URL building helper extraction | 🟢 LOW | 🟡 MEDIUM | Defer to Phase 4 |

---

## ✅ Fixed Issues

| # | Description | Priority | Effort | Status |
|---|-------------|----------|--------|--------|
| PR2-#1 | Timeout errors bypass CLI error handling | 🟠 HIGH | 🟢 LOW | ✅ Fixed in PR #2 |

---

## 📝 Action Plan

These items are deferred to Phase 4 (Polish & Cleanup) where they can be addressed as part of overall code quality improvements:

1. **PR2-#2:** Add comprehensive CliRunner tests
   - Test actual command behavior, not just --help
   - Test error handling paths
   - Test output formatting

2. **OC-1:** Normalize/validate API URL in APIClient constructor
   - Handle None, whitespace, and missing scheme
   - Match behavior of `_get_health_url()`

3. **OC-2:** Use typer.Choice for format options
   - Enforce valid values (table, json)
   - Improve UX by catching invalid values early

4. **OC-3:** Extract shared URL building helper
   - Reduce duplication between `check_backend_health` and `APIClient._url`
   - Ensure consistent URL normalization

---

## 🔗 Related

- [PR #2 Sourcery Review](../../../feedback/sourcery/pr2.md)
- [Phase 2 Document](../phase-2.md)
- [Phase 4 Document](../phase-4.md)

---

**Last Updated:** 2025-12-17

