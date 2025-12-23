# Project Type Support - Phase 1: Client Update

**Feature:** Add `project_type` parameter support  
**Phase:** 1 of 2  
**Status:** 🔴 Not Started  
**Estimated Effort:** ~2 hours  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Dependencies:** work-prod `project-type-field` Phase 3 complete

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

- [ ] API client supports `project_type` parameter
- [ ] CLI accepts `--type` option
- [ ] Output includes project_type field
- [ ] Unit tests added

---

## 📝 Tasks

### Task 1: Update API Client (~45 min)

**File:** `src/proj/api_client.py`

**Changes:**

1. Add `project_type` parameter to `list_projects()`:

```python
def list_projects(
    self,
    classification: Optional[str] = None,
    project_type: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
) -> List[Dict]:
    """List projects with optional filters."""
    params = {}
    if classification:
        params['classification'] = classification
    if project_type:
        params['project_type'] = project_type
    if search:
        params['search'] = search
    if limit:
        params['limit'] = limit
    
    response = self._request('GET', '/projects', params=params)
    return response.get('projects', [])
```

2. Add type validation (optional, API validates):

```python
VALID_PROJECT_TYPES = ['Work', 'Personal', 'Learning', 'Inactive']

def list_projects(self, ..., project_type: Optional[str] = None, ...):
    if project_type and project_type not in self.VALID_PROJECT_TYPES:
        raise ValueError(f"Invalid project_type. Must be one of: {self.VALID_PROJECT_TYPES}")
    # ...
```

**Acceptance Criteria:**
- [ ] Parameter added to method signature
- [ ] Parameter passed to API call
- [ ] Type validation added

---

### Task 2: Update CLI Command (~45 min)

**File:** `src/proj/commands/projects.py`

**Changes:**

1. Add `--type` option to `list` command:

```python
@app.command("list")
def list_projects(
    classification: Optional[str] = typer.Option(
        None, "--classification", "-c",
        help="Filter by classification (primary, secondary, archive, maintenance)"
    ),
    project_type: Optional[str] = typer.Option(
        None, "--type", "-t",
        help="Filter by project type (Work, Personal, Learning, Inactive)"
    ),
    search: Optional[str] = typer.Option(
        None, "--search", "-s",
        help="Search projects by name"
    ),
    limit: int = typer.Option(
        50, "--limit", "-l",
        help="Maximum number of projects to return"
    ),
    format: str = typer.Option(
        "table", "--format", "-f",
        help="Output format (table, json)"
    ),
):
    """List projects with optional filters."""
    try:
        projects = client.list_projects(
            classification=classification,
            project_type=project_type,
            search=search,
            limit=limit,
        )
        # ... output formatting
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
```

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
- [ ] `--type` option added
- [ ] Help text is clear
- [ ] Output includes project_type column

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
        classification=None,
        project_type="Work",
        search=None,
        limit=50,
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
    
    result = runner.invoke(app, ["list", "--type", "Work", "--classification", "primary"])
    
    assert result.exit_code == 0
    mock_client.list_projects.assert_called_once_with(
        classification="primary",
        project_type="Work",
        search=None,
        limit=50,
    )
```

**Acceptance Criteria:**
- [ ] Type filter test added
- [ ] Invalid type test added
- [ ] Combined filter test added
- [ ] All tests pass

---

## ✅ Phase Completion Criteria

- [ ] API client updated with `project_type` parameter
- [ ] CLI updated with `--type` option
- [ ] Output includes project_type column
- [ ] Unit tests added and passing
- [ ] Code committed to feature branch

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 2: Integration Testing](phase-2.md)
- [work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)

---

**Last Updated:** 2025-12-23

