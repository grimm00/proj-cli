# Research: Source of Truth

**Research Topic:** Work-Prod Integration  
**Question:** Should the local registry or work-prod API be the source of truth for projects?  
**Status:** ✅ Complete  
**Priority:** 🔴 High  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08  
**Completed:** 2026-01-08

---

## 🎯 Research Question

Should the local registry or work-prod API be the source of truth for projects? This fundamental decision affects all sync logic, conflict resolution, and offline behavior.

---

## 🔍 Research Goals

- [x] Goal 1: Understand trade-offs between local-first vs API-first patterns
- [x] Goal 2: Identify conflict scenarios and resolution strategies
- [x] Goal 3: Determine if different project types should have different truth sources
- [x] Goal 4: Research industry patterns for local/cloud sync systems

---

## 📚 Research Methodology

**Sources:**
- [x] Web search: Local-first software patterns and architectures
- [x] Web search: Sync conflict resolution strategies
- [x] Codebase analysis: Current registry and API implementation
- [x] Case studies: Git (local-first), cloud note apps, package managers

---

## 🔑 Sub-Questions

1. **Conflict Resolution:** What happens when registry and API disagree?
2. **Orphaned Projects:** How do we handle projects that exist in one but not the other?
3. **Project Type Differentiation:** Should template-created projects have different truth sources than API-created projects?

---

## 📊 Findings

### Finding 1: Industry Patterns Show Three Main Approaches

There are three primary patterns for source of truth in distributed systems:

| Pattern | Example | Truth | Offline | Complexity |
|---------|---------|-------|---------|------------|
| **API-Primary** | REST APIs, SaaS | Server | Limited | Low |
| **Local-First** | Git, Obsidian | Local | Full | High (sync) |
| **Hybrid/Split** | Package managers | Split by type | Partial | Medium |

**Source:** Web search + industry analysis

**Relevance:** Informs which pattern fits proj-cli's use case.

---

### Finding 2: Current proj-cli Architecture Already Uses Hybrid Pattern

Codebase analysis reveals the current architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    work-prod API                            │
│  Source of truth for: name, description, status, org,       │
│  classification, remote_url, timestamps                     │
└─────────────────────────────────────────────────────────────┘
                            ↑
                    sync (via work_prod_id)
                            ↑
┌─────────────────────────────────────────────────────────────┐
│                    Local Registry                           │
│  Sync overlay for: path, template, template_version,        │
│  created_at, work_prod_id (link to API)                     │
│  Purpose: Template sync tracking                            │
└─────────────────────────────────────────────────────────────┘
```

From `registry.py`:
> "This is a sync overlay, not a project store. All project metadata lives in inventory.json."

**Source:** Codebase analysis (`proj-cli/src/proj/registry.py` lines 35-47)

**Relevance:** The pattern is already established - registry is NOT meant to be source of truth.

---

### Finding 3: Git's Model Demonstrates Effective Local-First Pattern

Git uses a local-first pattern where:
- **Local repository** is a complete copy with full history
- **Remote** is a sync target, not the source of truth
- **Conflicts** are resolved explicitly by the user
- **Offline** work is fully supported, synced later

However, Git's use case (version control) differs from proj-cli (project tracking).

**Source:** Git documentation, distributed version control patterns

**Relevance:** Local-first works well when users need offline work and conflicts are expected. Less relevant for proj-cli where API consistency matters more.

---

### Finding 4: Package Managers Use Split-Truth Model

Package managers like npm/yarn demonstrate split responsibilities:
- **Registry (npmjs.com)** is truth for package definitions
- **Local cache** speeds up installs
- **package-lock.json** is truth for resolved dependencies

This matches proj-cli's current hybrid approach:
- **work-prod API** is truth for project metadata
- **Local registry** tracks template sync state

**Source:** npm/yarn architecture analysis

**Relevance:** Validates the split-truth model currently used by proj-cli.

---

### Finding 5: Current Gap - Incomplete Sync Consistency

While the architecture is sound, implementation has gaps:

| Operation | API | Registry | Filesystem | Gap? |
|-----------|-----|----------|------------|------|
| `create --template` | ✅ Sync | ✅ Register | ✅ Create | ✅ None |
| `create --api-only` | ✅ Create | ❌ Skip | ❌ Skip | ✅ None (by design) |
| `delete` | ✅ Delete | ❌ No cleanup | ❌ No cleanup | ⚠️ **Gap** |

**Source:** Codebase analysis (`proj-cli/src/proj/commands/projects/crud.py`)

**Relevance:** Delete operation leaves orphaned registry entries, violating consistency.

---

## 🔍 Analysis

### Current State Assessment

The proj-cli architecture correctly implements a **split-truth hybrid model**:

1. **work-prod API** = Source of truth for project metadata
2. **Local Registry** = Sync tracking overlay (not a truth source)
3. **Inventory** = Discovery/scanning (ephemeral, not a truth source)

This is the **right design** for proj-cli's use case because:
- Project metadata should be centralized for reporting/dashboard
- Local registry only needs to track sync state (minimal data)
- Offline support isn't critical (users aren't editing project metadata offline)

### The Real Problem

The issue isn't "which is source of truth?" - that's already decided (API). The problem is **incomplete consistency**:

1. **Create** properly syncs: Registry ← API
2. **Delete** doesn't clean up: Registry has orphaned entries
3. **No reconciliation**: No way to detect/fix drift

### Conflict Scenarios

| Scenario | Resolution Strategy |
|----------|---------------------|
| Registry entry, no API record | Offer to create in API or remove from registry |
| API record, no registry entry | Normal - project created via API only |
| Both exist, IDs match | Normal state |
| Both exist, IDs mismatch | Error - corruption, manual fix needed |

**Key Insights:**
- [x] Insight 1: API is already the source of truth by design - registry is just sync tracking
- [x] Insight 2: The gap isn't architecture, it's incomplete implementation (delete doesn't clean up)
- [x] Insight 3: No need for complex sync/conflict resolution - just complete the CRUD operations

---

## 💡 Recommendations

- [x] Recommendation 1: **Maintain current split-truth model** - API is truth, registry is sync overlay
- [x] Recommendation 2: **Complete the CRUD cycle** - Delete should clean up registry (Research Topic 2)
- [x] Recommendation 3: **Add registry status command** - Show sync state, identify orphans (Research Topic 5)
- [x] Recommendation 4: **No bidirectional sync** - Registry tracks API state, not the other way around
- [x] Recommendation 5: **Document the model clearly** - Users should understand API is authoritative

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-SOT-1:** API shall remain the source of truth for all project metadata
- [x] **FR-SOT-2:** Registry shall only track sync state (path, template, work_prod_id)
- [x] **FR-SOT-3:** All operations that modify API state shall also update registry accordingly
- [x] **FR-SOT-4:** CLI shall provide commands to detect and resolve registry/API inconsistencies

### Non-Functional Requirements

- [x] **NFR-SOT-1:** CLI shall work offline for local operations (create --local-only)
- [x] **NFR-SOT-2:** CLI shall fail gracefully when API is unavailable
- [x] **NFR-SOT-3:** Sync state shall be recoverable (registry can be rebuilt from API)

### Constraints

- [x] **C-SOT-1:** Registry schema is fixed - do not expand to duplicate API data
- [x] **C-SOT-2:** API is external dependency - cannot modify work-prod schema

---

## 🚀 Next Steps

1. ✅ Research complete
2. Continue with Research Topic 2 (Delete Architecture) to address the main gap
3. Use findings to inform `/decision work-prod-integration` phase

---

**Last Updated:** 2026-01-08
