# Research: Field Name Consistency

**Research Topic:** Work-Prod Integration  
**Question:** How should we standardize field names between proj-cli and work-prod?  
**Status:** 🟡 Partial (Bug Fixed)  
**Priority:** 🔴 High  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08

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

- [ ] Goal 1: Audit all field names in proj-cli vs work-prod API
- [ ] Goal 2: Decide on consistent naming convention (snake_case, camelCase)
- [ ] Goal 3: Identify fields that exist in one system but not the other
- [ ] Goal 4: Design mapping strategy for non-matching fields

---

## 📚 Research Methodology

**Sources:**
- [ ] Codebase analysis: proj-cli inventory export schema
- [ ] Codebase analysis: work-prod API endpoint schemas
- [ ] API documentation: work-prod OpenAPI spec
- [ ] Web search: API field naming conventions and best practices

---

## 🔑 Sub-Questions

1. **Standard Name:** Should we standardize on `path` or `local_path` internally?
2. **Other Inconsistencies:** What other field inconsistencies exist?
3. **Schema Alignment:** Should inventory JSON schema match work-prod API schema exactly?
4. **Extra Fields:** How do we handle fields that exist in inventory but not API (e.g., `languages`, `marker`)?

---

## 📊 Findings

### Finding 1: Path Field Inconsistency (FIXED)

Inventory export was using `local_path` while work-prod API expects `path`. This was causing all path data to be silently lost during import.

**Source:** Bug discovered during testing (BUG-001)

**Relevance:** Critical - path is essential project data. Fix applied in commit `49fae4f`.

---

### Finding 2: [Pending - Other Field Audit]

[Need to audit all fields for additional inconsistencies]

**Source:** [Pending codebase analysis]

**Relevance:** [TBD]

---

## 🔍 Analysis

**Partial - Bug Fix Complete:**

The immediate bug has been fixed. Remaining research will audit for other inconsistencies.

**Key Insights:**
- [x] Insight 1: Field naming mismatches cause silent data loss
- [ ] Insight 2: [Need comprehensive field audit]

---

## 💡 Recommendations

- [x] Recommendation 1: Fix `local_path` → `path` mismatch (DONE)
- [ ] Recommendation 2: Conduct comprehensive field audit
- [ ] Recommendation 3: Document field mapping between systems

---

## 📋 Requirements Discovered

- [x] REQ-F1: Inventory export must use `path` field name (matches API)
- [ ] REQ-F2: Field names should be consistent between proj-cli and work-prod
- [ ] REQ-F3: Field mapping should be documented

---

## 🚀 Next Steps

1. ✅ ~~Fix immediate bug~~ (Complete)
2. Conduct comprehensive field audit
3. Document field mapping
4. Consider schema validation

---

**Last Updated:** 2026-01-08
