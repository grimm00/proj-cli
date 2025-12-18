# Release v0.1.0 - Initial Release

**Version:** v0.1.0  
**Status:** 🟡 Ready for Release  
**Target Date:** 2025-12-18  
**Created:** 2025-12-18  
**Source:** proj-cli feature development  
**Type:** Minor Release (Initial)

---

## 📋 Quick Links

- **[Release Checklist](checklist.md)** - Release preparation checklist
- **[Release Notes](release-notes.md)** - Release notes and changelog
- **[CHANGELOG Draft](CHANGELOG-DRAFT.md)** - CHANGELOG draft for review

---

## 📊 Release Summary

**Version:** v0.1.0 - Initial Release  
**Target Date:** 2025-12-18  
**Status:** 🟡 Ready for Release

**Key Features:**
- Unified CLI tool (`proj`) for project and inventory management
- 8 project commands (list, get, create, update, delete, search, import-json, archive)
- 7 inventory commands (scan github/local, analyze, dedupe, export json/api, status)
- Configuration via YAML with XDG compliance
- First-run setup (`proj init`)
- Rich terminal output with status emojis and progress bars

**Development:**
- Phases: 4/4 complete
- PRs: 6 total (4 feature phases + 2 fix batches)
- Tests: 49 tests passing
- Coverage: 33%

---

## ✅ Release Checklist Status

**Pre-Release:**
- [x] All tests passing
- [x] Coverage acceptable (33%)
- [x] 0 linting errors
- [x] Documentation complete (README.md)
- [ ] Release checklist complete
- [ ] Release notes prepared
- [ ] CHANGELOG updated

**Release:**
- [ ] Version tagged in git
- [ ] Release notes finalized
- [ ] Documentation updated with version

**Post-Release:**
- [ ] Main merged to develop (if applicable)
- [ ] Release announcement (if applicable)
- [ ] Release docs updated

---

## 📈 What's Included

### Project Commands (from work-prod migration)

| Command | Description |
|---------|-------------|
| `proj list` | List all projects |
| `proj get <id>` | Get project details |
| `proj create` | Create new project |
| `proj update <id>` | Update project |
| `proj delete <id>` | Delete project |
| `proj search` | Search projects |
| `proj import-json` | Import from JSON |
| `proj archive <id>` | Archive project |

### Inventory Commands (new)

| Command | Description |
|---------|-------------|
| `proj inv scan github` | Scan GitHub repos |
| `proj inv scan local` | Scan local directories |
| `proj inv analyze` | Analyze tech stack |
| `proj inv dedupe` | Deduplicate entries |
| `proj inv export json` | Export to JSON |
| `proj inv export api` | Export to API |
| `proj inv status` | Show inventory status |

### Configuration

| Command | Description |
|---------|-------------|
| `proj init` | Interactive first-run setup |
| Config file | `~/.config/proj/config.yaml` |
| Data directory | `~/.local/share/proj/` |
| Env override | `PROJ_*` variables |

---

## 🔗 Related

- **Release Checklist:** [checklist.md](checklist.md)
- **Release Notes:** [release-notes.md](release-notes.md)
- **CHANGELOG Draft:** [CHANGELOG-DRAFT.md](CHANGELOG-DRAFT.md)
- **Feature Status:** [status-and-next-steps.md](../../features/proj-cli/status-and-next-steps.md)
- **Feature Plan:** [feature-plan.md](../../features/proj-cli/feature-plan.md)

---

**Last Updated:** 2025-12-18

