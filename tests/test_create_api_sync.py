"""Tests for API sync functionality."""
import yaml
from pathlib import Path
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from proj.cli import app
from proj.commands.projects import sync_to_api
from proj.error_handler import APIError, BackendConnectionError, TimeoutError

runner = CliRunner()


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
    call_args = mock_client.create_project.call_args[0][0]
    assert call_args["name"] == "test-project"
    assert call_args["path"] == "/tmp/test"
    assert call_args["description"] == "Test description"
    assert call_args["status"] == "active"


def test_sync_to_api_connection_error():
    """Test sync_to_api returns None on connection error."""
    mock_client = Mock()
    mock_client.create_project.side_effect = BackendConnectionError(
        "No connection"
    )

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


def test_sync_to_api_timeout_error():
    """Test sync_to_api returns None on timeout error."""
    mock_client = Mock()
    mock_client.create_project.side_effect = TimeoutError("Request timeout")

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result is None  # No exception raised


def test_sync_to_api_default_description():
    """Test sync_to_api uses default description when not provided."""
    mock_client = Mock()
    mock_client.create_project.return_value = {"id": 123}

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result == 123
    call_args = mock_client.create_project.call_args[0][0]
    assert "description" in call_args
    assert "standard-project" in call_args["description"]


def test_sync_to_api_with_console_output():
    """Test sync_to_api prints error message when console provided."""
    mock_client = Mock()
    mock_client.create_project.side_effect = APIError("Server error", 500)
    mock_console = Mock()

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
        console=mock_console,
    )

    assert result is None
    mock_console.print.assert_called_once()
    # Verify sanitized error message (no exception details)
    call_args = mock_console.print.call_args[0][0]
    assert "Could not sync to API. Project created locally." in call_args
    # Verify exception details are NOT leaked
    assert "Server error" not in call_args


def test_sync_to_api_sanitizes_error_messages():
    """Test sync_to_api does not leak exception details in user-facing messages."""
    mock_client = Mock()
    # Create exception with potentially sensitive details
    sensitive_error = APIError("Connection failed: http://internal-api:5000/secret-endpoint", 500)
    mock_client.create_project.side_effect = sensitive_error
    mock_console = Mock()

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
        console=mock_console,
    )

    assert result is None
    mock_console.print.assert_called_once()
    # Verify user message does NOT contain exception details
    call_args = mock_console.print.call_args[0][0]
    assert "Could not sync to API. Project created locally." in call_args
    # Verify sensitive details are NOT in message
    assert "internal-api" not in call_args
    assert "secret-endpoint" not in call_args
    assert "http://" not in call_args


# =============================================================================
# Task 4: Integrate API Sync into Template Flow - Integration Tests
# =============================================================================


def test_template_create_syncs_to_api(tmp_path, monkeypatch):
    """Test template creation syncs to API when enabled."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create template structure
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("Project: [Project Name]")

    # Create config with api_enabled=True
    config_dir = tmp_path / "proj"
    config_dir.mkdir(parents=True)
    config_data = {
        "api_url": "http://localhost:5000",
        "api_enabled": True,
        "templates": {
            "source": str(templates_source),
            "default": "standard-project",
        },
    }
    with open(config_dir / "config.yaml", "w") as f:
        yaml.dump(config_data, f)

    # Create target directory
    (tmp_path / "projects").mkdir()

    # Mock API client
    with patch("proj.commands.projects.APIClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.create_project.return_value = {
            "id": 99,
            "name": "test-project"
        }

        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--template",
                "standard-project",
                "--target-dir",
                str(tmp_path / "projects"),
                "--no-git",
            ],
        )

        assert result.exit_code == 0
        mock_instance.create_project.assert_called_once()


def test_template_create_skips_api_when_local_only(tmp_path, monkeypatch):
    """Test --local-only skips API sync."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create template structure
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("Project: [Project Name]")

    # Create config with api_enabled=True
    config_dir = tmp_path / "proj"
    config_dir.mkdir(parents=True)
    config_data = {
        "api_url": "http://localhost:5000",
        "api_enabled": True,
        "templates": {
            "source": str(templates_source),
            "default": "standard-project",
        },
    }
    with open(config_dir / "config.yaml", "w") as f:
        yaml.dump(config_data, f)

    # Create target directory
    (tmp_path / "projects").mkdir()

    with patch("proj.commands.projects.APIClient") as MockClient:
        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--template",
                "standard-project",
                "--local-only",
                "--target-dir",
                str(tmp_path / "projects"),
                "--no-git",
            ],
        )

        assert result.exit_code == 0
        MockClient.return_value.create_project.assert_not_called()


