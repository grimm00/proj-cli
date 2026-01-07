# ADR-0008: Template Generation Extension

**Status:** Accepted
**Date:** 2025-01-05
**Updated:** 2025-01-05 (Refined: inventory/registry relationship)
**Supersedes:** None
**Superseded By:** N/A
**Extends:** ADR-0007 (Unified CLI Architecture)

---

## Context

proj-cli (ADR-0007) successfully provides a unified CLI for project management and inventory operations. However, project creation currently requires two separate tools:

1. **`proj create "Name"`** - Creates a project record in the work-prod API
2. **`dev-infra/scripts/new-project.sh`** - Creates a project directory from templates

This creates a fragmented workflow where users must use two different tools for what should be a unified operation.

**Key Question:** How should proj-cli integrate template generation from dev-infra?

**Research Conducted:**

- [Exploration: proj-cli Architecture](../explorations/proj-cli-architecture/README.md)
- [Research: Unified Create Command](../research/proj-cli-architecture/research-unified-create-command.md)
- [Research: Config Extension](../research/proj-cli-architecture/research-config-extension.md)
- [Research: Template Fetching](../research/proj-cli-architecture/research-template-fetching.md)
- [Research: Local Registry](../research/proj-cli-architecture/research-local-registry.md)
- [Research: new-project.sh Port](../research/proj-cli-architecture/research-new-project-port.md)
- [Requirements Document](../research/proj-cli-architecture/requirements.md)

**Current State:**

- proj-cli talks to work-prod API for project records
- dev-infra's `new-project.sh` creates project directories from templates
- No local tracking of template-created projects
- No way to sync template updates to existing projects

**Constraints:**

- Must be backward compatible with existing `proj create` usage
- Should work offline when API is unavailable
- Should match interactive UX of `new-project.sh`

---

## Decision

**Extend the existing `proj create` command with modes** instead of adding a separate `proj new` command. This provides:

- **Interactive mode (default):** Prompts for project name, template, description, etc.
- **Template mode (`--template`):** Creates project from dev-infra template
- **API-only mode (`--api-only`):** Preserves current behavior (API record only)
- **Local-only mode (`--local-only`):** Works without API connectivity

**Config-driven behavior:** New configuration options control feature availability:

- `api_enabled`: Toggle API integration on/off
- `templates.source`: Path to dev-infra templates
- `templates.default`: Default template type
- `registry.path`: Local registry location

### Key Decisions

| Decision Point      | Choice                  | Rationale                                  |
| ------------------- | ----------------------- | ------------------------------------------ |
| **Command**         | Extend `proj create`    | Single mental model, backward compatible   |
| **Default Mode**    | Interactive             | Matches new-project.sh UX                  |
| **Template Source** | Local path reference    | Simple, offline, user has dev-infra        |
| **Primary Store**   | `inventory.json`        | Single source of truth for all projects    |
| **Sync Overlay**    | `registry.json`         | Minimal overlay for template sync tracking |
| **API Integration** | Config-driven, optional | Supports offline and API-less workflows    |

### Inventory vs Registry Architecture

**Clarification (2025-01-05):** The relationship between `inventory.json` and `registry.json` was refined during Phase 2 implementation.

#### inventory.json - Primary Project Store

| Aspect        | Details                                                         |
| ------------- | --------------------------------------------------------------- |
| **Location**  | `~/.local/share/proj/inventory.json`                            |
| **Purpose**   | All projects the user works with                                |
| **Sources**   | GitHub scan, local scan, manual addition, template creation     |
| **Use Cases** | Discovery, cataloging, status tracking, export to work-prod API |
| **Scope**     | Everything - single source of truth                             |

**Fields:** `name`, `description`, `remote_url`, `local_path`, `scan_source`, `languages`, `analyzed`, etc.

#### registry.json - Template Sync Overlay

| Aspect        | Details                                                          |
| ------------- | ---------------------------------------------------------------- |
| **Location**  | `~/.local/share/proj/registry.json`                              |
| **Purpose**   | Track template-created projects for sync                         |
| **Sources**   | Only `proj create --template`                                    |
| **Use Cases** | Enable `proj sync` to update projects to newer template versions |
| **Scope**     | Subset - only projects that want template tracking               |

