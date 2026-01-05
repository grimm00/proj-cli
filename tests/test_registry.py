"""Tests for local registry module."""
import json
import pytest
from datetime import datetime
from pathlib import Path


def test_registry_project_exists():
    """Test that RegistryProject class exists."""
    from proj.registry import RegistryProject
    assert RegistryProject is not None


def test_registry_project_has_required_fields():
    """Test that RegistryProject has all required fields (minimal schema)."""
    from proj.registry import RegistryProject
    
    project = RegistryProject(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime.now(),
    )
    
    assert project.path == Path("/Users/me/Projects/my-project")
    assert project.template == "standard-project"
    assert project.template_version == "0.8.0"
    assert isinstance(project.created_at, datetime)
    # Verify minimal schema - these fields should NOT exist
    assert not hasattr(project, 'id')
    assert not hasattr(project, 'name')
    assert not hasattr(project, 'work_prod_id')
    assert not hasattr(project, 'metadata')


def test_registry_exists():
    """Test that Registry class exists."""
    from proj.registry import Registry
    assert Registry is not None


def test_registry_has_version_and_projects():
    """Test Registry has version and projects fields."""
    from proj.registry import Registry

    registry = Registry()

    assert registry.version == "1.0"
    assert registry.projects == []


def test_registry_with_projects():
    """Test Registry can hold projects."""
    from proj.registry import Registry, RegistryProject
    from datetime import datetime
    from pathlib import Path

    # Minimal schema - only sync-related fields
    project = RegistryProject(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime.now(),
    )

    registry = Registry(projects=[project])

    assert len(registry.projects) == 1
    assert registry.projects[0].path == Path("/Users/me/Projects/my-project")


def test_registry_project_minimal_schema():
    """Test RegistryProject has only sync-related fields (minimal)."""
    from proj.registry import RegistryProject
    from datetime import datetime
    from pathlib import Path

    project = RegistryProject(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime.now(),
    )

    assert project.path == Path("/Users/me/Projects/my-project")
    assert project.template == "standard-project"
    assert project.template_version == "0.8.0"
    # These fields should NOT exist (moved to inventory)
    assert not hasattr(project, 'id')
    assert not hasattr(project, 'name')
    assert not hasattr(project, 'work_prod_id')
    assert not hasattr(project, 'metadata')


def test_load_registry_creates_empty_if_not_exists(tmp_path, monkeypatch):
    """Test that load_registry creates empty registry if file doesn't exist."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import load_registry

    registry = load_registry()

    assert registry.version == "1.0"
    assert registry.projects == []


def test_load_registry_reads_existing_file(tmp_path, monkeypatch):
    """Test that load_registry reads existing JSON file."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    # Create registry file
    registry_dir = tmp_path / "proj"
    registry_dir.mkdir(parents=True)
    registry_file = registry_dir / "registry.json"

    # Minimal schema - sync fields only
    registry_data = {
        "version": "1.0",
        "projects": [
            {
                "path": "/Users/me/Projects/my-project",
                "template": "standard-project",
                "template_version": "0.8.0",
                "created_at": "2025-01-05T10:30:00",
            }
        ],
    }
    with open(registry_file, "w") as f:
        json.dump(registry_data, f)

    from proj.registry import load_registry
    from pathlib import Path

    registry = load_registry()

    assert registry.version == "1.0"
    assert len(registry.projects) == 1
    assert registry.projects[0].path == Path("/Users/me/Projects/my-project")
    assert registry.projects[0].template == "standard-project"


def test_save_registry_creates_file(tmp_path, monkeypatch):
    """Test that save_registry creates registry file."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import Registry, RegistryProject, save_registry
    from datetime import datetime
    from pathlib import Path

    # Minimal schema
    project = RegistryProject(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime(2025, 1, 5, 10, 30, 0),
    )
    registry = Registry(projects=[project])

    save_registry(registry)

    registry_file = tmp_path / "proj" / "registry.json"
    assert registry_file.exists()


def test_save_registry_creates_valid_json(tmp_path, monkeypatch):
    """Test that saved JSON is valid and human-readable."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import Registry, RegistryProject, save_registry
    from datetime import datetime
    from pathlib import Path

    # Minimal schema
    project = RegistryProject(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime(2025, 1, 5, 10, 30, 0),
    )
    registry = Registry(projects=[project])

    save_registry(registry)

    registry_file = tmp_path / "proj" / "registry.json"
    with open(registry_file) as f:
        data = json.load(f)

    assert data["version"] == "1.0"
    assert len(data["projects"]) == 1
    assert data["projects"][0]["path"] == "/Users/me/Projects/my-project"
    assert data["projects"][0]["template"] == "standard-project"


