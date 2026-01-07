# Release Notes - v0.3.0

**Release Date:** TBD
**Status:** 🔴 Draft
**Type:** Minor Release

---

## What's New

### Project Type Filtering

**Filter projects by type:**

The `proj list` command now supports filtering by project type using the `--type` option.

```bash
proj list --type Work       # Show only Work projects
proj list --type Personal   # Show only Personal projects
proj list --type Learning   # Show only Learning projects
proj list --type Inactive   # Show only Inactive projects
```

**Valid Types:** Work, Personal, Learning, Inactive (case-sensitive)

### Combined Filters

Combine type filtering with other filters:

```bash
# Type with classification
proj list --type Work --class primary

# Type with search
proj list --type Personal --search "python"

# Multiple filters (AND logic)
proj list --type Work --status active --org personal
```

### Enhanced Output

- Project type column added to table output
- Type shown in both table and JSON formats

---

## Improvements

### Error Handling

- **Clear error messages:** Invalid type values show helpful error with list of valid options
- **Case sensitivity:** Type values are case-sensitive, error message clarifies valid formats

### Documentation

- **README updated:** New "Filtering Projects" section with type filter examples
- **CLI help updated:** `--type` option documented with valid values

---

## Technical Details

### Changes Summary

- **Files Changed:** 3
- **Tests Added:** 3 unit tests for type filtering
- **Coverage:** Maintained > 80%

### Key PRs

- PR #21: feat: Add project_type filtering support (Phase 1)
- Phase 2: Integration Testing (docs-only, direct merge)

### Dependencies

- Requires work-prod API with `project_type` filtering (PR #42)

---

## Known Issues

None in this release.

---

**Last Updated:** 2026-01-07
**Previous Release:** [v0.2.0](../v0.2.0/release-notes.md)