**Fields (minimal):** `path`, `template`, `template_version`, `created_at`

#### Relationship

```
┌─────────────────────────────────────────────────────┐
│                  inventory.json                      │
│  (All projects: scanned, manual, template-created)  │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │              registry.json                      │ │
│  │  (Template-created projects for sync tracking) │ │
│  │  Cross-references inventory via path           │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Key Points:**

1. Template-created projects appear in **both** files
2. Inventory stores the project metadata (name, path, description, etc.)
3. Registry stores only template sync data (template, version, created_at)
4. Registry cross-references inventory via `path` field
5. Registry is optional - only needed if user wants template sync capability

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
  --register

# API-only mode (backward compatible)
proj create "My Application" --api-only

# Local-only mode (offline)
proj create my-app --template standard --local-only

# Dry-run to preview
proj create my-app --template standard --dry-run
```

### Configuration Extension

```yaml
# ~/.config/proj/config.yaml

# API Settings (existing + new)
api_url: http://localhost:5000
api_enabled: true # NEW: Toggle API integration

# Template Settings (NEW)
templates:
  source: ~/.dev-infra/templates
  default: standard-project

# Registry Settings (NEW)
registry:
  path: ~/.local/share/proj/registry.json

# Default project location (NEW)
default_project_dir: ~/Projects

# Existing settings unchanged
github_token: null
github_username: null
local_scan_dirs:
  - ~/Projects
```

### Local Registry Schema (Minimal - Sync Only)

The registry schema is intentionally minimal - it only tracks what's needed for template sync operations. All other project metadata lives in `inventory.json`.

```json
{
  "version": "1.0",
  "projects": [
    {
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z"
    }
  ]
}
```

**Field Rationale:**

- `path` - Cross-reference key to inventory.json (unique identifier)
- `template` - Which template was used (needed for sync)
- `template_version` - Which version (needed to detect updates)
- `created_at` - When created (audit trail)

**Removed from original design:**

- `id` (UUID) - Not needed; path is unique
- `name` - Lives in inventory.json
- `work_prod_id` - Lives in inventory.json
- `metadata` - Lives in inventory.json

### Inventory Entry (Template-Created Project)

When a project is created via `proj create --template`, it gets an inventory entry:

```json
{
  "name": "my-app",
  "description": "My awesome app",
  "local_path": "/Users/me/Projects/my-app",
  "scan_source": "template",
  "template": "standard-project",
  "created_at": "2025-01-05T10:30:00Z"
}
```

**Note:** Inventory includes `template` field for reference, but detailed sync tracking (version, update history) lives in registry.

---

## Consequences

### Positive

- **Unified Workflow:** Single command for all project creation scenarios
- **Interactive-First:** Matches familiar `new-project.sh` UX
- **Backward Compatible:** `--api-only` preserves existing behavior
- **Offline Support:** Works without API when `api_enabled: false`
- **Single Source of Truth:** Inventory is the primary store for all projects
- **Minimal Registry:** Registry only tracks what's needed for sync (no duplication)
- **Config-Driven:** Behavior controlled by configuration, not code changes
- **Foundation:** Enables future `proj sync` command

### Negative

- **More Complex Command:** `proj create` has more modes to understand
- **Config Expansion:** More configuration options to manage
- **Template Dependency:** Requires dev-infra to be cloned locally
- **Migration Path:** Users need to configure `templates.source`
- **Two Files:** Registry and inventory are separate (by design - different purposes)

### Deferred (Phase 2)

- **`proj sync` command:** Sync template updates to existing projects
- **HTTP template download:** Fetch templates from dev-infra releases
- **GitHub repo creation:** Auto-create GitHub repository

---

## Alternatives Considered

### Alternative 1: Separate `proj new` Command

**Description:** Add a new `proj new` command for template creation, keep `proj create` for API-only.

**Pros:**

- Clear separation of concerns
- No changes to existing command
- Simpler individual commands

**Cons:**

- Two mental models for "creating a project"
- Users must remember which command to use
- Doesn't match "create" semantics

**Why Not Chosen:** Users expect "create" to create projects. Having two commands fragments the UX.

### Alternative 2: Template Bundling

**Description:** Bundle templates directly in proj-cli package.

**Pros:**

