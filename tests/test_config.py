"""Tests for configuration management."""
import yaml


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


def test_config_env_override(isolated_xdg, monkeypatch):
    """Test that environment variables override config."""
    monkeypatch.setenv("PROJ_API_URL", "http://test:8000")
    from proj.config import Config
    config = Config.load()
    assert config.api_url == "http://test:8000"


def test_config_has_api_enabled(tmp_path, monkeypatch):
    """Test that config has api_enabled setting."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'api_enabled')


def test_config_api_enabled_default_true(tmp_path, monkeypatch):
    """Test default api_enabled is True."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert config.api_enabled is True


def test_config_api_enabled_env_override(isolated_xdg, monkeypatch):
    """Test PROJ_API_ENABLED environment variable override."""
    monkeypatch.setenv("PROJ_API_ENABLED", "false")
    from proj.config import Config
    config = Config.load()
    assert config.api_enabled is False


def test_config_has_templates_nested(tmp_path, monkeypatch):
    """Test that config has templates nested config."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'templates')


def test_config_templates_source_default_none(tmp_path, monkeypatch):
    """Test templates.source defaults to None."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert config.templates.source is None


def test_config_templates_default_value(tmp_path, monkeypatch):
    """Test templates.default is standard-project."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert config.templates.default == "standard-project"


def test_config_templates_source_env_override(isolated_xdg, monkeypatch):
    """Test PROJ_TEMPLATES__SOURCE environment variable."""
    monkeypatch.setenv("PROJ_TEMPLATES__SOURCE", "/path/to/templates")
    from proj.config import Config
    config = Config.load()
    assert str(config.templates.source) == "/path/to/templates"


def test_config_has_registry_nested(tmp_path, monkeypatch):
    """Test that config has registry nested config."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'registry')


def test_config_registry_path_xdg_default(isolated_xdg):
    """Test registry.path defaults to XDG data dir."""
    from proj.config import Config, get_data_dir
    config = Config.load()
    expected = get_data_dir() / "registry.json"
    assert config.registry.path == expected


def test_config_registry_path_env_override(isolated_xdg, monkeypatch):
    """Test PROJ_REGISTRY__PATH environment variable."""
    monkeypatch.setenv("PROJ_REGISTRY__PATH", "/custom/registry.json")
    from proj.config import Config
    config = Config.load()
    assert str(config.registry.path) == "/custom/registry.json"


def test_config_has_default_project_dir(tmp_path, monkeypatch):
    """Test that config has default_project_dir setting."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    config = Config.load()
    assert hasattr(config, 'default_project_dir')


def test_config_default_project_dir_value(tmp_path, monkeypatch):
    """Test default_project_dir defaults to ~/Projects."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    from proj.config import Config
    from pathlib import Path
    config = Config.load()
    expected = Path.home() / "Projects"
    assert config.default_project_dir == expected


def test_config_default_project_dir_env_override(isolated_xdg, monkeypatch):
    """Test PROJ_DEFAULT_PROJECT_DIR environment variable."""
    monkeypatch.setenv("PROJ_DEFAULT_PROJECT_DIR", "/custom/projects")
    from proj.config import Config
    config = Config.load()
    assert str(config.default_project_dir) == "/custom/projects"


def test_config_save_includes_new_fields(tmp_path, monkeypatch):
    """Test that save() includes new configuration fields."""
    # Use temp directory for config
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    from proj.config import Config, get_config_file
    config = Config.load()
    config.save()

    config_file = get_config_file()
    with open(config_file) as f:
        saved = yaml.safe_load(f)

    assert 'api_enabled' in saved
    assert 'templates' in saved
    assert 'registry' in saved
    assert 'default_project_dir' in saved


def test_config_load_nested_from_yaml(tmp_path, monkeypatch):
    """Test loading nested config from YAML file."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

    from proj.config import get_config_dir, get_config_file, Config

    # Create config directory and file
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = get_config_file()
    config_content = {
        'api_enabled': False,
        'templates': {
            'source': '/custom/templates',
            'default': 'learning-project'
        },
        'registry': {
            'path': '/custom/registry.json'
        },
        'default_project_dir': '/custom/projects'
    }
    with open(config_file, 'w') as f:
        yaml.dump(config_content, f)

    config = Config.load()
    assert config.api_enabled is False
    assert str(config.templates.source) == '/custom/templates'
    assert config.templates.default == 'learning-project'
