# Research: Delete Command Architecture

**Research Topic:** Work-Prod Integration  
**Question:** How should `proj delete` handle API, registry, and filesystem cleanup?  
**Status:** ✅ Complete  
**Priority:** 🔴 High  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08  
**Completed:** 2026-01-08

---

## 🎯 Research Question

How should `proj delete` handle API, registry, and filesystem cleanup?

**Current Gap:** Delete only removes from API, leaving orphaned registry entries.

---

## 🔍 Research Goals

- [x] Goal 1: Design comprehensive delete workflow (API + registry + filesystem)
- [x] Goal 2: Determine flag vs automatic cascade behavior
- [x] Goal 3: Research CLI patterns for multi-target delete operations
- [x] Goal 4: Consider safety and undo mechanisms

---

## 📚 Research Methodology

**Sources:**

- [x] Web search: CLI delete command patterns and best practices
- [x] Codebase analysis: Current `proj delete` implementation
- [x] Case studies: Docker, kubectl, npm, git (multi-target delete commands)
- [x] User experience: What workflow makes sense for proj-cli users

---

## 🔑 Sub-Questions

1. **Flags vs Automatic:** Should delete require explicit flags (`--from-api`, `--from-registry`) or automatically cascade?
2. **Identifier Types:** Should delete accept both ID and path as identifiers?
3. **Cascade Order:** How should delete handle cascade (API → registry → filesystem)?
4. **Registry-Only Projects:** What about projects that exist only in registry (never synced)?
5. **Safety:** Should there be a `--dry-run` or confirmation prompt?

---

## 📊 Findings

### Finding 1: Current Implementation Only Deletes from API

The current `proj delete` command (in `crud.py` lines 112-131):

```python
def delete_project(
    project_id: int = typer.Argument(..., help="Project ID"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """Delete a project permanently."""
    # Only calls client.delete_project(project_id)
    # No registry cleanup
```

**Issues:**

- Only accepts integer API ID (not path)
- Only deletes from API
- Registry entries become orphaned
- No way to delete registry-only projects

**Source:** Codebase analysis (`proj-cli/src/proj/commands/projects/crud.py`)

**Relevance:** Confirms the gap and shows exactly what needs to change.

---

### Finding 2: Registry Infrastructure Already Exists

The registry module (`registry.py` lines 165-186) already has removal capability:

```python
def remove_project(path: Path) -> bool:
    """Remove a project from the registry by path."""
    # Removes by path, returns True if found

def get_project_by_path(path: Path) -> Optional[RegistryProject]:
    """Find a project by its path."""
```

**Gap Identified:** No `get_project_by_work_prod_id()` function exists. To clean up registry when deleting by API ID, we need to find the registry entry by its `work_prod_id` link.

**Source:** Codebase analysis (`proj-cli/src/proj/registry.py`)

**Relevance:** Infrastructure exists, just needs a new lookup function and integration into delete command.

---

### Finding 3: CLI Tool Patterns Analysis

| Tool             | Identifier        | Cascade             | Confirmation        | Flags                               |
| ---------------- | ----------------- | ------------------- | ------------------- | ----------------------------------- |
| `docker rm`      | Container ID/name | Container only      | No (unless running) | `--force`, `--volumes`              |
| `kubectl delete` | Type/name or file | Cascades by default | No                  | `--force`, `--dry-run`, `--cascade` |
| `git rm`         | File path         | Index + filesystem  | No                  | `--force`, `--cached`               |
| `npm uninstall`  | Package name      | Dependencies        | No                  | `--save-dev`                        |
| `rm` (unix)      | File path         | Single target       | No                  | `-f`, `-r`, `-i`                    |

**Key Patterns:**

- **Most CLIs cascade by default** - `kubectl delete` removes pod + service + etc.
- **Flags limit scope** - `--cached` in git rm means "only index, not filesystem"
- **Force skips confirmation** - Universal pattern
- **Dry-run for safety** - `kubectl delete --dry-run` is common