def test_template_create_skips_api_when_disabled(tmp_path, monkeypatch):
    """Test template creation skips API when api_enabled=False."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create template structure
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("Project: [Project Name]")

    # Create config with api_enabled=False
    config_dir = tmp_path / "proj"
    config_dir.mkdir(parents=True)
    config_data = {
        "api_url": "http://localhost:5000",
        "api_enabled": False,
        "templates": {
            "source": str(templates_source),
            "default": "standard-project",
        },
    }
    with open(config_dir / "config.yaml", "w") as f:
        yaml.dump(config_data, f)

    # Create target directory
    (tmp_path / "projects").mkdir()

    with patch("proj.commands.projects.APIClient") as MockClient:
        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--template",
                "standard-project",
                "--target-dir",
                str(tmp_path / "projects"),
                "--no-git",
            ],
        )

        assert result.exit_code == 0
        MockClient.return_value.create_project.assert_not_called()


def test_template_create_updates_registry_with_work_prod_id(
    tmp_path, monkeypatch
):
    """Test registry entry includes work_prod_id after API sync."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create template structure
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("Project: [Project Name]")

    # Create config with api_enabled=True
    config_dir = tmp_path / "proj"
    config_dir.mkdir(parents=True)
    config_data = {
        "api_url": "http://localhost:5000",
        "api_enabled": True,
        "templates": {
            "source": str(templates_source),
            "default": "standard-project",
        },
    }
    with open(config_dir / "config.yaml", "w") as f:
        yaml.dump(config_data, f)

    # Create target directory
    (tmp_path / "projects").mkdir()

    with patch("proj.commands.projects.APIClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.create_project.return_value = {
            "id": 77,
            "name": "test-project"
        }

        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--template",
                "standard-project",
                "--target-dir",
                str(tmp_path / "projects"),
                "--no-git",
            ],
        )

        assert result.exit_code == 0

        # Check registry
        from proj.registry import get_project_by_path

        project_path = tmp_path / "projects" / "test-project"
        project = get_project_by_path(project_path)
        assert project is not None
        assert project.work_prod_id == 77


def test_template_create_succeeds_even_if_api_fails(tmp_path, monkeypatch):
    """Test local creation succeeds even if API sync fails."""
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    # Create template structure
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("Project: [Project Name]")

    # Create config with api_enabled=True
    config_dir = tmp_path / "proj"
    config_dir.mkdir(parents=True)
    config_data = {
        "api_url": "http://localhost:5000",
        "api_enabled": True,
        "templates": {
            "source": str(templates_source),
            "default": "standard-project",
        },
    }
    with open(config_dir / "config.yaml", "w") as f:
        yaml.dump(config_data, f)

    # Create target directory
    (tmp_path / "projects").mkdir()

    with patch("proj.commands.projects.APIClient") as MockClient:
        mock_instance = MockClient.return_value
        mock_instance.create_project.side_effect = BackendConnectionError(
            "Connection failed"
        )

        result = runner.invoke(
            app,
            [
                "create",
                "test-project",
                "--template",
                "standard-project",
                "--target-dir",
                str(tmp_path / "projects"),
                "--no-git",
            ],
        )

        # Should succeed despite API failure
        assert result.exit_code == 0

        # Project should be created locally
        project_path = tmp_path / "projects" / "test-project"
        assert project_path.exists()
        assert (project_path / "README.md").exists()

        # Registry should exist but without work_prod_id
        from proj.registry import get_project_by_path

        project = get_project_by_path(project_path)
        assert project is not None
        assert project.work_prod_id is None
