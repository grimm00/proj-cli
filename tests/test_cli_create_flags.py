"""Tests for create command flags (Phase 4, Task 2)."""
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


def test_create_template_flag_recognized():
    """Test --template flag is recognized."""
    # Dry run to avoid side effects
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--dry-run"
    ])
    # Should not fail with "No such option" (Typer's error message)
    assert "no such option" not in result.output.lower()


def test_create_api_only_flag_recognized():
    """Test --api-only flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--api-only",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_local_only_flag_recognized():
    """Test --local-only flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--local-only",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_target_dir_flag_recognized():
    """Test --target-dir flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--target-dir", "/tmp",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_no_git_flag_recognized():
    """Test --no-git flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--no-git",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_register_flag_recognized():
    """Test --register flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--register",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_no_register_flag_recognized():
    """Test --no-register flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--no-register",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()


def test_create_dry_run_flag_recognized():
    """Test --dry-run flag is recognized."""
    result = runner.invoke(app, [
        "create", "test-app",
        "--template", "standard-project",
        "--dry-run"
    ])
    assert "no such option" not in result.output.lower()
