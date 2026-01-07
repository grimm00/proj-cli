# PR #14 Fix Tracking

**PR:** #14 - Phase 6: API Sync Enhancement  
**Merged:** 2026-01-06  
**Status:** 🟠 Partial (2/4 batches complete)  
**Last Updated:** 2026-01-06

---

## 📋 Quick Links

### Fix Batches

| Batch | Priority | Effort | Issues | Status |
|-------|----------|--------|--------|--------|
| [batch-high-low-01](batch-high-low-01.md) | 🟠 HIGH | 🟢 LOW | 1 | ✅ Complete (PR #15) |
| [batch-medium-low-01](batch-medium-low-01.md) | 🟡 MEDIUM | 🟢 LOW | 2 | ✅ Complete (PR #16) |
| [batch-low-low-01](batch-low-low-01.md) | 🟢 LOW | 🟢 LOW | 2 | 🔴 Not Started |
| [batch-low-medium-01](batch-low-medium-01.md) | 🟢 LOW | 🟡 MEDIUM | 1 | 🔴 Not Started |

### Source

- **[PR #14 Sourcery Review](../../../../feedback/sourcery/pr14.md)** - Code review analysis
- [PR #14 on GitHub](https://github.com/grimm00/proj-cli/pull/14)
- [Phase 6 Document](../../phase-6.md)

---

## 📊 Summary

**From Sourcery Review (6 issues):**

| Priority | Count | Batched |
|----------|-------|---------|
| 🟠 HIGH | 1 | batch-high-low-01 |
| 🟡 MEDIUM | 2 | batch-medium-low-01 |
| 🟢 LOW | 3 | batch-low-low-01 (2), batch-low-medium-01 (1) |

**Totals:**
- **6 issues** batched
- **4 batches** created
- **Estimated effort:** ~3 hours total

---

## 🎯 Recommended Order

1. **batch-high-low-01** (HIGH/LOW) - Security: sanitize error messages (~30 min)
2. **batch-medium-low-01** (MEDIUM/LOW) - Edge case + exception handling (~45 min)
3. **batch-low-low-01** (LOW/LOW) - Test output assertions (~30 min)
4. **batch-low-medium-01** (LOW/MEDIUM) - Test fixture refactoring (~1-1.5 hrs)

---

## 📁 Batch Details

### batch-high-low-01: Sanitize Error Messages (Security)
- **Issue:** #1 - Raw exception messages exposed to users
- **Impact:** Security - could reveal backend details
- **Fix:** Log exceptions at debug level, show generic user message

### batch-medium-low-01: Edge Cases + Exception Handling
- **Issues:** #4, Overall #1
- **Impact:** Code quality and test coverage
- **Fix:** Add missing id tests, narrow except clause

### batch-low-low-01: Test Output Assertions
- **Issues:** #2, #3
- **Impact:** Test quality - verify user-facing messages
- **Fix:** Add output assertions to existing tests

### batch-low-medium-01: Test Fixture Refactoring
- **Issue:** Overall #2
- **Impact:** Test maintainability - reduce duplication
- **Fix:** Extract shared setup into fixtures

---

## 📝 Notes

- Phase 6 was identified as scope creep during implementation
- API integration concerns separated into exploration for future dedicated design work
- See: `docs/maintainers/planning/explorations/work-prod-integration/`

---

**Last Updated:** 2026-01-06  
**Status:** 🟠 Partial (2/4 batches complete)  
**Action Plan:** HIGH and MEDIUM priority batches complete (PR #15, PR #16), continue with LOW batches when convenient
