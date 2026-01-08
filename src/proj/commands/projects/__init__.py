"""Project management commands."""

# Re-export all commands for backward compatibility
# These will be populated as we extract each module

__all__ = [
    # From helpers
    "STATUS_EMOJI",
    "get_client",
    "sync_to_api",
    "init_git",
    # From list
    "list_projects",
    "search_projects",
    # From crud
    "get_project",
    "update_project",
    "delete_project",
    "archive_project",
    # From create
    "create_project",
    "detect_create_mode",
    "prompt_for_create_options",
    # From import_export
    "import_json",
]

# Import helpers (extracted)
from .helpers import (
    STATUS_EMOJI,
    get_client,
    sync_to_api,
    init_git,
    console,
    logger,
)

# Temporary: Import remaining functions from legacy module until we extract
# This will be removed as we extract each module
from proj.commands.projects._legacy import (  # type: ignore
    list_projects,
    search_projects,
    get_project,
    update_project,
    delete_project,
    archive_project,
    create_project,
    detect_create_mode,
    prompt_for_create_options,
    import_json,
)
