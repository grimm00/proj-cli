"""Tests for inventory commands."""
import subprocess
import sys


def test_inv_command_group_exists():
    """Test that inv command group exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "scan" in result.stdout.lower()


def test_inv_scan_github_exists():
    """Test that inv scan github command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "scan", "github", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_scan_local_exists():
    """Test that inv scan local command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "scan", "local", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_analyze_exists():
    """Test that inv analyze command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "analyze", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_dedupe_exists():
    """Test that inv dedupe command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "dedupe", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_export_json_exists():
    """Test that inv export json command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "export", "json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_export_api_exists():
    """Test that inv export api command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "export", "api", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_inv_status_exists():
    """Test that inv status command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "inv", "status", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
