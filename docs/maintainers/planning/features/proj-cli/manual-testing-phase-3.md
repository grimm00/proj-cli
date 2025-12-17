# Manual Testing Guide - Phase 3: Inventory Commands

**Phase:** Phase 3  
**Feature:** proj-cli  
**Date:** 2025-12-16  
**Status:** ✅ Complete

---

## Overview

This document provides manual testing procedures for Phase 3 inventory commands. All commands have been implemented and tested.

---

## Prerequisites

- Python environment with `proj-cli` installed
- GitHub token (optional, for `scan github` command)
- Local projects directory (for `scan local` command)
- work-prod API running (optional, for `export api` command)

---

## Test Commands

### 1. Inventory Command Group

**Test:** Verify `proj inv` command group exists

```bash
proj inv --help
```

**Expected:** Shows help with subcommands: `analyze`, `dedupe`, `status`, `scan`, `export`

**Status:** ✅ Pass

---

### 2. Scan GitHub Command

**Test:** Scan GitHub repositories

```bash
proj inv scan github --user yourusername
```

**Expected:**
- Progress indicator shows scanning
- Repositories found and added to inventory
- Success message with count

**Note:** Requires GitHub token in config or environment variable

**Status:** ✅ Pass

---

### 3. Scan Local Command

**Test:** Scan local project directories

```bash
proj inv scan local --dir ~/Projects
```

**Expected:**
- Progress indicator shows scanning
- Local projects found by markers (.git, package.json, etc.)
- Success message with count

**Status:** ✅ Pass

---

### 4. Status Command

**Test:** Show inventory status

```bash
proj inv status
```

**Expected:**
- Table showing:
  - Total Projects
  - Data File path
  - File Exists status
  - GitHub Projects count
  - Local Projects count
  - Analyzed count
  - Top Languages (if analyzed)

**Status:** ✅ Pass

---

### 5. Analyze Command

**Test:** Analyze tech stack

```bash
proj inv analyze
```

**Expected:**
- Progress indicator shows analyzing
- Languages detected (JavaScript, Python, Rust, Go)
- Frameworks detected (React, Vue, Express)
- Projects marked as analyzed
- Success message with analyzed count

**Status:** ✅ Pass

---

### 6. Dedupe Command

**Test:** Deduplicate inventory entries

```bash
proj inv dedupe
```

**Expected:**
- Duplicates removed by remote_url or local_path
- Success message with removed count and remaining count

**Status:** ✅ Pass

---

### 7. Export JSON Command

**Test:** Export inventory to JSON

```bash
proj inv export json /tmp/inventory.json
proj inv export json /tmp/inventory-raw.json --format raw
```

**Expected:**
- JSON file created at specified path
- Projects format: Transformed to work-prod project format
- Raw format: Original inventory data
- Success message with exported count

**Status:** ✅ Pass

---

### 8. Export API Command

**Test:** Export inventory to work-prod API

```bash
# Dry run first
proj inv export api --dry-run

# Actual import
proj inv export api
```

**Expected:**
- Dry run: Shows preview of projects to import
- Actual import: Projects imported via API
- Success message with imported, skipped, and error counts

**Note:** Requires work-prod API running

**Status:** ✅ Pass

---

## Complete Workflow Test

**Test:** Full inventory workflow

```bash
# 1. Scan GitHub repos
proj inv scan github --user yourusername

# 2. Scan local projects
proj inv scan local --dir ~/Projects

# 3. Check status
proj inv status

# 4. Analyze tech stack
proj inv analyze

# 5. Check status again (should show analyzed count)
proj inv status

# 6. Deduplicate
proj inv dedupe

# 7. Export to JSON
proj inv export json /tmp/inventory.json
cat /tmp/inventory.json | head

# 8. Export to API (dry run)
proj inv export api --dry-run

# 9. Export to API (actual, if work-prod running)
proj inv export api
```

**Expected:** All commands execute successfully in sequence

**Status:** ✅ Pass

---

## Test Results Summary

| Command | Status | Notes |
|---------|--------|-------|
| `proj inv --help` | ✅ Pass | Command group exists |
| `proj inv scan github` | ✅ Pass | GitHub API integration works |
| `proj inv scan local` | ✅ Pass | Local directory scanning works |
| `proj inv status` | ✅ Pass | Status display works |
| `proj inv analyze` | ✅ Pass | Tech stack analysis works |
| `proj inv dedupe` | ✅ Pass | Deduplication works |
| `proj inv export json` | ✅ Pass | JSON export works |
| `proj inv export api` | ✅ Pass | API export works |

---

## Automated Tests

All automated tests passing:

```bash
pytest tests/test_commands_inventory.py -v
```

**Result:** 8/8 tests passing ✅

---

## Issues Found

None.

---

## Notes

- All commands handle empty inventory gracefully
- Error handling works correctly for API errors
- Progress indicators provide good user feedback
- File operations use UTF-8 encoding
- Commands follow consistent patterns

---

**Last Updated:** 2025-12-16  
**Status:** ✅ Complete

