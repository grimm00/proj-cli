# proj-cli Architecture - Exploration Hub

**Purpose:** Explore adding dev-infra template generation to proj-cli
**Status:** 🟠 In Progress (Ready for Research/ADR)
**Created:** 2025-12-22
**Last Updated:** 2025-01-05

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Main exploration document with refined design
- **[Research Topics](research-topics.md)** - Research questions (mostly resolved)

---

## 🎯 Overview

This exploration examines how to extend proj-cli to include template generation from dev-infra, creating a unified CLI for all project operations.

### Key Design Decision

**Extend `proj create` with modes** instead of adding a separate `proj new` command:

```bash
# Interactive mode (default) - prompts for all options
proj create

# Non-interactive with template
proj create my-app --template standard

# API-only mode (backward compatible)
proj create "My Application" --api-only

# Local-only mode (offline)
proj create my-app --template standard --local-only
```

### Behavior Driven by Config

```yaml
# ~/.config/proj/config.yaml
api_url: http://localhost:5000
api_enabled: true  # Toggle API integration

templates:
  source: ~/.dev-infra/templates
  default: standard-project

registry:
  path: ~/.local/share/proj/registry.json
```

---

## 🏗️ Architecture Vision

```
┌─────────────────────────────────────────────────────────┐
│                      proj-cli                            │
│         (User-Facing CLI tool - installed globally)      │
│                                                          │
│  Commands:                                               │
│  • proj create [name] --template standard                │
│  • proj list / get / update / delete                     │
│  • proj inv scan / analyze                               │
│  • proj sync (future)                                    │
└─────────────────────────────────────────────────────────┘
                          │
           ┌──────────────┴──────────────┐
           ▼                              ▼
┌─────────────────────┐       ┌─────────────────────┐
│ dev-infra           │       │ work-prod API       │
│ (Template source)   │       │ (Project registry)  │
│                     │       │                     │
│ • Templates         │       │ • Cloud sync        │
│ • Sync rules        │       │ • Cross-machine     │
│ • Version manifests │       │                     │
└─────────────────────┘       └─────────────────────┘
```

---

## 📊 Status

| Topic | Status |
|-------|--------|
| Command Design | ✅ Resolved - Unified `proj create` |
| Config Extension | ✅ Designed - Ready for implementation |
| Template Fetching | ✅ Resolved - Local path reference |
| Local Registry | ✅ Designed - XDG-compliant |
| API Integration | ✅ Resolved - Config-driven |
| Sync Command | 🔴 Pending - Future enhancement |

**Next Steps:**
1. Create ADR for unified `proj create` design
2. Create feature plan for implementation
3. Begin implementation (config extension first)

---

## 🔗 Related

- **[dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh)** - Source script to port
- **[dev-infra Command Distribution](https://github.com/grimm00/dev-infra/blob/develop/admin/planning/features/command-distribution/)** - Related infrastructure
- **[ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)** - Current proj-cli architecture

---

**Last Updated:** 2025-01-05

