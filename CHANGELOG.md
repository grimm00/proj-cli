# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Changes not yet released_

## [0.3.2] - 2026-01-08

### Fixed

- **Inventory Export:** Fixed blank "path" field in inventory export by using correct field name to match work-prod API schema (BUG-001)

### Changed

- **Code Structure:** Refactored `projects.py` (943 lines) into focused package with 5 modules: `helpers.py`, `list.py`, `crud.py`, `create.py`, `import_export.py` (PR #25)
- **Test Structure:** Reorganized tests into hierarchical structure: `unit/`, `integration/`, `commands/`, `create/` (PR #26)
- **Test Helper:** Created `assert_command_exists()` helper function, refactored 16 command-existence tests (PR #29)

### Removed

- **Dead Code:** Removed unused `_get_client()` function from `create.py` (PR #28)

## [0.3.1] - 2026-01-07

### Changed

- **Centralized project type constants:** Created `constants.py` with `VALID_PROJECT_TYPES` and `PROJECT_TYPE_HELP` to avoid duplication (PR #23)
- **Custom exception for type validation:** Added `InvalidProjectTypeError` for safer error handling instead of catching all `ValueError` (PR #23)
- **Improved test assertions:** Strengthened invalid project type test with specific error format verification (PR #23)

## [0.3.0] - 2026-01-07

### Added

- **Project Type Filtering:** Filter projects by type using `proj list --type` (PR #21)
  - `--type Work` - Show only Work projects
  - `--type Personal` - Show only Personal projects
  - `--type Learning` - Show only Learning projects
  - `--type Inactive` - Show only Inactive projects

- **Combined Filters:** Type filtering works with other filters (PR #21)
  - Type + classification: `proj list --type Work --class primary`
  - Type + search: `proj list --type Personal --search "python"`

- **Type Column:** Project type shown in table output (PR #21)

- **Documentation:** Added "Filtering Projects" section to README

### Changed

- **Error Messages:** Invalid type values show clear error with list of valid options

## [0.2.0] - 2026-01-07

### Added

- **Template Generation:** Create projects from templates (PR #11, #12)
  - `proj create --template standard-project` - Create from standard template
  - `proj create --template learning-project` - Create from learning template
  - Automatic placeholder replacement (project name, date, author)
  - Git repository initialization with `--no-git` option to skip

- **Local Registry:** Track locally created projects (PR #10)
  - Registry location: `~/.local/share/proj/registry.json`
  - Tracks path, template, template_version, created_at, work_prod_id
  - `--register/--no-register` flags to control registration

- **API Sync Enhancement:** Automatic sync to work-prod API (PR #14)
  - Template creation syncs to API when `api_enabled: true`
  - Graceful degradation when API unavailable
  - `work_prod_id` stored in registry for synced projects
  - `--local-only` flag to skip API sync

- **Enhanced Create Command:** New modes and flags (PR #12)
  - `--template, -t` - Template type to use
  - `--local-only` - Create locally only (requires --template)
  - `--api-only` - Create in API only (backward compatible)
  - `--target-dir` - Target directory for template creation
  - `--no-git` - Skip git initialization
  - `--dry-run` - Preview creation without side effects
  - `--desc, -d` - Project description

- **Configuration Extension:** New config fields (PR #8)
  - `api_enabled` - Enable/disable API sync
  - `templates.source` - Path to templates directory
  - `templates.default` - Default template type
  - `registry.path` - Path to registry file
  - `default_project_dir` - Default directory for new projects

- **Interactive Mode:** Guided project creation (PR #12)
  - Prompts for project name, template, target directory, description
  - Template selection from available templates

- **proj init Enhancement:** Templates source prompt (PR #12)
  - Interactive setup now prompts for templates source directory
  - Improved GitHub username UX

### Changed

- **Test Coverage:** Improved core module coverage to >90% (PR #13)
  - templates.py: 96%
  - registry.py: 99%
  - config.py: 96%

### Fixed

- **Learning Project Placeholder:** `[Learning Project Name]` now replaced correctly (PR #13)
- **Empty Templates Check:** Better error when no templates available (PR #15)
- **Error Message Sanitization:** Security improvement for error messages (PR #15)
- **Config Environment Variables:** Fixed nested env var handling (PR #16)
- **Dry-Run Validation:** Flag conflicts validated in dry-run mode (PR #16)
- **Non-Writable Directory:** Proper error for non-writable target directories (PR #16)
- **Test Isolation:** XDG config isolation in tests (PR #9, #16, #17)
- **Test Reliability:** Improved assertions and edge case coverage (PR #17, #18, #19)

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

[Unreleased]: https://github.com/grimm00/proj-cli/compare/v0.3.2...HEAD
[0.3.2]: https://github.com/grimm00/proj-cli/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/grimm00/proj-cli/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/grimm00/proj-cli/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/grimm00/proj-cli/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/grimm00/proj-cli/releases/tag/v0.1.0

