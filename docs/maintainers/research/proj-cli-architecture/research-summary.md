# Research Summary - proj-cli Architecture

**Purpose:** Summary of all research findings for extending proj-cli with template generation
**Status:** 🟠 Research (5/6 complete)
**Created:** 2025-01-05
**Last Updated:** 2025-01-05

---

## 📋 Research Overview

This research examined how to extend proj-cli to include template generation from dev-infra, creating a unified CLI for all project operations.

**Research Topics:** 6 topics
**Completed:** 5/6 (83%)
**Pending:** 1 (Sync Command - Phase 2 feature)

---

## 🔍 Key Findings

### Finding 1: Unified Command is Better Than Separate

Extending `proj create` with modes is preferable to adding a separate `proj new` command because:
- Single mental model: "create" is the command for making projects
- Interactive by default matches new-project.sh behavior
- Config-driven modes provide flexibility
- Backward compatible with `--api-only` flag

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

---

### Finding 2: Config Extension is Straightforward

The existing Pydantic config system easily supports:
- Nested config models (`templates`, `registry`)
- Environment variable overrides (`PROJ_TEMPLATES__SOURCE`)
- XDG-compliant paths for registry

**Source:** [research-config-extension.md](research-config-extension.md)

---

### Finding 3: Local Path Reference is Simplest

For template fetching, local path reference (`templates.source`) is recommended because:
- Works offline
- Users typically have dev-infra cloned already
- Simple configuration
- HTTP download can be added later as enhancement

**Source:** [research-template-fetching.md](research-template-fetching.md)

---

### Finding 4: JSON Registry with XDG Path

Local registry should use:
- Location: `~/.local/share/proj/registry.json`
- Format: JSON with schema versioning
- Fields: id, name, path, template, template_version, work_prod_id

**Source:** [research-local-registry.md](research-local-registry.md)

---

### Finding 5: new-project.sh Port is Well-Defined

Key functions to port from Bash to Python:
- Project name validation and sanitization
- Target directory validation
- Template copying (including hidden files)
- Placeholder replacement
- Git initialization
- Interactive prompts (using Typer/Rich)

**Source:** [research-new-project-port.md](research-new-project-port.md)

---

## 💡 Key Insights

- [x] **Insight 1:** Interactive-first UX matches user expectations
- [x] **Insight 2:** Config-driven modes reduce command complexity
- [x] **Insight 3:** Backward compatibility is essential
- [x] **Insight 4:** Templates are static at creation time
- [x] **Insight 5:** Sync command is Phase 2 (not blocking)

---

## 📋 Requirements Summary

**Total Requirements:** 25+
**Functional:** 19
**Non-Functional:** 8
**See:** [requirements.md](requirements.md) for complete requirements document

**High Priority Categories:**
1. Unified create command with modes
2. Config extension for templates and registry
3. Local registry implementation
4. Template copying and customization

---

## 🎯 Recommendations

1. **Extend `proj create`** with modes instead of adding `proj new`
2. **Use local path reference** for templates initially
3. **Implement config extension first** (foundation for other features)
4. **Follow XDG spec** for registry location
5. **Defer sync command** to Phase 2

---

## 🚀 Next Steps

1. ✅ Research complete (5/6 topics)
2. 🔜 Use `/decision proj-cli-architecture --from-research` to create ADR
3. 🔜 Use `/transition-plan --from-adr` to create feature plan
4. 🔜 Begin implementation (config extension first)

---

## 🔗 Related Documents

- **[Requirements](requirements.md)** - Complete requirements document
- **[Exploration](../../explorations/proj-cli-architecture/README.md)** - Original exploration
- **[Research Hub](../README.md)** - Main research hub

---

**Last Updated:** 2025-01-05

