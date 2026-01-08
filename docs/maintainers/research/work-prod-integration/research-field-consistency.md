# Research: Field Name Consistency

**Research Topic:** Work-Prod Integration  
**Question:** How should we standardize field names between proj-cli and work-prod?  
**Status:** ✅ Complete  
**Priority:** 🔴 High  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08  
**Completed:** 2026-01-08

---

## 🎯 Research Question

How should we standardize field names between proj-cli and work-prod?

**Bug Discovered (FIXED):** Inventory export used `local_path` but API expected `path`. This caused all path data to be lost during API import.

---

## ✅ Immediate Bug Fix (Complete)

**Issue:** Export sends `local_path` but work-prod API expects `path`  
**Location:** `proj-cli/src/proj/commands/inventory.py` lines 489, 563  
**Fix:** Changed `"local_path"` to `"path"` in both export_json and export_api functions  
**Commit:** `49fae4f fix(inventory): use 'path' field name to match work-prod API (BUG-001)`

---

## 🔍 Research Goals

- [x] Goal 1: Audit all field names in proj-cli vs work-prod API
- [x] Goal 2: Decide on consistent naming convention (snake_case, camelCase)
- [x] Goal 3: Identify fields that exist in one system but not the other
- [x] Goal 4: Design mapping strategy for non-matching fields

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase analysis: proj-cli inventory export schema
- [x] Codebase analysis: work-prod API endpoint schemas
- [x] API documentation: work-prod OpenAPI spec (`backend/openapi.yaml`)
- [x] Web search: API field naming conventions and best practices

---

## 🔑 Sub-Questions

1. **Standard Name:** Should we standardize on `path` or `local_path` internally?
2. **Other Inconsistencies:** What other field inconsistencies exist?
3. **Schema Alignment:** Should inventory JSON schema match work-prod API schema exactly?
4. **Extra Fields:** How do we handle fields that exist in inventory but not API (e.g., `languages`, `marker`)?

---

## 📊 Findings

### Finding 1: Complete Field Mapping Audit

**work-prod API Project Schema** (from OpenAPI spec):

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `id` | integer | Yes | Auto-generated |
| `name` | string | Yes | Max 200 chars |
| `path` | string | No | Unique, max 500 chars |
| `organization` | string | No | Max 100 chars |
| `classification` | enum | No | primary, secondary, archive, maintenance |
| `status` | enum | Yes | active, paused, completed, cancelled |
| `project_type` | enum | No | Work, Personal, Learning, Inactive |
| `description` | string | No | - |
| `remote_url` | string | No | URI format, max 500 chars |
| `created_at` | datetime | Yes | Auto-generated |
| `updated_at` | datetime | Yes | Auto-generated |

**proj-cli Inventory Internal Schema** (from inventory.py):

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `name` | string | github/local | Directory or repo name |
| `local_path` | string | local scan | Local filesystem path |
| `remote_url` | string | github/local | Git remote URL |
| `description` | string | github | From GitHub API |
| `source` | string | - | "github" or "local" |
| `language` | string | github | Primary language |
| `languages` | array | github | All languages |
| `marker` | string | local | Detection marker (.git, etc.) |
| `updated_at` | string | github | Last GitHub update |

**Source:** Codebase analysis + OpenAPI spec

**Relevance:** Complete field inventory enables comprehensive mapping strategy.

---

### Finding 2: Field Mapping Analysis

| proj-cli Internal | work-prod API | Status | Action |
|-------------------|---------------|--------|--------|
| `name` | `name` | ✅ Match | None needed |
| `local_path` | `path` | ⚠️ **FIXED** | Export maps correctly |
| `remote_url` | `remote_url` | ✅ Match | None needed |
| `description` | `description` | ✅ Match | None needed |
| `source` | N/A | ℹ️ proj-cli only | Not exported |
| `language` | N/A | ℹ️ proj-cli only | Not exported |
| `languages` | N/A | ℹ️ proj-cli only | Not exported |
| `marker` | N/A | ℹ️ proj-cli only | Not exported |
| `updated_at` | `updated_at` | ⚠️ Partial | Not sent on create |
| N/A | `organization` | ℹ️ API only | Not in inventory |
| N/A | `classification` | ℹ️ API only | Not in inventory |
| N/A | `status` | ⚠️ Hardcoded | Always "active" on export |
| N/A | `project_type` | ℹ️ API only | Not in inventory |

**Source:** Codebase comparison

**Relevance:** Identifies one additional potential issue: `status` is always hardcoded to "active".

---

### Finding 3: Naming Convention Analysis

Both systems use **snake_case** consistently:
- work-prod: `remote_url`, `project_type`, `created_at`
- proj-cli: `local_path`, `remote_url`, `updated_at`

**Exception found:** `project_type` uses PascalCase for enum values (Work, Personal, Learning, Inactive)

**Source:** OpenAPI spec + codebase analysis

