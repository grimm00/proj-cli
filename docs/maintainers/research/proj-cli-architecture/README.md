# proj-cli Architecture - Research Hub

**Purpose:** Research for extending proj-cli with dev-infra template generation
**Status:** 🟠 Research (5/6 complete)
**Created:** 2025-01-05
**Last Updated:** 2025-01-05

---

## 📋 Quick Links

- **[Research Summary](research-summary.md)** - Summary of all research findings
- **[Requirements](requirements.md)** - Requirements discovered during research

### Research Documents

| Topic | Priority | Status | Document |
|-------|----------|--------|----------|
| Unified Create Command | High | ✅ Complete | [research-unified-create-command.md](research-unified-create-command.md) |
| Config Extension | High | ✅ Complete | [research-config-extension.md](research-config-extension.md) |
| Local Registry | High | ✅ Complete | [research-local-registry.md](research-local-registry.md) |
| Template Fetching | High | ✅ Complete | [research-template-fetching.md](research-template-fetching.md) |
| new-project.sh Port | High | ✅ Complete | [research-new-project-port.md](research-new-project-port.md) |
| Sync Command | Medium | 🔴 Pending | [research-sync-command.md](research-sync-command.md) |

---

## 🎯 Research Overview

This research examines how to extend proj-cli to include template generation from dev-infra, creating a unified CLI for all project operations.

**Core Decision:** Extend `proj create` with modes instead of adding separate `proj new` command.

**Research Topics:** 6 topics
**Completed:** 5/6 (83%)
**Pending:** 1 (Sync Command - Phase 2 feature)

---

## 🚀 Next Steps

1. ✅ Review requirements in `requirements.md`
2. 🔜 Use `/decision proj-cli-architecture --from-research` to create ADR
3. 🔜 Use `/transition-plan --from-adr` to create feature plan

---

## 🔗 Related Documents

- **[Exploration](../../explorations/proj-cli-architecture/README.md)** - Original exploration
- **[ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)** - Current proj-cli architecture
- **[dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh)** - Source script to port

---

**Last Updated:** 2025-01-05

