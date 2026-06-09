"""CLI tests for expected_skills warn-not-error validation."""

from unittest.mock import MagicMock, patch

from typer.testing import CliRunner

from proj.cli import app

runner = CliRunner()


def _dev_infra_yml(skills: list[str]) -> str:
    return (
        "template: standard-project\n"
        "expected_skills:\n"
        + "".join(f"  - {skill}\n" for skill in skills)
    )


@patch("proj.commands.projects.create.warn_missing_expected_skills")
@patch("proj.commands.projects.init_git")
@patch("proj.commands.projects.create_from_template")
@patch("proj.commands.projects.get_templates_source")
@patch("proj.commands.projects.Config.load")
def test_create_warns_on_missing_skills_without_failing(
    mock_config_load,
    mock_get_source,
    mock_create,
    mock_init_git,
    mock_warn_skills,
    tmp_path,
):
    """Missing skills emit warnings but create still exits 0."""
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
    project_path.mkdir(parents=True)
    (project_path / ".dev-infra.yml").write_text(
        _dev_infra_yml(["explore", "research"]),
        encoding="utf-8",
    )
    mock_create.return_value = project_path
    mock_init_git.return_value = True

    def _warn(path, console, skill_roots=None):
        console.print("[yellow]⚠ Missing expected workflow skills (2 of 2):[/yellow]")
        console.print("[yellow]  • explore[/yellow]")
        console.print("[yellow]  • research[/yellow]")
        return ["explore", "research"]

    mock_warn_skills.side_effect = _warn

    (tmp_path / "projects").mkdir(exist_ok=True)

    result = runner.invoke(
        app,
        [
            "create",
            "my-app",
            "--template",
            "standard-project",
            "--local-only",
            "--no-register",
        ],
    )

    assert result.exit_code == 0
    mock_warn_skills.assert_called_once()
    assert "missing expected workflow skills" in result.output.lower()


@patch("proj.commands.projects.init_git")
@patch("proj.commands.projects.create_from_template")
@patch("proj.commands.projects.get_templates_source")
@patch("proj.commands.projects.Config.load")
def test_create_integration_warns_when_skills_absent(
    mock_config_load,
    mock_get_source,
    mock_create,
    mock_init_git,
    tmp_path,
    monkeypatch,
):
    """Real validation warns and still succeeds when skills are not installed."""
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
    project_path.mkdir(parents=True)
    (project_path / ".dev-infra.yml").write_text(
        _dev_infra_yml(["explore"]),
        encoding="utf-8",
    )
    mock_create.return_value = project_path
    mock_init_git.return_value = True

    empty_skills = tmp_path / "empty-skills"
    empty_skills.mkdir()
    monkeypatch.setattr(
        "proj.skills.DEFAULT_SKILL_ROOTS",
        (empty_skills,),
    )

    (tmp_path / "projects").mkdir(exist_ok=True)

    result = runner.invoke(
        app,
        [
            "create",
            "my-app",
            "--template",
            "standard-project",
            "--local-only",
            "--no-register",
        ],
    )

    assert result.exit_code == 0
    assert "missing expected workflow skills" in result.output.lower()
    assert "explore" in result.output.lower()
    assert "adr-002" in result.output.lower()