**Source:** CLI tool documentation analysis

**Relevance:** Suggests automatic cascade is the expected behavior, with flags to limit scope.

---

### Finding 4: Project Lifecycle States

Analysis of possible project states reveals four scenarios:

| State                     | API | Registry | Filesystem | Delete Behavior                   |
| ------------------------- | --- | -------- | ---------- | --------------------------------- |
| **API-only**              | ✅  | ❌       | ❌         | Delete from API only              |
| **Template (synced)**     | ✅  | ✅       | ✅         | Delete from API, cleanup registry |
| **Template (local-only)** | ❌  | ✅       | ✅         | Delete from registry only         |
| **Orphaned**              | ❌  | ✅       | ❌         | Registry cleanup only             |

**Source:** Architectural analysis based on Topic 1 findings

**Relevance:** Delete must handle all four states gracefully.

---

### Finding 5: Identifier Resolution Strategy

Users may want to delete by:

1. **API ID** - `proj delete 42` (current behavior)
2. **Project path** - `proj delete ~/Projects/my-app`
3. **Project name** - `proj delete --name my-app`

**Usability Consideration:** While name-based deletion can be ambiguous, lack of usability is itself a security/bug risk. Users are more likely to remember project names than IDs, and typing full paths is cumbersome.

**Resolution Order (proposed):**

1. If `--name` flag provided → force name search (skip path/ID detection)
2. If argument is numeric → treat as API ID
3. If argument contains `/` or path exists on filesystem → Path lookup
4. **Otherwise → Automatic name search** (with disambiguation if needed)

**Automatic Name Resolution:**

When the identifier doesn't look like an ID or path, we automatically try name search:
- `proj delete my-app` → searches for projects named "my-app"
- `proj delete 42` → deletes API ID 42 (numeric = ID)
- `proj delete ./my-app` → deletes by path (contains `/`)
- `proj delete ~/Projects/foo` → deletes by path (exists on disk)

**Name-Based Deletion Safety:**

- Use existing search/filter API to find projects by name
- If exactly 1 match → proceed with confirmation
- If multiple matches → show list and require user to pick (interactive) or use ID/path
- If no matches → error with suggestions

**`--name` Flag Purpose:**

The `--name` flag is optional but useful for:
- Forcing name interpretation when name looks like a path (e.g., `proj delete --name path/like-name`)
- Explicitness when desired

**Source:** UX analysis + usability consideration

**Relevance:** Automatic name fallback provides intuitive UX without sacrificing safety.

---

### Finding 6: Filesystem Deletion is Dangerous

Filesystem deletion should be:

- **Opt-in only** - Never delete files automatically
- **Explicit flag required** - `--delete-files` or `--rm-local`
- **Separate confirmation** - Extra warning for filesystem deletion

**Pattern from other tools:**

- `kubectl delete` never touches local files
- `git rm` only affects tracked files, not the directory
- `docker rm` only removes container, not volumes (unless `--volumes`)

**Source:** CLI safety pattern analysis

**Relevance:** Filesystem deletion should be a separate, explicit action.

---

## 🔍 Analysis

### Recommended Delete Architecture

Based on findings, the recommended approach is **Automatic Cascade with Scope Flags**:

```
proj delete <identifier>
  │
  ├── Resolve identifier (ID or path)
  │
  ├── Delete from API (if synced)
  │
  └── Delete from registry (if registered)
      │
      └── [only if --delete-files] Delete filesystem
```

### Flag Design

