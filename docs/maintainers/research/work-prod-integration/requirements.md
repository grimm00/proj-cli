# Requirements - Work-Prod Integration

**Source:** Research on work-prod integration patterns  
**Status:** Draft  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08

---

## 📋 Overview

This document captures requirements discovered during research on how proj-cli should integrate with the work-prod backend API.

**Research Source:** [research-summary.md](research-summary.md)

---

## ✅ Functional Requirements

### FR-1: Field Name Consistency

**Description:** Inventory export must use `path` field name to match work-prod API schema

**Source:** [research-field-consistency.md](research-field-consistency.md)

**Priority:** High

**Status:** ✅ Implemented (commit `49fae4f`)

---

### FR-2: [Pending - Source of Truth]

**Description:** [TBD after research]

**Source:** [research-source-of-truth.md](research-source-of-truth.md)

**Priority:** High

**Status:** 🔴 Pending

---

### FR-3: [Pending - Delete Architecture]

**Description:** [TBD after research]

**Source:** [research-delete-architecture.md](research-delete-architecture.md)

**Priority:** High

**Status:** 🔴 Pending

---

### FR-4: [Pending - Sync Strategy]

**Description:** [TBD after research]

**Source:** [research-sync-strategy.md](research-sync-strategy.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

### FR-5: [Pending - Registry Commands]

**Description:** [TBD after research]

**Source:** [research-registry-commands.md](research-registry-commands.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

## 🎯 Non-Functional Requirements

### NFR-1: Offline Capability

**Description:** CLI commands should degrade gracefully when API is unavailable

**Source:** [research-offline-mode.md](research-offline-mode.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

### NFR-2: Consistent API Integration

**Description:** All commands should follow consistent patterns for API integration

**Source:** [research-summary.md](research-summary.md)

**Priority:** High

**Status:** 🔴 Pending

---

## ⚠️ Constraints

### C-1: Work-Prod API Compatibility

**Description:** proj-cli must be compatible with existing work-prod API schema

**Source:** [research-field-consistency.md](research-field-consistency.md)

---

### C-2: Backward Compatibility

**Description:** Changes should not break existing workflows using proj-cli

**Source:** [General requirement]

---

## 💭 Assumptions

### A-1: API Availability

**Description:** work-prod API will be available for most operations but offline mode needed

**Source:** [research-offline-mode.md](research-offline-mode.md)

---

### A-2: Local Registry Continues

**Description:** Local registry will continue to be used for template-created projects

**Source:** [research-source-of-truth.md](research-source-of-truth.md)

---

## 🔗 Related Documents

- [Research Summary](research-summary.md)
- [Research Documents](README.md)
- [Exploration Hub](../../explorations/work-prod-integration/README.md)

---

## 🚀 Next Steps

1. Complete research for all topics
2. Refine requirements based on findings
3. Use `/decision work-prod-integration --from-research` to make decisions

---

**Last Updated:** 2026-01-08
