# Fix Tracking - PR #5

**PR:** #5 - feat: Polish & Cleanup (Phase 4)  
**Sourcery Review:** `docs/maintainers/feedback/sourcery/pr5.md`  
**Status:** Deferred  
**Created:** 2025-12-17

---

## Summary

| Priority | Count | Status |
|----------|-------|--------|
| 🔴 CRITICAL | 0 | - |
| 🟠 HIGH | 1 | Deferred |
| 🟡 MEDIUM | 2 | Deferred |
| 🟢 LOW | 5 | Deferred |
| **Total** | **8** | **Deferred** |

---

## Deferred Issues

### HIGH Priority

| ID | Description | Effort | Notes |
|----|-------------|--------|-------|
| PR5-#3 | Broad `except Exception` in integration tests hides failures | 🟢 LOW | Catch specific exceptions only |

### MEDIUM Priority

| ID | Description | Effort | Notes |
|----|-------------|--------|-------|
| PR5-#1 | Duplicate status_emoji dict in multiple functions | 🟢 LOW | Extract to shared constant |
| PR5-#5 | Missing CLI error path tests | 🟡 MEDIUM | Add tests for API error handling |

### LOW Priority

| ID | Description | Effort | Notes |
|----|-------------|--------|-------|
| PR5-#2 | Normalize scan directories in init | 🟡 MEDIUM | Path normalization |
| PR5-#4 | Missing exit code assertion in test | 🟢 LOW | Quick fix |
| PR5-#6 | Assert config file created after load | 🟢 LOW | Quick fix |
| PR5-#7 | Missing env precedence test | 🟡 MEDIUM | Edge case test |
| PR5-#8 | Typo in PR reference in docs | 🟢 LOW | Quick fix |

### Overall Comments

| ID | Description | Effort | Notes |
|----|-------------|--------|-------|
| PR5-OC1 | Status emoji mapping duplication | 🟢 LOW | Same as #1 |
| PR5-OC2 | URL consistency (grimm00 vs yourusername) | 🟢 LOW | Doc cleanup |

---

## Quick Wins Candidates

Low effort issues that could be batched:
- PR5-#3: Exception handling in tests
- PR5-#4: Exit code assertion
- PR5-#6: Config file assertion
- PR5-#8: Typo fix
- PR5-OC2: URL consistency

---

## References

- **Sourcery Review:** `docs/maintainers/feedback/sourcery/pr5.md`
- **PR:** https://github.com/grimm00/proj-cli/pull/5

---

**Last Updated:** 2025-12-17

