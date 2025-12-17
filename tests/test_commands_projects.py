"""Tests for project commands."""
import subprocess
import sys


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
