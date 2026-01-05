"""Template operations for proj-cli."""
import os
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Optional

from proj.config import Config


class TemplateError(Exception):
    """Base exception for template operations."""
    pass


class InvalidProjectNameError(TemplateError):
    """Raised when project name is invalid."""
    pass


class DirectoryNotFoundError(TemplateError):
    """Raised when target directory does not exist."""
    pass


class DirectoryNotWritableError(TemplateError):
    """Raised when target directory is not writable."""
    pass


class TemplateNotFoundError(TemplateError):
    """Raised when template type is not found."""
    pass


class ProjectExistsError(TemplateError):
    """Raised when project directory already exists."""
    pass


def validate_project_name(name: str) -> str:
    """Validate project name matches allowed pattern.

    Args:
        name: Project name to validate.

    Returns:
        Validated name (stripped of leading/trailing whitespace).

    Raises:
        InvalidProjectNameError: If name is invalid.
    """
    # Strip and check for empty
    name = name.strip()
    if not name:
        raise InvalidProjectNameError("Project name cannot be empty")

    # Check for whitespace characters
    if re.search(r'\s', name):
        raise InvalidProjectNameError(
            "Project name cannot contain whitespace. "
            "Use hyphens or underscores instead."
        )

    # Check for valid characters only
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise InvalidProjectNameError(
            "Project name can only contain letters, numbers, "
            "hyphens, and underscores."
        )

    return name


def sanitize_project_name(name: str) -> Optional[str]:
    """Sanitize a project name by fixing common issues.

    Args:
        name: Project name to sanitize.

    Returns:
        Sanitized name, or None if name cannot be sanitized.
    """
    # Strip whitespace
    name = name.strip()
    if not name:
        return None

    # Replace whitespace with hyphens
    name = re.sub(r'\s+', '-', name)

    # Remove invalid characters (keep alphanumeric, hyphen, underscore)
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)

    # Collapse consecutive hyphens
    name = re.sub(r'-+', '-', name)

    # Strip leading/trailing hyphens
    name = name.strip('-')

    return name if name else None


def validate_target_directory(path: Path) -> Path:
    """Validate target directory exists and is writable.

    Args:
        path: Path to target directory.

    Returns:
        Resolved absolute path to directory.

    Raises:
        DirectoryNotFoundError: If directory does not exist.
        DirectoryNotWritableError: If directory is not writable.
    """
    # Check if path is empty before expansion
    # Path("") has no parts and string representation is "."
    if not path.parts or (len(path.parts) == 0 and str(path) == "."):
        raise DirectoryNotFoundError("Target directory path cannot be empty")

    # Expand ~ to home directory
    path = path.expanduser()

    # Resolve to absolute path
    path = path.resolve()

    # Check if exists
    if not path.exists():
        raise DirectoryNotFoundError(
            f"Target directory does not exist: {path}"
        )

    # Check if directory (not file)
    if not path.is_dir():
        raise DirectoryNotFoundError(
            f"Path is not a directory: {path}"
        )

    # Check if writable
    if not os.access(path, os.W_OK):
        raise DirectoryNotWritableError(
            f"Target directory is not writable: {path}"
        )

    return path


def list_templates(source: Path) -> list[str]:
    """List available template types from source directory.

    Args:
        source: Path to templates source directory.

    Returns:
        List of template type names (directory names).

    Raises:
        DirectoryNotFoundError: If source directory does not exist.
    """
    source = source.expanduser().resolve()

    if not source.exists():
        raise DirectoryNotFoundError(
            f"Templates source directory does not exist: {source}"
        )

    if not source.is_dir():
        raise DirectoryNotFoundError(
            f"Templates source is not a directory: {source}"
        )

    templates = []
    for item in source.iterdir():
        # Skip hidden directories and files
        if item.name.startswith('.'):
            continue
        if item.is_dir():
            templates.append(item.name)

    return sorted(templates)


