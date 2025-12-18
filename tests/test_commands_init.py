"""Tests for init command."""
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from proj.cli import app

runner = CliRunner()


def test_init_command_exists():
    """Test that init command exists."""
    result = runner.invoke(app, ["init", "--help"])
    assert result.exit_code == 0
    assert "Initialize proj configuration" in result.stdout


def test_init_command_creates_config(mock_xdg_dirs):
    """Test that init command creates config file."""
    from proj.config import get_config_file

    config_file = get_config_file()
    # Ensure config doesn't exist
    if config_file.exists():
        config_file.unlink()

    # Mock user input
    with patch("proj.commands.init.Prompt") as mock_prompt:
        mock_prompt.ask.side_effect = [
            "http://test:8000",  # API URL
            "testuser",  # GitHub username
            str(Path.home() / "Projects"),  # Scan dirs
        ]

        result = runner.invoke(app, ["init", "--force"])

        assert result.exit_code == 0
        assert config_file.exists()
        assert "Configuration saved" in result.stdout


def test_init_command_with_existing_config(mock_xdg_dirs):
    """Test that init command handles existing config."""
    from proj.config import Config, get_config_file

    config_file = get_config_file()
    # Create existing config
    config = Config(api_url="http://old:5000")
    config.save()

    # Mock user declining overwrite
    with patch("proj.commands.init.Confirm") as mock_confirm:
        mock_confirm.ask.return_value = False

        result = runner.invoke(app, ["init"])

        # Should abort without overwriting
        assert result.exit_code == 1  # typer.Abort() raises SystemExit(1)


def test_init_command_force_overwrites(mock_xdg_dirs):
    """Test that --force overwrites existing config."""
    from proj.config import Config, get_config_file

    config_file = get_config_file()
    # Create existing config
    config = Config(api_url="http://old:5000")
    config.save()

    # Mock user input
    with patch("proj.commands.init.Prompt") as mock_prompt:
        mock_prompt.ask.side_effect = [
            "http://new:8000",  # API URL
            "newuser",  # GitHub username
            str(Path.home() / "Projects"),  # Scan dirs
        ]

        result = runner.invoke(app, ["init", "--force"])

        assert result.exit_code == 0
        # Verify config was overwritten
        loaded = Config.load()
        assert loaded.api_url == "http://new:8000"
        assert loaded.github_username == "newuser"

