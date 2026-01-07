# CHANGELOG Draft - v0.2.0

**Draft Created:** 2026-01-07  
**Status:** ✅ Merged to CHANGELOG.md

---

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

---

## Review Checklist

- [x] All PRs listed
- [x] Categorization correct (Added/Changed/Fixed)
- [x] PR numbers accurate
- [x] Descriptions clear and user-facing
- [x] Ready to merge into CHANGELOG.md

---

**Ready for merge:** [x] Yes - Merged 2026-01-07

