"""Tests for import project command."""
import subprocess
import sys


def test_import_command_exists():
    """Test that import command exists."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "import-json", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
