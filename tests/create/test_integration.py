"""Integration tests for full create workflow (Phase 4, Task 9)."""
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


@patch('proj.commands.projects.add_project')
@patch('proj.commands.projects.init_git')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.Config.load')
def test_create_template_registers_and_inits_git(
    mock_config_load, mock_get_source, mock_create, mock_init_git,
    mock_add_project, tmp_path
):
    """Integration test: template + register + git all work together."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.registry.path = tmp_path / "registry.json"
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    project_path = tmp_path / "projects" / "my-app"
    project_path.mkdir(parents=True)
    mock_create.return_value = project_path
    mock_init_git.return_value = True

    target_dir = tmp_path / "projects"
    target_dir.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
    ])

    assert result.exit_code == 0
    # Should have created from template
    mock_create.assert_called_once()
    # Should have initialized git
    mock_init_git.assert_called_once_with(project_path)
    # Should have registered project
    mock_add_project.assert_called_once_with(
        path=project_path,
        template="standard-project",
        template_version="unknown",
    )


@patch('proj.commands.projects.get_client')
@patch('proj.commands.projects.Config.load')
def test_create_api_only_backward_compatibility(
    mock_config_load, mock_get_client, tmp_path
):
    """Integration test: api-only mode maintains backward compatibility."""
    mock_config = MagicMock()
    mock_config.api_enabled = True
    mock_config_load.return_value = mock_config

    mock_client = MagicMock()
    mock_client.create_project.return_value = {
        "id": 123,
        "name": "My Application",
        "status": "active",
    }
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, [
        "create", "My Application",
        "--api-only",
    ])

    assert result.exit_code == 0
    # Should have called API
    mock_client.create_project.assert_called_once()
    # Should have shown success message
    assert "Created project" in result.output
    assert "123" in result.output


@patch('proj.commands.projects.get_client')
@patch('proj.commands.projects.Config.load')
def test_create_name_only_falls_back_to_api(
    mock_config_load, mock_get_client, tmp_path
):
    """Providing only a name falls back to API (backward compatible)."""
    mock_config = MagicMock()
    mock_config.api_enabled = True
    mock_config_load.return_value = mock_config

    mock_client = MagicMock()
    mock_client.create_project.return_value = {
        "id": 456,
        "name": "My Application",
        "status": "active",
    }
    mock_get_client.return_value = mock_client

    result = runner.invoke(app, ["create", "My Application"])

    assert result.exit_code == 0
    mock_client.create_project.assert_called_once()
    assert "Created project" in result.output


@patch('proj.commands.projects.add_project')
@patch('proj.commands.projects.init_git')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.commands.projects.get_client')
@patch('proj.commands.projects.Config.load')
def test_create_local_only_template_no_api_call(
    mock_config_load, mock_get_client, mock_get_source, mock_create,
    mock_init_git, mock_add_project, tmp_path
):
    """Integration test: local-only + template does NOT call API."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.registry.path = tmp_path / "registry.json"
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates

    project_path = tmp_path / "projects" / "my-app"
    project_path.mkdir(parents=True)
    mock_create.return_value = project_path
    mock_init_git.return_value = True

    target_dir = tmp_path / "projects"
    target_dir.mkdir(exist_ok=True)

    result = runner.invoke(app, [
        "create", "my-app",
        "--template", "standard-project",
        "--target-dir", str(target_dir),
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # Should have created from template
    mock_create.assert_called_once()
    # Should NOT have called API
    mock_get_client.assert_not_called()
    # Should have initialized git
    mock_init_git.assert_called_once_with(project_path)
    # Should NOT have registered (--no-register)
    mock_add_project.assert_not_called()
