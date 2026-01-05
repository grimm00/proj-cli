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

