# Usage Guide

**Purpose:** CLI command reference and examples  
**Status:** 🔴 Not Started  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

- **[Quick Start](../README.md)** - Installation and basics
- **[Configuration](../configuration/README.md)** - Config file reference

---

## 🎯 Overview

The `proj` command provides unified access to project management and inventory operations.

### Command Groups

| Group | Description |
|-------|-------------|
| Project Commands | `proj list`, `proj get`, `proj create`, etc. |
| Inventory Commands | `proj inv scan`, `proj inv export`, etc. |

---

## ⌨️ Project Commands

```bash
proj list                    # List all projects
proj get <id>                # Get project details
proj create "Name"           # Create new project
proj update <id>             # Update project
proj delete <id>             # Delete project
proj search "query"          # Search projects
proj import-json <file>      # Import from JSON
```

---

## 📦 Inventory Commands

```bash
proj inv scan github         # Scan GitHub repos
proj inv scan local          # Scan local directories
proj inv analyze             # Analyze tech stack
proj inv export json <file>  # Export to JSON
proj inv export api          # Push to work-prod API
proj inv status              # Show inventory status
```

---

## 📚 Related

- [Configuration Reference](../configuration/README.md)
- [Main README](../../README.md)

---

**Last Updated:** 2025-12-16  
**Status:** 🔴 Not Started  
**Next:** Document project commands in detail

