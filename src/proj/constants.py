"""Shared constants for proj-cli."""

# Valid project types supported by the API
VALID_PROJECT_TYPES = ['Work', 'Personal', 'Learning', 'Inactive']

# Help text for CLI options
PROJECT_TYPE_HELP = f"Filter by type ({', '.join(VALID_PROJECT_TYPES)})"
