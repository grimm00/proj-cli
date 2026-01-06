# Template Generation - Phase 6: API Sync Enhancement

**Phase:** 6 - API Sync Enhancement  
**Duration:** ~2-3 hours (estimated)  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 4 complete, Phase 5 Tasks 1-4 complete  
**Last Updated:** 2026-01-06

---

## 📋 Overview

Add API synchronization to template creation flow. Currently, `proj create --template` only creates locally and registers in the local registry. This phase adds the ability to also create a corresponding record in the work-prod API, linking local and remote records.

**Gap Identified:** Template creation doesn't sync to work-prod API - users must manually create API records or use separate commands.

**Success Definition:** Template creation can optionally sync to API, with graceful handling of offline/API-unavailable scenarios.

---

## 🎯 Goals

1. **API Integration:** Call work-prod API after successful template creation
2. **Registry Linking:** Store `work_prod_id` in local registry entry
3. **Graceful Degradation:** Handle API errors without failing local creation
4. **User Control:** Respect `--local-only` flag and `api_enabled` config

---

## 📝 Tasks

### Task 1: Registry Schema Update (TDD)

**Purpose:** Add `work_prod_id` field to `RegistryProject` for API linkage.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [x] Test: `RegistryProject` accepts optional `work_prod_id`
   - [x] Test: Registry serializes/deserializes `work_prod_id` correctly
   - [x] Test: `work_prod_id=None` is valid (default)

   **Test file:** `tests/test_registry.py`

   ```python
   def test_registry_project_with_work_prod_id(tmp_path, monkeypatch):
       """Test RegistryProject stores work_prod_id."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       project = add_project(
           path=tmp_path / "test-proj",
           template="standard-project",
           template_version="1.0",
           work_prod_id=42,  # New field
       )

       assert project.work_prod_id == 42

       # Verify it persists
       loaded = get_project_by_path(tmp_path / "test-proj")
       assert loaded.work_prod_id == 42

   def test_registry_project_work_prod_id_optional(tmp_path, monkeypatch):
       """Test work_prod_id is optional (None by default)."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       project = add_project(
           path=tmp_path / "test-proj",
           template="standard-project",
           template_version="1.0",
           # No work_prod_id - should default to None
       )

       assert project.work_prod_id is None

   def test_registry_serializes_work_prod_id(tmp_path, monkeypatch):
       """Test registry.json includes work_prod_id."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       add_project(
           path=tmp_path / "test-proj",
           template="standard-project",
           template_version="1.0",
           work_prod_id=123,
       )

       # Read raw JSON
       registry_path = tmp_path / "proj" / "registry.json"
       import json
       with open(registry_path) as f:
           data = json.load(f)

       assert data["projects"][0]["work_prod_id"] == 123
   ```

2. **GREEN - Implement:**

   - [x] Add `work_prod_id: Optional[int] = None` to `RegistryProject`
   - [x] Update `add_project()` to accept `work_prod_id` parameter
   - [x] Update `save_registry()` to serialize `work_prod_id`
   - [x] Update `load_registry()` to deserialize `work_prod_id`

   **Implementation in `src/proj/registry.py`:**

   ```python
   @dataclass
   class RegistryProject:
       """A project tracked in the registry for template sync."""
       path: Path
       template: str
       template_version: str
       created_at: datetime
       work_prod_id: Optional[int] = None  # Link to work-prod API record
   ```

3. **REFACTOR:**

   - [x] Ensure backward compatibility with existing registry.json files
   - [x] Handle missing `work_prod_id` field gracefully in `load_registry()`

**Checklist:**

- [x] Tests written and passing
- [x] `work_prod_id` field added to `RegistryProject`
- [x] `add_project()` accepts `work_prod_id` parameter
- [x] Serialization/deserialization works correctly
- [x] Backward compatible with existing registry files

---

### Task 2: Update Registry Entry Function (TDD)

**Purpose:** Add function to update `work_prod_id` for existing registry entries.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [x] Test: `update_project_work_prod_id()` updates existing entry
   - [x] Test: Returns `True` if updated, `False` if not found
   - [x] Test: Persists update to disk

   **Test file:** `tests/test_registry.py`

   ```python
   def test_update_project_work_prod_id(tmp_path, monkeypatch):
       """Test updating work_prod_id for existing project."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       project_path = tmp_path / "test-proj"

       # Create project without work_prod_id
       add_project(
           path=project_path,
           template="standard-project",
           template_version="1.0",
       )

       # Update with work_prod_id
       result = update_project_work_prod_id(project_path, 42)

       assert result is True

       # Verify update persisted
       loaded = get_project_by_path(project_path)
       assert loaded.work_prod_id == 42

   def test_update_project_work_prod_id_not_found(tmp_path, monkeypatch):
       """Test update returns False for non-existent project."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       result = update_project_work_prod_id(tmp_path / "non-existent", 42)

       assert result is False
   ```

