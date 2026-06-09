"""Expected skills validation for generated projects (ADR-001 / FR-BNDL-3)."""

from pathlib import Path
from typing import Optional

import yaml
from rich.console import Console

# Placeholder until ADR-002 defines automated corpus install
CORPUS_INSTALL_GUIDANCE = (
    "Install workflow skills globally under ~/.cursor/skills/<name>/ "
    "(or ~/.claude/skills/<name>/). "
    "The skill corpus is a separate product from dev-infra templates (ADR-001); "
    "automated corpus install is pending ADR-002."
)

DEFAULT_SKILL_ROOTS = (
    Path.home() / ".cursor" / "skills",
    Path.home() / ".claude" / "skills",
)


def load_expected_skills(project_path: Path) -> list[str]:
    """Load expected_skills identifiers from project-root `.dev-infra.yml`."""
    meta_path = project_path / ".dev-infra.yml"
    if not meta_path.is_file():
        return []

    with meta_path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    skills = data.get("expected_skills") or []
    if not isinstance(skills, list):
        return []

    return [name for name in skills if isinstance(name, str) and name.strip()]


def is_skill_installed(
    skill_name: str,
    skill_roots: Optional[tuple[Path, ...]] = None,
) -> bool:
    """Return True when a skill directory exists under any global skills root."""
    roots = skill_roots or DEFAULT_SKILL_ROOTS
    for root in roots:
        if (root / skill_name).is_dir():
            return True
    return False


def find_missing_skills(
    project_path: Path,
    skill_roots: Optional[tuple[Path, ...]] = None,
) -> list[str]:
    """Return sorted list of expected skills that are not installed."""
    missing = []
    for name in load_expected_skills(project_path):
        if not is_skill_installed(name, skill_roots):
            missing.append(name)
    return sorted(missing)


def warn_missing_expected_skills(
    project_path: Path,
    console: Console,
    skill_roots: Optional[tuple[Path, ...]] = None,
) -> list[str]:
    """Warn for missing expected skills; never raise or block setup."""
    expected = load_expected_skills(project_path)
    if not expected:
        return []

    missing = find_missing_skills(project_path, skill_roots)
    if not missing:
        return []

    console.print(
        "[yellow]⚠ Missing expected workflow skills "
        f"({len(missing)} of {len(expected)}):[/yellow]"
    )
    for name in missing:
        console.print(f"[yellow]  • {name}[/yellow]")
    console.print(f"[dim]{CORPUS_INSTALL_GUIDANCE}[/dim]")
    return missing
