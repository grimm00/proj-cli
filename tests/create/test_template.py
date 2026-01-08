"""Tests for template mode (Phase 4, Task 4)."""
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
    (standard / "start.txt").write_text("[Project Name]")
    return templates


@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_creates_directory(
    mock_config_load, mock_get_source, mock_templates_source, tmp_path
):
    """Test template mode creates local directory."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    assert (target_dir / "my-app").exists()


@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_replaces_placeholders(
    mock_config_load, mock_get_source, mock_templates_source, tmp_path
):
    """Test template mode replaces placeholders."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    readme = (target_dir / "my-app" / "README.md").read_text()
    assert "my-app" in readme
    assert "[Project Name]" not in readme


@patch('proj.commands.projects.add_project')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_registers_project(
    mock_config_load, mock_get_source, mock_add_project,
    mock_templates_source, tmp_path
):
    """Test template mode registers project by default."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.registry.path = tmp_path / "registry.json"
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
    ])

    assert result.exit_code == 0
    mock_add_project.assert_called_once()


@patch('proj.registry.add_project')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_no_register_skips_registry(
    mock_config_load, mock_get_source, mock_add_project,
    mock_templates_source, tmp_path
):
    """Test template mode with --no-register skips registry."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    mock_add_project.assert_not_called()


@patch('subprocess.run')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_initializes_git(
    mock_config_load, mock_get_source, mock_subprocess,
    mock_templates_source, tmp_path
):
    """Test template mode initializes git by default."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source
    mock_subprocess.return_value = MagicMock(returncode=0)

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # git init should be called
    mock_subprocess.assert_called()
    call_args = mock_subprocess.call_args_list
    assert any("git" in str(c) and "init" in str(c) for c in call_args)


@patch('subprocess.run')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_no_git_skips_init(
    mock_config_load, mock_get_source, mock_subprocess,
    mock_templates_source, tmp_path
):
    """Test template mode with --no-git skips git init."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config
    mock_get_source.return_value = mock_templates_source

    target_dir = tmp_path / "projects"
    target_dir.mkdir()

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-git",
        "--no-register",
    ])

    assert result.exit_code == 0
    # git init should NOT be called
    if mock_subprocess.called:
        call_args = mock_subprocess.call_args_list
        assert not any(
            "git" in str(c) and "init" in str(c) for c in call_args
        )
