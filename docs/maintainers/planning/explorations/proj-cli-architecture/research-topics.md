# Research Topics - proj-cli Architecture

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** 2025-12-22  
**Last Updated:** 2025-12-22

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before making decisions.

### Research Topic 1: Template Fetching Strategy

**Question:** How should proj-cli fetch templates from dev-infra?

**Why:** This determines how `proj new` gets template files.

**Priority:** High

**Status:** 🔴 Not Started

**Options to Explore:**
1. **Clone/fetch dev-infra repo** - Use git to clone/pull templates
2. **HTTP download from releases** - Download tarballs from GitHub releases
3. **Bundle templates in proj-cli** - Include templates in package
4. **Git submodule/subtree** - Embed templates as submodule

**Sub-questions:**
- What's the tradeoff between freshness and speed?
- How to handle versioning?
- What about offline support?

---

### Research Topic 2: `proj new` Command Design

**Question:** What should the `proj new` command look like?

**Why:** Need to design the UX for template generation.

**Priority:** High

**Status:** 🔴 Not Started

**Sub-questions:**
- Interactive prompts vs flags?
- Should it auto-register with work-prod API?
- What customization options during generation?
- How to handle existing directory conflicts?

**Comparison:**
```bash
# Option A: Minimal
proj new myapp

# Option B: With template
proj new myapp --template standard

# Option C: Interactive
proj new  # Prompts for name, template, options

# Option D: Full control
proj new myapp --template standard --no-git --no-register
```

---

### Research Topic 3: Local Registry Integration

**Question:** How does proj-cli integrate with the local registry?

**Why:** Need to track dev-infra projects locally for sync and management.

**Priority:** High

**Status:** 🔴 Not Started

**Context:** Work-prod-integration research already defined:
- Location: `~/.dev-infra/registry.json`
- Format: JSON with jq support
- Schema: `project_id`, `path`, `template`, `version`, etc.

**Sub-questions:**
- Should `proj new` auto-register projects?
- How to handle projects created before registry existed?
- Should registry be separate from work-prod data?
- How to handle orphaned entries (deleted projects)?

---

### Research Topic 4: Sync Command Design

**Question:** How should `proj sync` work?

**Why:** Need to design the UX for syncing template updates.

**Priority:** Medium

**Status:** 🔴 Not Started

**Sub-questions:**
- What triggers sync eligibility?
- How to show what would change (dry-run)?
- How to handle conflicts with customizations?
- Pull model (user initiates) vs push model (notified)?

**Possible Commands:**
```bash
proj sync              # Sync current project
proj sync --check      # Check for updates without applying
proj sync --all        # Sync all registered projects
proj sync --force      # Force sync, overwrite customizations
```

---

### Research Topic 5: Work-prod API Integration

**Question:** Should `proj new` automatically create a work-prod project?

**Why:** Currently `proj create` and template generation are separate.

**Priority:** Medium

**Status:** 🔴 Not Started

**Options:**
1. **Auto-register:** `proj new` creates both local project AND work-prod entry
2. **Separate:** Keep `proj new` (local) and `proj create` (API) separate
3. **Optional:** `proj new --register` to optionally create API entry

**Sub-questions:**
- What if work-prod API is unavailable?
- Should local registry link to work-prod ID?
- How to handle projects that exist in API but not locally?

---

### Research Topic 6: Offline Support

**Question:** How should proj-cli handle offline scenarios?

**Why:** Templates shouldn't require internet for every operation.

**Priority:** Medium

**Status:** 🔴 Not Started

**Sub-questions:**
- Cache templates locally after first fetch?
- How long before cache is stale?
- Graceful degradation when offline?
- What operations require internet vs work offline?

---

## 🎯 Research Workflow

1. Use `/research proj-cli-architecture --from-explore` to conduct research
2. Research will create documents in `docs/maintainers/research/proj-cli-architecture/`
3. After research complete, use `/decision` to make architectural decisions

---

## 📊 Priority Matrix

| Topic | Priority | Complexity | Dependency |
|-------|----------|------------|------------|
| Template Fetching | High | Medium | None |
| `proj new` Design | High | Low | Template Fetching |
| Local Registry | High | Low | Already researched |
| Sync Command | Medium | High | All above |
| Work-prod Integration | Medium | Medium | `proj new` |
| Offline Support | Medium | Medium | Template Fetching |

**Recommended Order:**
1. Template Fetching Strategy (foundational)
2. `proj new` Command Design (builds on fetching)
3. Local Registry Integration (already researched, just integrate)
4. Work-prod API Integration (depends on `proj new`)
5. Sync Command Design (depends on all above)
6. Offline Support (cross-cutting)

---

**Last Updated:** 2025-12-22

