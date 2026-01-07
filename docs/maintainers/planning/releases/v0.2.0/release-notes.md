# Release Notes - v0.2.0

**Release Date:** 2026-01-07  
**Status:** 🔴 Draft  
**Type:** Minor Release

---

## What's New

### Template Generation

Create new projects from pre-defined templates with a single command:

```bash
# Create a standard project
proj create my-app --template standard-project --local-only

# Create a learning project
proj create my-learning --template learning-project --local-only

# Preview without creating
proj create my-app --template standard-project --dry-run
```

**Key capabilities:**

- Two template types: `standard-project` and `learning-project`
- Automatic placeholder replacement (project name, date, author)
- Git repository initialization (optional with `--no-git`)
- Local registry tracking for created projects
- Automatic API sync when enabled (with graceful degradation)

### Enhanced `proj create` Command

The `proj create` command now supports multiple modes:

| Mode | Description | Example |
|------|-------------|---------|
| **Template** | Create from local template | `--template standard-project` |
| **Local-Only** | Create locally without API | `--local-only` |
| **API-Only** | Create in API only (original) | `--api-only` |
| **Dry-Run** | Preview without side effects | `--dry-run` |
| **Interactive** | Guided prompts | `proj create` (no args) |

**New command flags:**

- `--template, -t` - Template type to use
- `--local-only` - Create locally only (requires --template)
- `--api-only` - Create in API only (backward compatible)
- `--target-dir` - Target directory for template creation
- `--no-git` - Skip git initialization
- `--register/--no-register` - Control local registry
- `--dry-run` - Preview creation without side effects
- `--desc, -d` - Project description

### Local Registry

Track locally created projects with metadata:

- **Location:** `~/.local/share/proj/registry.json`
- **Tracked fields:** path, template, template_version, created_at, work_prod_id
- Projects sync to work-prod API automatically when enabled

### Configuration Enhancements

New configuration options in `~/.config/proj/config.yaml`:

```yaml
api_enabled: true  # Enable/disable API sync
templates:
  source: ~/Projects/dev-infra/templates
  default: standard-project
registry:
  path: ~/.local/share/proj/registry.json
default_project_dir: ~/Projects
```

---

## Improvements

### User Experience

- **Interactive setup:** `proj init` now prompts for templates source
- **Clear error messages:** Descriptive errors for common issues
- **Dry-run preview:** See what would be created before executing

### Reliability

- **Graceful degradation:** API unavailability doesn't break local creation
- **Offline support:** `--local-only` mode works without network
- **Test coverage:** Core modules >90% coverage

---

## Bug Fixes

### Fixed in This Release

- **Learning project placeholder:** `[Learning Project Name]` now replaced correctly (PR #13)
- **Empty templates check:** Better error when no templates available (PR #15)
- **Error message sanitization:** Security improvement for error messages (PR #15)
- **Config env prefix:** Fixed environment variable handling (PR #16)
- **Dry-run validation:** Flag conflicts validated in dry-run mode (PR #16)
- **Test reliability:** Improved test isolation and assertions (PR #17, #18, #19)

---

## Breaking Changes

None in this release. Backward compatible with v0.1.0.

---

## Technical Details

### Changes Summary

- **PRs Merged:** 12 (PR #8-19)
- **Phases Completed:** 6/6
- **Requirements Verified:** 30/30
- **Manual Testing Scenarios:** 17/17 pass

### Key PRs

| PR | Description |
|----|-------------|
| #8 | Config Extension (Phase 1) - api_enabled, templates, registry config |
| #10 | Local Registry (Phase 2) - registry.json for project tracking |
| #11 | Template Copying (Phase 3) - template validation, copying, placeholders |
| #12 | Create Command Extension (Phase 4) - all new flags and modes |
| #13 | Testing & Polish (Phase 5) - bug fix, coverage, documentation |
| #14 | API Sync Enhancement (Phase 6) - work_prod_id, sync_to_api |
| #15-19 | Fix PRs - HIGH/MEDIUM/LOW priority issues addressed |

---

## Known Issues

### Registry Cleanup

- `proj delete` only removes from API, not from local registry
- Workaround: Manual registry cleanup (documented in feature status)
- Planned fix: Future `proj registry remove` command

---

## Upgrade Guide

### From v0.1.0

1. Update proj-cli: `pip install -e .` (or your preferred method)
2. Run `proj init --force` to add new config fields (templates source, etc.)
3. Verify templates location: `ls ~/Projects/dev-infra/templates/`

### New Configuration

The following config fields are new in v0.2.0:

```yaml
api_enabled: true
templates:
  source: /path/to/templates
  default: standard-project
registry:
  path: ~/.local/share/proj/registry.json
default_project_dir: ~/Projects
```

---

**Last Updated:** 2026-01-07  
**Next Release:** v0.3.0 - Project Type Support

