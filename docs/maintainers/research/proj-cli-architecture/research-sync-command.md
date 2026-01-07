# Research: Sync Command Design

**Research Topic:** proj-cli Architecture
**Question:** How should `proj sync` work to update existing projects with template changes?
**Status:** 🔴 Not Started
**Created:** 2025-01-05
**Last Updated:** 2025-01-05

---

## 🎯 Research Question

How should proj-cli synchronize template updates to existing projects created from dev-infra templates?

---

## 🔍 Research Goals

- [ ] Goal 1: Determine what files are "syncable" vs "project-specific"
- [ ] Goal 2: Design conflict resolution strategy
- [ ] Goal 3: Define metadata requirements for sync eligibility

---

## 📚 Research Methodology

**Note:** This research is pending. Use web search for current information on:
- Template synchronization patterns
- Configuration file merging strategies
- Selective file sync approaches

**Sources to investigate:**

- [ ] dev-infra template structure: Identify sync candidates
- [ ] Industry patterns: How other template tools handle updates
- [ ] Git merge strategies: Conflict resolution approaches
- [ ] Web search: Template synchronization best practices

---

## 📊 Findings

### Finding 1: [Pending Research]

*This section will be populated during research.*

---

## 🔍 Analysis

*Pending research completion.*

---

## 💡 Recommendations

*Pending research completion.*

---

## 📋 Requirements Discovered

*Requirements will be extracted during research.*

Preliminary considerations:
- [ ] **FR-SYNC-1:** Must track template version in generated projects
- [ ] **FR-SYNC-2:** Must identify files safe to update
- [ ] **FR-SYNC-3:** Must preview changes before applying (--check flag)
- [ ] **FR-SYNC-4:** Must handle customized files gracefully

---

## 📝 Research Questions

### Sub-questions to investigate:

1. **What triggers sync eligibility?**
   - Template version mismatch?
   - Time-based check?
   - Manual trigger only?

2. **What files are "syncable"?**
   - Cursor commands (`.cursor/commands/`)
   - CI/CD workflows (`.github/workflows/`)
   - Documentation templates?
   - NOT: Source code, project-specific config

3. **How to handle conflicts?**
   - Overwrite with warning?
   - Skip modified files?
   - Three-way merge?
   - User choice per file?

4. **What metadata is needed?**
   - `.dev-infra.yml` in generated projects?
   - Template version
   - Generation timestamp
   - Sync manifest (files to sync)

---

## 🚀 Next Steps

1. 🔴 Conduct research on sync patterns
2. 🔴 Define syncable file categories
3. 🔴 Design metadata schema
4. 🔴 Create ADR for sync command

**Note:** This is a Phase 2 feature. Core `proj create` functionality should be implemented first.

---

**Last Updated:** 2025-01-05

