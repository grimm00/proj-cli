# Research: Sync Strategy

**Research Topic:** Work-Prod Integration  
**Question:** What sync patterns should proj-cli support?  
**Status:** ✅ Complete  
**Priority:** 🟡 Medium  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09

---

## 🎯 Research Question

What sync patterns should proj-cli support?

**Context:** Need to decide between auto-sync, manual sync, or hybrid approach.

**Prior Research:** This builds on findings from:
- Topic 1 (Source of Truth): API is truth, registry is sync overlay
- Topic 4 (Offline Mode): Local-first development, explicit sync command needed

---

## 🔍 Research Goals

- [x] Goal 1: Evaluate auto-sync vs manual sync trade-offs
- [x] Goal 2: Design conflict resolution strategy
- [x] Goal 3: Determine if sync should be bidirectional
- [x] Goal 4: Research sync patterns from similar tools

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase: Current Phase 6 auto-sync behavior (`sync_to_api()`)
- [x] Prior Research: Topic 1 (Source of Truth) findings
- [x] Prior Research: Topic 4 (Offline Mode) recommendations
- [x] Architecture patterns: Git (explicit), Dropbox (auto), Hybrid models

---

## 🔑 Sub-Questions

1. **Auto-sync Timing:** Should sync happen automatically on create? (current Phase 6 behavior)
2. **Explicit Command:** Should there be a `proj sync` command for explicit sync?
3. **Conflict Resolution:** How should sync conflicts be resolved?
4. **Direction:** Should sync be bidirectional (API → registry and registry → API)?

---

## 📊 Findings

### Finding 1: Current Auto-Sync Behavior (Phase 6)

The current implementation in `src/proj/commands/projects/helpers.py`:

```python
def sync_to_api(client, name, path, template, description=None, console=None):
    """Sync project to work-prod API."""
    project_data = {
        "name": name,
        "path": str(path),
        "description": description or f"Created from {template} template",
        "status": "active",
    }
    result = client.create_project(project_data)
    return result.get("id")  # work_prod_id
```

**Current behavior:**
- Auto-sync happens on `proj create` unless `--local-only` or `api_enabled=false`
- Sync is **one-way**: local → API (push only)
- Sync creates API record and stores `work_prod_id` in registry
- API failure is graceful: "Could not sync to API. Project created locally."

**Source:** `src/proj/commands/projects/create.py` lines 435-458

**Relevance:** This is the foundation we're building on.

---

### Finding 2: Three Sync Architecture Patterns

| Pattern | Example | Pros | Cons |
|---------|---------|------|------|
| **Auto-Sync** | Dropbox, iCloud | Seamless, no user action | Conflicts, network dependency |
| **Explicit-Sync** | Git push/pull | User control, offline-first | Requires discipline, extra step |
| **Hybrid** | VS Code Settings Sync | Best of both, flexible | Complexity, needs clear UX |

**Analysis for proj-cli:**

Given Topic 1 findings (API is source of truth) and Topic 4 (local-first development), the **Hybrid pattern** is most appropriate:
1. Auto-sync on create (current behavior) - optimistic, reduces friction
2. Explicit `proj sync` for recovery and batch operations

**Source:** Architecture pattern analysis

**Relevance:** Informs which pattern to adopt.

---

### Finding 3: Sync Direction Analysis

From Topic 1 research, the architecture is:

```
work-prod API (Source of Truth)
       ↑ push via work_prod_id
Local Registry (Sync Overlay)
```

**Sync directions needed:**

| Direction | Use Case | Priority |
|-----------|----------|----------|
| **Local → API (Push)** | New local projects | High ✅ |
| **API → Local (Pull)** | Rebuild registry from API | Low |
| **Bidirectional** | Two-way sync | Not needed ❌ |

**Key insight from Topic 1:**
> "No bidirectional sync - Registry tracks API state, not the other way around"

The registry is a **sync overlay**, not a data store. It only needs to know which local projects are synced and their API IDs.

**Source:** [research-source-of-truth.md](research-source-of-truth.md)

**Relevance:** Simplifies sync design significantly.

---

### Finding 4: Conflict Scenarios Are Minimal

Since API is authoritative (Topic 1), conflicts are actually rare:

| Scenario | Conflict? | Resolution |
|----------|-----------|------------|
| Local project, no API record | No | Push to create |
| API record, no registry entry | No | Normal (API-only project) |
| Both exist, IDs match | No | Already synced |
| Both exist, IDs mismatch | Yes | Error - manual fix |
| Local project, API deleted | Soft | Re-push or accept deletion |

**Real conflicts only occur when:**
1. Registry has stale `work_prod_id` pointing to deleted API record
2. Registry corrupted with wrong `work_prod_id`

**Resolution strategy:** 
- Detect during sync: "API record not found for ID {work_prod_id}"
- Offer options: Re-push as new, or remove from registry

**Source:** Topic 1 conflict scenarios analysis

**Relevance:** Conflict handling is simpler than expected.

---

### Finding 5: Sync Status Tracking

From Topic 4 research, we need visibility into sync state:

**Current state:**
- `work_prod_id` in registry = synced
- `work_prod_id` is None = not synced

**Missing:**
- No command to see sync status
- No way to identify unsynced projects
- No batch sync capability

**Proposed `proj sync --status`:**
```
Sync Status:
  ✅ Synced:   12 projects
  ⚠️  Unsynced: 3 projects
  
Unsynced Projects:
  • my-new-app (created 2026-01-08)
  • test-project (created 2026-01-07)
  • experiment (created 2026-01-05)

Run 'proj sync' to push unsynced projects to API.
```

**Source:** [research-offline-mode.md](research-offline-mode.md)

