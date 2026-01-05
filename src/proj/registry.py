"""Local registry for tracking template-created projects."""
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from proj.config import get_data_dir


@dataclass
class RegistryProject:
    """A project tracked in the registry for template sync.

    Minimal schema - only sync-related fields.
    Project metadata lives in inventory.json.
    Cross-references inventory via path field.
    
    Attributes:
        path: Cross-reference key to inventory.json
        template: Template type used to create the project
        template_version: Version of the template used (for sync detection)
        created_at: Timestamp when the project was created
    """
    
    path: Path  # Cross-reference key to inventory
    template: str  # Template type used
    template_version: str  # Template version for sync
    created_at: datetime  # When created


@dataclass
class Registry:
    """Local registry for template sync tracking.

    This is a sync overlay, not a project store.
    All project metadata lives in inventory.json.
    
    Attributes:
        version: Registry schema version
        projects: List of registered projects for sync tracking
    """

    version: str = "1.0"
    projects: list[RegistryProject] = field(default_factory=list)


def _get_registry_path() -> Path:
    """Get the path to the registry file."""
    return get_data_dir() / "registry.json"


def load_registry() -> Registry:
    """Load registry from disk, creating empty registry if not exists."""
    registry_path = _get_registry_path()

    if not registry_path.exists():
        return Registry()

    with open(registry_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    projects = []
    for proj_data in data.get("projects", []):
        # Minimal schema - only sync fields
        projects.append(
            RegistryProject(
                path=Path(proj_data["path"]),
                template=proj_data["template"],
                template_version=proj_data["template_version"],
                created_at=datetime.fromisoformat(proj_data["created_at"]),
            )
        )

    return Registry(version=data.get("version", "1.0"), projects=projects)


def save_registry(registry: Registry) -> None:
    """Save registry to disk with atomic write."""
    registry_path = _get_registry_path()

    # Ensure directory exists
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert to JSON-serializable dict (minimal schema)
    data = {
        "version": registry.version,
        "projects": [
            {
                "path": str(proj.path),
                "template": proj.template,
                "template_version": proj.template_version,
                "created_at": proj.created_at.isoformat(),
            }
            for proj in registry.projects
        ],
    }

    # Write with indentation for human readability
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_project(
    path: Path,
    template: str,
    template_version: str,
) -> RegistryProject:
    """Add a new project to the registry for sync tracking.

    Note: This only adds to registry. Caller should also add to inventory.
    
    Args:
        path: Project path (cross-reference key to inventory)
        template: Template type used
        template_version: Template version for sync
        
    Returns:
        RegistryProject instance that was added
        
    Raises:
        ValueError: If project at path is already registered
    """
    registry = load_registry()

    # Check for duplicates
    for existing in registry.projects:
        if existing.path == path:
            raise ValueError(f"Project at {path} already registered")

    project = RegistryProject(
        path=path,
        template=template,
        template_version=template_version,
        created_at=datetime.now(),
    )

    registry.projects.append(project)
    save_registry(registry)

    return project


def remove_project(path: Path) -> bool:
    """Remove a project from the registry by path.
    
    Args:
        path: Project path to remove
        
    Returns:
        True if project was removed, False if not found
    """
    registry = load_registry()

    original_count = len(registry.projects)
    registry.projects = [p for p in registry.projects if p.path != path]

    if len(registry.projects) < original_count:
        save_registry(registry)
        return True

    return False


def get_project_by_path(path: Path) -> Optional[RegistryProject]:
    """Find a project by its path (cross-reference key).
    
    Args:
        path: Project path to look up
        
    Returns:
        RegistryProject if found, None otherwise
    """
    registry = load_registry()
    for project in registry.projects:
        if project.path == path:
            return project
    return None


def is_registered(path: Path) -> bool:
    """Check if a project path is registered for sync tracking.
    
    Args:
        path: Project path to check
        
    Returns:
        True if project is registered, False otherwise
    """
    return get_project_by_path(path) is not None

