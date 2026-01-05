"""Local registry for tracking template-created projects."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class RegistryProject:
    """A project tracked in the local registry.
    
    Attributes:
        id: Unique identifier (UUID) for the project
        name: Project name
        path: Absolute path to the project directory
        template: Template type used to create the project (e.g., "standard-project")
        template_version: Version of the template used
        created_at: Timestamp when the project was created
        work_prod_id: Optional ID linking to work-prod API project (if synced)
        metadata: Optional dictionary for additional project metadata
    """
    
    id: str
    name: str
    path: Path
    template: str
    template_version: str
    created_at: datetime
    work_prod_id: Optional[int] = None
    metadata: dict = field(default_factory=dict)

