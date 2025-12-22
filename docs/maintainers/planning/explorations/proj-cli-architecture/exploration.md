# proj-cli Architecture - Exploration

**Status:** 🔴 Exploration  
**Created:** 2025-12-22  
**Last Updated:** 2025-12-22

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

1. **Unified workflow:** `proj new myapp` creates directory AND registers project
2. **Local registry:** Track all dev-infra projects in `~/.dev-infra/registry.json`
3. **Sync capability:** `proj sync` to pull template updates
4. **Consistent UX:** One CLI for all project operations

---

## 💡 Initial Thoughts

### Command Structure

```bash
# New commands (template integration)
proj new myapp --template standard      # Create from template
proj new myapp --template learning      # Learning project
proj sync                               # Sync current project with template
proj sync --check                       # Check for available updates

# Existing commands (unchanged)
proj list                               # List projects (from work-prod API)
proj get <id>                           # Get project details
proj create "Name"                      # Create project record (API only)
proj inv scan                           # Scan inventory
```

### Template Source Options

| Option | Pros | Cons |
|--------|------|------|
| **Clone dev-infra repo** | Always latest, full history | Requires git, slow |
| **HTTP download releases** | Simple, versioned | Needs internet, packaging |
| **Bundle in proj-cli** | Offline, fast | Stale templates, larger package |
| **Git submodule** | Versioned, updatable | Git complexity |

### Local Registry Location

The work-prod-integration research already defined:
- Location: `~/.dev-infra/registry.json`
- Format: JSON with jq support
- Fields: `project_id`, `path`, `template`, `version`, `created_at`, `work_prod_id`

---

## 🔍 Key Questions

- [ ] **Q1:** How should proj-cli fetch templates from dev-infra?
- [ ] **Q2:** Should `proj new` automatically register with work-prod API?
- [ ] **Q3:** How does `proj sync` determine what to update?
- [ ] **Q4:** Should proj-cli bundle templates or fetch on-demand?
- [ ] **Q5:** How to handle offline scenarios?
- [ ] **Q6:** What metadata does proj-cli need to read from `.dev-infra.yml`?

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research proj-cli-architecture --from-explore` to conduct research
3. After research, use `/decision` to make architectural decisions

---

## 📝 Notes

### Relationship with dev-infra

- **dev-infra** = Template source, sync rules, metadata format
- **proj-cli** = Consumer, CLI implementation, local registry

This is a clean separation of concerns:
- dev-infra doesn't need to become a CLI tool
- proj-cli extends its existing architecture
- Template metadata bridges the two

### Existing Infrastructure to Leverage

From proj-cli:
- Typer CLI framework
- Pydantic configuration
- XDG-compliant paths
- Rich terminal output
- work-prod API client

From dev-infra:
- Template structure
- `new-project.sh` logic (to port)
- Template metadata research
- Local registry format research

---

**Last Updated:** 2025-12-22

