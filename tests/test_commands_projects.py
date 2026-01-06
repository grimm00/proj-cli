"""Tests for project commands."""
import subprocess
import sys
from pathlib import Path

import pytest
import typer
from unittest.mock import MagicMock, patch
from proj.commands.projects import detect_create_mode, prompt_for_create_options


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
    config = MagicMock()
    config.api_enabled = True
    mode = detect_create_mode(
        config=config,
        template=None,
        api_only=False,
        local_only=False,
    )
    assert mode == "interactive"


def test_detect_mode_api_only():
    """Test api-only mode detection."""
    config = MagicMock()
    mode = detect_create_mode(
        config=config,
        template=None,
        api_only=True,
        local_only=False,
    )
    assert mode == "api-only"


def test_detect_mode_local_only():
    """Test local-only mode detection."""
    config = MagicMock()
    mode = detect_create_mode(
        config=config,
        template=None,
        api_only=False,
        local_only=True,
    )
    assert mode == "local-only"


def test_detect_mode_template():
    """Test template mode detection."""
    config = MagicMock()
    mode = detect_create_mode(
        config=config,
        template="standard-project",
        api_only=False,
        local_only=False,
    )
    assert mode == "template"


def test_detect_mode_conflict_raises():
    """Test conflicting flags raise error."""
    config = MagicMock()
    with pytest.raises(ValueError) as exc:
        detect_create_mode(
            config=config,
            template=None,
            api_only=True,
            local_only=True,
        )
    assert "conflict" in str(exc.value).lower()


def test_prompt_for_create_options_no_templates_available(tmp_path):
    """Test that prompt_for_create_options exits with error when no templates available."""
    config = MagicMock()
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    
    with patch('proj.commands.projects.get_templates_source', return_value=templates_source):
        with patch('proj.commands.projects.list_templates', return_value=[]):
            with pytest.raises(typer.Exit) as exc_info:
                prompt_for_create_options(config)
            
            # Should exit with code 1
            assert exc_info.value.exit_code == 1
