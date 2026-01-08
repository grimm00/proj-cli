"""Project management commands.

This package provides CLI commands for project management:
- list_projects, search_projects - List and search operations
- get_project, update_project, delete_project, archive_project - CRUD operations
- create_project - Project creation with multiple modes
- import_json - Import projects from JSON

Module structure:
- helpers.py - Shared utilities (API client, status emoji, etc.)
- list.py - List and search commands
- crud.py - CRUD operations (get, update, delete, archive)
- create.py - Project creation with interactive/template/API modes
- import_export.py - Import/export functionality
"""

__all__ = [
    # Helpers
    "STATUS_EMOJI",
    "get_client",
    "sync_to_api",
    "init_git",
    "console",
    "logger",
    # List
    "list_projects",
    "search_projects",
    # CRUD
    "get_project",
    "update_project",
    "delete_project",
    "archive_project",
    # Create
    "create_project",
    "detect_create_mode",
    "prompt_for_create_options",
    # Import/Export
    "import_json",
]

# Helpers - shared utilities
from .helpers import (
    STATUS_EMOJI,
    get_client,
    sync_to_api,
    init_git,
    console,
    logger,
)

# List - list and search operations
from .list import list_projects, search_projects

# CRUD - get, update, delete, archive operations
from .crud import (
    get_project,
    update_project,
    delete_project,
    archive_project,
)

# Create - project creation with multiple modes
from .create import (
    create_project,
    detect_create_mode,
    prompt_for_create_options,
)

# Import/Export - JSON import functionality
from .import_export import import_json
