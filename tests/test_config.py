"""Tests for configuration management."""
import os
from unittest.mock import patch


def test_config_class_exists():
    """Test that Config class exists."""
    from proj.config import Config
    assert Config is not None


def test_config_has_api_url():
    """Test that config has api_url setting."""
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'api_url')


def test_config_default_api_url():
    """Test default API URL."""
    from proj.config import Config
    config = Config.load()
    assert config.api_url == "http://localhost:5000"


def test_config_xdg_config_path():
    """Test that config uses XDG config path."""
    from proj.config import get_config_dir
    config_dir = get_config_dir()
    # Should be ~/.config/proj or XDG_CONFIG_HOME/proj
    assert "proj" in str(config_dir)


def test_config_xdg_data_path():
    """Test that config uses XDG data path."""
    from proj.config import get_data_dir
    data_dir = get_data_dir()
    # Should be ~/.local/share/proj or XDG_DATA_HOME/proj
    assert "proj" in str(data_dir)


def test_config_env_override():
    """Test that environment variables override config."""
    with patch.dict(os.environ, {"PROJ_API_URL": "http://test:8000"}):
        from proj.config import Config
        # Force reload by creating new instance
        config = Config.load()
        assert config.api_url == "http://test:8000"
