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

