# Research: Registry Command Design

**Research Topic:** Work-Prod Integration  
**Question:** What commands should be available for registry management?  
**Status:** ✅ Complete  
**Priority:** 🟡 Medium  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09

---

## 🎯 Research Question

What commands should be available for registry management?

**Context:** Users need tools to manage local registry (cleanup, inspect, sync).

**Prior Research:**
- Topic 1: Registry is sync overlay, not data store
- Topic 3: `proj sync` command for push to API
- Topic 4: `proj registry list` for local-first visibility

---

## 🔍 Research Goals

- [x] Goal 1: Define minimal useful set of registry commands
- [x] Goal 2: Design command structure (subcommand vs flags)
- [x] Goal 3: Determine registry-API interaction patterns
- [x] Goal 4: Research CLI subcommand organization patterns

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase: Current registry implementation (`src/proj/registry.py`)
- [x] Codebase: CLI structure pattern (`src/proj/cli.py`)
- [x] Prior research: Topics 1, 3, 4 findings
- [x] CLI patterns: Docker, npm, git subcommand design

---

## 🔑 Sub-Questions

1. **Minimal Set:** What's the minimal useful set of registry commands?
2. **Command Structure:** Should registry have its own subcommand (`proj registry list`)?
3. **API Interaction:** How should registry commands interact with API?

---

## 📊 Findings

### Finding 1: Current Registry Functions Available

The `registry.py` module provides these functions ready to expose:

| Function | Purpose | CLI Mapping |
|----------|---------|-------------|
| `list_projects(template=None)` | List all/filtered projects | `proj registry list` |
| `get_project_by_path(path)` | Get single project | `proj registry get` |
| `remove_project(path)` | Remove from registry | `proj registry remove` |
| `is_registered(path)` | Check if registered | (internal use) |
| `add_project(...)` | Add to registry | (via `proj create`) |
| `update_project_work_prod_id(...)` | Update API ID | (via `proj sync`) |

**Missing functions needed (from Topic 2):**
- `get_project_by_work_prod_id()` - Find by API ID

**Source:** `src/proj/registry.py`

**Relevance:** Most CLI commands can be thin wrappers around existing functions.

---

### Finding 2: CLI Structure Pattern

proj-cli uses Typer subcommand groups:

```python
# Current structure
app = typer.Typer(name="proj")
app.command(name="list")(...)      # proj list
app.command(name="create")(...)    # proj create
app.add_typer(inv_app, name="inv") # proj inv scan, proj inv analyze
```

**Pattern for registry:**

```python
# Proposed structure
registry_app = typer.Typer(name="registry", help="Manage local project registry.")
app.add_typer(registry_app, name="registry")  # proj registry list, etc.
```

**Source:** `src/proj/cli.py`

**Relevance:** Follows established pattern - consistent UX.

---

### Finding 3: Sync Command Placement Decision

From Topic 3 and Topic 4 research, there's overlap:

| Command | Location Options | Recommendation |
|---------|------------------|----------------|
| `proj sync` | Top-level | ✅ Primary (Topic 3) |
| `proj registry sync` | Subcommand | ❌ Redundant |
| `proj sync --status` | Flag | ✅ Keep with sync |
| `proj registry status` | Subcommand | 🟡 Optional alias |

**Decision:** Keep `proj sync` at top level (per Topic 3), don't duplicate as `proj registry sync`.

**Source:** Topic 3 Sync Strategy research

**Relevance:** Avoids command duplication and confusion.

---

### Finding 4: Minimal Useful Command Set

Based on user workflows and local-first needs (Topic 4):

**Essential Commands:**

| Command | Purpose | Use Case |
|---------|---------|----------|
| `proj registry list` | List registered projects | "What's in my registry?" |
| `proj registry get <path>` | Show project details | "What's the sync state of X?" |
| `proj registry remove <path>` | Remove from registry | "Clean up orphaned entry" |

**Already Covered Elsewhere:**

| Need | Covered By |
|------|------------|
| Sync to API | `proj sync` (Topic 3) |
| Sync status | `proj sync --status` (Topic 3) |
| Add to registry | `proj create --template` |

**Optional (Low Priority):**

| Command | Purpose | Priority |
|---------|---------|----------|
| `proj registry clean` | Remove orphaned entries | Low |
| `proj registry rebuild` | Rebuild from API | Low |

**Source:** User workflow analysis + prior research

**Relevance:** Focus on essential commands first.

---

### Finding 5: Output Format Design

Following `proj list` and `proj inv` patterns:

**`proj registry list` output:**

```
📋 Registry: 5 projects

  Path                          Template          Synced    Created
  ~/Projects/my-app             standard-project  ✅ ID:42  2026-01-08
  ~/Projects/test-proj          standard-project  ✅ ID:43  2026-01-07
  ~/Projects/new-experiment     learning-project  ⚠️ No     2026-01-09
  ~/Projects/old-project        standard-project  ✅ ID:12  2025-12-15
  ~/Projects/quick-test         standard-project  ⚠️ No     2026-01-09

💡 2 projects not synced. Run 'proj sync' to push to API.
```

**`proj registry get ~/Projects/my-app` output:**

```
📋 Registry Entry

  Path:             ~/Projects/my-app
  Template:         standard-project
  Template Version: unknown
  Created:          2026-01-08 10:30:45
  Sync Status:      ✅ Synced
  API ID:           42
```

