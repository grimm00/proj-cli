"""Tests for CRUD project commands (get, update, delete, archive)."""
from tests.conftest import assert_command_exists


def test_get_command_exists():
    """Test that get command exists."""
    assert_command_exists(["get"])


def test_update_command_exists():
    """Test that update command exists."""
    assert_command_exists(["update"])


def test_delete_command_exists():
    """Test that delete command exists."""
    assert_command_exists(["delete"])


def test_archive_command_exists():
    """Test that archive command exists."""
    assert_command_exists(["archive"])
