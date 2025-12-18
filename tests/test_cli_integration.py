"""Integration tests for CLI commands using CliRunner."""
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from proj.cli import app

runner = CliRunner()


def test_cli_version_command():
    """Test that --version works."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "proj version" in result.stdout


def test_cli_help_command():
    """Test that --help works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()
    assert "list" in result.stdout
    assert "inv" in result.stdout


def test_cli_no_args_shows_help():
    """Test that no args shows help."""
    result = runner.invoke(app, [])
    # Typer with no_args_is_help=True shows help and exits 0
    assert result.exit_code == 0
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()


@patch("proj.commands.projects.APIClient")
def test_cli_list_command(mock_api_client_class):
    """Test that list command works."""
    mock_client = Mock()
    mock_client.list_projects.return_value = [
        {"id": 1, "name": "Test Project", "status": "active"},
    ]
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "Test Project" in result.stdout


@patch("proj.commands.projects.APIClient")
def test_cli_list_command_json_format(mock_api_client_class):
    """Test that list command with --format json works."""
    mock_client = Mock()
    mock_client.list_projects.return_value = [
        {"id": 1, "name": "Test Project", "status": "active"},
    ]
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["list", "--format", "json"])
    assert result.exit_code == 0
    assert "Test Project" in result.stdout
    # Should be valid JSON
    import json
    json.loads(result.stdout)


@patch("proj.commands.projects.APIClient")
def test_cli_get_command(mock_api_client_class):
    """Test that get command works."""
    mock_client = Mock()
    mock_client.get_project.return_value = {
        "id": 1,
        "name": "Test Project",
        "status": "active",
    }
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["get", "1"])
    assert result.exit_code == 0
    assert "Test Project" in result.stdout


@patch("proj.commands.projects.APIClient")
def test_cli_create_command(mock_api_client_class):
    """Test that create command works."""
    mock_client = Mock()
    mock_client.create_project.return_value = {
        "id": 1,
        "name": "New Project",
        "status": "active",
    }
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["create", "New Project"])
    assert result.exit_code == 0
    assert "New Project" in result.stdout
    assert "created" in result.stdout.lower() or "1" in result.stdout


@patch("proj.commands.projects.APIClient")
def test_cli_search_command(mock_api_client_class):
    """Test that search command works."""
    mock_client = Mock()
    mock_client.search_projects.return_value = [
        {"id": 1, "name": "Test Project", "status": "active"},
    ]
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["search", "Test"])
    assert result.exit_code == 0
    assert "Test Project" in result.stdout


@patch("proj.commands.projects.APIClient")
def test_cli_search_command_wide_option(mock_api_client_class):
    """Test that search command with --wide option works."""
    mock_client = Mock()
    mock_client.search_projects.return_value = [
        {
            "id": 1,
            "name": "Test Project",
            "status": "active",
            "organization": "Test Org",
        },
    ]
    mock_api_client_class.return_value = mock_client

    result = runner.invoke(app, ["search", "Test", "--wide"])
    assert result.exit_code == 0
    # Rich tables split "Test Project" across lines, check for both parts
    assert "Test" in result.stdout and "Project" in result.stdout
    assert "Test Org" in result.stdout  # Verify wide option shows org column


def test_cli_inv_status_command(mock_xdg_dirs):
    """Test that inv status command works."""
    from proj.commands.inventory import get_inventory_file
    import json

    # Create empty inventory file
    inv_file = get_inventory_file()
    inv_file.parent.mkdir(parents=True, exist_ok=True)
    with open(inv_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    result = runner.invoke(app, ["inv", "status"])
    assert result.exit_code == 0
    assert "Total Projects" in result.stdout or "inventory" in result.stdout.lower()


def test_cli_inv_status_command_with_data(mock_xdg_dirs):
    """Test that inv status command shows data."""
    from proj.commands.inventory import get_inventory_file
    import json

    # Create inventory file with data
    inv_file = get_inventory_file()
    inv_file.parent.mkdir(parents=True, exist_ok=True)
    inventory_data = [
        {
            "name": "test-project",
            "remote_url": "https://github.com/user/test-project",
            "source": "github",
        },
    ]
    with open(inv_file, "w", encoding="utf-8") as f:
        json.dump(inventory_data, f)

    result = runner.invoke(app, ["inv", "status"])
    assert result.exit_code == 0
    assert "1" in result.stdout or "Total Projects" in result.stdout