2. **GREEN - Implement:**

   - [x] Create `update_project_work_prod_id(path: Path, work_prod_id: int) -> bool`
   - [x] Load registry, find project by path, update `work_prod_id`, save

   **Implementation in `src/proj/registry.py`:**

   ```python
   def update_project_work_prod_id(path: Path, work_prod_id: int) -> bool:
       """Update work_prod_id for an existing registry entry.

       Args:
           path: Project path to update
           work_prod_id: API ID to store

       Returns:
           True if project found and updated, False otherwise
       """
       path = path.resolve()
       registry = load_registry()

       for project in registry.projects:
           if project.path == path:
               project.work_prod_id = work_prod_id
               save_registry(registry)
               return True

       return False
   ```

3. **REFACTOR:**

   - [x] Consider combining with `add_project()` logic if appropriate
   - [x] Ensure consistent path normalization

**Checklist:**

- [x] Tests written and passing
- [x] `update_project_work_prod_id()` function implemented
- [x] Updates persist to disk
- [x] Returns correct boolean status

---

### Task 3: API Sync Helper Function (TDD)

**Purpose:** Create a helper function to sync project to API with error handling.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Test: `sync_to_api()` calls `APIClient.create_project()`
   - [ ] Test: Returns `work_prod_id` on success
   - [ ] Test: Returns `None` on API error (doesn't raise)
   - [ ] Test: Returns `None` on connection error (doesn't raise)

   **Test file:** `tests/test_create_api_sync.py` (new file)

   ```python
   import pytest
   from pathlib import Path
   from unittest.mock import Mock, patch

   from proj.commands.projects import sync_to_api
   from proj.error_handler import APIError, BackendConnectionError


   def test_sync_to_api_success():
       """Test sync_to_api returns work_prod_id on success."""
       mock_client = Mock()
       mock_client.create_project.return_value = {"id": 42, "name": "test"}

       result = sync_to_api(
           client=mock_client,
           name="test-project",
           path=Path("/tmp/test"),
           template="standard-project",
           description="Test description",
       )

       assert result == 42
       mock_client.create_project.assert_called_once()

   def test_sync_to_api_connection_error():
       """Test sync_to_api returns None on connection error."""
       mock_client = Mock()
       mock_client.create_project.side_effect = BackendConnectionError("No connection")

       result = sync_to_api(
           client=mock_client,
           name="test-project",
           path=Path("/tmp/test"),
           template="standard-project",
       )

       assert result is None  # No exception raised

   def test_sync_to_api_api_error():
       """Test sync_to_api returns None on API error."""
       mock_client = Mock()
       mock_client.create_project.side_effect = APIError("Server error", 500)

       result = sync_to_api(
           client=mock_client,
           name="test-project",
           path=Path("/tmp/test"),
           template="standard-project",
       )

       assert result is None  # No exception raised
   ```

2. **GREEN - Implement:**

   - [ ] Create `sync_to_api()` helper in `src/proj/commands/projects.py`
   - [ ] Build project data dict from parameters
   - [ ] Call `APIClient.create_project()`
   - [ ] Handle errors gracefully, return `None` on failure

   **Implementation in `src/proj/commands/projects.py`:**

   ```python
   def sync_to_api(
       client: APIClient,
       name: str,
       path: Path,
       template: str,
       description: Optional[str] = None,
       console: Optional[Console] = None,
   ) -> Optional[int]:
       """Sync project to work-prod API.

       Args:
           client: APIClient instance
           name: Project name
           path: Local project path
           template: Template type used
           description: Optional project description
           console: Console for output (optional)

       Returns:
           work_prod_id if successful, None if failed
       """
       try:
           project_data = {
               "name": name,
               "path": str(path),
               "description": description or f"Created from {template} template",
               "status": "active",
           }
           result = client.create_project(project_data)
           return result.get("id")
       except (APIError, BackendConnectionError, TimeoutError) as e:
           if console:
               console.print(
                   f"[yellow]⚠ Could not sync to API: {e}[/yellow]"
               )
           return None
   ```

3. **REFACTOR:**

   - [ ] Ensure error messages are user-friendly
   - [ ] Consider logging for debugging

**Checklist:**

- [ ] Tests written and passing
- [ ] `sync_to_api()` helper implemented
- [ ] Returns `work_prod_id` on success
- [ ] Returns `None` on any error (graceful degradation)
- [ ] Error messages displayed to user

---

### Task 4: Integrate API Sync into Template Flow (TDD)

**Purpose:** Add API sync call to the template creation flow in `create_project` command.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Test: Template creation calls API when `api_enabled=True` and not `--local-only`
   - [ ] Test: Template creation skips API when `--local-only`
   - [ ] Test: Template creation skips API when `api_enabled=False`
   - [ ] Test: Registry updated with `work_prod_id` on successful API sync
   - [ ] Test: Local creation succeeds even if API fails

   **Test file:** `tests/test_create_api_sync.py`

   ```python
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   def test_template_create_syncs_to_api(tmp_path, monkeypatch):
       """Test template creation syncs to API when enabled."""
       # Setup mocks
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
       monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

       # Mock API client
       with patch("proj.commands.projects.APIClient") as MockClient:
           mock_instance = MockClient.return_value
           mock_instance.create_project.return_value = {"id": 99, "name": "test"}

           # Create config with api_enabled=True
           config_dir = tmp_path / "proj"
           config_dir.mkdir(parents=True)
           (config_dir / "config.yaml").write_text(
               "api_url: http://localhost:5000\n"
               "api_enabled: true\n"
               f"templates:\n  source: {templates_source}\n"
           )

           result = runner.invoke(app, [
               "create", "test-project",
               "--template", "standard-project",
               "--target-dir", str(tmp_path / "projects"),
               "--no-git",
           ])

           assert result.exit_code == 0
           mock_instance.create_project.assert_called_once()

   def test_template_create_skips_api_when_local_only(tmp_path, monkeypatch):
       """Test --local-only skips API sync."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       with patch("proj.commands.projects.APIClient") as MockClient:
           result = runner.invoke(app, [
               "create", "test-project",
               "--template", "standard-project",
               "--local-only",
               "--target-dir", str(tmp_path / "projects"),
               "--no-git",
           ])

           assert result.exit_code == 0
           MockClient.return_value.create_project.assert_not_called()

   def test_template_create_updates_registry_with_work_prod_id(tmp_path, monkeypatch):
       """Test registry entry includes work_prod_id after API sync."""
       monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

       with patch("proj.commands.projects.APIClient") as MockClient:
           mock_instance = MockClient.return_value
           mock_instance.create_project.return_value = {"id": 77, "name": "test"}

           # ... create project ...

           # Check registry
           from proj.registry import get_project_by_path
           project = get_project_by_path(tmp_path / "projects" / "test-project")
           assert project.work_prod_id == 77
   ```

2. **GREEN - Implement:**

   - [ ] Add API sync logic after successful `create_from_template()`
   - [ ] Check `api_enabled` config and `--local-only` flag
   - [ ] Call `sync_to_api()` helper
   - [ ] Update registry with `work_prod_id` via `update_project_work_prod_id()`

   **Implementation in `src/proj/commands/projects.py` (around line 571-591):**

   ```python
   # After successful template creation and registration...

   # Sync to API (unless --local-only or api_enabled=False)
   if not local_only and config.api_enabled:
       from proj.api_client import APIClient
       client = APIClient(config)
       work_prod_id = sync_to_api(
           client=client,
           name=name,
           path=project_path,
           template=template,
           description=description,
           console=console,
       )
       if work_prod_id:
           update_project_work_prod_id(project_path, work_prod_id)
           console.print(
               f"[dim]✓ Synced to API (ID: {work_prod_id})[/dim]"
           )
   elif local_only:
       console.print("[dim]ℹ Skipped API sync (--local-only)[/dim]")
   elif not config.api_enabled:
       console.print("[dim]ℹ Skipped API sync (api_enabled=False)[/dim]")
   ```

3. **REFACTOR:**

   - [ ] Ensure import placement is optimal
   - [ ] Consider moving sync logic to separate function for clarity
   - [ ] Verify output messages are helpful

**Checklist:**

- [ ] Tests written and passing
- [ ] API sync integrated into template flow
- [ ] Respects `--local-only` flag
- [ ] Respects `api_enabled` config
- [ ] Registry updated with `work_prod_id`
- [ ] Clear output messages for user

---

### Task 5: Documentation & Manual Testing

**Purpose:** Update documentation and manual testing guide.

**Implementation:**

1. **Update README.md:**

   - [ ] Document API sync behavior
   - [ ] Explain when sync happens (default) vs when it's skipped
   - [ ] Add examples showing `--local-only` usage

   **Content to add:**

   ````markdown
   ## API Synchronization

   By default, template creation syncs to the work-prod API if:

   - `api_enabled: true` in config (default)
   - `--local-only` flag is NOT used

   This creates a project record in the API and stores the `work_prod_id`
   in the local registry for future sync operations.

   ### Offline Mode

   Use `--local-only` for offline development:

   ```bash
   proj create my-app --template standard-project --local-only
   ```
   ````

   This skips API sync entirely. You can sync later using:

   ```bash
   proj sync my-app  # Future feature
   ```

   ### API Errors

   If the API is unavailable, local creation continues successfully.
   You'll see a warning but the project will be created and registered locally.

   ```

   ```

2. **Update Manual Testing Guide:**

   - [ ] Add scenario: Template + API sync (happy path)
   - [ ] Add scenario: Template + API offline/error
   - [ ] Add scenario: Template + `--local-only` explicit skip

   **Scenarios to add:**

   ````markdown
   ### Scenario 4.20: Template Creation with API Sync

   **Prerequisites:** work-prod backend running, `api_enabled: true`

   **Test:**

   ```bash
   proj create api-test --template standard-project --target-dir /tmp/proj-test --no-git
   ```
   ````

   **Expected:**

   - Project created locally
   - "✓ Synced to API (ID: N)" message shown
   - `proj list` shows project in API

   ***

   ### Scenario 4.21: Template Creation with API Offline

   **Prerequisites:** work-prod backend NOT running

   **Test:**

   ```bash
   proj create offline-test --template standard-project --target-dir /tmp/proj-test --no-git
   ```

   **Expected:**

   - Project created locally (success)
   - "⚠ Could not sync to API: Connection refused" warning
   - Local registry entry created (work_prod_id=null)

   ***

   ### Scenario 4.22: Template Creation with --local-only

   **Test:**

   ```bash
   proj create local-test --template standard-project --local-only --target-dir /tmp/proj-test --no-git
   ```

   **Expected:**

   - Project created locally
   - "ℹ Skipped API sync (--local-only)" message
   - NO API call attempted

   ```

   ```

3. **Update Requirements (if needed):**

   - [ ] Check if new requirements are needed for API sync
   - [ ] Update `requirements.md` if necessary

**Checklist:**

- [ ] README updated with API sync documentation
- [ ] Manual testing guide has new scenarios
- [ ] Requirements reviewed

---

## 📊 Progress Tracking

| Task                                   | Status         | Notes                         |
| -------------------------------------- | -------------- | ----------------------------- |
| Task 1: Registry Schema Update         | ✅ Complete    | Add work_prod_id field        |
| Task 2: Update Registry Entry Function | 🔴 Not Started | update_project_work_prod_id() |
| Task 3: API Sync Helper Function       | 🔴 Not Started | sync_to_api() helper          |
| Task 4: Integrate API Sync             | 🔴 Not Started | Main integration              |
| Task 5: Documentation & Manual Testing | 🔴 Not Started | Docs update                   |

---

## ✅ Completion Criteria

- [ ] `work_prod_id` field added to `RegistryProject`
- [ ] `update_project_work_prod_id()` function implemented
- [ ] `sync_to_api()` helper handles errors gracefully
- [ ] Template creation syncs to API by default (when enabled)
- [ ] `--local-only` skips API sync
- [ ] API errors don't break local creation
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Manual testing scenarios pass
- [ ] PR reviewed and merged

---

## 📦 Deliverables

- Updated `src/proj/registry.py` with `work_prod_id` support
- Updated `src/proj/commands/projects.py` with API sync integration
- New test file `tests/test_create_api_sync.py`
- Updated `tests/test_registry.py` with new tests
- Updated `README.md` with API sync documentation
- Updated `manual-testing.md` with new scenarios

---

## 🔗 Dependencies

### Prerequisites

- Phase 4 complete (template creation working)
- Phase 5 Tasks 1-4 complete (bug fixes, coverage, docs, requirements)

### Blocks

- Phase 5 Tasks 5-6 (manual testing requires Phase 6 complete)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Phase 5 - Testing & Polish](phase-5.md) (paused pending this phase)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)
- [API Client](../../../../src/proj/api_client.py)
- [Registry Module](../../../../src/proj/registry.py)

---

**Last Updated:** 2026-01-06  
**Status:** ✅ Expanded  
**Next:** Begin implementation with `/task-phase 6 1`
