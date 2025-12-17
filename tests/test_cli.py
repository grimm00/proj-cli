"""Tests for CLI entry point."""
import subprocess
import sys


def test_cli_version():
    """Test that proj --version works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_cli_help():
    """Test that proj --help works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    stdout_lower = result.stdout.lower()
    assert "project" in stdout_lower or "inventory" in stdout_lower


def test_cli_no_args():
    """Test that proj with no args shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "proj"],
        capture_output=True,
        text=True,
    )
    # no_args_is_help=True means Typer exits with code 2 but shows help
    assert result.returncode == 2
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()
