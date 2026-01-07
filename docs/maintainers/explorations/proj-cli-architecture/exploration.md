# proj-cli Architecture - Exploration

**Status:** 🟠 In Progress
**Created:** 2025-12-22
**Last Updated:** 2025-01-05

---

## 🎯 What Are We Exploring?

**The core question:** How should proj-cli integrate dev-infra template generation?

### Background

proj-cli already provides:

- **Project management:** `proj list`, `proj get`, `proj create` (work-prod API)
- **Inventory management:** `proj inv scan`, `proj inv analyze`
- **Configuration:** Typer + Pydantic + XDG paths (`~/.config/proj/`)

dev-infra provides:

- **Templates:** `standard-project`, `learning-project`
- **Generation script:** `./scripts/new-project.sh`
- **Template sync:** Validation and sync infrastructure (in development)

**The insight:** Rather than having two separate tools, proj-cli should become the unified CLI that consumes dev-infra as a "template layer."

---

## 🤔 Why Explore This?

### Current Pain Points

1. **Two tools for project creation:**

   - `proj create "Name"` → Creates project record in work-prod API
   - `dev-infra/new-project.sh` → Creates project directory from template
   - These are separate operations that should be unified

2. **No local registry:**

   - proj-cli talks to work-prod API (remote)
   - dev-infra projects have no local tracking
   - Can't easily list "all projects on this machine"

3. **Template updates are manual:**
   - No way to sync template improvements to existing projects
   - No versioning/metadata on generated projects

### Benefits of Integration

1. **Unified workflow:** `proj create myapp` creates directory AND registers project
2. **Local registry:** Track all dev-infra projects in local JSON
3. **Sync capability:** `proj sync` to pull template updates
4. **Consistent UX:** One CLI for all project operations
5. **Config-driven behavior:** API integration is optional, controlled by config

---

## 💡 Refined Design: Unified `proj create` Command

### Design Decision: Extend `create` Instead of Adding `new`

**Rationale:** Instead of adding a separate `proj new` command, we extend `proj create` with modes:

1. **Single mental model** - "create" is the command for making projects
2. **Interactive by default** - Matches `new-project.sh` behavior
3. **Config-driven** - `api_enabled` controls whether API options appear
4. **Backward compatible** - `--api-only` preserves current behavior

### Command Structure

```bash
# Interactive mode (default) - prompts for all options
proj create

# Non-interactive with template
proj create my-app --template standard

# Full non-interactive (for CI/scripts)
proj create my-app \
  --template standard \
  --desc "My app" \
  --target-dir ~/Projects \
  --no-git \
  --register     # or --no-register

# API-only mode (backward compatible with current behavior)
proj create "My Application" --api-only

# Local-only mode (offline, no API)
proj create my-app --template standard --local-only

# Dry-run to preview what would happen
proj create my-app --template standard --dry-run
```

### Interactive Flow (Default)

When someone runs `proj create` without explicit flags:

```
$ proj create

🚀 Project Creation
===================

? Project name: my-awesome-app
? Project type:
  > Standard Project (application, tool, service)
    Learning Project (tutorial, exercises, reference)
? Description: My awesome application
? Target directory: [~/Projects]
? Initialize git repository? [Y/n]
? Register with work-prod API? [Y/n]  ← Only shown if api_enabled: true

✓ Created project: ~/Projects/my-awesome-app
✓ Registered in local registry
✓ Registered with work-prod API (ID: 42)
```

### Behavior Matrix

| Config State                              | `proj create myapp` Behavior                        |
| ----------------------------------------- | --------------------------------------------------- |
| `api_enabled: true`, templates available  | Interactive: template + local registry + API prompt |
| `api_enabled: false`, templates available | Interactive: template + local registry only         |
| `templates.source: null`                  | API-only mode (current behavior)                    |

### Naming Considerations

There's a subtle naming tension between API and template creation:

- **API creation** uses a **display name**: `"My Cool Project"`
- **Template creation** uses a **directory name**: `my-cool-project`

The solution:

```bash
# Template-based: uses directory name
proj create my-app --template standard

# With custom display name for API
proj create my-app --template standard --register --name "My Application"
# Creates: ~/Projects/my-app/
# API name: "My Application"
```

---

## 🔧 Config Extension

### Proposed Config File

```yaml
# ~/.config/proj/config.yaml

# API Settings
api_url: http://localhost:5000
api_enabled: true # Toggle API integration on/off

# Template Settings
templates:
  source: ~/.dev-infra/templates # Local path to templates
  default: standard-project # Default template type

# Local Registry Settings
registry:
  path: ~/.local/share/proj/registry.json # XDG-compliant location

# Default project location
default_project_dir: ~/Projects

# GitHub Settings (existing)
github_token: null
github_username: null

# Scan Settings (existing)
local_scan_dirs:
  - ~/Projects
```

### Extended Config Model

