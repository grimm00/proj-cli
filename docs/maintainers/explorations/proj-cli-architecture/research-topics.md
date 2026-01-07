# Research Topics - proj-cli Architecture

**Purpose:** List of research topics/questions to investigate
**Status:** 🟠 Partially Resolved
**Created:** 2025-12-22
**Last Updated:** 2025-01-05

---

## 📋 Research Topics Summary

| Topic | Priority | Status | Resolution |
|-------|----------|--------|------------|
| Template Fetching Strategy | High | ✅ Resolved | Local path reference |
| Command Design | High | ✅ Resolved | Unified `proj create` with modes |
| Local Registry | High | ✅ Resolved | XDG-compliant path |
| Work-prod Integration | Medium | ✅ Resolved | Config-driven, optional |
| Offline Support | Medium | ✅ Resolved | `api_enabled` config + `--local-only` |
| Sync Command | Medium | 🔴 Pending | Needs research |

---

## ✅ Resolved Topics

### Research Topic 1: Template Fetching Strategy ✅

**Question:** How should proj-cli fetch templates from dev-infra?

**Resolution:** Local path reference via `templates.source` config

**Rationale:**
- Simple, no network dependency
- User already has dev-infra cloned for other purposes
- Future enhancement: HTTP download from GitHub releases

**Config:**
```yaml
templates:
  source: ~/.dev-infra/templates  # or ~/Projects/dev-infra/templates
  default: standard-project
```

---

### Research Topic 2: Command Design ✅

**Question:** What should the command for template generation look like?

**Resolution:** Extend existing `proj create` with modes instead of adding `proj new`

**Rationale:**
- Single mental model: "create" is the command for making projects
- Interactive by default (matches new-project.sh behavior)
- Config-driven modes via `api_enabled`
- Backward compatible: `--api-only` preserves current behavior

**Command Structure:**
```bash
# Interactive (default)
proj create

# Non-interactive with template
proj create my-app --template standard

# API-only (backward compatible)
proj create "My Application" --api-only

# Local-only (offline)
proj create my-app --template standard --local-only
```

---

### Research Topic 3: Local Registry Integration ✅

**Question:** How does proj-cli integrate with the local registry?

**Resolution:** XDG-compliant location with configurable path

**Location:** `~/.local/share/proj/registry.json` (default)

**Schema:**
```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "uuid",
      "name": "my-app",
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z",
      "work_prod_id": 42
    }
  ]
}
```

---

### Research Topic 5: Work-prod API Integration ✅

**Question:** Should project creation automatically register with work-prod API?

**Resolution:** Config-driven with interactive prompt

**Behavior:**
- If `api_enabled: true` → Prompt in interactive mode, or use `--register` flag
- If `api_enabled: false` → Skip API integration entirely
- `--api-only` flag for backward compatibility (API record only)

---

### Research Topic 6: Offline Support ✅

**Question:** How should proj-cli handle offline scenarios?

**Resolution:** Config-driven with flag override

**Mechanisms:**
1. **Config:** `api_enabled: false` disables all API calls
2. **Flag:** `--local-only` overrides config for single command
3. **Templates:** Local path reference means no network needed

---

## 🔴 Pending Topics

### Research Topic 4: Sync Command Design

**Question:** How should `proj sync` work?

**Why:** Need to design the UX for syncing template updates to existing projects.

**Priority:** Medium (Phase 2 feature)

**Status:** 🔴 Not Started

**Sub-questions:**
- What triggers sync eligibility?
- How to show what would change (dry-run)?
- How to handle conflicts with customizations?
- What files are "syncable" vs "project-specific"?

**Possible Commands:**
```bash
proj sync              # Sync current project
proj sync --check      # Check for updates without applying
proj sync --all        # Sync all registered projects
proj sync --force      # Force sync, overwrite customizations
```

**Dependencies:**
- Requires `.dev-infra.yml` metadata in generated projects
- Requires template versioning in dev-infra
- May need sync-manifest defining what files to update

---

## 🎯 Research Workflow

For remaining topics:

1. Use `/research [topic] --from-explore proj-cli-architecture` to conduct research
2. Research will create documents in `docs/maintainers/research/`
3. After research complete, use `/decision` to create ADRs

---

## 📊 Implementation Priority

Based on resolved research, implementation order:

1. **Config Extension** - Add `templates`, `registry`, `api_enabled` to config
2. **`proj create` Enhancement** - Add template mode with interactive prompts
3. **Local Registry** - Implement registry read/write
4. **Template Copying** - Port new-project.sh logic to Python
5. **Sync Command** (Future) - After core create flow is working

---

**Last Updated:** 2025-01-05

