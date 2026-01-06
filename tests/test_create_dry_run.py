"""Tests for dry-run mode (Phase 4, Task 6)."""
import pytest
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


@pytest.fixture
def mock_templates_source(tmp_path):
    """Create mock templates directory."""
    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    return templates


@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_dry_run_shows_preview(
    mock_config_load, mock_get_source, mock_create, tmp_path
):
    """Test dry-run shows preview."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--dry-run",
    ])

    assert (
        "would create" in result.output.lower() or
        "preview" in result.output.lower()
    )
    mock_create.assert_not_called()


@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_dry_run_does_not_create_directory(
    mock_config_load, mock_get_source, tmp_path
):
    """Test dry-run does NOT create directory."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--dry-run",
    ])

    assert result.exit_code == 0
    assert not (target_dir / "my-app").exists()


@patch('proj.commands.projects.get_client')
def test_create_dry_run_api_does_not_call_api(mock_get_client):
    """Test dry-run with api-only does NOT call API."""
    result = runner.invoke(app, [
        "create", "Test App",
        "--api-only",
        "--dry-run",
    ])

    assert (
        "would create" in result.output.lower() or
        "preview" in result.output.lower()
    )
    mock_get_client.assert_not_called()


@patch('proj.commands.projects.add_project')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_dry_run_does_not_register(
    mock_config_load, mock_get_source, mock_add_project, tmp_path
):
    """Test dry-run does NOT register."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--dry-run",
    ])

    assert result.exit_code == 0
    mock_add_project.assert_not_called()
