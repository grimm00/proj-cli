# Release Notes - v0.1.0

**Release Date:** 2025-12-18  
**Status:** ✅ Final  
**Type:** Initial Release

---

## 🎉 What's New

### Unified CLI Tool

**proj-cli** is a unified command-line interface for project and inventory management. It consolidates the project CLI from work-prod with new inventory scanning capabilities into a single, modern Python package.

**Key Highlights:**
- Single `proj` command for all operations
- Modern Python tooling (Typer, Pydantic, Rich)
- XDG-compliant configuration
- Beautiful terminal output with colors and emojis

---

## 📦 Features

### Project Management Commands

Commands migrated from work-prod with full feature parity:

| Command | Description |
|---------|-------------|
| `proj list` | List all projects with table or JSON output |
| `proj get <id>` | Get detailed project information |
| `proj create` | Create a new project interactively |
| `proj update <id>` | Update project fields |
| `proj delete <id>` | Delete a project |
| `proj search` | Search projects by name, status, or tech stack |
| `proj import-json <file>` | Bulk import projects from JSON |
| `proj archive <id>` | Archive a project |

### Inventory Management Commands

New commands for scanning and managing project inventory:

| Command | Description |
|---------|-------------|
| `proj inv scan github` | Scan GitHub repositories for a user |
| `proj inv scan local <path>` | Scan local directories for projects |
| `proj inv analyze` | Analyze tech stack of scanned projects |
| `proj inv dedupe` | Remove duplicate entries |
| `proj inv export json <file>` | Export inventory to JSON file |
| `proj inv export api` | Export inventory to work-prod API |
| `proj inv status` | Show inventory statistics |

### Configuration

| Feature | Description |
|---------|-------------|
| `proj init` | Interactive first-run configuration |
| Config file | `~/.config/proj/config.yaml` |
| Data directory | `~/.local/share/proj/` |
| Environment override | `PROJ_API_URL`, `PROJ_GITHUB_USERNAME`, etc. |

---

## ✨ Improvements

### Rich Terminal Output

- **Status Emojis:** 🟢 Active, ⚪ Inactive, 📦 Archived, ✅ Completed
- **Progress Bars:** Enhanced progress indicators for scanning operations
- **Table Styling:** Professional table output with header styling
- **Colored Messages:** Error, warning, and success messages with appropriate colors

### First-Run Experience

- Interactive `proj init` command guides new users through setup
- Creates configuration file with sensible defaults
- Prompts for API URL, GitHub username, and scan directories

### Error Handling

- Graceful handling of API connection errors
- Defensive JSON parsing for corrupted files
- Clear error messages with actionable guidance

---

## 🔧 Technical Details

### Requirements

- Python 3.10 or higher
- Dependencies: typer, pyyaml, pydantic-settings, requests

### Installation

```bash
# Clone the repository
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli

# Install in development mode
pip install -e .

# Or install for production
pip install .
```

### Configuration

Default configuration location: `~/.config/proj/config.yaml`

```yaml
api_url: http://localhost:5000
github_username: your-username
local_scan_dirs:
  - ~/Projects
```

### Changes Summary

- **Files:** 25 source files
- **Tests:** 49 tests passing
- **Coverage:** 33%
- **PRs:** 6 merged

---

## 📋 Known Limitations

### Deferred for Future Releases

**Test Coverage (22 items):**
- Additional tests for Config, CLI error paths, and inventory commands
- These don't affect functionality, only test completeness

**Performance (1 item):**
- Depth-limited traversal for `scan local` (not needed unless scanning very deep directories)

**Enhancements (3 items):**
- Smart dedupe with field merging
- Multi-directory scan configuration
- Exclusion patterns for scan

---

## 🔗 Related

- **Repository:** https://github.com/grimm00/proj-cli
- **work-prod API:** Required for project commands and API export
- **GitHub API:** Required for GitHub scanning (token optional for public repos)

---

## 🙏 Acknowledgments

This release consolidates and improves upon the original `scripts/project_cli/` and `scripts/inventory/` from work-prod. The migration was tracked through ADR-0007.

---

**Last Updated:** 2025-12-18 (Finalized)  
**Next Release:** v0.2.0 (planned - test coverage improvements)

