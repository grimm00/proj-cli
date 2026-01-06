"""Tests for git initialization (Phase 4, Task 7)."""
import pytest
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


@patch('proj.commands.projects.init_git')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_git_init_runs_by_default(
    mock_config_load, mock_get_source, mock_create, mock_init_git, tmp_path
):
    """Test git init runs by default."""
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

    project_path = tmp_path / "projects" / "my-app"
    # Create the directory so init_git can use it
    project_path.mkdir(parents=True)
    mock_create.return_value = project_path
    mock_init_git.return_value = True

    target_dir = tmp_path / "projects"
    target_dir.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # git init should be called
    mock_init_git.assert_called_once_with(project_path)


@patch('proj.commands.projects.init_git')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_no_git_skips_init(
    mock_config_load, mock_get_source, mock_create, mock_init_git, tmp_path
):
    """Test --no-git skips git init."""
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

    project_path = tmp_path / "projects" / "my-app"
    mock_create.return_value = project_path

    target_dir = tmp_path / "projects"
    target_dir.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--local-only",
        "--no-git",
        "--no-register",
    ])

    assert result.exit_code == 0
    # git init should NOT be called
    mock_init_git.assert_not_called()


@patch('proj.commands.projects.init_git')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_git_init_handles_errors_gracefully(
    mock_config_load, mock_get_source, mock_create, mock_init_git, tmp_path
):
    """Test git init handles errors gracefully."""
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

    project_path = tmp_path / "projects" / "my-app"
    # Create the directory so init_git can use it
    project_path.mkdir(parents=True)
    mock_create.return_value = project_path
    # Simulate git init failure
    mock_init_git.return_value = False

    target_dir = tmp_path / "projects"
    target_dir.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--local-only",
        "--no-register",
    ])

    # Should still succeed (git init failure is non-fatal)
    assert result.exit_code == 0
    # Should show warning about git init failure
    assert "failed to initialize git" in result.output.lower()
    # git init should have been attempted
    mock_init_git.assert_called_once_with(project_path)