| Flag              | Purpose                                          | Default |
| ----------------- | ------------------------------------------------ | ------- |
| `--force` / `-f`  | Skip confirmation                                | Off     |
| `--dry-run`       | Preview what would be deleted                    | Off     |
| `--name` / `-n`   | Force name search (skip ID/path auto-detection)  | Off     |
| `--api-only`      | Only delete from API (don't touch registry)      | Off     |
| `--registry-only` | Only delete from registry (don't touch API)      | Off     |
| `--delete-files`  | Also delete local filesystem                     | Off     |

### Identifier Resolution

```python
def resolve_identifier(identifier: str, force_name: bool = False) -> DeleteTarget:
    # 1. If --name flag, force name search (skip other detection)
    if force_name:
        return _search_by_name(identifier)

    # 2. Check if numeric (API ID)
    if identifier.isdigit():
        return DeleteTarget(api_id=int(identifier))

    # 3. Check if it looks like a path (contains / or exists on disk)
    if "/" in identifier or Path(identifier).exists():
        path = Path(identifier).resolve()
        registry_entry = get_project_by_path(path)
        if registry_entry:
            return DeleteTarget(
                path=path,
                api_id=registry_entry.work_prod_id,  # May be None
            )
        # Path specified but not in registry
        raise NotFoundError(f"No project registered at: {path}")

    # 4. Automatic name fallback - try searching by name
    return _search_by_name(identifier)


def _search_by_name(name: str) -> DeleteTarget:
    """Search for project by name with disambiguation."""
    matches = client.list_projects(search=name)
    # Filter to exact name matches (case-insensitive)
    exact = [p for p in matches if p["name"].lower() == name.lower()]

    if len(exact) == 0:
        raise NotFoundError(f"No project found with name: {name}")
    elif len(exact) == 1:
        project = exact[0]
        return DeleteTarget(
            api_id=project["id"],
            path=Path(project["path"]) if project.get("path") else None,
            name=project["name"],
        )
    else:
        # Multiple matches - require disambiguation
        raise AmbiguousNameError(
            f"Multiple projects match '{name}':",
            matches=exact
        )
```

### Missing Infrastructure

Need to add to `registry.py`:

```python
def get_project_by_work_prod_id(work_prod_id: int) -> Optional[RegistryProject]:
    """Find a project by its work_prod_id link."""
    registry = load_registry()
    for project in registry.projects:
        if project.work_prod_id == work_prod_id:
            return project
    return None

def remove_project_by_work_prod_id(work_prod_id: int) -> bool:
    """Remove a project from registry by its API ID link."""
    project = get_project_by_work_prod_id(work_prod_id)
    if project:
        return remove_project(project.path)
    return False
```

**Key Insights:**

- [x] Insight 1: Automatic cascade to registry is expected behavior (matches kubectl pattern)
- [x] Insight 2: Filesystem deletion must be opt-in only (safety critical)
- [x] Insight 3: Path-based identifier would improve UX for template projects
- [x] Insight 4: Need `get_project_by_work_prod_id()` function in registry
- [x] Insight 5: Automatic name fallback improves usability; disambiguation handles safety

---

## 💡 Recommendations

- [x] Recommendation 1: **Automatic cascade** - API delete should automatically clean up registry entry
- [x] Recommendation 2: **Add path identifier** - Accept both API ID and project path as arguments
- [x] Recommendation 3: **Add `--dry-run`** - Preview what would be deleted before committing
- [x] Recommendation 4: **Filesystem opt-in** - Add `--delete-files` flag (off by default, extra confirmation)
- [x] Recommendation 5: **Add scope flags** - `--api-only` and `--registry-only` for limiting scope
- [x] Recommendation 6: **Add registry lookup** - Implement `get_project_by_work_prod_id()` function
- [x] Recommendation 7: **Add name identifier** - Support `--name` flag with disambiguation for multiple matches

---

## 📋 Requirements Discovered

### Functional Requirements

- [x] **FR-DEL-1:** Delete shall automatically remove from both API and registry when both exist
- [x] **FR-DEL-2:** Delete shall accept API ID, project path, or project name as identifier
- [x] **FR-DEL-3:** Delete shall support `--dry-run` to preview deletion targets
- [x] **FR-DEL-4:** Delete shall support `--delete-files` for filesystem cleanup (opt-in)
- [x] **FR-DEL-5:** Delete shall support `--api-only` to skip registry cleanup
- [x] **FR-DEL-6:** Delete shall support `--registry-only` to skip API deletion
- [x] **FR-DEL-7:** Registry shall provide `get_project_by_work_prod_id()` lookup function
- [x] **FR-DEL-8:** Delete shall handle all four project states (API-only, synced, local-only, orphaned)
- [x] **FR-DEL-9:** Delete by name (`--name`) shall require disambiguation when multiple projects match

### Non-Functional Requirements

- [x] **NFR-DEL-1:** Filesystem deletion shall require explicit flag AND confirmation
- [x] **NFR-DEL-2:** Delete shall fail gracefully if API is unavailable (registry-only cleanup still works)
- [x] **NFR-DEL-3:** Delete output shall clearly indicate what was deleted from each target

### Constraints

- [x] **C-DEL-1:** Cannot delete filesystem without explicit `--delete-files` flag
- [x] **C-DEL-2:** Current `--force` flag behavior must be preserved (confirmation skip)

---

## 🚀 Next Steps

1. ✅ Research complete
2. Implement `get_project_by_work_prod_id()` in registry.py
3. Refactor `delete_project()` command with new architecture
4. Add tests for all four project states
5. Update documentation

---

## 📝 Implementation Sketch

```python
def delete_project(
    identifier: str = typer.Argument(..., help="Project ID, path, or name"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview deletion"),
    force_name: bool = typer.Option(False, "--name", "-n", help="Force name search"),
    api_only: bool = typer.Option(False, "--api-only", help="Only delete from API"),
    registry_only: bool = typer.Option(False, "--registry-only", help="Only delete from registry"),
    delete_files: bool = typer.Option(False, "--delete-files", help="Also delete local files"),
):
    """Delete a project from API and/or registry.
    
    Identifier resolution:
    - Numeric → API ID (e.g., 42)
    - Contains / or exists → Path (e.g., ~/Projects/foo)
    - Otherwise → Name search (e.g., my-app)
    
    Use --name to force name search when identifier looks like a path.
    """

    # 1. Resolve identifier (auto-detects ID, path, or name)
    try:
        target = resolve_identifier(identifier, force_name=force_name)
    except AmbiguousNameError as e:
        console.print(f"[yellow]{e.message}[/yellow]")
        for p in e.matches:
            console.print(f"  • ID {p['id']}: {p['name']} ({p.get('path', 'no path')})")
        console.print("\n[dim]Use ID or path to specify which project to delete.[/dim]")
        raise typer.Exit(1)

    # 2. Determine what to delete
    will_delete_api = target.api_id and not registry_only
    will_delete_registry = target.path and not api_only
    will_delete_files = delete_files and target.path

    # 3. Dry run output
    if dry_run:
        console.print("[bold]Would delete:[/bold]")
        if will_delete_api:
            console.print(f"  • API: project {target.api_id}")
        if will_delete_registry:
            console.print(f"  • Registry: {target.path}")
        if will_delete_files:
            console.print(f"  • Files: {target.path}")
        return

    # 4. Confirmation
    if not force:
        confirm = typer.confirm("Proceed with deletion?")
        if not confirm:
            raise typer.Abort()

    # 5. Extra confirmation for filesystem
    if will_delete_files and not force:
        confirm = typer.confirm("⚠️  Also delete local files? This cannot be undone!")
        if not confirm:
            will_delete_files = False

    # 6. Execute deletions
    if will_delete_api:
        client.delete_project(target.api_id)
        console.print(f"[green]✓ Deleted from API: {target.api_id}[/green]")

    if will_delete_registry:
        remove_project(target.path)
        console.print(f"[green]✓ Removed from registry: {target.path}[/green]")

    if will_delete_files:
        shutil.rmtree(target.path)
        console.print(f"[green]✓ Deleted files: {target.path}[/green]")
```

---

**Last Updated:** 2026-01-08
