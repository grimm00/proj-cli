# Work-Prod Integration - Research Hub

**Purpose:** Research for proj-cli integration with work-prod API  
**Status:** 🟠 Research (6/8 complete)  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09

---

## 📋 Quick Links

- **[Research Summary](research-summary.md)** - Summary of all research findings
- **[Requirements](requirements.md)** - Requirements discovered during research

### Research Documents (8 Topics)

| #   | Priority  | Topic                      | Document                                                               | Status         |
| --- | --------- | -------------------------- | ---------------------------------------------------------------------- | -------------- |
| 1   | 🔴 High   | Source of Truth            | [research-source-of-truth.md](research-source-of-truth.md)             | ✅ Complete    |
| 2   | 🔴 High   | Delete Architecture        | [research-delete-architecture.md](research-delete-architecture.md)     | ✅ Complete    |
| 8   | 🔴 High   | Field Name Consistency     | [research-field-consistency.md](research-field-consistency.md)         | ✅ Complete    |
| 4   | 🟡 Medium | Offline Mode (Local-First) | [research-offline-mode.md](research-offline-mode.md)                   | ✅ Complete    |
| 3   | 🟡 Medium | Sync Strategy              | [research-sync-strategy.md](research-sync-strategy.md)                 | ✅ Complete    |
| 5   | 🟡 Medium | Registry Commands          | [research-registry-commands.md](research-registry-commands.md)         | ✅ Complete    |
| 7   | 🟡 Medium | Creation Date Semantics    | [research-creation-date.md](research-creation-date.md)                 | 🔴 Not Started |
| 6   | 🟢 Low    | Inventory Integration      | [research-inventory-integration.md](research-inventory-integration.md) | 🔴 Not Started |

---

## 🎯 Research Overview

This research examines how `proj-cli` should integrate with the `work-prod` backend API across all commands and features.

**Context:** During template generation development (Phase 6), API sync functionality was added. This revealed that API integration is a cross-cutting concern that deserves dedicated design work, separate from individual features.

**Source:** [Exploration Document](../../explorations/work-prod-integration/exploration.md)

**Research Topics:** 8 topics  
**High Priority:** 3 (Source of Truth, Delete Architecture, Field Consistency)  
**Medium Priority:** 4 (Sync, Offline, Registry, Creation Date)  
**Low Priority:** 1 (Inventory Integration)

---

## 🚨 Current Gaps Identified

| Gap                   | Issue                                                     |
| --------------------- | --------------------------------------------------------- |
| `proj delete`         | Removes from API but not from registry → orphaned entries |
| No `proj registry`    | No commands to manage/cleanup local registry              |
| Inconsistent patterns | Each feature implements API integration differently       |
| Field name mismatch   | ✅ FIXED: `local_path` → `path` (BUG-001)                 |

---

## 📊 Research Progress

**Overall Status:** 🟠 Research (6/8 complete)

### High Priority (Complete First)

- [x] Research Topic 1: Source of Truth ✅
- [x] Research Topic 2: Delete Architecture ✅
- [x] Research Topic 8: Field Name Consistency ✅

### Medium Priority

- [x] Research Topic 4: Offline Mode (Local-First Development) ✅
- [x] Research Topic 3: Sync Strategy ✅
- [x] Research Topic 5: Registry Commands ✅
- [ ] Research Topic 7: Creation Date Semantics

### Low Priority

- [ ] Research Topic 6: Inventory Integration

---

## 🚀 Next Steps

1. ✅ High-priority topics complete (1, 2, 8)
2. ✅ Offline Mode research complete (Topic 4)
3. ✅ Sync Strategy research complete (Topic 3)
4. ✅ Registry Commands research complete (Topic 5)
5. Continue with remaining topics (7, 6)
6. After all research complete, use `/decision work-prod-integration --from-research`

---

## 🔗 Related

- **[Exploration Hub](../../explorations/work-prod-integration/README.md)** - Exploration that identified these topics
- **[Research Topics Source](../../explorations/work-prod-integration/research-topics.md)** - Original research topics document

---

**Last Updated:** 2026-01-09
