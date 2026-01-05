# Research: Config Extension

**Research Topic:** proj-cli Architecture
**Question:** How should proj-cli config be extended for template and registry support?
**Status:** ✅ Complete
**Created:** 2025-01-05
**Completed:** 2025-01-05

---

## 🎯 Research Question

What configuration settings are needed to support template generation and local registry, and how should they integrate with the existing Pydantic-based config system?

---

## 🔍 Research Goals

- [x] Goal 1: Identify required configuration fields
- [x] Goal 2: Design nested config structure
- [x] Goal 3: Ensure XDG compliance for new paths

---

## 📚 Research Methodology

**Sources:**

- [x] Current proj-cli config.py: Existing Pydantic configuration
- [x] XDG Base Directory Specification: Standard for config/data paths
- [x] Pydantic Settings: Nested configuration support

---

## 📊 Findings

### Finding 1: Current Config Structure

Current config uses Pydantic with:
- YAML file: `~/.config/proj/config.yaml`
- Environment prefix: `PROJ_`
- Fields: `api_url`, `github_token`, `github_username`, `local_scan_dirs`

**Source:** `proj-cli/src/proj/config.py`

**Relevance:** Extension must follow existing patterns.

---

### Finding 2: Nested Config with Pydantic Settings

Pydantic Settings supports nested models with `env_nested_delimiter`:
```python
model_config = SettingsConfigDict(
    env_nested_delimiter="__",  # PROJ_TEMPLATES__SOURCE
)
```

**Source:** Pydantic Settings documentation

**Relevance:** Enables clean YAML structure with env overrides.

---

### Finding 3: XDG Paths for Data

Current code already has XDG helpers:
- `get_xdg_config_home()` → `~/.config/`
- `get_xdg_data_home()` → `~/.local/share/`

Local registry should use data directory, not config.

**Source:** `proj-cli/src/proj/config.py`

**Relevance:** Registry goes in data dir, config in config dir.

---

## 🔍 Analysis

**Required New Configuration:**

1. **API toggle:** `api_enabled: bool`
2. **Template settings:** `templates.source`, `templates.default`
3. **Registry settings:** `registry.path`
4. **Default project dir:** `default_project_dir`

**Key Insights:**

- [x] Insight 1: `api_enabled` controls whether API features are available
- [x] Insight 2: Nested config keeps YAML clean and organized
- [x] Insight 3: Environment overrides enable CI/scripting flexibility

---

## 💡 Recommendations

- [x] **Recommendation 1:** Add `api_enabled: bool` field (default: true)
- [x] **Recommendation 2:** Add nested `TemplateConfig` for template settings
- [x] **Recommendation 3:** Add nested `RegistryConfig` for registry settings
- [x] **Recommendation 4:** Use XDG data dir for registry: `~/.local/share/proj/registry.json`

---

## 📋 Requirements Discovered

- [x] **FR-CONFIG-1:** Config must include `api_enabled` toggle
- [x] **FR-CONFIG-2:** Config must support `templates.source` path
- [x] **FR-CONFIG-3:** Config must support `registry.path` setting
- [x] **FR-CONFIG-4:** Config must support environment variable overrides
- [x] **NFR-CONFIG-1:** Registry must use XDG data directory by default
- [x] **NFR-CONFIG-2:** Config file must remain YAML format

---

## 📝 Proposed Config Schema

```yaml
# ~/.config/proj/config.yaml

# API Settings
api_url: http://localhost:5000
api_enabled: true

# Template Settings
templates:
  source: ~/.dev-infra/templates
  default: standard-project

# Local Registry Settings
registry:
  path: ~/.local/share/proj/registry.json

# Default project location
default_project_dir: ~/Projects

# Existing settings...
github_token: null
github_username: null
local_scan_dirs:
  - ~/Projects
```

---

## 🚀 Next Steps

1. ✅ Config design validated
2. 🔜 Implement config extension in config.py
3. 🔜 Add `proj init` updates for new fields

---

**Last Updated:** 2025-01-05