**Relevance:** Supports local-first workflow with visibility.

---

### Finding 6: Sync Command Design

Based on all findings, the `proj sync` command should:

**Basic usage:**
```bash
proj sync              # Push all unsynced projects
proj sync --status     # Show sync status only
proj sync --dry-run    # Preview what would be synced
proj sync my-app       # Sync specific project by path/name
```

**Advanced flags:**
```bash
proj sync --force      # Re-push even if already synced (update API)
proj sync --all        # Sync all registry projects (not just unsynced)
```

**Source:** Topic 4 recommendations + best practices

**Relevance:** Complete design for sync command.

---

## 🔍 Analysis

### Hybrid Sync Strategy

The recommended approach combines:

1. **Auto-sync on create** (current behavior)
   - Reduces friction for normal workflow
   - Can be disabled with `--local-only` or config

2. **Explicit `proj sync` command**
   - Recovery for failed auto-syncs
   - Batch sync for offline-created projects
   - Status visibility

### Why Not Full Manual Sync (Git Model)?

Git's explicit push/pull works because:
- Complex merge conflicts are expected
- Branching is a core concept
- Users are trained on the model

proj-cli is simpler:
- No branches or complex state
- API is always authoritative
- Conflicts are rare/simple
- Reduce cognitive load

### Sync State Machine

```
┌─────────────────┐     proj create      ┌─────────────────┐
│   Not Created   │ ─────────────────────▶│ Local Only      │
└─────────────────┘     --local-only     │ (no work_prod_id)│
                                         └────────┬────────┘
                                                  │
                        proj create               │ proj sync
                        (auto-sync)               │
                              │                   ▼
                              │          ┌─────────────────┐
                              └─────────▶│    Synced       │
                                         │ (has work_prod_id)│
                                         └─────────────────┘
```

**Key Insights:**
- [x] Insight 1: Hybrid pattern is best - auto-sync on create, explicit sync for recovery
- [x] Insight 2: Bidirectional sync not needed - API is truth, registry is overlay
- [x] Insight 3: Conflicts are rare and simple - just detect stale IDs
- [x] Insight 4: Sync status visibility is essential for local-first workflow
- [x] Insight 5: Keep it simple - no branches, no complex merging

---

## 💡 Recommendations

- [x] Recommendation 1: **Keep auto-sync on create** - Current behavior is good, don't remove
- [x] Recommendation 2: **Add `proj sync` command** - For recovery and batch operations
- [x] Recommendation 3: **Add `proj sync --status`** - Show sync state of all projects
- [x] Recommendation 4: **No bidirectional sync** - Push only, API is authoritative
- [x] Recommendation 5: **Simple conflict handling** - Detect stale IDs, offer re-push or remove
- [x] Recommendation 6: **Support `--dry-run`** - Preview sync before executing
- [x] Recommendation 7: **Support project targeting** - `proj sync <path>` for specific project

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-SYNC-1:** CLI shall provide `proj sync` command to push unsynced projects to API
- [x] **FR-SYNC-2:** CLI shall provide `proj sync --status` to show sync state of all projects
- [x] **FR-SYNC-3:** `proj sync` shall support `--dry-run` to preview operations
- [x] **FR-SYNC-4:** `proj sync` shall support targeting specific project by path
- [x] **FR-SYNC-5:** Auto-sync on create shall remain as default behavior
- [x] **FR-SYNC-6:** Sync shall detect stale work_prod_id (API record deleted)
- [x] **FR-SYNC-7:** Sync shall offer resolution options for stale IDs

### Non-Functional Requirements

- [x] **NFR-SYNC-1:** Sync status shall show count of synced vs unsynced projects
- [x] **NFR-SYNC-2:** Sync shall fail gracefully when API is unavailable
- [x] **NFR-SYNC-3:** Sync shall provide clear feedback for each project synced

### Constraints

- [x] **C-SYNC-1:** Sync shall be one-way only (local → API push)
- [x] **C-SYNC-2:** No bidirectional sync or API → local pull (except registry rebuild, separate feature)

---

## 🚀 Next Steps

1. ✅ Research complete
2. Use Topic 5 (Registry Commands) for `proj sync --status` integration
3. Use findings in `/decision work-prod-integration --from-research`

---

## 📊 Sync Command Reference

### Command Specification

```
proj sync [OPTIONS] [PROJECT]

Push unsynced projects to work-prod API.

Arguments:
  PROJECT    Optional project path or name to sync

Options:
  --status    Show sync status without syncing
  --dry-run   Preview what would be synced
  --force     Re-push even if already synced
  --all       Sync all registry projects

Examples:
  proj sync                    # Push all unsynced projects
  proj sync --status           # Show sync status
  proj sync --dry-run          # Preview sync
  proj sync ~/Projects/my-app  # Sync specific project
```

### Output Examples

**`proj sync --status`:**
```
📊 Sync Status

  ✅ Synced:   12 projects
  ⚠️  Unsynced: 3 projects

Unsynced Projects:
  Path                          Created
  ~/Projects/my-new-app         2026-01-08
  ~/Projects/test-project       2026-01-07
  ~/Projects/experiment         2026-01-05

💡 Run 'proj sync' to push unsynced projects to API.
```

**`proj sync --dry-run`:**
```
🔍 Dry Run - Would sync 3 projects:

  • my-new-app → Create in API
  • test-project → Create in API  
  • experiment → Create in API

Run without --dry-run to execute.
```

**`proj sync`:**
```
📤 Syncing 3 projects to API...

  ✅ my-new-app → ID: 42
  ✅ test-project → ID: 43
  ✅ experiment → ID: 44

✅ Synced 3 projects successfully.
```

---

**Last Updated:** 2026-01-09
