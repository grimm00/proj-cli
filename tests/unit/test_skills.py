"""Unit tests for expected_skills validation (ADR-001 / Group 5)."""

from pathlib import Path

import yaml
from rich.console import Console

from proj.skills import (
    CORPUS_INSTALL_GUIDANCE,
    find_missing_skills,
    is_skill_installed,
    load_expected_skills,
    warn_missing_expected_skills,
)


def _write_dev_infra(project_path: Path, skills: list[str]) -> None:
    content = {"template": "standard-project", "expected_skills": skills}
    (project_path / ".dev-infra.yml").write_text(
        yaml.dump(content, default_flow_style=False),
        encoding="utf-8",
    )


def test_load_expected_skills_parses_manifest(tmp_path):
    _write_dev_infra(tmp_path, ["explore", "research"])

    assert load_expected_skills(tmp_path) == ["explore", "research"]


def test_load_expected_skills_missing_file_returns_empty(tmp_path):
    assert load_expected_skills(tmp_path) == []


def test_is_skill_installed_checks_cursor_and_claude_roots(tmp_path):
    cursor_root = tmp_path / ".cursor" / "skills"
    claude_root = tmp_path / ".claude" / "skills"
    roots = (cursor_root, claude_root)

    (cursor_root / "explore").mkdir(parents=True)
    assert is_skill_installed("explore", skill_roots=roots) is True
    assert is_skill_installed("missing", skill_roots=roots) is False

    (claude_root / "research").mkdir(parents=True)
    assert is_skill_installed("research", skill_roots=roots) is True


def test_find_missing_skills_returns_sorted_missing(tmp_path):
    _write_dev_infra(tmp_path, ["commit", "explore", "research"])
    roots = (tmp_path / "skills",)
    (tmp_path / "skills" / "explore").mkdir(parents=True)

    assert find_missing_skills(tmp_path, skill_roots=roots) == [
        "commit",
        "research",
    ]


def test_warn_missing_expected_skills_prints_guidance(tmp_path, capsys):
    _write_dev_infra(tmp_path, ["explore"])
    console = Console(force_terminal=True, width=120)

    missing = warn_missing_expected_skills(
        tmp_path,
        console,
        skill_roots=(tmp_path / "empty",),
    )

    assert missing == ["explore"]
    output = capsys.readouterr().out
    assert "explore" in output
    assert "ADR-002" in output
    assert CORPUS_INSTALL_GUIDANCE.split(".")[0] in output


def test_warn_missing_expected_skills_silent_when_all_present(tmp_path, capsys):
    _write_dev_infra(tmp_path, ["explore"])
    roots = (tmp_path / "skills",)
    (tmp_path / "skills" / "explore").mkdir(parents=True)
    console = Console(force_terminal=True, width=120)

    missing = warn_missing_expected_skills(tmp_path, console, skill_roots=roots)

    assert missing == []
    assert capsys.readouterr().out == ""
