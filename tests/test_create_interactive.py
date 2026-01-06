"""Tests for interactive mode (Phase 4, Task 8)."""
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner
from proj.cli import app

runner = CliRunner()


@patch('rich.prompt.Prompt')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.templates.list_templates')
@patch('proj.commands.projects.Config.load')
def test_create_interactive_prompts_for_name(
    mock_config_load, mock_list_templates, mock_get_source, mock_create,
    mock_prompt, tmp_path
):
    """Test interactive mode prompts for project name."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.templates.default = "standard-project"
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates
    mock_list_templates.return_value = ["standard-project", "learning-project"]

    project_path = tmp_path / "my-app"
    project_path.mkdir()
    mock_create.return_value = project_path

    # Simulate user input
    mock_prompt.ask.side_effect = [
        "my-app",  # Project name
        "standard-project",  # Template type
        str(tmp_path),  # Target directory
        "",  # Description (optional)
    ]

    result = runner.invoke(app, [
        "create",
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # Should have prompted for name
    assert mock_prompt.ask.called


@patch('proj.commands.projects.Prompt')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.templates.list_templates')
@patch('proj.commands.projects.Config.load')
def test_create_interactive_prompts_for_template(
    mock_config_load, mock_list_templates, mock_get_source, mock_create,
    mock_prompt, tmp_path
):
    """Test interactive mode prompts for template type."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.templates.default = "standard-project"
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates
    mock_list_templates.return_value = ["standard-project", "learning-project"]

    project_path = tmp_path / "my-app"
    project_path.mkdir()
    mock_create.return_value = project_path

    # Simulate user input
    mock_prompt.ask.side_effect = [
        "my-app",           # Project name
        "learning-project", # Template type (user choice)
        str(tmp_path),      # Target directory
        "",                 # Description (optional)
    ]

    result = runner.invoke(app, [
        "create",
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # Should have prompted for template
    call_args = [str(call) for call in mock_prompt.ask.call_args_list]
    template_prompted = any(
        "template" in str(call).lower() for call in call_args
    )
    assert template_prompted


@patch('proj.commands.projects.Prompt')
@patch('proj.commands.projects.create_from_template')
@patch('proj.commands.projects.get_templates_source')
@patch('proj.templates.list_templates')
@patch('proj.commands.projects.Config.load')
def test_create_interactive_prompts_for_target_dir(
    mock_config_load, mock_list_templates, mock_get_source, mock_create,
    mock_prompt, tmp_path
):
    """Test interactive mode prompts for target directory."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config.templates.default = "standard-project"
    mock_config_load.return_value = mock_config

    templates = tmp_path / "templates"
    templates.mkdir()
    standard = templates / "standard-project"
    standard.mkdir()
    (standard / "README.md").write_text("[Project Name]")
    mock_get_source.return_value = templates
    mock_list_templates.return_value = ["standard-project"]

    project_path = tmp_path / "my-app"
    project_path.mkdir()
    mock_create.return_value = project_path

    custom_target = tmp_path / "custom"
    custom_target.mkdir()

    # Simulate user input
    mock_prompt.ask.side_effect = [
        "my-app",           # Project name
        "standard-project", # Template type
        str(custom_target), # Target directory (user choice)
        "",                 # Description (optional)
    ]

    result = runner.invoke(app, [
        "create",
        "--local-only",
        "--no-register",
    ])

    assert result.exit_code == 0
    # Should have prompted for target directory
    call_args = [str(call) for call in mock_prompt.ask.call_args_list]
    target_prompted = any(
        "target" in str(call).lower() or "directory" in str(call).lower()
        for call in call_args
    )
    assert target_prompted


@patch('rich.prompt.Prompt')
@patch('proj.commands.projects.Config.load')
def test_create_interactive_handles_cancellation(
    mock_config_load, mock_prompt, tmp_path
):
    """Test interactive mode handles cancellation gracefully."""
    mock_config = MagicMock()
    mock_config.default_project_dir = tmp_path
    mock_config.api_enabled = False
    mock_config_load.return_value = mock_config

    # Simulate user cancellation (KeyboardInterrupt)
    mock_prompt.ask.side_effect = KeyboardInterrupt()

    result = runner.invoke(app, [
        "create",
        "--local-only",
    ])

    # Should exit gracefully (not crash)
    assert result.exit_code != 0
    # Should not show error traceback
    assert "Traceback" not in result.output

