# Research: Offline Mode Design (Local-First Development)

**Research Topic:** Work-Prod Integration  
**Question:** How should offline mode work across all commands?  
**Status:** ✅ Complete  
**Priority:** 🟡 Medium  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09

---

## 🎯 Research Question

How should offline mode work across all commands?

**Extended Context:** Beyond network unavailability, this research now includes:
- What is "fully functional local"?
- How should development be sequenced (local-first)?
- Which commands should work completely without API?

**Context:** Users may work without network access; CLI should still be useful. Additionally, development should validate local functionality before API integration.

---

## 🔍 Research Goals

- [x] Goal 1: Categorize commands by API dependency (required vs optional)
- [x] Goal 2: Design offline detection vs explicit configuration
- [x] Goal 3: Plan transition behavior (offline → online)
- [x] Goal 4: Define "fully functional local" for development sequencing

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase: Current API dependency per command (primary source)
- [x] Architecture: Git's local-first model as reference
- [x] Prior Research: Topic 1 (Source of Truth) findings
- [x] Prior Research: Topic 2 (Delete Architecture) findings

---

## 🔑 Sub-Questions

1. **Command Classification:** What commands work offline vs require API?
2. **Detection vs Config:** How is offline mode detected vs configured?
3. **Online Transition:** What happens when going from offline → online?
4. **Explicit Flag:** Should there be a `--offline` flag for all commands?
5. **Local-First Dev:** What's the MVP local experience before API integration?

---

## 📊 Findings

### Finding 1: Current Command API Dependency Audit

Comprehensive audit of all proj-cli commands for API dependency:

**Commands That Work Locally (No API Required):**

| Command | Description | Notes |
|---------|-------------|-------|
| `proj create --local-only` | Create project from template | Requires `--template` flag |
| `proj inv scan local` | Scan local directories | Fully local |
| `proj inv analyze` | Analyze tech stack | Works on local inventory |
| `proj inv dedupe` | Deduplicate inventory | Local inventory operation |
| `proj inv export json` | Export to JSON file | Local file operation |
| `proj inv status` | Show inventory status | Local inventory stats |

**Commands That Require API:**

| Command | Description | Why API Required |
|---------|-------------|------------------|
| `proj list` | List projects | Fetches from API |
| `proj get` | Get project details | Fetches from API |
| `proj create` (default) | Create project | Creates in API first |
| `proj update` | Update project | Updates API record |
| `proj delete` | Delete project | Deletes from API |
| `proj archive` | Archive project | Updates API status |
| `proj inv export api` | Push to API | Obvious |

**Commands That Need External Network (Not work-prod):**

| Command | Description | External Dependency |
|---------|-------------|---------------------|
| `proj inv scan github` | Scan GitHub repos | GitHub API |

**Source:** Codebase audit of `src/proj/commands/`

**Relevance:** Defines the boundary between local and API operations.

---

### Finding 2: Registry is 100% Local

The registry (`registry.py`) is fully local with no API dependencies:

```python
# All registry operations are local:
load_registry()         # Local file read
save_registry()         # Local file write
add_project()           # Local only
remove_project()        # Local only
get_project_by_path()   # Local lookup
list_projects()         # Local list
is_registered()         # Local check
update_project_work_prod_id()  # Local update (stores API ID)
```

The `work_prod_id` field is the **only** connection to API - it stores the API ID after sync but doesn't require API to function.

**Source:** `src/proj/registry.py` analysis

**Relevance:** Registry is the foundation for local-first operation.

---

### Finding 3: Git's Local-First Model as Reference

Git's architecture is the gold standard for local-first CLI design:

| Git Concept | proj-cli Equivalent | Current State |
|-------------|---------------------|---------------|
| Local commits | Local registry entries | ✅ Implemented |
| `git push` | `proj sync` (proposed) | ❌ Missing |
| `git pull` | `proj sync` (proposed) | ❌ Missing |
| Working directory | Project files | ✅ Unchanged |
| Remote tracking | `work_prod_id` field | ✅ Implemented |

**Key Principles from Git:**
1. **All operations work locally first** - Then sync when ready
2. **Explicit sync commands** - User controls when to push/pull
3. **Offline is the default** - Network is opt-in, not required
4. **Conflict handling** - Detected at sync time, not operation time

**Source:** Git architecture analysis

**Relevance:** Provides proven model for local-first CLI design.

---

### Finding 4: Current Gaps for "Fully Functional Local"

To have a fully functional local experience, these gaps exist:

| Gap | Description | Priority |
|-----|-------------|----------|
| **No local list** | `proj list` only shows API projects | High |
| **No local get** | `proj get` only fetches from API | High |
| **No local delete** | `proj delete` only removes from API | High (Topic 2) |
| **No registry list command** | Can't see registered projects | Medium |
| **No sync command** | Can't push local → API on demand | Medium |

**What "Fully Functional Local" Means:**

1. **Create** → Works locally with `--local-only` ✅
2. **List** → Should show local registry projects ❌ (Gap)
3. **Get** → Should show local project details ❌ (Gap)
4. **Delete** → Should clean up local registry ❌ (Gap, Topic 2)
5. **Sync** → Should push local to API when ready ❌ (Gap)

**Source:** Codebase analysis + Topic 2 findings

**Relevance:** Defines MVP for local-first development phase.

---

### Finding 5: Config Already Supports Offline

The config has `api_enabled` flag that can disable API:

```python
# From create.py
if not local_only and config.api_enabled:
    # Sync to API
    ...
elif not config.api_enabled:
    console.print("[dim]ℹ Skipped API sync (api_enabled=False)[/dim]")
```

This pattern could be extended to all commands for consistent offline handling.

