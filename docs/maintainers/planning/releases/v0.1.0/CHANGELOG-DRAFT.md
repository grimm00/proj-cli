# CHANGELOG Draft - v0.1.0

**Draft Created:** 2025-12-18  
**Status:** ✅ Merged to CHANGELOG.md

---

## [0.1.0] - 2025-12-18

### Added

- **Project Commands:** Full CRUD operations for project management
  - `proj list` - List all projects with table/JSON output (PR #2)
  - `proj get <id>` - Get project details (PR #2)
  - `proj create` - Create new project interactively (PR #2)
  - `proj update <id>` - Update project fields (PR #2)
  - `proj delete <id>` - Delete project (PR #2)
  - `proj search` - Search by name, status, tech stack (PR #2)
  - `proj import-json <file>` - Bulk import from JSON (PR #2)
  - `proj archive <id>` - Archive project (PR #2)

- **Inventory Commands:** Scan and manage project inventory
  - `proj inv scan github` - Scan GitHub repositories (PR #3)
  - `proj inv scan local <path>` - Scan local directories (PR #3)
  - `proj inv analyze` - Analyze tech stack (PR #3)
  - `proj inv dedupe` - Remove duplicates (PR #3)
  - `proj inv export json <file>` - Export to JSON (PR #3)
  - `proj inv export api` - Export to work-prod API (PR #3)
  - `proj inv status` - Show inventory statistics (PR #3)

- **Configuration System:**
  - XDG-compliant config: `~/.config/proj/config.yaml` (PR #1)
  - XDG-compliant data: `~/.local/share/proj/` (PR #1)
  - Environment variable overrides: `PROJ_*` (PR #1)
  - `proj init` - Interactive first-run setup (PR #5)

- **CLI Framework:**
  - Typer-based CLI with type hints (PR #1)
  - Rich terminal output with colors and tables (PR #1)
  - Status emojis: 🟢 Active, ⚪ Inactive, 📦 Archived, ✅ Completed (PR #5)
  - Enhanced progress bars (PR #5)

- **API Client:**
  - Requests-based API client for work-prod (PR #2)
  - URL validation and normalization (PR #4)
  - Error handling with retries (PR #2)

- **Error Handling:**
  - Graceful API connection error handling (PR #2)
  - Defensive JSON parsing for corrupted files (PR #4, #6)
  - Clear error messages with guidance (PR #2)

### Changed

- **Migrated from work-prod:**
  - `scripts/project_cli/` → `proj` commands (PR #2)
  - `scripts/inventory/` → `proj inv` commands (PR #3)
  - Argparse → Typer conversion (PR #2)

### Fixed

- **Quick Wins Batch 01 (PR #4):**
  - Explicit encoding for config file operations
  - Brittle return code test assertions
  - Version metadata consistency
  - API URL validation
  - Format option validation with click.Choice
  - Defensive JSON parsing for inventory.json
  - Dedupe logic documentation alignment

- **Quick Wins Batch 02 (PR #6):**
  - Broad exception handling in integration tests
  - Centralized STATUS_EMOJI constant
  - Exit code assertions in CLI tests
  - Corrupted inventory file backup
  - URL consistency in documentation
  - JSON error logging for debugging
  - PR reference typos in docs

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct (Added/Changed/Fixed)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing
- [x] Ready to merge into CHANGELOG.md ✅

---

**Ready for merge:** [x] Yes - Merged to CHANGELOG.md on 2025-12-18

