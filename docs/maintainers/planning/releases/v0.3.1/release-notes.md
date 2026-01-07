# Release Notes - v0.3.1

**Release Date:** TBD
**Status:** 🔴 Draft
**Type:** Patch Release

---

## What's New

This is a patch release focused on code quality improvements based on Sourcery review feedback from PR #21.

---

## Improvements

### Code Quality

- **Centralized Constants:** Created `src/proj/constants.py` with `VALID_PROJECT_TYPES` and `PROJECT_TYPE_HELP` to avoid duplication between API client and CLI
- **Custom Exception:** Added `InvalidProjectTypeError` exception for safer project type validation (instead of catching all `ValueError`)
- **Better Test Assertions:** Strengthened test assertions to verify error message formatting

### Technical Changes

- New file: `src/proj/constants.py` - Shared constants for project types
- Updated: `src/proj/error_handler.py` - Added `InvalidProjectTypeError` class
- Updated: `src/proj/api_client.py` - Uses centralized constants and custom exception
- Updated: `src/proj/commands/projects.py` - Uses centralized help text and catches specific exception
- Updated: `tests/test_commands_projects.py` - Improved test assertions

---

## Bug Fixes

None - this is a code quality improvement release.

---

## Breaking Changes

None - all changes are backward compatible.

---

## Technical Details

### Changes Summary

- **Files Changed:** 5
- **Tests Updated:** 3
- **New Files:** 1 (`constants.py`)

### Key PRs

- PR #23: Centralize project type constants and add custom exception

---

## Known Issues

None.

---

**Last Updated:** 2026-01-07
**Previous Release:** v0.3.0

