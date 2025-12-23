# Project Type Support - Transition Plan

**Feature:** Add `project_type` parameter support  
**Source ADR:** [ADR-003: Add project_type Field](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)  
**Status:** 🔴 Not Started  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23

---

## 📋 Transition Overview

This transition plan implements the client-side support for ADR-003 in proj-cli.

**Transition Type:** Feature (Client Enhancement)

**Key Changes:**
1. Add `project_type` parameter to API client
2. Add `--type` option to `proj list` command
3. Update output formatting to display project type
4. Integration testing with work-prod

---

## 🎯 Transition Goals

From ADR-003:
- Enable users to filter projects by type from CLI
- Support filtering: `proj list --type Work`, `proj list --type Personal`, etc.
- Display project type in list output

---

## ⚠️ Dependency

**BLOCKING:** This feature depends on work-prod completing `project-type-field` Phase 3.

**Check Before Starting:**
```bash
# Verify work-prod API supports project_type parameter
curl "http://localhost:5000/api/projects?project_type=Work"
```

If this returns a 400 error about invalid parameter, work-prod is not ready.

---

## 📅 Transition Phases

| Phase | Name | Status | Effort | Dependencies |
|-------|------|--------|--------|--------------|
| 1 | Client Update | 🔴 Not Started | ~2 hours | work-prod Phase 3 |
| 2 | Integration Testing | 🔴 Not Started | ~1 hour | Phase 1 |

**Total Estimated Effort:** ~3 hours

---

## 📋 Phase Summaries

### Phase 1: Client Update

**Goal:** Add `project_type` support to API client and CLI

**Key Tasks:**
1. Update `api_client.py` with `project_type` parameter
2. Add `--type` option to `proj list` command
3. Update output formatting
4. Add unit tests

**Code Changes:**

```python
# api_client.py
def list_projects(
    self,
    classification: Optional[str] = None,
    project_type: Optional[str] = None,  # NEW
    search: Optional[str] = None,
    limit: int = 50,
) -> List[Dict]:
    params = {}
    if classification:
        params['classification'] = classification
    if project_type:  # NEW
        params['project_type'] = project_type
    # ...
```

```python
# commands/projects.py
@app.command("list")
def list_projects(
    classification: Optional[str] = typer.Option(None, "--classification", "-c"),
    project_type: Optional[str] = typer.Option(None, "--type", "-t"),  # NEW
    # ...
):
    projects = client.list_projects(
        classification=classification,
        project_type=project_type,  # NEW
    )
```

**Exit Criteria:**
- [ ] API client supports parameter
- [ ] CLI accepts `--type` option
- [ ] Unit tests pass

---

### Phase 2: Integration Testing

**Goal:** Verify integration with work-prod API

**Key Tasks:**
1. Start work-prod server
2. Test filtering commands
3. Verify output formatting
4. Update documentation

**Test Commands:**
```bash
# Test each type filter
proj list --type Work
proj list --type Personal
proj list --type Learning
proj list --type Inactive

# Test with other filters combined
proj list --type Work --classification primary
proj list --type Learning --search "python"

# Test invalid type
proj list --type Invalid  # Should show error
```

**Exit Criteria:**
- [ ] All filter commands work
- [ ] Combined filters work
- [ ] Invalid type shows error
- [ ] Documentation updated

---

## 📊 Requirements Traceability

| Requirement | Satisfied By |
|-------------|--------------|
| FR-2d | API Filtering by Project Type | Phase 1 |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Phase 1: Client Update](phase-1.md)
- [Phase 2: Integration Testing](phase-2.md)
- [work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)
- [ADR-003](../../../../../dev-infra/admin/decisions/project-model-definition/adr-003-add-project-type-field.md)

---

**Last Updated:** 2025-12-23

