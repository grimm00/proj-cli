# Phase 2 - Manual Testing Guide

**Phase:** Phase 2 - Migrate Project Commands  
**Status:** 🟡 Ready for Testing  
**Last Updated:** 2025-12-17

---

## 📋 Prerequisites

- [ ] work-prod API running on `localhost:5000`
- [ ] `proj-cli` installed/available in PATH
- [ ] Test data available in work-prod database

**Start API:**
```bash
cd ~/Projects/work-prod/backend
flask run
```

---

## ✅ Command Structure Verification

**Verified:** All 8 commands properly registered and showing help:

- ✅ `proj list` - List all projects with optional filters
- ✅ `proj get` - Get a project by ID
- ✅ `proj create` - Create a new project
- ✅ `proj update` - Update a project
- ✅ `proj delete` - Delete a project permanently
- ✅ `proj search` - Search projects by name or description
- ✅ `proj import-json` - Import projects from JSON file
- ✅ `proj archive` - Archive a project

---

## 🧪 Integration Tests

### Test 1: List Command

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

### Test 2: Get Command

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

### Test 3: Create Command

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

### Test 4: Update Command

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

### Test 5: Search Command

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

### Test 6: Archive Command

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

### Test 7: Delete Command

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

### Test 8: Import Command

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

## 🔍 Error Handling Tests

### Connection Error

```bash
# Stop API, then run any command
proj list
```

**Expected:**
- [ ] Rich panel error message displayed
- [ ] Helpful suggestions provided
- [ ] Error message mentions backend connection

### Invalid Project ID

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

### Invalid JSON Import

```bash
# Create invalid JSON
echo "invalid json" > /tmp/invalid.json
proj import-json /tmp/invalid.json
```

**Expected:**
- [ ] JSON decode error handled
- [ ] Clear error message about invalid JSON

---

## ✅ Feature Parity Checklist

Compare with original work-prod CLI:

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
- [ ] Help text is clear and matches original

---

## 📝 Test Results

**Date:** _______________  
**Tester:** _______________  
**API Version:** _______________  
**CLI Version:** _______________

### Results Summary

- [ ] All integration tests passing
- [ ] All error handling tests passing
- [ ] Feature parity verified
- [ ] Ready for Phase 3

### Issues Found

(Record any issues or discrepancies here)

---

**Last Updated:** 2025-12-17