```python
class TemplateConfig(BaseSettings):
    """Template-related configuration."""
    source: Optional[Path] = Field(
        default=None,
        description="Path to dev-infra templates directory",
    )
    default: str = Field(
        default="standard-project",
        description="Default template type",
    )


class RegistryConfig(BaseSettings):
    """Local registry configuration."""
    path: Path = Field(
        default_factory=lambda: get_data_dir() / "registry.json",
        description="Path to local project registry",
    )


class Config(BaseSettings):
    """Application configuration with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="PROJ_",
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__",  # For PROJ_TEMPLATES__SOURCE
    )

    # API Settings
    api_url: str = Field(
        default="http://localhost:5000",
        description="URL of the work-prod API",
    )
    api_enabled: bool = Field(
        default=True,
        description="Whether to use the work-prod API",
    )

    # Template Settings
    templates: TemplateConfig = Field(default_factory=TemplateConfig)

    # Registry Settings
    registry: RegistryConfig = Field(default_factory=RegistryConfig)

    # Default project location
    default_project_dir: Path = Field(
        default_factory=lambda: Path.home() / "Projects",
        description="Default directory for new projects",
    )

    # ... existing fields ...
```

### Environment Variable Overrides

```bash
# Override via environment
PROJ_API_ENABLED=false proj create my-app
PROJ_TEMPLATES__SOURCE=~/dev-infra/templates proj create my-app
PROJ_DEFAULT_PROJECT_DIR=~/Code proj create my-app
```

---

## 📋 Template Source Options

| Option                     | Pros                        | Cons                            |
| -------------------------- | --------------------------- | ------------------------------- |
| **Clone dev-infra repo**   | Always latest, full history | Requires git, slow              |
| **HTTP download releases** | Simple, versioned           | Needs internet, packaging       |
| **Bundle in proj-cli**     | Offline, fast               | Stale templates, larger package |
| **Local path reference**   | Simple, offline             | User must clone dev-infra       |

**Recommended:** Start with **local path reference** (`templates.source: ~/.dev-infra/templates`), add HTTP download from releases as enhancement later.

---

## 📝 Local Registry

### Location

Following XDG specification:

- Default: `~/.local/share/proj/registry.json`
- Configurable via `registry.path` in config

### Schema

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "uuid-here",
      "name": "my-app",
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z",
      "work_prod_id": 42, // null if not registered
      "metadata": {
        "description": "My awesome app",
        "author": "me"
      }
    }
  ]
}
```

---

## 🔍 Key Questions

### Resolved ✅

- [x] **Q1:** How should proj-cli fetch templates from dev-infra?
  - **Answer:** Local path reference initially (`templates.source`), HTTP download from releases as enhancement
- [x] **Q2:** Should `proj create` automatically register with work-prod API?
  - **Answer:** Configurable via `api_enabled` + interactive prompt or `--register` flag
- [x] **Q4:** Should proj-cli bundle templates or fetch on-demand?
  - **Answer:** Reference local dev-infra installation; don't bundle
- [x] **Q5:** How to handle offline scenarios?
  - **Answer:** `api_enabled: false` in config, or `--local-only` flag

### Open 🔴

- [ ] **Q3:** How does `proj sync` determine what to update?
  - Needs research on template versioning and sync strategy
- [ ] **Q6:** What metadata does proj-cli need to read from `.dev-infra.yml`?
  - Depends on sync feature requirements

---

## 🚀 Next Steps

1. ✅ Refine command design (unified `proj create` with modes)
2. ✅ Define config extension for templates and registry
3. 🔜 Create research document for remaining questions
4. 🔜 Create ADR for unified create command design
5. 🔜 Create feature plan for implementation

---

## 📝 Notes

### Relationship with dev-infra

- **dev-infra** = Template source, sync rules, metadata format
- **proj-cli** = Consumer, CLI implementation, local registry

This is a clean separation of concerns:

- dev-infra doesn't need to become a CLI tool
- proj-cli extends its existing architecture
- Template source path bridges the two

### Existing Infrastructure to Leverage

From proj-cli:

- Typer CLI framework
- Pydantic configuration (extensible for templates/registry)
- XDG-compliant paths
- Rich terminal output (for interactive prompts)
- work-prod API client

From dev-infra:

- Template structure (`templates/standard-project/`, `templates/learning-project/`)
- `new-project.sh` logic (to port: validation, customization, git init)
- Command distribution infrastructure (already established)

### Logic to Port from new-project.sh

Key functions to translate from Bash to Python:

1. **`validate_project_name()`** - Character validation, whitespace handling
2. **`validate_target_directory()`** - Path resolution, permissions check
3. **`copy_template()`** - Template copying with hidden files
4. **`customize_project()`** - Placeholder replacement (README, start.txt)
5. **`init_git_repo()`** - Git initialization, optional GitHub repo creation
6. **`prompt_yes_no()`** - Interactive prompts (use Rich/Typer prompts)

### Design Patterns

**Interactive-First:**

- Default behavior is interactive (like new-project.sh)
- Non-interactive mode via explicit flags for CI/scripts
- Config file sets sensible defaults

**Config-Driven:**

- `api_enabled` controls API integration availability
- `templates.source` controls template availability
- Environment variables override config file

**Backward Compatible:**

- `proj create "Name" --api-only` works exactly like current behavior
- No breaking changes to existing commands

---

## 🔗 Related Work

- **[dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh)** - Source script to port
- **[Command Distribution Feature](https://github.com/grimm00/dev-infra/blob/develop/admin/planning/features/command-distribution/)** - Related infrastructure
- **[ADR-001: Command Distribution](../../../decisions/ADR-0007-unified-cli-architecture.md)** - Current proj-cli architecture

---

**Last Updated:** 2025-01-05
