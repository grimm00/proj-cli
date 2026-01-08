# Bug Fix: Local Path Field Mismatch

**Bug ID:** BUG-001  
**Priority:** 🟠 HIGH  
**Effort:** 🟢 LOW  
**Status:** ✅ Fixed  
**Created:** 2026-01-08  
**Fixed:** 2026-01-08  
**Discovered By:** Manual testing with `proj list`

---

## 🐛 Bug Description

When exporting inventory to work-prod API, all `path` data is lost because proj-cli sends `local_path` but the work-prod API expects `path`.

**Symptoms:**
- `proj list` shows empty Path column for all projects
- Projects imported from inventory scan have no path information in work-prod

**Root Cause:**
Field name mismatch between proj-cli and work-prod:
- **proj-cli sends:** `local_path`
- **work-prod expects:** `path`

---

## 📍 Affected Code

**File:** `src/proj/commands/inventory.py`

**Location 1 - Line 489 (`export_json` function):**
```python
project = {
    "name": item.get("name", ""),
    "description": item.get("description", ""),
    "remote_url": item.get("remote_url", ""),
    "local_path": item.get("local_path", ""),  # BUG: Should be "path"
    "status": "active",
}
```

**Location 2 - Line 563 (`export_api` function):**
```python
project = {
    "name": item.get("name", ""),
    "description": item.get("description", ""),
    "remote_url": item.get("remote_url", ""),
    "local_path": item.get("local_path", ""),  # BUG: Should be "path"
    "status": "active",
}
```

---

## ✅ Fix

Change `"local_path"` key to `"path"` in both locations (keep reading from `local_path` internally):

**Fixed code (both locations):**
```python
project = {
    "name": item.get("name", ""),
    "description": item.get("description", ""),
    "remote_url": item.get("remote_url", ""),
    "path": item.get("local_path", ""),  # Fixed: send as "path" to match work-prod API
    "status": "active",
}
```

---

## 📝 Implementation Steps

1. [x] Identify all occurrences of field mismatch
2. [x] Fix `export_json` function (line 489)
3. [x] Fix `export_api` function (line 563)
4. [x] Run existing tests to verify no regressions (9 tests pass)
5. [ ] Add/update tests for export functions (optional - defer to future)
6. [x] Manual test: `proj inv export json` verifies `path` field populated correctly

---

## 🧪 Testing

### Existing Tests to Verify
- [ ] `tests/commands/test_inventory.py` - export functions

### Manual Test Steps
1. Run `proj inv scan local`
2. Run `proj inv export api`
3. Run `proj list` - verify Path column populated
4. Run `proj get <id>` - verify path field has value

---

## 🔗 Related

- **Discovery:** Manual investigation while reviewing work-prod integration gaps
- **Research Topic:** [Research Topic 8: Field Name Consistency](../../../../../../explorations/work-prod-integration/research-topics.md)
- **work-prod API:** `backend/app/api/projects.py` - expects `path` field

---

## 📊 Impact

**Without fix:**
- All path information lost when syncing to work-prod
- No ability to track local project locations in work-prod
- Reduced usefulness for project management

**With fix:**
- Path data properly synced to work-prod
- `proj list` shows accurate path information
- Full project tracking capability restored

---

**Last Updated:** 2026-01-08