**Relevance:** No convention mismatch - snake_case is used consistently for field names.

---

### Finding 4: Export Transformation is Correct Pattern

The current export implementation (post-fix) correctly transforms internal schema to API schema:

```python
# From inventory.py export functions
project = {
    "name": item.get("name", ""),
    "description": item.get("description", ""),
    "remote_url": item.get("remote_url", ""),
    "path": item.get("local_path", ""),  # Mapping happens here
    "status": "active",  # Hardcoded default
}
```

This transformation layer is the **correct pattern** - internal schema should not be changed.

**Source:** Codebase analysis (`inventory.py` lines 485-494, 559-565)

**Relevance:** Validates that transformation on export is the right approach.

---

### Finding 5: Registry Uses Path Consistently

The registry module correctly uses `path` (not `local_path`) and stores it as a Path object:

```python
@dataclass
class RegistryProject:
    path: Path  # Cross-reference key to inventory
    template: str
    template_version: str
    created_at: datetime
    work_prod_id: Optional[int] = None
```

**Source:** Codebase analysis (`registry.py`)

**Relevance:** Registry is already aligned with API schema. Inventory is the only place using `local_path` internally.

---

### Finding 6: proj-cli Only Fields Are Valuable

Fields that exist only in proj-cli serve specific purposes:

| Field | Purpose | Should Export? |
|-------|---------|----------------|
| `source` | Track where project came from (github/local) | No - internal tracking |
| `language` | Primary programming language | Could be useful, but not in API schema |
| `languages` | All languages detected | Could be useful, but not in API schema |
| `marker` | How project was detected (.git, pyproject.toml, etc.) | No - internal tracking |

**Recommendation:** These are intentionally not exported - they're for local inventory management.

**Source:** Functional analysis

**Relevance:** No action needed - current behavior is correct.

---

## 🔍 Analysis

### Current State Assessment

After the bug fix, field consistency is **mostly good**:

1. ✅ Core fields match (`name`, `remote_url`, `description`)
2. ✅ `path` field mapping is fixed
3. ✅ Registry uses `path` correctly
4. ✅ snake_case convention is consistent
5. ⚠️ `status` is hardcoded to "active" (minor issue)
6. ℹ️ proj-cli only fields are intentionally not exported

### Recommendations

1. **Keep internal `local_path`** - Internal schema doesn't need to change
2. **Maintain transformation layer** - Export functions handle mapping
3. **Consider `status` enhancement** - Allow specifying status on export (optional)
4. **Document field mapping** - Create reference documentation

**Key Insights:**
- [x] Insight 1: Field naming mismatches cause silent data loss (confirmed by BUG-001)
- [x] Insight 2: Transformation on export is the correct pattern (don't change internal schema)
- [x] Insight 3: Registry is already aligned with API schema
- [x] Insight 4: proj-cli only fields serve valid purposes and should not be exported

---

## 💡 Recommendations

- [x] Recommendation 1: ✅ Fix `local_path` → `path` mismatch (DONE - commit `49fae4f`)
- [x] Recommendation 2: ✅ Keep transformation layer in export functions (current pattern is correct)
- [x] Recommendation 3: Document field mapping in developer docs
- [x] Recommendation 4: Consider adding `--status` flag to export commands (optional enhancement)
- [x] Recommendation 5: No changes needed to internal `local_path` field name

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-FC-1:** Inventory export must use `path` field name (matches API) - ✅ DONE
- [x] **FR-FC-2:** Export transformation layer shall map internal fields to API schema
- [x] **FR-FC-3:** Registry shall use `path` field (not `local_path`) - ✅ Already correct
- [ ] **FR-FC-4:** Export commands should optionally accept `--status` flag (enhancement)

### Non-Functional Requirements

- [x] **NFR-FC-1:** Field names shall use snake_case convention - ✅ Already consistent
- [x] **NFR-FC-2:** Field mapping shall be documented for developers

### Constraints

- [x] **C-FC-1:** Internal inventory schema (`local_path`) shall not be changed
- [x] **C-FC-2:** work-prod API schema is external and cannot be modified

---

## 📊 Field Mapping Reference

### Export Mapping (proj-cli → work-prod)

```
proj-cli Internal    →    work-prod API
─────────────────────────────────────────
name                 →    name
local_path           →    path          (transformation)
remote_url           →    remote_url
description          →    description
[hardcoded]          →    status = "active"
source               →    [not exported]
language             →    [not exported]
languages            →    [not exported]
marker               →    [not exported]
updated_at           →    [not sent on create]
```

### Import Mapping (work-prod → proj-cli)

Currently not implemented for inventory. API responses are used directly by CLI commands.

---

## 🚀 Next Steps

1. ✅ Research complete
2. Optional: Add `--status` flag to export commands
3. Document field mapping in developer documentation
4. Consider adding import capability to merge API data back to inventory

---

**Last Updated:** 2026-01-08