def test_save_load_roundtrip(tmp_path, monkeypatch):
    """Test that save_registry + load_registry preserves all fields."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import Registry, RegistryProject, save_registry, load_registry
    from datetime import datetime
    from pathlib import Path

    # Create a registry with known values
    original_dt = datetime(2025, 1, 5, 10, 30, 45)
    original = Registry(
        version="1.0",
        projects=[
            RegistryProject(
                path=Path("/Users/me/Projects/test-project"),
                template="standard-project",
                template_version="0.8.0",
                created_at=original_dt,
            )
        ],
    )

    # Save and load
    save_registry(original)
    loaded = load_registry()

    # Assert all fields are preserved
    assert loaded.version == original.version
    assert len(loaded.projects) == 1
    
    loaded_proj = loaded.projects[0]
    original_proj = original.projects[0]
    
    assert loaded_proj.path == original_proj.path
    assert loaded_proj.template == original_proj.template
    assert loaded_proj.template_version == original_proj.template_version
    assert loaded_proj.created_at == original_proj.created_at


def test_load_registry_handles_z_suffix(tmp_path, monkeypatch):
    """Test that load_registry handles ISO 8601 Z suffix timestamps."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import load_registry
    from datetime import datetime, timezone
    import json

    # Create registry file with Z suffix timestamp (common in JSON APIs)
    registry_file = tmp_path / "proj" / "registry.json"
    registry_file.parent.mkdir(parents=True, exist_ok=True)
    
    data = {
        "version": "1.0",
        "projects": [
            {
                "path": "/Users/me/Projects/test",
                "template": "standard-project",
                "template_version": "0.8.0",
                "created_at": "2025-01-05T10:30:00Z",  # Z suffix
            }
        ],
    }
    with open(registry_file, "w") as f:
        json.dump(data, f)

    # Load should succeed without error
    registry = load_registry()
    
    assert len(registry.projects) == 1
    # Timestamp should be parsed correctly (Z = UTC = +00:00)
    assert registry.projects[0].created_at.tzinfo is not None


def test_add_project_to_registry(tmp_path, monkeypatch):
    """Test adding a project to the registry."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, load_registry
    from pathlib import Path

    project = add_project(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
    )

    assert project.path == Path("/Users/me/Projects/my-project")
    assert project.template == "standard-project"
    assert project.created_at is not None  # Timestamp set

    # Verify persisted
    registry = load_registry()
    assert len(registry.projects) == 1
    assert registry.projects[0].path == Path("/Users/me/Projects/my-project")


def test_add_project_prevents_duplicates(tmp_path, monkeypatch):
    """Test that adding duplicate path raises error."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, load_registry
    from pathlib import Path
    import pytest

    # Add first project
    add_project(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
    )

    # Try to add duplicate - should raise
    with pytest.raises(ValueError, match="already registered"):
        add_project(
            path=Path("/Users/me/Projects/my-project"),
            template="standard-project",
            template_version="0.9.0",
        )

    # Verify only one project
    registry = load_registry()
    assert len(registry.projects) == 1


def test_remove_project_from_registry(tmp_path, monkeypatch):
    """Test removing a project from the registry."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, remove_project, load_registry
    from pathlib import Path

    # Add a project first (minimal schema)
    add_project(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
    )

    # Remove it
    removed = remove_project(Path("/Users/me/Projects/my-project"))

    assert removed is True

    # Verify removed
    registry = load_registry()
    assert len(registry.projects) == 0


def test_remove_nonexistent_project(tmp_path, monkeypatch):
    """Test removing a non-existent project returns False."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import remove_project
    from pathlib import Path

    removed = remove_project(Path("/nonexistent/path"))

    assert removed is False


def test_get_project_by_path(tmp_path, monkeypatch):
    """Test finding a project by its path."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, get_project_by_path
    from pathlib import Path

    add_project(
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
    )

    project = get_project_by_path(Path("/Users/me/Projects/my-project"))

    assert project is not None
    assert project.template == "standard-project"
    assert project.template_version == "0.8.0"


def test_get_project_by_path_not_found(tmp_path, monkeypatch):
    """Test get_project_by_path returns None if not found."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import get_project_by_path
    from pathlib import Path

    project = get_project_by_path(Path("/nonexistent/path"))

    assert project is None


def test_is_registered(tmp_path, monkeypatch):
    """Test is_registered helper function."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, is_registered
    from pathlib import Path

    path = Path("/Users/me/Projects/my-project")

    # Not registered yet
    assert is_registered(path) is False

    # Add project
    add_project(
        path=path,
        template="standard-project",
        template_version="0.8.0",
    )

    # Now registered
    assert is_registered(path) is True


def test_list_projects_empty(tmp_path, monkeypatch):
    """Test listing projects from empty registry."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import list_projects

    projects = list_projects()

    assert projects == []


def test_list_projects(tmp_path, monkeypatch):
    """Test listing all projects."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, list_projects
    from pathlib import Path

    add_project(
        path=Path("/Users/me/Projects/project-1"),
        template="standard-project",
        template_version="0.8.0",
    )
    add_project(
        path=Path("/Users/me/Projects/project-2"),
        template="learning-project",
        template_version="0.8.0",
    )

    projects = list_projects()

    assert len(projects) == 2


def test_list_projects_filter_by_template(tmp_path, monkeypatch):
    """Test filtering projects by template type."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))

    from proj.registry import add_project, list_projects
    from pathlib import Path

    add_project(
        path=Path("/Users/me/Projects/project-1"),
        template="standard-project",
        template_version="0.8.0",
    )
    add_project(
        path=Path("/Users/me/Projects/project-2"),
        template="learning-project",
        template_version="0.8.0",
    )

    projects = list_projects(template="standard-project")

    assert len(projects) == 1
    assert projects[0].path == Path("/Users/me/Projects/project-1")

