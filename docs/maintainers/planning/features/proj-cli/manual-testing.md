# Manual Testing Guide - proj-cli

**Feature:** proj-cli - Unified CLI Tool  
**Phases Covered:** Phase 2, Phase 3  
**Last Updated:** 2025-12-16  
**Status:** Active

---

## Overview

This guide provides step-by-step instructions for manually verifying the proj-cli feature. It covers all project management commands (Phase 2) and inventory management commands (Phase 3).

**Purpose:**
- Verify user-facing functionality works as expected
- Test edge cases and error handling
- Validate documentation and user experience

---

## Prerequisites

**General:**
- Python environment with `proj-cli` installed/available in PATH
- `proj --version` and `proj --help` work correctly

**For Project Commands (Phase 2):**
- work-prod API running on `localhost:5000`
- Test data available in work-prod database

**For Inventory Commands (Phase 3):**
- GitHub token (optional, for `scan github` command)
- Local projects directory (for `scan local` command)

**Start API (if needed):**
```bash
cd ~/Projects/work-prod/backend
flask run
```

---

## Phase 2: Project Commands

### Command Structure Verification

**Verified:** All 8 commands properly registered and showing help:

- `proj list` - List all projects with optional filters
- `proj get` - Get a project by ID
- `proj create` - Create a new project
- `proj update` - Update a project
- `proj delete` - Delete a project permanently
- `proj search` - Search projects by name or description
- `proj import-json` - Import projects from JSON file
- `proj archive` - Archive a project

---

### Test 2.1: List Command

```bash
# Basic list
proj list

# JSON format
proj list --format json

# Filter by status
proj list --status active

# Wide view (all columns)
proj list --wide

# Filter by organization
proj list --org work

# Filter by classification
proj list --class primary

# Search
proj list --search "test"

# Combined filters
proj list --status active --org work --wide
```

**Expected:**
- [ ] Table output shows projects correctly
- [ ] JSON output is valid JSON
- [ ] Filters work correctly
- [ ] Wide view shows all columns
- [ ] Search returns matching projects

---

### Test 2.2: Get Command

```bash
# Get project by ID (replace 1 with actual ID)
proj get 1

# JSON format
proj get 1 --format json
```

**Expected:**
- [ ] Project details displayed in table format
- [ ] JSON format shows all fields
- [ ] Error handling works for non-existent ID

---

### Test 2.3: Create Command

```bash
# Basic create
proj create "Test Project"

# With all options
proj create "Test Project" \
  --desc "Testing new CLI" \
  --status active \
  --org work \
  --class primary \
  --path /path/to/project \
  --url https://github.com/user/repo
```

**Expected:**
- [ ] Project created successfully
- [ ] Success message shows project ID and name
- [ ] All fields saved correctly
- [ ] Error handling for invalid data

---

### Test 2.4: Update Command

```bash
# Update status (replace <id> with actual ID)
proj update <id> --status paused

# Update multiple fields
proj update <id> --name "New Name" --desc "New Description"

# Update organization
proj update <id> --org new-org

# Update classification
proj update <id> --class secondary

# Update path
proj update <id> --path /new/path
```

**Expected:**
- [ ] Updates applied successfully
- [ ] Success message shows project ID
- [ ] Only provided fields updated
- [ ] Error handling for non-existent ID

---

### Test 2.5: Search Command

```bash
# Basic search
proj search "test"

# JSON format
proj search "test" --format json
```

**Expected:**
- [ ] Search returns matching projects
- [ ] Results displayed in table format
- [ ] JSON format works correctly
- [ ] Empty results show appropriate message

---

### Test 2.6: Archive Command

```bash
# Archive with confirmation (replace <id> with actual ID)
proj archive <id>

# Archive without confirmation
proj archive <id> --force
```

**Expected:**
- [ ] Confirmation prompt appears (without --force)
- [ ] Project archived successfully
- [ ] Success message shows project ID and name
- [ ] Project status set to completed
- [ ] Project classification set to archive

---

### Test 2.7: Delete Command

```bash
# Delete with confirmation (replace <id> with actual ID)
proj delete <id>

# Delete without confirmation
proj delete <id> --force
```

**Expected:**
- [ ] Confirmation prompt appears (without --force)
- [ ] Project deleted successfully
- [ ] Success message shows project ID
- [ ] Project no longer appears in list
- [ ] Error handling for non-existent ID

---

### Test 2.8: Import Command

```bash
# Import from JSON file (if available)
proj import-json ~/Projects/work-prod/scripts/projects.json

# Or create test JSON file
cat > /tmp/test-projects.json <<EOF
[
  {
    "name": "Imported Project 1",
    "status": "active",
    "description": "Test import"
  },
  {
    "name": "Imported Project 2",
    "status": "paused",
    "organization": "work"
  }
]
EOF
proj import-json /tmp/test-projects.json
```

**Expected:**
- [ ] Projects imported successfully
- [ ] Import statistics shown (imported, skipped, errors)
- [ ] Error handling for invalid JSON
- [ ] Error handling for invalid file path

---

### Phase 2: Error Handling Tests

#### Connection Error

```bash
# Stop API, then run any command
proj list
```

