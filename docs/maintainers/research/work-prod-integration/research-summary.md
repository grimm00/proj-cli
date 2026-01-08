# Research Summary - Work-Prod Integration

**Purpose:** Summary of all research findings for work-prod integration  
**Status:** 🔴 Research  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08

---

## 📋 Research Overview

This research examines how `proj-cli` should integrate with the `work-prod` backend API across all commands and features. The goal is to establish clear boundaries and consistent patterns for API integration.

**Research Topics:** 8 topics  
**Research Documents:** 8 documents  
**Status:** 🟠 Research (3/8 complete)

**Source:** [Exploration - Work-Prod Integration](../../explorations/work-prod-integration/exploration.md)

---

## 🔍 Key Findings

### Finding 1: Field Name Mismatch (FIXED)

Inventory export was using `local_path` while work-prod API expects `path`, causing silent data loss.

**Source:** [research-field-consistency.md](research-field-consistency.md)

**Resolution:** Fixed in commit `49fae4f`

---

### Finding 2: Split-Truth Model Already Correct

Research confirms proj-cli's architecture is sound: **API is source of truth** for project metadata, **registry is sync overlay** for template tracking. This is the right pattern for the use case.

**Source:** [research-source-of-truth.md](research-source-of-truth.md)

---

### Finding 3: Gap is Implementation, Not Architecture

The issue isn't "which is source of truth?" - that's decided (API). The gap is **incomplete CRUD consistency**: delete doesn't clean up registry, leaving orphaned entries.

**Source:** [research-source-of-truth.md](research-source-of-truth.md)

---

### Finding 4: Delete Architecture Design Complete

Research identified comprehensive delete architecture:
- **Automatic cascade** from API to registry (matches kubectl pattern)
- **Path identifier support** for better UX
- **Filesystem deletion opt-in only** with extra confirmation
- **Dry-run support** for safe previewing

**Source:** [research-delete-architecture.md](research-delete-architecture.md)

---

### Finding 5: Registry Infrastructure Gap

Need `get_project_by_work_prod_id()` function to clean up registry when deleting by API ID.

**Source:** [research-delete-architecture.md](research-delete-architecture.md)

---

### Finding 6: Field Mapping Complete - Only One Issue Found

Comprehensive audit found only one field mismatch (`local_path` → `path`), which is already fixed. Both systems use snake_case consistently. Transformation on export is the correct pattern.

**Source:** [research-field-consistency.md](research-field-consistency.md)

---

## 💡 Key Insights

- [x] Insight 1: Field naming mismatches cause silent data loss - must audit all fields
- [x] Insight 2: API is already the source of truth by design - registry is just sync tracking
- [x] Insight 3: No complex sync needed - just complete the CRUD operations (delete cleanup)
- [x] Insight 4: Automatic cascade is expected behavior (kubectl pattern)
- [x] Insight 5: Filesystem deletion must be opt-in only (safety critical)
- [x] Insight 6: Transformation on export is correct pattern - don't change internal schema
- [ ] Insight 7: [Pending research on remaining topics]

---

## 📊 Research Progress

| # | Topic | Priority | Status |
|---|-------|----------|--------|
| 1 | Source of Truth | 🔴 High | ✅ Complete |
| 2 | Delete Architecture | 🔴 High | ✅ Complete |
| 8 | Field Consistency | 🔴 High | ✅ Complete |
| 3 | Sync Strategy | 🟡 Medium | 🔴 Not Started |
| 4 | Offline Mode | 🟡 Medium | 🔴 Not Started |
| 5 | Registry Commands | 🟡 Medium | 🔴 Not Started |
| 7 | Creation Date | 🟡 Medium | 🔴 Not Started |
| 6 | Inventory Integration | 🟢 Low | 🔴 Not Started |

---

## 📋 Requirements Summary

**See:** [requirements.md](requirements.md) for complete requirements document

### Discovered So Far

- **FR-1:** Inventory export must use `path` field name ✅ (Fixed)
- **FR-SOT-1:** API shall remain the source of truth for all project metadata
- **FR-SOT-2:** Registry shall only track sync state (path, template, work_prod_id)
- **FR-SOT-3:** All operations that modify API state shall also update registry accordingly
- **FR-SOT-4:** CLI shall provide commands to detect and resolve registry/API inconsistencies
- **FR-DEL-1:** Delete shall automatically cascade from API to registry
- **FR-DEL-2:** Delete shall accept both API ID and project path
- **FR-DEL-3:** Delete shall support `--dry-run` flag
- **FR-DEL-4:** Delete shall support `--delete-files` flag (opt-in, extra confirmation)
- **FR-DEL-7:** Registry shall provide `get_project_by_work_prod_id()` lookup
- **FR-FC-1:** Inventory export must use `path` field name ✅ (Fixed)
- **FR-FC-2:** Export transformation layer shall map internal fields to API schema

---

## 🎯 Recommendations

[To be completed after research]

- [ ] Recommendation 1: [Pending]
- [ ] Recommendation 2: [Pending]

---

## 🚀 Next Steps

1. Conduct research on high-priority topics (1, 2, 8)
2. Continue with medium-priority topics
3. Review requirements in `requirements.md`
4. Use `/decision work-prod-integration --from-research` when complete

---

## 📌 Architecture Summary

Based on Topic 1 research, the architecture pattern is:

```
┌─────────────────────────────────────────────────┐
│            work-prod API (Source of Truth)      │
│  Project metadata: name, desc, status, etc.     │
└─────────────────────────────────────────────────┘
                       ↑ sync via work_prod_id
┌─────────────────────────────────────────────────┐
│          Local Registry (Sync Overlay)          │
│  Sync state: path, template, work_prod_id       │
└─────────────────────────────────────────────────┘
```

**Key Decision:** API is truth, registry is tracking overlay only.

---

**Last Updated:** 2026-01-08