- Works without dev-infra installed
- Single install for everything
- Always available offline

**Cons:**

- Templates become stale between releases
- Larger package size
- Maintenance burden (sync templates to package)
- No customization of templates

**Why Not Chosen:** Template staleness and maintenance burden outweigh convenience.

### Alternative 3: HTTP Download from Releases

**Description:** Fetch templates from dev-infra GitHub releases on demand.

**Pros:**

- Always get latest templates
- No local clone needed
- Versioned templates

**Cons:**

- Requires internet connection
- Slower than local copy
- Release packaging complexity

**Why Not Chosen:** Added as future enhancement, not Phase 1 requirement. Local path is simpler.

---

## Decision Rationale

**Key Factors:**

1. **UX Consistency:** Interactive-first matches `new-project.sh` behavior users know
2. **Single Mental Model:** "Create" is the action, modes specify how
3. **Backward Compatibility:** Existing workflows must not break
4. **Offline Support:** API-less operation is a valid use case
5. **Simplicity First:** Local path reference before HTTP download

**Research Support:**

- Finding 1: new-project.sh is interactive by default
- Finding 2: Users expect "create" to create projects
- Finding 3: Templates are static at creation time
- Finding 4: XDG compliance for registry location

---

## Requirements Impact

**Requirements Addressed:**

| Requirement                            | Status       |
| -------------------------------------- | ------------ |
| FR-CREATE-1: Interactive mode          | ✅ Addressed |
| FR-CREATE-2: Template-based creation   | ✅ Addressed |
| FR-CREATE-3: API-only mode             | ✅ Addressed |
| FR-CREATE-4: Local-only mode           | ✅ Addressed |
| FR-CONFIG-1: api_enabled toggle        | ✅ Addressed |
| FR-CONFIG-2: templates.source          | ✅ Addressed |
| FR-CONFIG-3: registry.path             | ✅ Addressed |
| FR-TMPL-1-3: Template handling         | ✅ Addressed |
| FR-REG-1-4: Local registry             | ✅ Addressed |
| FR-PORT-1-7: new-project.sh port       | ✅ Addressed |
| NFR-CREATE-1: Backward compatibility   | ✅ Addressed |
| NFR-TMPL-1: Offline operation          | ✅ Addressed |
| NFR-REG-1-2: XDG location, JSON format | ✅ Addressed |

**See:** [requirements.md](../research/proj-cli-architecture/requirements.md) for complete requirements

---

## Implementation Notes

### Phase 1: Config Extension (~2 hours) ✅ Complete

- Add `api_enabled` field to Config
- Add `TemplateConfig` nested model
- Add `RegistryConfig` nested model
- Add `default_project_dir` field
- Update `proj init` to handle new fields

### Phase 2: Local Registry (~2 hours) 🟠 In Progress

**Updated scope:** Registry is a sync overlay, not a standalone store.

- Create `src/proj/registry.py` module (minimal schema)
- Integrate with existing `inventory.py` module
- Add `scan_source: "template"` for template-created projects
- Registry operations: load, save, add, remove, lookup by path
- Inventory integration: add template project to inventory when created

### Phase 3: Template Copying (~3 hours)

- Create `src/proj/templates.py` module
- Port validation logic from new-project.sh
- Implement template copying with hidden files
- Implement placeholder replacement

### Phase 4: Create Command Extension (~3 hours)

- Add `--template` flag to create command
- Add `--api-only` and `--local-only` flags
- Implement interactive prompts
- Wire up template + registry integration

### Phase 5: Testing & Polish (~2 hours)

- Unit tests for new modules
- Integration tests for create modes
- Update documentation
- Manual testing

**Estimated Total:** ~12 hours

---

## References

- [ADR-0007: Unified CLI Architecture](ADR-0007-unified-cli-architecture.md)
- [Exploration: proj-cli Architecture](../explorations/proj-cli-architecture/README.md)
- [Research Hub](../research/proj-cli-architecture/README.md)
- [Research Summary](../research/proj-cli-architecture/research-summary.md)
- [Requirements Document](../research/proj-cli-architecture/requirements.md)
- [dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh)
- [Typer Documentation](https://typer.tiangolo.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

**Last Updated:** 2025-01-05 (Refined: inventory/registry relationship)
