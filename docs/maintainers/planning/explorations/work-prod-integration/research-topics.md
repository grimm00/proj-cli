# Research Topics - Work-Prod Integration

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** 2026-01-06  
**Last Updated:** 2026-01-06

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before making decisions about work-prod integration architecture.

---

### Research Topic 1: Registry vs API Source of Truth

**Question:** Should the local registry or work-prod API be the source of truth for projects?

**Why:** This fundamental decision affects all sync logic, conflict resolution, and offline behavior.

**Sub-questions:**
- What happens when registry and API disagree?
- How do we handle projects that exist in one but not the other?
- Should some project types (template-created) have different truth sources?

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 2: Delete Command Architecture

**Question:** How should `proj delete` handle API, registry, and filesystem cleanup?

**Why:** Current gap: delete only removes from API, leaving orphaned registry entries.

**Sub-questions:**
- Should delete require explicit flags (`--from-api`, `--from-registry`)?
- Should delete accept both ID and path as identifiers?
- How should delete handle cascade (API → registry → filesystem)?
- What about projects that exist only in registry (never synced)?

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 3: Sync Strategy

**Question:** What sync patterns should proj-cli support?

**Why:** Need to decide between auto-sync, manual sync, or hybrid approach.

**Sub-questions:**
- Should sync happen automatically on create? (current Phase 6 behavior)
- Should there be a `proj sync` command for explicit sync?
- How should sync conflicts be resolved?
- Should sync be bidirectional (API → registry and registry → API)?

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 4: Offline Mode Design

**Question:** How should offline mode work across all commands?

**Why:** Users may work without network access; CLI should still be useful.

**Sub-questions:**
- What commands work offline vs require API?
- How is offline mode detected vs configured?
- What happens when going from offline → online?
- Should there be a `--offline` flag for all commands?

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 5: Registry Command Design

**Question:** What commands should be available for registry management?

**Why:** Users need tools to manage local registry (cleanup, inspect, sync).

**Sub-questions:**
- What's the minimal useful set of registry commands?
- Should registry have its own subcommand (`proj registry list`)?
- How should registry commands interact with API?

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 6: Inventory Integration

**Question:** How does the registry relate to inventory scanning?

**Why:** Both track local projects; need to understand overlap and distinction.

**Sub-questions:**
- Should inventory scanning update the registry?
- Should registry entries appear in inventory results?
- Is there duplication between these concepts?

**Priority:** Low

**Status:** 🔴 Not Started

---

## 🎯 Research Workflow

1. Use `/research work-prod-integration` to conduct research on each topic
2. Research will create documents in `docs/maintainers/research/`
3. After research complete, use `/decision` to make architectural decisions
4. Create ADR documenting the integration architecture

---

## 📊 Priority Summary

| Priority | Topics |
|----------|--------|
| **High** | Source of Truth, Delete Architecture |
| **Medium** | Sync Strategy, Offline Mode, Registry Commands |
| **Low** | Inventory Integration |

---

**Last Updated:** 2026-01-06