**Flags:**
- `--format json` - JSON output
- `--template <type>` - Filter by template type
- `--unsynced` - Show only unsynced projects

**Source:** proj-cli output conventions

**Relevance:** Consistent UX across commands.

---

### Finding 6: API Interaction Pattern

Registry commands should be **local-only** by default:

| Command | API Interaction | Notes |
|---------|-----------------|-------|
| `proj registry list` | ❌ None | Pure local |
| `proj registry get` | ❌ None | Pure local |
| `proj registry remove` | ❌ None | Registry only (no API delete) |
| `proj registry clean` | 🟡 Optional | Could verify API exists |

**Key distinction:**
- `proj registry remove` - Only removes from registry (local cleanup)
- `proj delete` - Full delete (API + registry + optional files, per Topic 2)

**Source:** Topic 1 (API is truth) + Topic 4 (local-first)

**Relevance:** Clear separation of local vs API operations.

---

## 🔍 Analysis

### Command Hierarchy

```
proj
├── registry                    # Registry management (NEW)
│   ├── list                    # List registered projects
│   ├── get <path>              # Show project details  
│   └── remove <path>           # Remove from registry
├── sync                        # Push to API (from Topic 3)
│   └── --status                # Show sync status
├── create                      # Creates + registers
├── delete                      # Full delete (API + registry)
└── inv                         # Inventory commands (existing)
```

### Registry vs Sync Separation

| Concern | Command | Scope |
|---------|---------|-------|
| **Local registry management** | `proj registry *` | Registry only |
| **API synchronization** | `proj sync` | Registry → API |
| **Full project delete** | `proj delete` | API + Registry + Files |

### Implementation Priority

1. **Phase 1 (MVP):** `list`, `get`, `remove` - Essential for local-first
2. **Phase 2:** `clean` - Orphan detection and cleanup
3. **Phase 3:** `rebuild` - Full registry reconstruction from API

**Key Insights:**
- [x] Insight 1: Registry functions already exist - commands are thin wrappers
- [x] Insight 2: Follow `inv` subcommand pattern for consistency
- [x] Insight 3: Keep registry commands local-only (no API calls)
- [x] Insight 4: Sync belongs at top level, not under registry
- [x] Insight 5: Three essential commands cover most use cases

---

## 💡 Recommendations

- [x] Recommendation 1: **Create `proj registry` subcommand group** - Follow inv pattern
- [x] Recommendation 2: **Implement 3 essential commands** - list, get, remove
- [x] Recommendation 3: **Keep registry commands local-only** - No API calls
- [x] Recommendation 4: **Don't duplicate sync** - Keep `proj sync` at top level
- [x] Recommendation 5: **Add filter flags** - `--template`, `--unsynced`
- [x] Recommendation 6: **Support JSON output** - `--format json`
- [x] Recommendation 7: **Clear distinction** - `registry remove` ≠ `delete`

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-REG-1:** CLI shall provide `proj registry list` to show all registered projects
- [x] **FR-REG-2:** CLI shall provide `proj registry get <path>` to show project details
- [x] **FR-REG-3:** CLI shall provide `proj registry remove <path>` to remove from registry only
- [x] **FR-REG-4:** `proj registry list` shall support `--template <type>` filter
- [x] **FR-REG-5:** `proj registry list` shall support `--unsynced` filter
- [x] **FR-REG-6:** All registry commands shall support `--format json` output

### Non-Functional Requirements

- [x] **NFR-REG-1:** Registry commands shall not make API calls (local-only)
- [x] **NFR-REG-2:** Registry list shall show sync status for each project
- [x] **NFR-REG-3:** Registry commands shall follow existing CLI output patterns

### Constraints

- [x] **C-REG-1:** `proj registry remove` shall NOT delete from API (use `proj delete` for that)
- [x] **C-REG-2:** `proj registry sync` shall NOT exist (use `proj sync` instead)

---

## 🚀 Next Steps

1. ✅ Research complete
2. Implement `proj registry` subcommand group
3. Add `list`, `get`, `remove` commands
4. Use findings in `/decision work-prod-integration --from-research`

---

## 📊 Command Reference

### `proj registry list`

```
proj registry list [OPTIONS]

List all projects in the local registry.

Options:
  --template TEXT    Filter by template type (e.g., standard-project)
  --unsynced         Show only unsynced projects
  --format TEXT      Output format: table (default), json
  --help             Show this message and exit

Examples:
  proj registry list                           # All projects
  proj registry list --template learning-project
  proj registry list --unsynced                # Only unsynced
  proj registry list --format json             # JSON output
```

### `proj registry get`

```
proj registry get PATH [OPTIONS]

Show details for a registered project.

Arguments:
  PATH    Project path (absolute or relative)

Options:
  --format TEXT      Output format: table (default), json
  --help             Show this message and exit

Examples:
  proj registry get ~/Projects/my-app
  proj registry get . --format json
```

### `proj registry remove`

```
proj registry remove PATH [OPTIONS]

Remove a project from the local registry.

NOTE: This only removes from registry. Does NOT delete from API.
Use 'proj delete' for full deletion (API + registry + optional files).

Arguments:
  PATH    Project path to remove

Options:
  --force, -f        Skip confirmation
  --help             Show this message and exit

Examples:
  proj registry remove ~/Projects/old-project
  proj registry remove ~/Projects/old-project --force
```

---

**Last Updated:** 2026-01-09
