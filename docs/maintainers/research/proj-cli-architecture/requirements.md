# Requirements - proj-cli Architecture

**Source:** Research on extending proj-cli with template generation
**Status:** Draft
**Created:** 2025-01-05
**Last Updated:** 2025-01-05

---

## 📋 Overview

This document captures requirements discovered during research on extending proj-cli with dev-infra template generation capabilities.

**Research Source:** [research-summary.md](research-summary.md)

---

## ✅ Functional Requirements

### Command Requirements

#### FR-CREATE-1: Interactive Mode

**Description:** `proj create` must support interactive mode as default behavior

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CREATE-2: Template-Based Creation

**Description:** `proj create` must support template-based project creation via `--template` flag or interactive selection

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CREATE-3: API-Only Mode

**Description:** `proj create --api-only` must preserve current behavior (API record only)

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CREATE-4: Local-Only Mode

**Description:** `proj create --local-only` must work without API connectivity

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

**Priority:** High

**Status:** 🔴 Pending

---

### Config Requirements

#### FR-CONFIG-1: API Toggle

**Description:** Config must include `api_enabled` boolean toggle

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CONFIG-2: Templates Source

**Description:** Config must support `templates.source` path setting

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CONFIG-3: Registry Path

**Description:** Config must support `registry.path` setting

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-CONFIG-4: Environment Overrides

**Description:** Config must support environment variable overrides (PROJ_* prefix)

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

### Template Requirements

#### FR-TMPL-1: Local Template Source

**Description:** Must support local path to templates via `templates.source` config

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-TMPL-2: Template Validation

**Description:** Must validate template directory exists and contains expected structure

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-TMPL-3: Template Types

**Description:** Must support both template types: standard-project, learning-project

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Priority:** High

**Status:** 🔴 Pending

---

### Registry Requirements

#### FR-REG-1: Project Tracking

**Description:** Registry must track all template-created projects

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-REG-2: Project Path

**Description:** Registry must include absolute project path

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-REG-3: Template Info

**Description:** Registry must include template type and version used

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-REG-4: API Linkage

**Description:** Registry must support linking to work-prod API records (`work_prod_id`)

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

### Port Requirements (from new-project.sh)

#### FR-PORT-1: Name Validation

**Description:** Must validate project name (no spaces, valid characters only)

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-PORT-2: Directory Validation

**Description:** Must validate target directory exists and is writable

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-PORT-3: Template Copying

**Description:** Must copy template including hidden files (.gitignore, .cursor/)

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-PORT-4: Placeholder Replacement

**Description:** Must replace placeholders in README.md and start.txt

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-PORT-5: Git Initialization

**Description:** Must support optional git initialization

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### FR-PORT-6: Interactive Prompts

**Description:** Must support interactive prompts for all inputs

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### FR-PORT-7: Non-Interactive Mode

**Description:** Must support non-interactive mode via flags for CI/scripts

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** High

**Status:** 🔴 Pending

---

## 🎯 Non-Functional Requirements

#### NFR-CREATE-1: Backward Compatibility

**Description:** Command changes must not break existing `proj create` usage

**Source:** [research-unified-create-command.md](research-unified-create-command.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### NFR-CONFIG-1: XDG Registry Location

**Description:** Registry must use XDG data directory by default (`~/.local/share/proj/`)

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### NFR-CONFIG-2: YAML Format

**Description:** Config file must remain YAML format

**Source:** [research-config-extension.md](research-config-extension.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### NFR-TMPL-1: Offline Operation

**Description:** Template creation should work offline when `templates.source` is configured

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Priority:** High

**Status:** 🔴 Pending

---

#### NFR-TMPL-2: Clear Errors

**Description:** Should provide clear error messages if templates not available

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### NFR-REG-1: Human-Readable

**Description:** Registry must be human-readable (JSON format)

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### NFR-REG-2: XDG Location

**Description:** Registry must use XDG-compliant location

**Source:** [research-local-registry.md](research-local-registry.md)

**Priority:** Medium

**Status:** 🔴 Pending

---

#### NFR-PORT-1: Name Sanitization

**Description:** Should offer to sanitize invalid project names

**Source:** [research-new-project-port.md](research-new-project-port.md)

**Priority:** Low

**Status:** 🔴 Pending

---

## ⚠️ Constraints

#### C-1: No Template Bundling

**Description:** Templates must NOT be bundled in proj-cli package

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Rationale:** Would add maintenance burden and cause stale templates

---

#### C-2: Existing Config Structure

**Description:** Config extension must work within existing Pydantic settings framework

**Source:** [research-config-extension.md](research-config-extension.md)

**Rationale:** Maintain consistency with existing codebase

---

## 💭 Assumptions

#### A-1: dev-infra Availability

**Description:** Users who want template generation have dev-infra cloned locally

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Rationale:** Primary users are developers working with dev-infra ecosystem

---

#### A-2: Template Stability

**Description:** Template structure is stable and changes infrequently

**Source:** [research-template-fetching.md](research-template-fetching.md)

**Rationale:** Templates are mature and well-tested

---

## 🔗 Related Documents

- [Research Summary](research-summary.md)
- [Research Documents](README.md)

---

## 🚀 Next Steps

1. Review and refine requirements
2. Use `/decision proj-cli-architecture --from-research` to make decisions
3. Decisions may refine requirements
4. Use requirements in transition-plan phase documents

---

**Last Updated:** 2025-01-05

