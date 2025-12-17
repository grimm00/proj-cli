"""Test fixtures for proj-cli."""
import json
import os
from pathlib import Path
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

