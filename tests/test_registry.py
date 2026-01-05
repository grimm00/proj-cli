"""Tests for local registry module."""
import pytest
from datetime import datetime
from pathlib import Path


def test_registry_project_exists():
    """Test that RegistryProject class exists."""
    from proj.registry import RegistryProject
    assert RegistryProject is not None


def test_registry_project_has_required_fields():
    """Test that RegistryProject has all required fields."""
    from proj.registry import RegistryProject
    
    project = RegistryProject(
        id="test-uuid",
        name="my-project",
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime.now(),
    )
    
    assert project.id == "test-uuid"
    assert project.name == "my-project"
    assert project.path == Path("/Users/me/Projects/my-project")
    assert project.template == "standard-project"
    assert project.template_version == "0.8.0"
    assert project.work_prod_id is None  # Optional
    assert project.metadata == {}  # Default empty dict


def test_registry_project_with_optional_fields():
    """Test RegistryProject with optional work_prod_id and metadata."""
    from proj.registry import RegistryProject
    
    project = RegistryProject(
        id="test-uuid",
        name="my-project",
        path=Path("/Users/me/Projects/my-project"),
        template="standard-project",
        template_version="0.8.0",
        created_at=datetime.now(),
        work_prod_id=42,
        metadata={"description": "My app", "author": "me"},
    )
    
    assert project.work_prod_id == 42
    assert project.metadata["description"] == "My app"

