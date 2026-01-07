# Fix Plan: PR #12 Batch HIGH LOW - 01

**PR:** #12  
**Batch:** high-low-01  
**Priority:** 🟠 HIGH  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-06  
**Completed:** 2026-01-06  
**PR:** #15  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR12-#1 | 🟠 HIGH | 🟡 MEDIUM | 🟢 LOW | Empty templates check in prompt |

---

## Overview

This batch contains 1 HIGH priority issue with LOW effort. This issue addresses a UX bug where `prompt_for_create_options` could prompt the user to select from an empty templates list.

**Estimated Time:** 30-45 minutes  
**Files Affected:** `src/proj/commands/projects.py`

---

## Issue Details

### Issue PR12-#1: Empty Templates Check

**Location:** `src/proj/commands/projects.py:64-73`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟠 HIGH | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
`prompt_for_create_options` passes `available = list_templates(templates_source)` directly to `Prompt.ask` as `choices`. If `available` is empty, this will prompt the user to select from no options, likely causing an error or confusing UX. Consider explicitly handling the empty case by either failing with a clear message or skipping the template question and using a non-template flow.

**Current Code:**

```python
# List available templates
templates_source = get_templates_source(config)
available = list_templates(templates_source)
default_template = (
    config.templates.default if hasattr(config, 'templates') and
    hasattr(config.templates, 'default') else None
)
template = Prompt.ask(
    "Template type",
    choices=available,
    # ...
)
```

**Proposed Solution:**

```python
# List available templates
templates_source = get_templates_source(config)
available = list_templates(templates_source)

if not available:
    console.print("[red]Error:[/red] No templates available.")
    console.print(f"[dim]Templates source: {templates_source}[/dim]")
    raise typer.Exit(1)

default_template = (
    config.templates.default if hasattr(config, 'templates') and
    hasattr(config.templates, 'default') else None
)
template = Prompt.ask(
    "Template type",
    choices=available,
    # ...
)
```

---

## Implementation Steps

1. **PR12-#1: Empty Templates Check**
   - [x] Add check for empty `available` list after `list_templates()` call
   - [x] Print clear error message with templates source path
   - [x] Exit with code 1 (error)
   - [x] Add test: `test_prompt_for_create_options_no_templates_available`

---

## Testing

- [x] All existing tests pass
- [x] New test added for empty templates case
- [x] Test improved with message assertions (PR15-#1)
- [x] Manual testing: verify error message is clear
- [x] No regressions introduced

---

## Files to Modify

- `src/proj/commands/projects.py` - Add empty check in `prompt_for_create_options`
- `tests/test_commands_projects.py` - Add test for empty templates case

---

## Definition of Done

- [x] Empty templates case handled with clear error
- [x] Tests passing
- [x] Code reviewed (PR15 Sourcery review addressed)
- [x] Ready for PR

---

**Batch Rationale:**
This is the only HIGH priority issue, warranting its own batch for immediate attention. It's a UX bug that could confuse users.

