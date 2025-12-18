# PR #3 - Phase 3: Add Inventory Commands

**PR:** #3  
**Phase:** 3 - Add Inventory Commands  
**Merged:** 2025-12-17  
**Status:** ✅ Complete

---

## 📋 Deferred Issues

**Date:** 2025-12-17  
**Review:** PR #3 Sourcery feedback + User manual testing  
**Status:** 🟡 **DEFERRED** - MEDIUM/LOW priority items for Phase 4

### Sourcery Review Issues

| ID | Description | Priority | Effort | Notes |
|----|-------------|----------|--------|-------|
| PR3-#2 | Depth-limited traversal for scan_local | 🟡 MEDIUM | 🟠 HIGH | Performance optimization - requires glob rewrite |
| PR3-#3 | Defensive JSON parsing for inventory.json | 🟡 MEDIUM | 🟢 LOW | Handle corrupted files gracefully |
| PR3-#5 | Missing tests for scan_github behavior | 🟡 MEDIUM | 🟠 HIGH | Config usage, pagination, error handling |
| PR3-#6 | Missing tests for scan_local discovery | 🟡 MEDIUM | 🟠 HIGH | Markers, depth, git remote detection |
| PR3-#7 | Missing tests for export_json/api output | 🟡 MEDIUM | 🟠 HIGH | Validate file structure |
| PR3-#8 | Missing tests for status/analyze/dedupe | 🟡 MEDIUM | 🟠 HIGH | Inventory mutation tests |
| Overall | Dedupe logic docs alignment | 🟢 LOW | 🟢 LOW | Align implementation and plan docs |

### Fixed in PR #3

| ID | Description | Priority | Action |
|----|-------------|----------|--------|
| PR3-#1 | Add timeout to GitHub API requests | 🟠 HIGH | ✅ Fixed - Added `timeout=15` |
| PR3-#4 | Validate --format option | 🟠 HIGH | ✅ Fixed - Used `click.Choice` |
| Overall | Duplicate imports in export_api | 🟢 LOW | ✅ Fixed - Removed redundant imports |

### User Feedback Issues (Fixed)

| ID | Description | Severity | Action |
|----|-------------|----------|--------|
| U1 | `--wide` option missing from `search` | 🟡 MEDIUM | ✅ Fixed - Added option |
| U2 | Progress indicator ordering in analyze | 🟢 LOW | ✅ Fixed - Moved output outside Progress |
| U3 | Duplicates after export api | 🟠 HIGH | ✅ Fixed - Auto-dedupe with `--no-dedupe` |
| U4 | Subdirectories scanned as projects | 🟠 HIGH | ✅ Fixed - Skip subdirs in git repos |

---

## 📝 Deferred Enhancements

These are new enhancements identified during Phase 3 for future work:

### D1: Smart Dedupe with Field Merging

**Priority:** 🟡 MEDIUM  
**Component:** `proj inv dedupe`

When dedupe finds duplicates from different sources (GitHub + local), it should merge the records instead of dropping one.

### D2: Multi-Directory Scan Configuration

**Priority:** 🟢 LOW  
**Component:** `proj inv scan local`

Support config-driven multi-directory scanning with per-directory depth settings.

### D3: Exclusion Patterns for Scan

**Priority:** 🟢 LOW  
**Component:** `proj inv scan local`

Add `--exclude` option for pattern-based directory exclusion.

---

## 📊 Summary

| Category | Count |
|----------|-------|
| Sourcery Issues (Deferred) | 7 |
| Sourcery Issues (Fixed) | 3 |
| User Feedback (Fixed) | 4 |
| New Enhancements (Deferred) | 3 |

**Action Plan:** Deferred items will be addressed in Phase 4 or future PRs. Test coverage improvements have HIGH effort due to need for mocking and temp directory fixtures.

---

**Last Updated:** 2025-12-17