**Expected:**
- [ ] Rich panel error message displayed
- [ ] Helpful suggestions provided
- [ ] Error message mentions backend connection

#### Invalid Project ID

```bash
# Use non-existent ID
proj get 99999
proj update 99999 --name "Test"
proj delete 99999 --force
proj archive 99999 --force
```

**Expected:**
- [ ] 404 error handled gracefully
- [ ] Rich panel error message displayed
- [ ] Clear error message about resource not found

#### Invalid JSON Import

```bash
# Create invalid JSON
echo "invalid json" > /tmp/invalid.json
proj import-json /tmp/invalid.json
```

**Expected:**
- [ ] JSON decode error handled
- [ ] Clear error message about invalid JSON

---

## Phase 3: Inventory Commands

### Test 3.1: Inventory Command Group

**Test:** Verify `proj inv` command group exists

```bash
proj inv --help
```

**Expected:** Shows help with subcommands: `analyze`, `dedupe`, `status`, `scan`, `export`

---

### Test 3.2: Scan GitHub Command

**Test:** Scan GitHub repositories

```bash
proj inv scan github --user yourusername
```

**Expected:**
- [ ] Progress indicator shows scanning
- [ ] Repositories found and added to inventory
- [ ] Success message with count

**Note:** Requires GitHub token in config or environment variable

---

### Test 3.3: Scan Local Command

**Test:** Scan local project directories

```bash
proj inv scan local --dir ~/Projects
```

**Expected:**
- [ ] Progress indicator shows scanning
- [ ] Local projects found by markers (.git, package.json, etc.)
- [ ] Success message with count

---

### Test 3.4: Status Command

**Test:** Show inventory status

```bash
proj inv status
```

**Expected:**
- [ ] Table showing:
  - Total Projects
  - Data File path
  - File Exists status
  - GitHub Projects count
  - Local Projects count
  - Analyzed count
  - Top Languages (if analyzed)

---

### Test 3.5: Analyze Command

**Test:** Analyze tech stack

```bash
proj inv analyze
```

**Expected:**
- [ ] Progress indicator shows analyzing
- [ ] Languages detected (JavaScript, Python, Rust, Go)
- [ ] Frameworks detected (React, Vue, Express)
- [ ] Projects marked as analyzed
- [ ] Success message with analyzed count

---

### Test 3.6: Dedupe Command

**Test:** Deduplicate inventory entries

```bash
proj inv dedupe
```

**Expected:**
- [ ] Duplicates removed by remote_url or local_path
- [ ] Success message with removed count and remaining count

---

### Test 3.7: Export JSON Command

**Test:** Export inventory to JSON

```bash
proj inv export json /tmp/inventory.json
proj inv export json /tmp/inventory-raw.json --format raw
```

**Expected:**
- [ ] JSON file created at specified path
- [ ] Projects format: Transformed to work-prod project format
- [ ] Raw format: Original inventory data
- [ ] Success message with exported count

---

### Test 3.8: Export API Command

**Test:** Export inventory to work-prod API

```bash
# Dry run first
proj inv export api --dry-run

# Actual import
proj inv export api
```

**Expected:**
- [ ] Dry run: Shows preview of projects to import
- [ ] Actual import: Projects imported via API
- [ ] Success message with imported, skipped, and error counts

**Note:** Requires work-prod API running

---

### Phase 3: Complete Workflow Test

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

---

## Acceptance Criteria Checklist

### Phase 2: Project Commands

- [ ] `proj list` output matches (Rich tables)
- [ ] `proj list --wide` shows all columns
- [ ] `proj get` output matches
- [ ] `proj create` behavior matches
- [ ] `proj update` behavior matches
- [ ] `proj delete` behavior matches
- [ ] `proj search` output matches
- [ ] `proj archive` behavior matches
- [ ] `proj import-json` behavior matches
- [ ] Error messages are helpful (Rich panels)
- [ ] Help text is clear

### Phase 3: Inventory Commands

- [ ] `proj inv --help` shows command group
- [ ] `proj inv scan github` functional
- [ ] `proj inv scan local` functional
- [ ] `proj inv status` functional
- [ ] `proj inv analyze` functional
- [ ] `proj inv dedupe` functional
- [ ] `proj inv export json` functional
- [ ] `proj inv export api` functional
- [ ] Complete workflow passes

---

## Test Results

**Date:** _______________  
**Tester:** _______________  
**API Version:** _______________  
**CLI Version:** _______________

### Results Summary

- [ ] All Phase 2 integration tests passing
- [ ] All Phase 2 error handling tests passing
- [ ] All Phase 3 inventory tests passing
- [ ] Feature parity verified
- [ ] Ready for Phase 4

### Issues Found

(Record any issues or discrepancies here)

---

## Notes

- All commands handle empty inventory gracefully
- Error handling works correctly for API errors
- Progress indicators provide good user feedback
- File operations use UTF-8 encoding
- Commands follow consistent patterns

---

## Change History

| Date | Phase | Changes |
|------|-------|---------|
| 2025-12-17 | Phase 2 | Initial Phase 2 test scenarios added |
| 2025-12-16 | Phase 3 | Phase 3 inventory command tests added |

---

**Last Updated:** 2025-12-16

