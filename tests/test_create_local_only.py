"""Tests for local-only mode (Phase 4, Task 5)."""
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


def test_create_local_only_requires_template():
    """Test local-only mode requires --template."""
    result = runner.invoke(app, [
        "create", "my-app",
        "--local-only",
        # No --template
    ])

    assert result.exit_code != 0
    assert "template" in result.output.lower()


@patch('proj.commands.projects.get_client')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_local_only_does_not_call_api(
    mock_config_load, mock_get_source, mock_get_client, tmp_path
):
    """Test local-only mode does NOT call API."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = True  # Even with API enabled
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    target = tmp_path / "projects"
    target.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target),
        "--local-only",
        "--no-register",
        "--no-git",
    ])

    assert result.exit_code == 0
    mock_get_client.assert_not_called()


@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_local_only_works_when_api_disabled(
    mock_config_load, mock_get_source, tmp_path
):
    """Test local-only mode works when api_enabled=False."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    target = tmp_path / "projects"
    target.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target),
        "--local-only",
        "--no-register",
        "--no-git",
    ])

    assert result.exit_code == 0
    assert (target / "my-app").exists()


@patch('proj.commands.projects.add_project')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_local_only_registers_locally(
    mock_config_load, mock_get_source, mock_add_project, tmp_path
):
    """Test local-only mode registers locally."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    target = tmp_path / "projects"
    target.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target),
        "--local-only",
        "--no-git",
    ])

    assert result.exit_code == 0
    mock_add_project.assert_called_once()
