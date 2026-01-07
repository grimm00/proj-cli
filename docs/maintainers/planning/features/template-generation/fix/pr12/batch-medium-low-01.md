# Fix Plan: PR #12 Batch MEDIUM LOW - 01

**PR:** #12  
**Batch:** medium-low-01  
**Priority:** 🟡 MEDIUM  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-06  
**Completed:** 2026-01-06  
**Merged:** PR #16 (Fix PR #2)  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-#2 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Dry-run bypasses validation |

---

## Overview

This batch contains 1 MEDIUM priority issue with LOW effort. This issue addresses an edge case where `--dry-run` mode skips mode-specific validation checks.

**Estimated Time:** 30-45 minutes  
**Files Affected:** `src/proj/commands/projects.py`

---

## Issue Details

### Issue PR12-#2: Dry-Run Validation Bypass

**Location:** `src/proj/commands/projects.py:383-392`  
**Sourcery Comment:** Comment #2  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Because the dry-run branch returns before `detect_create_mode` runs, it skips the `api_only && local_only` conflict check and the `local-only` + `--template` requirement, so mode-specific validation is not mirrored. For instance, `--dry-run --api-only --local-only` currently succeeds but would fail without `--dry-run`. Consider either calling `detect_create_mode` in dry-run, or at least duplicating the conflict checks there so dry-run reliably indicates whether a real run would be valid.

**Current Behavior:**
- `proj create test --dry-run --api-only --local-only` → Succeeds (shows preview)
- `proj create test --api-only --local-only` → Fails (conflict error)

**Proposed Solution:**
Call `detect_create_mode` in dry-run path to validate flags before showing preview:

```python
# Handle dry-run mode (preview without side effects)
if dry_run:
    # Still validate mode conflicts
    detect_create_mode(config, template, api_only, local_only)
    
    console.print("[bold cyan]DRY RUN MODE[/bold cyan]")
    # ... rest of dry-run preview
```

---

## Implementation Steps

1. **PR12-#2: Dry-Run Validation**
   - [ ] Move `detect_create_mode` call before dry-run check
   - [ ] Or add validation call inside dry-run branch
   - [ ] Add test: `test_create_dry_run_validates_flag_conflicts`

---

## Testing

- [ ] All existing tests pass
- [ ] New test added for dry-run flag conflict validation
- [ ] Manual testing: verify `--dry-run --api-only --local-only` fails
- [ ] No regressions introduced

---

## Files to Modify

- `src/proj/commands/projects.py` - Add validation in dry-run path
- `tests/test_create_dry_run.py` - Add test for flag conflict in dry-run

---

## Definition of Done

- [ ] Dry-run validates flag conflicts same as real run
- [ ] Tests passing
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
Single MEDIUM priority issue that ensures dry-run behavior matches real execution for validation.

