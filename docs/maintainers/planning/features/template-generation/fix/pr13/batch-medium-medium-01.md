# Fix Plan: PR #13 Batch MEDIUM MEDIUM - 01

**PR:** #13  
**Batch:** medium-medium-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟡 MEDIUM  
**Status:** ✅ Complete  
**Created:** 2026-01-06  
**Completed:** 2026-01-06  
**Merged:** PR #16 (Fix PR #2)  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR13-Overall-#2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟡 MEDIUM | Requirements count reconciliation across docs |

---

## Overview

This batch contains 1 MEDIUM priority issue with MEDIUM effort. This issue addresses inconsistent requirement counts across planning and requirements documents.

**Estimated Time:** 1-2 hours  
**Files Affected:** Multiple planning documents

---

## Issue Details

### Issue PR13-Overall-#2: Requirements Count Reconciliation

**Location:** Multiple planning documents  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟡 MEDIUM

**Description:**
The requirements counts and breakdown (e.g., totals of 22 FR vs 23 items in some tables, and 30 overall in the PR description) appear inconsistent across the planning and requirements documents; it would help to reconcile these numbers so a reader can clearly see a single source of truth for how many requirements exist and which are verified.

**Files to Check:**
- `docs/maintainers/planning/features/template-generation/phase-5.md`
- `docs/maintainers/planning/features/template-generation/requirements.md` (if exists)
- PR descriptions mentioning requirement counts
- Any other planning docs with FR counts

**Proposed Solution:**
1. Audit all documents for requirement counts
2. Establish single source of truth (likely `requirements.md` or a dedicated section)
3. Update all references to point to or match the source
4. Add note about where authoritative count lives

---

## Implementation Steps

1. **Audit Documents**
   - [ ] Find all documents mentioning requirement counts
   - [ ] List discrepancies found
   - [ ] Identify which count is correct

2. **Reconcile Counts**
   - [ ] Update phase-5.md requirement summary
   - [ ] Update any other affected documents
   - [ ] Ensure FR categories (CREATE, CONFIG, TMPL, REG, Port) are consistent

3. **Add Source of Truth Note**
   - [ ] Document where authoritative count lives
   - [ ] Add cross-references as needed

---

## Testing

- [ ] All requirement counts are consistent
- [ ] Single source of truth is clear
- [ ] No broken cross-references

---

## Files to Modify

- `docs/maintainers/planning/features/template-generation/phase-5.md` - Main reconciliation
- Other planning docs as discovered during audit

---

## Definition of Done

- [ ] All requirement counts match across documents
- [ ] Source of truth is documented
- [ ] No inconsistencies remain
- [ ] Ready for PR

---

**Batch Rationale:**
Single MEDIUM/MEDIUM issue that requires auditing multiple documents. Better done as focused task than piecemeal.

