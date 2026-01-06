# PR #12 Fix Tracking

**PR:** Phase 4 - Create Command Extension  
**Merged:** 2026-01-06  
**Status:** 🟠 Partial (2/4 batches complete)  
**Last Updated:** 2026-01-06

---

## 📋 Quick Links

### Fix Batches

| Batch                                         | Priority  | Effort  | Issues | Status              |
| --------------------------------------------- | --------- | ------- | ------ | ------------------- |
| [batch-high-low-01](batch-high-low-01.md)     | 🟠 HIGH   | 🟢 LOW  | 1      | ✅ Complete (PR #15) |
| [batch-medium-low-01](batch-medium-low-01.md) | 🟡 MEDIUM | 🟢 LOW  | 1      | ✅ Complete (PR #16) |
| [batch-low-low-01](batch-low-low-01.md)       | 🟢 LOW    | 🟢 LOW  | 4      | 🔴 Not Started      |
| [batch-low-high-01](batch-low-high-01.md)     | 🟢 LOW    | 🟠 HIGH | 1      | 🔴 Not Started      |

### Individual Issues

| ID  | Issue                                                                          | Priority  | Effort | Status         |
| --- | ------------------------------------------------------------------------------ | --------- | ------ | -------------- |
| 1   | [Learning project placeholder not replaced](./issue-1-learning-placeholder.md) | 🟡 MEDIUM | 🟢 LOW | 🔴 Not Started |

### Source

- **[PR #12 Sourcery Review](../../../../feedback/sourcery/pr12.md)** - Code review analysis

---

## 📊 Summary

**From Sourcery Review (7 issues):**

| Priority  | Count | Batched                                     |
| --------- | ----- | ------------------------------------------- |
| 🟠 HIGH   | 1     | batch-high-low-01                           |
| 🟡 MEDIUM | 1     | batch-medium-low-01                         |
| 🟢 LOW    | 5     | batch-low-low-01 (4), batch-low-high-01 (1) |

**From Manual Testing:**

- 1 bug found during manual testing (issue-1-learning-placeholder)

**Totals:**

- **8 issues** total
- **4 batches** + 1 individual issue
- **Estimated effort:** ~5-6 hours total

---

## 🎯 Recommended Order

1. **batch-high-low-01** (HIGH/LOW) - Empty templates check (~30 min)
2. **batch-medium-low-01** (MEDIUM/LOW) - Dry-run validation (~30 min)
3. **batch-low-low-01** (LOW/LOW) - Test improvements (~1 hr)
4. **issue-1-learning-placeholder** (MEDIUM/LOW) - Manual testing bug (~30 min)
5. **batch-low-high-01** (LOW/HIGH) - Refactor (defer to code quality sprint)

---

## 📁 Batch Details

### batch-high-low-01: Empty Templates Handling

- **Issue:** #1 - Interactive prompting doesn't handle empty templates list
- **Impact:** UX bug - confusing error when no templates available
- **Fix:** Add explicit check and clear error message

### batch-medium-low-01: Dry-Run Validation

- **Issue:** #2 - Dry-run bypasses flag conflict validation
- **Impact:** `--dry-run --api-only --local-only` succeeds but real run fails
- **Fix:** Call validation in dry-run path

### batch-low-low-01: Test Improvements & Cleanup

- **Issues:** #3, #4, #5, Overall-1
- **Impact:** Better test coverage, cleaner code
- **Fix:** Add tests for precedence, dry-run prompts, implicit API; remove unused param

### batch-low-high-01: Refactor create_project

- **Issue:** Overall-2 - Function too large and branchy
- **Impact:** Maintainability improvement
- **Fix:** Extract mode-specific helpers (defer to dedicated sprint)

---

**Last Updated:** 2026-01-06  
**Action Plan:** HIGH priority complete (PR #15), continue with MEDIUM/LOW batches, defer LOW/HIGH to code quality sprint
