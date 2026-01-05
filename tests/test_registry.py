"""Tests for local registry module."""
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

