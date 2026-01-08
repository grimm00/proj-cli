"""Test fixtures for proj-cli."""
import subprocess
import sys
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_config_dir(tmp_path):
    """Create temporary config directory."""
    config_dir = tmp_path / ".config" / "proj"
    config_dir.mkdir(parents=True)
    return config_dir


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create temporary data directory."""
    data_dir = tmp_path / ".local" / "share" / "proj"
    data_dir.mkdir(parents=True)
    return data_dir


@pytest.fixture
def mock_xdg_dirs(temp_config_dir, temp_data_dir, monkeypatch):
    """Mock XDG directories to use temp dirs."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(temp_config_dir.parent.parent))
    monkeypatch.setenv("XDG_DATA_HOME", str(temp_data_dir.parent.parent))
    return {"config": temp_config_dir, "data": temp_data_dir}


@pytest.fixture
def isolated_xdg(tmp_path, monkeypatch):
    """Fixture to isolate XDG directories for config tests."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    return tmp_path


@pytest.fixture
def sample_inventory():
    """Sample inventory data."""
    return [
        {
            "name": "project-a",
            "remote_url": "https://github.com/user/project-a",
            "source": "github",
        },
        {
            "name": "project-b",
            "local_path": "/home/user/Projects/project-b",
            "source": "local",
        },
    ]


@pytest.fixture
def mock_api_client():
    """Mock API client."""
    with patch("proj.api_client.APIClient") as mock:
        client = Mock()
        mock.return_value = client
        yield client


def assert_command_exists(args: list[str], expected_text: str | None = None):
    """Helper to verify a command exists and shows help.

    Args:
        args: Command arguments (e.g., ["list"], ["inv", "scan", "github"])
        expected_text: Optional text that should appear in help output

    Returns:
        subprocess.CompletedProcess: The completed process result

    Raises:
        AssertionError: If command fails or expected_text not found
    """
    result = subprocess.run(
        [sys.executable, "-m", "proj"] + args + ["--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Command {' '.join(args)} --help failed with exit code {result.returncode}"
    if expected_text:
        assert expected_text.lower() in result.stdout.lower(), f"Expected text '{expected_text}' not found in help output"
    return result
