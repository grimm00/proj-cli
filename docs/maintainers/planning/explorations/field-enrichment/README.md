# Field Enrichment - Exploration Hub

**Purpose:** Explore how to populate and manage project fields across creation, scanning, and ongoing use  
**Status:** 🔴 Exploration  
**Created:** 2026-01-09  
**Last Updated:** 2026-01-09

---

## 📋 Quick Links

- **[Exploration Document](exploration.md)** - Main exploration document
- **[Research Topics](research-topics.md)** - Research questions to investigate

---

## 🎯 Overview

After creating projects or running inventory scans, many important project fields remain empty:

- `organization` - Not populated from any source
- `classification` - Not populated from any source  
- `project_type` - Not settable via create or update commands
- `status` - Hardcoded to "active"

This exploration investigates:

1. **Usability-first approach** - How configs, init, and project creation can set the stage
2. **File-system implications** - Should metadata like `project_type` influence directory structure?
3. **Multi-channel population** - How fields get populated via API, registry, and inventory
4. **Enrichment workflows** - Interactive and batch approaches to filling missing fields

---

## 📊 Status

**Current Phase:** Exploration  
**Next Step:** Conduct research on topics identified in research-topics.md

---

## 🔗 Related Documents

- [Research: Field Consistency](../../research/work-prod-integration/research-field-consistency.md)
- [Research: Source of Truth](../../research/work-prod-integration/research-source-of-truth.md)
- [Feature: Project Type Support](../features/project-type-support/README.md)

---

**Last Updated:** 2026-01-09
