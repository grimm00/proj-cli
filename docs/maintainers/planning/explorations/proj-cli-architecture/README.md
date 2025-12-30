# proj-cli Architecture - Exploration Hub

**Purpose:** Explore adding dev-infra template generation to proj-cli
**Status:** 🔴 Exploration
**Created:** 2025-12-22
**Last Updated:** 2025-12-22

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Main exploration document
- **[Research Topics](research-topics.md)** - Research questions to investigate

---

## 🎯 Overview

This exploration examines how to extend proj-cli to include template generation from dev-infra, creating a unified CLI for all project operations:

- **Project management:** `proj list`, `proj get`, `proj create` (work-prod API)
- **Inventory management:** `proj inv scan`, `proj inv analyze`
- **Template generation:** `proj new [name]` (NEW - from dev-infra)
- **Project sync:** `proj sync` (NEW - sync with dev-infra updates)

---

## 🏗️ Architecture Vision

```
┌─────────────────────────────────────────────────────────┐
│                      proj-cli                            │
│         (User-Facing CLI tool - installed globally)      │
│                                                          │
│  Commands:                                               │
│  • proj new [name] --template standard                   │
│  • proj list / get / create                              │
│  • proj inv scan / analyze                               │
│  • proj sync                                             │
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

**Current Phase:** Exploration
**Next Step:** Conduct research on topics identified in research-topics.md

---

## 🔗 Related

- **[dev-infra Identity Exploration](https://github.com/grimm00/dev-infra/blob/develop/admin/explorations/dev-infra-identity-and-focus/exploration.md)** - Defines dev-infra as "template layer"
- **[ADR-0007: Unified CLI Architecture](../../decisions/ADR-0007-unified-cli-architecture.md)** - Current proj-cli architecture
- **[dev-infra Template Metadata Research](https://github.com/grimm00/dev-infra/blob/develop/admin/research/template-metadata/README.md)** - Metadata format for templates

---

**Last Updated:** 2025-12-22

