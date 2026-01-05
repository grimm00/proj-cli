"""Template operations for proj-cli."""
import os
import re
from pathlib import Path
from typing import Optional


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
