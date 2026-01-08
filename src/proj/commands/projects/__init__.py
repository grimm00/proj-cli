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

# Import import_export (extracted)
from .import_export import import_json

# Import crud (extracted)
from .crud import (
    get_project,
    update_project,
    delete_project,
    archive_project,
)

# Import list (extracted)
from .list import list_projects, search_projects

# Import create (extracted)
from .create import (
    create_project,
    detect_create_mode,
    prompt_for_create_options,
)
