"""Tests for API-only mode (Phase 4, Task 3)."""
import pytest
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


@patch('proj.commands.projects.get_client')
def test_create_api_only_calls_api(mock_get_client):
    """Test api-only mode creates project via API."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {"id": 1, "name": "Test"}
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, [
        "create", "Test Project", "--api-only"
    ])

    assert result.exit_code == 0
    mock_client.create_project.assert_called_once()


@patch('proj.commands.projects.get_client')
def test_create_api_only_does_not_create_directory(mock_get_client, tmp_path, monkeypatch):
    """Test api-only mode does NOT create local directory."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {"id": 1, "name": "test-app"}
    mock_get_client.return_value = mock_client

    # Change to tmp_path to check if directory is created there
    import os
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, [
        "create", "test-app", "--api-only"
    ])

    # No local directory should be created
    assert not (tmp_path / "test-app").exists()
    assert result.exit_code == 0


@patch('proj.commands.projects.get_client')
@patch('proj.registry.add_project')
def test_create_api_only_does_not_register(
    mock_add_project, mock_get_client
):
    """Test api-only mode does NOT register locally."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {"id": 1, "name": "test-app"}
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, [
        "create", "test-app", "--api-only"
    ])

    assert result.exit_code == 0
    mock_add_project.assert_not_called()


@patch('proj.commands.projects.get_client')
def test_create_api_only_matches_original_behavior(mock_get_client):
    """Test api-only mode matches original behavior."""
    mock_client = MagicMock()
    mock_client.create_project.return_value = {
        "id": 42,
        "name": "My Project",
        "status": "active"
    }
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, [
        "create", "My Project",
        "--desc", "Test description",
        "--status", "active",
        "--api-only"
    ])

    assert result.exit_code == 0
    mock_client.create_project.assert_called_once()
    call_args = mock_client.create_project.call_args[0][0]
    assert call_args["name"] == "My Project"
    assert call_args["status"] == "active"
    assert call_args["description"] == "Test description"

