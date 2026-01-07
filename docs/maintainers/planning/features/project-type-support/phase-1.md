# Project Type Support - Phase 1: Client Update

**Feature:** Add `project_type` parameter support
**Phase:** 1 of 2
**Status:** ✅ Complete
**Completed:** 2026-01-07
**Estimated Effort:** ~1.75 hours
**Created:** 2025-12-23
**Last Updated:** 2026-01-07
**Dependencies:** ✅ work-prod `project-type-field` complete (PR #42)
**Pre-Phase Review:** ✅ Complete ([phase-1-review.md](phase-1-review.md))

---

## 📋 Phase Overview

Add `project_type` parameter support to API client and `--type` option to CLI.

**Goal:** Users can filter projects by type using `proj list --type Work`.

---

## ⚠️ Pre-Requisite Check

Before starting this phase, verify work-prod API is ready:

```bash
# Should return filtered projects, not 400 error
curl "http://localhost:5000/api/projects?project_type=Work"
```

---

## 🎯 Phase Goals

- [x] API client supports `project_type` parameter
- [x] CLI accepts `--type` option
- [x] Output includes project_type field
- [x] Unit tests added

---

## 📝 Tasks

### Task 1: Update API Client (~45 min)

**File:** `src/proj/api_client.py`

**Changes:**

1. Add `project_type` parameter to `list_projects()`:

```python
def list_projects(
    self,
    status: Optional[str] = None,
    organization: Optional[str] = None,
    classification: Optional[str] = None,
    project_type: Optional[str] = None,  # NEW
    search: Optional[str] = None,
) -> List[Dict]:
    """List all projects with optional filters."""
    params = {}
    if status:
        params["status"] = status
    if organization:
        params["organization"] = organization
    if classification:
        params["classification"] = classification
    if project_type:  # NEW
        params["project_type"] = project_type
    if search:
        params["search"] = search
    # ... rest of method
```

> **Note:** Follow existing code pattern - current client has `status`, `organization`, `classification`, `search` parameters.

2. Add type validation (optional, API validates):

```python
VALID_PROJECT_TYPES = ['Work', 'Personal', 'Learning', 'Inactive']

def list_projects(self, ..., project_type: Optional[str] = None, ...):
    if project_type and project_type not in self.VALID_PROJECT_TYPES:
        raise ValueError(f"Invalid project_type. Must be one of: {self.VALID_PROJECT_TYPES}")
    # ...
```

**Acceptance Criteria:**

- [x] Parameter added to method signature
- [x] Parameter passed to API call
- [x] Type validation added

---

### Task 2: Update CLI Command (~45 min)

**File:** `src/proj/commands/projects.py`

**Changes:**

1. Add `--type` option to `list` command:

```python
# Add to existing list_projects function (registered via app.command(name="list"))
def list_projects(
    status: Optional[str] = typer.Option(
        None, "--status", "-s", help="Filter by status"
    ),
    organization: Optional[str] = typer.Option(
        None, "--org", "-o", help="Filter by organization"
    ),
    classification: Optional[str] = typer.Option(
        None, "--class", "-c", help="Filter by classification"
    ),
    project_type: Optional[str] = typer.Option(  # NEW
        None, "--type", "-t",
        help="Filter by project type (Work, Personal, Learning, Inactive)"
    ),
    search: Optional[str] = typer.Option(
        None, "--search", help="Search in names and descriptions"
    ),
    # ... existing wide, format options
):
    """List all projects with optional filters."""
    try:
        client = get_client()
        projects = client.list_projects(
            status=status,
            organization=organization,
            classification=classification,
            project_type=project_type,  # NEW
            search=search,
        )
        # ... output formatting
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
```

> **Note:** `-t` flag is safe - Typer handles flags per-command. `create` uses `-t` for `--template`, but that's a different command.

2. Update output formatting to include project_type:

```python
# For table output
table.add_column("Type", style="cyan")

for project in projects:
    table.add_row(
        str(project['id']),
        project['name'],
        project.get('project_type', '-'),  # NEW
        project.get('classification', '-'),
        # ...
    )
```

**Acceptance Criteria:**

- [x] `--type` option added
- [x] Help text is clear
- [x] Output includes project_type column

---

### Task 3: Add Unit Tests (~30 min)

**File:** `tests/test_commands_projects.py`

**Test Cases:**

```python
def test_list_projects_with_type_filter(mock_client):
    """Test proj list --type Work."""
    mock_client.list_projects.return_value = [
        {'id': 1, 'name': 'Work Project', 'project_type': 'Work'}
    ]

    result = runner.invoke(app, ["list", "--type", "Work"])

    assert result.exit_code == 0
    mock_client.list_projects.assert_called_once_with(
        status=None,
        organization=None,
        classification=None,
        project_type="Work",
        search=None,
    )

def test_list_projects_with_invalid_type(mock_client):
    """Test proj list --type Invalid shows error."""
    mock_client.list_projects.side_effect = ValueError(
        "Invalid project_type. Must be one of: ['Work', 'Personal', 'Learning', 'Inactive']"
    )

    result = runner.invoke(app, ["list", "--type", "Invalid"])

    assert result.exit_code == 1
    assert "Invalid project_type" in result.output

def test_list_projects_with_type_and_classification(mock_client):
    """Test combining --type and --classification filters."""
    mock_client.list_projects.return_value = []

    result = runner.invoke(app, ["list", "--type", "Work", "--class", "primary"])

    assert result.exit_code == 0
    mock_client.list_projects.assert_called_once_with(
        status=None,
        organization=None,
        classification="primary",
        project_type="Work",
        search=None,
    )
```

> **Note:** Test assertions updated to match current API client signature (no `limit` parameter).

**Acceptance Criteria:**

- [x] Type filter test added
- [x] Invalid type test added
- [x] Combined filter test added
- [x] All tests pass

---

## ✅ Phase Completion Criteria

- [x] API client updated with `project_type` parameter
- [x] CLI updated with `--type` option
- [x] Output includes project_type column
- [x] Unit tests added and passing
- [x] Code committed to feature branch

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 2: Integration Testing](phase-2.md)
- [work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)

---

**Last Updated:** 2025-12-23