**Source:** `src/proj/commands/projects/create.py` lines 436-458

**Relevance:** Pattern exists for disabling API - can be generalized.

---

### Finding 6: Detection vs Explicit Configuration

**Current Behavior:**
- `api_enabled` in config controls API usage globally
- `--local-only` flag on create command for per-command control
- No automatic network detection

**Recommended Approach:**
1. **Auto-detect** when API is unreachable (graceful degradation)
2. **Config flag** for explicit offline mode (`api_enabled: false`)
3. **Per-command flags** for override (`--local-only`, `--api-only`)

**Detection Priority:**
1. Per-command flag (highest priority)
2. Config setting
3. Auto-detection (fallback)

**Source:** Best practices analysis

**Relevance:** Defines how offline mode should be triggered.

---

## 🔍 Analysis

### The Local-First Development Approach

Based on findings, proj-cli should adopt a **local-first development strategy**:

**Phase 1: Complete Local Operations (No API Required)**
1. Registry CRUD - Create, List, Get, Delete locally
2. Inventory operations - Already complete
3. Template creation - Already works with `--local-only`

**Phase 2: Add Sync Layer**
1. `proj sync` command - Push local → API
2. `proj sync --pull` - Pull API → local (for completeness)
3. Conflict detection and resolution

**Phase 3: API-First Commands as Enhancement**
1. Keep existing API commands for power users
2. API becomes "sync target" not "primary source"

### Command Mode Matrix

| Command | Default Mode | With `--local` | With `--api` |
|---------|--------------|----------------|--------------|
| `proj create` | Template → sync | Template only | API only |
| `proj list` | Both sources | Registry only | API only |
| `proj get` | Prefer local | Registry only | API only |
| `proj delete` | Cascade (Topic 2) | Registry only | API only |
| `proj sync` | Push local→API | N/A | N/A |

### Offline Transition Behavior

**When going offline → online:**
1. Detect API availability on command start
2. Queue operations if offline (future enhancement)
3. Offer sync prompt: "X projects created offline. Sync now?"

**For MVP:**
- Just fail gracefully with clear message when API unavailable
- Suggest using `--local` flag or `api_enabled: false`

**Key Insights:**
- [x] Insight 1: Registry provides 100% local foundation - just need commands to expose it
- [x] Insight 2: Git's local-first model is the right pattern for proj-cli
- [x] Insight 3: Config already has `api_enabled` - extend pattern to all commands
- [x] Insight 4: "Fully functional local" = registry CRUD + inventory + template create
- [x] Insight 5: Development should sequence: Local complete → Sync layer → API enhancement

---

## 💡 Recommendations

- [x] Recommendation 1: **Add `proj registry list` command** - Show all registered projects (local)
- [x] Recommendation 2: **Add `proj list --local` flag** - Show registry projects instead of API
- [x] Recommendation 3: **Add `proj get --local` behavior** - Prefer registry data, fallback to API
- [x] Recommendation 4: **Implement Topic 2 delete refactor** - Cascade to registry (local cleanup)
- [x] Recommendation 5: **Add `proj sync` command** - Explicit push of local projects to API
- [x] Recommendation 6: **Generalize `api_enabled` config** - Consistent offline handling across commands
- [x] Recommendation 7: **Auto-detect API availability** - Graceful degradation on network failure
- [x] Recommendation 8: **Sequence development local-first** - Complete local CRUD before API features

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-OFF-1:** CLI shall provide `--local` flag on list/get commands to show registry data
- [x] **FR-OFF-2:** CLI shall provide `proj registry list` to show all registered projects
- [x] **FR-OFF-3:** CLI shall detect API unavailability and suggest local alternatives
- [x] **FR-OFF-4:** CLI shall provide `proj sync` command to push local projects to API
- [x] **FR-OFF-5:** Registry operations shall work without any network access

### Non-Functional Requirements

- [x] **NFR-OFF-1:** Local operations shall complete without network latency
- [x] **NFR-OFF-2:** CLI shall fail gracefully with clear message when API unavailable
- [x] **NFR-OFF-3:** Offline mode shall be configurable via `api_enabled` config
- [x] **NFR-OFF-4:** Per-command flags (`--local`, `--api`) shall override config setting

### Development Sequencing Requirements

- [x] **DEV-OFF-1:** Local CRUD operations shall be implemented before API enhancements
- [x] **DEV-OFF-2:** All local operations shall be testable without API mock
- [x] **DEV-OFF-3:** Sync layer shall be added after local operations are complete

---

## 🚀 Next Steps

1. ✅ Research complete
2. Consider Topic 5 (Registry Commands) for registry list/status implementation
3. Use Topic 2 (Delete Architecture) for local delete cleanup
4. Use `/decision work-prod-integration --from-research` when all topics complete

---

## 📊 Local-First Development Checklist

Use this checklist to track "fully functional local" implementation:

**Phase 1: Local CRUD (MVP)**
- [ ] `proj registry list` - List registered projects
- [ ] `proj registry get <path>` - Get project details from registry
- [ ] `proj delete --registry-only` - Clean up registry (Topic 2)
- [ ] `proj create --local-only` - Already works ✅

**Phase 2: Unified Commands with Local Mode**
- [ ] `proj list --local` - Show registry projects
- [ ] `proj get --local <id>` - Prefer registry data
- [ ] `proj delete` cascade - Auto-clean registry (Topic 2)

**Phase 3: Sync Layer**
- [ ] `proj sync` - Push unsynced projects to API
- [ ] `proj sync --status` - Show sync state
- [ ] Auto-sync on create (current behavior, keep optional)

---

**Last Updated:** 2026-01-09
