"""Integration tests for configuration."""
import os
import yaml

import pytest


def test_config_creates_default_on_first_run(mock_xdg_dirs):
    """Test that default config is created on first run."""
    from proj.config import Config, get_config_file

    config_file = get_config_file()
    assert not config_file.exists()

    # Load config (should use defaults)
    config = Config.load()
    assert config.api_url == "http://localhost:5000"


def test_config_saves_and_loads(mock_xdg_dirs):
    """Test that config can be saved and loaded."""
    from proj.config import Config, get_config_file

    # Create and save config
    config = Config(api_url="http://custom:8000")
    config.save()

    # Load config
    loaded = Config.load()
    assert loaded.api_url == "http://custom:8000"


def test_config_env_override(mock_xdg_dirs, monkeypatch):
    """Test environment variable override."""
    monkeypatch.setenv("PROJ_API_URL", "http://env:9000")

    from proj.config import Config
    config = Config()
    assert config.api_url == "http://env:9000"


def test_config_github_settings(mock_xdg_dirs):
    """Test GitHub settings in config."""
    from proj.config import Config

    config = Config(
        github_username="testuser",
        github_token="test-token",
    )
    config.save()

    loaded = Config.load()
    assert loaded.github_username == "testuser"
    assert loaded.github_token == "test-token"


def test_config_local_scan_dirs(mock_xdg_dirs):
    """Test local scan directories in config."""
    from proj.config import Config

    scan_dirs = ["/path/to/projects", "/another/path"]
    config = Config(local_scan_dirs=scan_dirs)
    config.save()

    loaded = Config.load()
    assert loaded.local_scan_dirs == scan_dirs

