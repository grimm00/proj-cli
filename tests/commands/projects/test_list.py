"""Tests for list and search project commands."""
import pytest
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch

from proj.cli import app
from proj.error_handler import InvalidProjectTypeError
from tests.conftest import assert_command_exists

runner = CliRunner()


def test_list_command_exists():
    """Test that list command exists."""
    assert_command_exists(["list"], expected_text="list")


def test_search_command_exists():
    """Test that search command exists."""
    assert_command_exists(["search"])


def test_search_command_has_wide_option():
    """Test that search command has --wide option."""
    result = assert_command_exists(["search"])
    assert "--wide" in result.stdout or "-w" in result.stdout


# Tests for project_type filtering (Phase 1, Task 3)
@patch('proj.commands.projects.get_client')
def test_list_projects_with_type_filter(mock_get_client):
    """Test proj list --type Work."""
    mock_client = MagicMock()
    mock_client.list_projects.return_value = [
        {'id': 1, 'name': 'Work Project', 'project_type': 'Work'}
    ]
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list", "--type", "Work"])

    assert result.exit_code == 0
    mock_client.list_projects.assert_called_once_with(
        status=None,
        organization=None,
        classification=None,
        project_type="Work",
        search=None,
    )


@patch('proj.commands.projects.get_client')
def test_list_projects_with_invalid_type(mock_get_client):
    """Test proj list --type Invalid shows error with proper formatting."""
    mock_client = MagicMock()
    mock_client.list_projects.side_effect = InvalidProjectTypeError(
        "Invalid project_type. Must be one of: ['Work', 'Personal', 'Learning', 'Inactive']"
    )
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list", "--type", "Invalid"])

    assert result.exit_code == 1
    assert "Invalid project_type" in result.output
    # Verify specific InvalidProjectTypeError handling (not generic handle_error)
    assert "Error:" in result.output


@patch('proj.commands.projects.get_client')
def test_list_projects_other_value_error_not_caught(mock_get_client):
    """Test that other ValueError exceptions are not caught as type errors."""
    mock_client = MagicMock()
    # Raise a generic ValueError (not InvalidProjectTypeError)
    mock_client.list_projects.side_effect = ValueError("Some other error")
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list"])

    # Generic ValueError should propagate (not be handled as type error)
    # Result should have exit_code 1 due to unhandled exception
    assert result.exit_code == 1
    # Should NOT show the formatted "Error:" prefix that InvalidProjectTypeError uses
    # The error may appear in output but not with our specific formatting
    assert "Error:" not in result.output


@patch('proj.commands.projects.get_client')
def test_list_projects_with_type_and_classification(mock_get_client):
    """Test combining --type and --classification filters."""
    mock_client = MagicMock()
    mock_client.list_projects.return_value = []
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list", "--type", "Work", "--class", "primary"])

    assert result.exit_code == 0
    mock_client.list_projects.assert_called_once_with(
        status=None,
        organization=None,
        classification="primary",
        project_type="Work",
        search=None,
    )


@patch('proj.commands.projects.get_client')
def test_list_projects_uses_patched_get_client_via_package_imports(mock_get_client):
    """Regression test: patching proj.commands.projects.get_client affects submodules using get_package_imports.
    
    This test explicitly verifies that patching at the package level (proj.commands.projects.get_client)
    correctly affects submodules that use get_package_imports() for late binding. This documents the
    patching pattern and protects against regressions if the late-binding implementation changes.
    """
    mock_client = MagicMock()
    mock_client.list_projects.return_value = []

    # When get_client is patched at package level, commands that use get_package_imports
    # (such as `list`) should still see the patched version.
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["list"])

    assert result.exit_code == 0
    mock_get_client.assert_called_once()
    mock_client.list_projects.assert_called_once()
