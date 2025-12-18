# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Changes not yet released_

## [0.1.0] - 2025-12-18

### Added

- **Project Commands:** Full CRUD operations for project management
  - `proj list` - List all projects with table/JSON output
  - `proj get <id>` - Get project details
  - `proj create` - Create new project interactively
  - `proj update <id>` - Update project fields
  - `proj delete <id>` - Delete project
  - `proj search` - Search by name, status, tech stack
  - `proj import-json <file>` - Bulk import from JSON
  - `proj archive <id>` - Archive project

- **Inventory Commands:** Scan and manage project inventory
  - `proj inv scan github` - Scan GitHub repositories
  - `proj inv scan local <path>` - Scan local directories
  - `proj inv analyze` - Analyze tech stack
  - `proj inv dedupe` - Remove duplicates
  - `proj inv export json <file>` - Export to JSON
  - `proj inv export api` - Export to work-prod API
  - `proj inv status` - Show inventory statistics

- **Configuration System:**
  - XDG-compliant config: `~/.config/proj/config.yaml`
  - XDG-compliant data: `~/.local/share/proj/`
  - Environment variable overrides: `PROJ_*`
  - `proj init` - Interactive first-run setup

- **CLI Framework:**
  - Typer-based CLI with type hints
  - Rich terminal output with colors and tables
  - Status emojis: 🟢 Active, ⚪ Inactive, 📦 Archived, ✅ Completed
  - Enhanced progress bars

- **API Client:**
  - Requests-based API client for work-prod
  - URL validation and normalization
  - Error handling with retries

### Changed

- Migrated from work-prod `scripts/project_cli/` and `scripts/inventory/`
- Converted argparse to Typer

### Fixed

- Explicit encoding for config file operations
- Brittle return code test assertions
- Version metadata consistency
- API URL validation
- Format option validation with click.Choice
- Defensive JSON parsing for inventory.json
- Broad exception handling in integration tests
- Centralized STATUS_EMOJI constant
- URL consistency in documentation

---

[Unreleased]: https://github.com/grimm00/proj-cli/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/grimm00/proj-cli/releases/tag/v0.1.0

