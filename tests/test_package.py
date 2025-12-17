"""Tests for package structure and metadata."""
import importlib.metadata


def test_package_importable():
    """Test that proj package can be imported."""
    import proj
    assert proj is not None


def test_package_has_version():
    """Test that package has version metadata."""
    version = importlib.metadata.version("proj-cli")
    assert version is not None
    assert len(version) > 0


def test_version_matches_metadata():
    """Test that __version__ matches installed package metadata."""
    from proj import __version__
    metadata_version = importlib.metadata.version("proj-cli")
    assert __version__ == metadata_version


def test_cli_module_exists():
    """Test that cli module exists."""
    from proj import cli
    assert cli is not None


def test_config_module_exists():
    """Test that config module exists."""
    from proj import config
    assert config is not None
