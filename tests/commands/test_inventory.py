"""Tests for inventory commands."""
from tests.conftest import assert_command_exists


def test_inv_command_group_exists():
    """Test that inv command group exists."""
    assert_command_exists(["inv"], expected_text="scan")


def test_inv_scan_github_exists():
    """Test that inv scan github command exists."""
    assert_command_exists(["inv", "scan", "github"])


def test_inv_scan_local_exists():
    """Test that inv scan local command exists."""
    assert_command_exists(["inv", "scan", "local"])


def test_inv_analyze_exists():
    """Test that inv analyze command exists."""
    assert_command_exists(["inv", "analyze"])


def test_inv_dedupe_exists():
    """Test that inv dedupe command exists."""
    assert_command_exists(["inv", "dedupe"])


def test_inv_export_json_exists():
    """Test that inv export json command exists."""
    assert_command_exists(["inv", "export", "json"])


def test_inv_export_api_exists():
    """Test that inv export api command exists."""
    assert_command_exists(["inv", "export", "api"])


def test_inv_export_api_has_no_dedupe_option():
    """Test that inv export api command has --no-dedupe option."""
    result = assert_command_exists(["inv", "export", "api"])
    assert "--no-dedupe" in result.stdout


def test_inv_status_exists():
    """Test that inv status command exists."""
    assert_command_exists(["inv", "status"])
