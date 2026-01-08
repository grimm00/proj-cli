"""Tests for import project command."""
from tests.conftest import assert_command_exists


def test_import_command_exists():
    """Test that import command exists."""
    assert_command_exists(["import-json"])
