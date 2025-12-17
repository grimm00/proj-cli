# Configuration Reference

**Purpose:** Configuration file and environment variable documentation  
**Status:** 🔴 Not Started  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

- **[Usage Guide](../usage/README.md)** - CLI commands
- **[Main README](../../README.md)** - Quick start

---

## 🎯 Overview

The `proj` CLI uses XDG Base Directory compliant configuration paths and supports both file-based configuration and environment variable overrides.

---

## 📁 Configuration Locations

| Type | Path |
|------|------|
| Config File | `~/.config/proj/config.yaml` |
| Data Directory | `~/.local/share/proj/` |

These paths respect `XDG_CONFIG_HOME` and `XDG_DATA_HOME` environment variables.

---

## ⚙️ Config File Format

```yaml
# ~/.config/proj/config.yaml

# API Settings
api_url: http://localhost:5000

# GitHub Settings
github_username: yourusername
github_token: null  # Use PROJ_GITHUB_TOKEN env var instead

# Scan Settings
local_scan_dirs:
  - /Users/you/Projects
```

---

## 🌍 Environment Variables

Environment variables override config file settings.

| Variable | Description | Default |
|----------|-------------|---------|
| `PROJ_API_URL` | work-prod API URL | `http://localhost:5000` |
| `PROJ_GITHUB_TOKEN` | GitHub personal access token | `null` |
| `PROJ_GITHUB_USERNAME` | GitHub username | `null` |

---

## 📚 Related

- [Usage Guide](../usage/README.md)
- [Development Guide](../development/README.md)

---

**Last Updated:** 2025-12-16  
**Status:** 🔴 Not Started  
**Next:** Document all configuration options

