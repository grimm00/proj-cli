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


def test_config_has_api_enabled():
    """Test that config has api_enabled setting."""
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'api_enabled')


def test_config_api_enabled_default_true():
    """Test default api_enabled is True."""
    from proj.config import Config
    config = Config.load()
    assert config.api_enabled is True


def test_config_api_enabled_env_override():
    """Test PROJ_API_ENABLED environment variable override."""
    with patch.dict(os.environ, {"PROJ_API_ENABLED": "false"}):
        from proj.config import Config
        config = Config.load()
        assert config.api_enabled is False


def test_config_has_templates_nested():
    """Test that config has templates nested config."""
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'templates')


def test_config_templates_source_default_none():
    """Test templates.source defaults to None."""
    from proj.config import Config
    config = Config.load()
    assert config.templates.source is None


def test_config_templates_default_value():
    """Test templates.default is standard-project."""
    from proj.config import Config
    config = Config.load()
    assert config.templates.default == "standard-project"


def test_config_templates_source_env_override():
    """Test PROJ_TEMPLATES__SOURCE environment variable."""
    with patch.dict(os.environ, {"PROJ_TEMPLATES__SOURCE": "/path/to/templates"}):
        from proj.config import Config
        config = Config.load()
        assert str(config.templates.source) == "/path/to/templates"


def test_config_has_registry_nested():
    """Test that config has registry nested config."""
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'registry')


def test_config_registry_path_xdg_default():
    """Test registry.path defaults to XDG data dir."""
    from proj.config import Config, get_data_dir
    config = Config.load()
    expected = get_data_dir() / "registry.json"
    assert config.registry.path == expected


def test_config_registry_path_env_override():
    """Test PROJ_REGISTRY__PATH environment variable."""
    with patch.dict(os.environ, {"PROJ_REGISTRY__PATH": "/custom/registry.json"}):
        from proj.config import Config
        config = Config.load()
        assert str(config.registry.path) == "/custom/registry.json"
