# Fix Plan: PR #14 Batch HIGH LOW - 01

**PR:** #14  
**Batch:** high-low-01  
**Priority:** 🟠 HIGH  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-06  
**Completed:** 2026-01-06  
**PR:** #15 (combined with pr12-batch-high-low-01)  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR14-#1 | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW | Sanitize error messages in sync_to_api |

---

## Overview

This batch contains 1 HIGH priority security issue with LOW effort. Raw exception messages are being exposed to users which could reveal backend details.

**Estimated Time:** 30 minutes  
**Files Affected:** `src/proj/commands/projects.py`

---

## Issue Details

### Issue PR14-#1: Sanitize Error Messages (Security)

**Location:** `src/proj/commands/projects.py:43-52`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟠 HIGH | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`f"[yellow]⚠ Could not sync to API: {e}[/yellow]"` will surface the raw exception string to users. Depending on how `APIError`/`BackendConnectionError` are built, this may reveal internal URLs, payloads, or other backend details. Prefer logging the full exception at a debug/logging level and showing a generic, user-friendly error here.

**Current Code:**

```python
except (APIError, BackendConnectionError, TimeoutError) as e:
    if console:
        console.print(
            f"[yellow]⚠ Could not sync to API: {e}[/yellow]"
        )
    return None
```

**Proposed Solution:**

```python
import logging

logger = logging.getLogger(__name__)

except (APIError, BackendConnectionError, TimeoutError) as e:
    # Log full exception for debugging
    logger.debug(f"API sync failed: {e}", exc_info=True)
    
    if console:
        # Show user-friendly message without internal details
        console.print(
            "[yellow]⚠ Could not sync to API. Project created locally.[/yellow]"
        )
    return None
```

---

## Implementation Steps

1. **PR14-#1: Sanitize Error Messages**
   - [x] Add logging import if not present
   - [x] Create logger instance for module
   - [x] Log full exception at debug level
   - [x] Replace user-facing message with generic text
   - [x] Add test to verify no exception details leaked

---

## Testing

- [ ] All existing tests pass
- [ ] Test verifies user message doesn't contain exception details
- [ ] Manual testing: trigger API error, verify message is sanitized
- [ ] No regressions introduced

---

## Files to Modify

- `src/proj/commands/projects.py` - Sanitize error output in `sync_to_api`

---

## Definition of Done

- [x] Error messages sanitized
- [x] Full exception logged at debug level
- [x] Tests passing
- [ ] Code reviewed
- [x] Ready for PR

---

**Batch Rationale:**
Security issue that should be addressed promptly. Simple fix with low effort.

