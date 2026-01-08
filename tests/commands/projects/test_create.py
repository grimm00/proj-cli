"""Tests for create project command and related functions."""
import subprocess
import sys
from io import StringIO

import pytest
import typer
from rich.console import Console
from unittest.mock import MagicMock, patch

from proj.cli import app
from proj.commands.projects import (
    detect_create_mode,
    prompt_for_create_options,
)


def test_create_command_exists():
    """Test that create command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "create", "--help"],
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
