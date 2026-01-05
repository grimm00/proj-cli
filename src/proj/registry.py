"""Local registry for tracking template-created projects."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


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

