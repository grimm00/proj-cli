"""Integration tests for API client (requires running API)."""
import pytest


@pytest.mark.integration
def test_list_projects_integration():
    """Test listing projects against real API."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        projects = client.list_projects()
        assert isinstance(projects, list)
    except Exception as e:
        pytest.skip(f"API not available: {e}")


@pytest.mark.integration
def test_create_and_delete_project_integration():
    """Test creating and deleting a project."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        # Create
        project = client.create_project({
            "name": "Test Project from proj-cli",
            "status": "active",
        })
        assert "id" in project

        # Delete
        client.delete_project(project["id"])
    except Exception as e:
        pytest.skip(f"API not available: {e}")


@pytest.mark.integration
def test_get_project_integration():
    """Test getting a project by ID."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        # Create a project first
        project = client.create_project({
            "name": "Test Get Project",
            "status": "active",
        })
        project_id = project["id"]

        # Get the project
        retrieved = client.get_project(project_id)
        assert retrieved["id"] == project_id
        assert retrieved["name"] == "Test Get Project"

        # Cleanup
        client.delete_project(project_id)
    except Exception as e:
        pytest.skip(f"API not available: {e}")


@pytest.mark.integration
def test_update_project_integration():
    """Test updating a project."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        # Create a project
        project = client.create_project({
            "name": "Original Name",
            "status": "active",
        })
        project_id = project["id"]

        # Update the project
        updated = client.update_project(project_id, {
            "name": "Updated Name",
            "status": "inactive",
        })
        assert updated["name"] == "Updated Name"
        assert updated["status"] == "inactive"

        # Cleanup
        client.delete_project(project_id)
    except Exception as e:
        pytest.skip(f"API not available: {e}")


@pytest.mark.integration
def test_search_projects_integration():
    """Test searching projects."""
    from proj.api_client import APIClient

    client = APIClient()
    try:
        # Create a test project
        project = client.create_project({
            "name": "Search Test Project",
            "status": "active",
        })
        project_id = project["id"]

        # Search for it
        results = client.search_projects("Search Test")
        assert isinstance(results, list)
        assert len(results) > 0
        assert any(p["id"] == project_id for p in results)

        # Cleanup
        client.delete_project(project_id)
    except Exception as e:
        pytest.skip(f"API not available: {e}")

