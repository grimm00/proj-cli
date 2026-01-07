"""Tests for project commands."""
import subprocess
import sys
from io import StringIO

import pytest
import typer
from rich.console import Console
from typer.testing import CliRunner
from unittest.mock import MagicMock, patch

from proj.cli import app
from proj.commands.projects import (
    detect_create_mode,
    prompt_for_create_options,
)
from proj.error_handler import InvalidProjectTypeError

runner = CliRunner()


def test_list_command_exists():
    """Test that list command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "list", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "List" in result.stdout or "list" in result.stdout.lower()


def test_get_command_exists():
    """Test that get command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "get", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_create_command_exists():
    """Test that create command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "create", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_update_command_exists():
    """Test that update command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "update", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_delete_command_exists():
    """Test that delete command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "delete", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_search_command_exists():
    """Test that search command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "search", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_search_command_has_wide_option():
    """Test that search command has --wide option."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "search", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "--wide" in result.stdout or "-w" in result.stdout


def test_import_command_exists():
    """Test that import command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "import-json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_archive_command_exists():
    """Test that archive command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "archive", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


# Tests for detect_create_mode function (Phase 4, Task 1)
def test_detect_mode_default_interactive():
    """Test default mode is interactive when no flags."""
    mode = detect_create_mode(
        template=None,
        api_only=False,
        local_only=False,
    )
    assert mode == "interactive"


def test_detect_mode_api_only():
    """Test api-only mode detection."""
    mode = detect_create_mode(
        template=None,
        api_only=True,
        local_only=False,
    )
    assert mode == "api-only"


def test_detect_mode_local_only():
    """Test local-only mode detection."""
    mode = detect_create_mode(
        template=None,
        api_only=False,
        local_only=True,
    )
    assert mode == "local-only"


def test_detect_mode_template():
    """Test template mode detection."""
    mode = detect_create_mode(
        template="standard-project",
        api_only=False,
        local_only=False,
    )
    assert mode == "template"


def test_detect_mode_template_with_api_only_flag():
    """Explicit api_only flag takes precedence over template."""
    mode = detect_create_mode(
        template="standard-project",
        api_only=True,
        local_only=False,
    )
    assert mode == "api-only"


def test_detect_mode_template_with_local_only_flag():
    """Explicit local_only flag takes precedence over template."""
    mode = detect_create_mode(
        template="standard-project",
        api_only=False,
        local_only=True,
    )
    assert mode == "local-only"


def test_detect_mode_conflict_raises():
    """Test conflicting flags raise error."""
    with pytest.raises(ValueError) as exc:
        detect_create_mode(
            template=None,
            api_only=True,
            local_only=True,
        )
    assert "conflict" in str(exc.value).lower()


def test_prompt_for_create_options_no_templates_available(tmp_path):
    """Test prompt_for_create_options exits when no templates available."""
    config = MagicMock()
    templates_source = tmp_path / "templates"
    templates_source.mkdir()

    # Capture console output
    test_console = Console(file=StringIO(), force_terminal=True)

    templates_mock = 'proj.commands.projects.get_templates_source'
    list_mock = 'proj.commands.projects.list_templates'
    console_mock = 'proj.commands.projects.console'
    prompt_mock = 'proj.commands.projects.Prompt.ask'

    with patch(templates_mock, return_value=templates_source):
        with patch(list_mock, return_value=[]):
            with patch(console_mock, test_console):
                # Mock Prompt.ask (called before template check)
                with patch(prompt_mock, return_value="test-project"):
                    with pytest.raises(typer.Exit) as exc_info:
                        prompt_for_create_options(config)

                    # Should exit with code 1
                    assert exc_info.value.exit_code == 1

                    # Verify error message output
                    output = test_console.file.getvalue()
                    assert "No templates available" in output
                    # Path may be wrapped, check key parts
                    assert "Templates source:" in output
                    assert "templates" in output


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
    # Should NOT show the "Error:" format (that's for InvalidProjectTypeError)
    assert "Error:" not in result.output or "Some other error" not in result.output


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