def validate_template_type(template_type: str, source: Path) -> Path:
    """Validate template type exists in source directory.

    Args:
        template_type: Template type name (e.g., "standard-project").
        source: Path to templates source directory.

    Returns:
        Path to the template directory.

    Raises:
        TemplateNotFoundError: If template type does not exist.
    """
    source = source.expanduser().resolve()
    template_path = source / template_type

    if not template_path.exists() or not template_path.is_dir():
        available = list_templates(source)
        available_str = ", ".join(available) if available else "none"
        raise TemplateNotFoundError(
            f"Template '{template_type}' not found in {source}. "
            f"Available templates: {available_str}"
        )

    return template_path


def copy_template(
    template_path: Path,
    target_dir: Path,
    project_name: str,
) -> Path:
    """Copy template to target directory.

    Args:
        template_path: Path to template directory.
        target_dir: Path to target parent directory.
        project_name: Name for the new project directory.

    Returns:
        Path to the created project directory.

    Raises:
        ProjectExistsError: If project directory already exists.
    """
    project_path = target_dir / project_name

    if project_path.exists():
        raise ProjectExistsError(
            f"Project directory already exists: {project_path}"
        )

    # Copy template including hidden files
    # shutil.copytree copies everything by default
    shutil.copytree(template_path, project_path)

    return project_path


def replace_placeholders(
    project_path: Path,
    project_name: str,
    description: Optional[str] = None,
    author: Optional[str] = None,
) -> None:
    """Replace placeholders in project files.

    Replaces the following placeholders:
    - [Project Name] -> project_name
    - [Brief description of what this project does] -> description
    - [Date] -> current date (YYYY-MM-DD)
    - [Author] -> author

    Args:
        project_path: Path to project directory.
        project_name: Project name for replacement.
        description: Project description (optional).
        author: Author name (optional).
    """
    current_date = date.today().strftime("%Y-%m-%d")

    # Default values
    description = description or f"{project_name} project"
    author = author or ""

    # Files to process
    files_to_process = ["README.md", "start.txt"]

    for filename in files_to_process:
        file_path = project_path / filename
        if not file_path.exists():
            continue

        content = file_path.read_text()

        # Replace placeholders
        content = content.replace("[Project Name]", project_name)
        content = content.replace(
            "[Brief description of what this project does]",
            description
        )
        content = content.replace("[Date]", current_date)
        content = content.replace("[Author]", author)

        file_path.write_text(content)


def create_from_template(
    project_name: str,
    template_type: str,
    target_dir: Path,
    templates_source: Path,
    description: Optional[str] = None,
    author: Optional[str] = None,
) -> Path:
    """Create a new project from a template.

    Orchestrates the full workflow:
    1. Validate project name
    2. Validate target directory
    3. Validate template type
    4. Copy template to target
    5. Replace placeholders

    Args:
        project_name: Name for the new project.
        template_type: Template type (e.g., "standard-project").
        target_dir: Directory to create project in.
        templates_source: Path to templates source directory.
        description: Project description (optional).
        author: Author name (optional).

    Returns:
        Path to the created project directory.

    Raises:
        InvalidProjectNameError: If project name is invalid.
        DirectoryNotFoundError: If target or source directory doesn't exist.
        DirectoryNotWritableError: If target directory isn't writable.
        TemplateNotFoundError: If template type doesn't exist.
        ProjectExistsError: If project directory already exists.
    """
    # Validate inputs
    project_name = validate_project_name(project_name)
    target_dir = validate_target_directory(target_dir)
    template_path = validate_template_type(template_type, templates_source)

    # Copy template
    project_path = copy_template(
        template_path=template_path,
        target_dir=target_dir,
        project_name=project_name,
    )

    # Replace placeholders
    replace_placeholders(
        project_path=project_path,
        project_name=project_name,
        description=description,
        author=author,
    )

    return project_path


def get_templates_source(config: Config) -> Path:
    """Get templates source path from config.

    Args:
        config: proj-cli configuration.

    Returns:
        Path to templates source directory.

    Raises:
        TemplateError: If templates source not configured.
    """
    if config.templates.source is None:
        raise TemplateError(
            "Templates source not configured. "
            "Run 'proj init' and set templates.source in config, "
            "or use --templates-source flag."
        )

    return config.templates.source.expanduser().resolve()
