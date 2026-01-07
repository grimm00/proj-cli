# proj-cli Releases

**Purpose:** Track and document proj-cli releases
**Status:** ✅ Active
**Last Updated:** 2026-01-07

---

## 📋 Quick Links

### In Progress

- **[v0.2.0](v0.2.0/README.md)** - Template Generation Extension (🟢 Ready)

### Current Release

- **[v0.1.0](v0.1.0/README.md)** - Initial Release (✅ Released 2025-12-18)

### Release Documents

- **[CHANGELOG.md](../../../CHANGELOG.md)** - Root changelog

---

## 📅 Release Timeline

| Version | Status | Date | Type | Description |
|---------|--------|------|------|-------------|
| v0.2.0 | 🟢 Ready | 2026-01-07 | Minor | Template Generation Extension |
| v0.1.0 | ✅ Released | 2025-12-18 | Initial | Full CLI tool with project and inventory commands |

---

## 🔄 Release Workflow

### Commands

1. **`/release-prep vX.Y.Z`** - Create release documentation
2. **`/release-finalize vX.Y.Z`** - Finalize release documents
3. **Tag and publish release**

### Process

1. Feature development complete
2. Create release directory with `/release-prep`
3. Review and finalize documents
4. Tag release: `git tag vX.Y.Z`
5. Push tag: `git push origin vX.Y.Z`
6. Create GitHub release (optional)

---

## 📊 Version History

### v0.2.0 - Template Generation Extension (2026-01-07) 🟢 Ready

**Key Features:**
- Template Generation: `proj create --template standard-project`
- Local Registry: Track locally created projects
- API Sync: Automatic sync with graceful degradation
- Enhanced create command with new modes

**PRs:**
- #8-14: Template Generation feature (6 phases)
- #15-19: Fix PRs (24 issues fixed)

### v0.1.0 - Initial Release (2025-12-18)

**Key Features:**
- 8 project commands (migrated from work-prod)
- 7 inventory commands (new)
- Configuration system with XDG compliance
- Rich terminal output

**PRs:**
- #1: Phase 1 - Repository Setup
- #2: Phase 2 - Migrate Project Commands
- #3: Phase 3 - Add Inventory Commands
- #4: Fix: Quick Wins Batch 01
- #5: Phase 4 - Polish & Cleanup
- #6: Fix: Quick Wins Batch 02

---

## 📁 Directory Structure

```
releases/
├── README.md           # This hub file
└── vX.Y.Z/             # Per-version directory
    ├── README.md       # Release hub
    ├── checklist.md    # Release checklist
    ├── release-notes.md # Release notes
    └── CHANGELOG-DRAFT.md # CHANGELOG draft
```

---

**Last Updated:** 2026-01-07

