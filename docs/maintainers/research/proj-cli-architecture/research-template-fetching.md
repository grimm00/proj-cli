# Research: Template Fetching Strategy

**Research Topic:** proj-cli Architecture
**Question:** How should proj-cli fetch templates from dev-infra?
**Status:** ✅ Complete
**Created:** 2025-01-05
**Completed:** 2025-01-05

---

## 🎯 Research Question

What is the best strategy for proj-cli to access dev-infra templates for project generation?

---

## 🔍 Research Goals

- [x] Goal 1: Evaluate template source options
- [x] Goal 2: Assess offline vs online trade-offs
- [x] Goal 3: Determine recommended approach

---

## 📚 Research Methodology

**Sources:**

- [x] dev-infra template structure: Current template organization
- [x] GitHub Releases: Release artifact patterns
- [x] Industry patterns: How scaffolding tools fetch templates

---

## 📊 Findings

### Finding 1: Templates are Static at Creation Time

Templates are only needed at project creation time, not runtime. Once a project is created, it has its own copy of template files.

**Source:** dev-infra new-project.sh

**Relevance:** No need for dynamic template fetching during normal operation.

---

### Finding 2: Four Source Options Available

| Option | Pros | Cons |
|--------|------|------|
| **Clone dev-infra repo** | Always latest, full history | Requires git, slow, heavy |
| **HTTP download releases** | Simple, versioned | Needs internet, packaging |
| **Bundle in proj-cli** | Offline, fast | Stale templates, larger package |
| **Local path reference** | Simple, offline | User must have dev-infra |

**Source:** Exploration analysis

**Relevance:** Need to choose based on user workflow.

---

### Finding 3: Users Already Have dev-infra

In the target workflow, users who want template generation likely already have dev-infra cloned for:
- Command development
- Template customization
- Contributing to dev-infra

**Source:** User workflow analysis

**Relevance:** Local path reference is practical for primary users.

---

## 🔍 Analysis

**Key Insights:**

- [x] Insight 1: Local path is simplest and works offline
- [x] Insight 2: HTTP download is good enhancement for new users
- [x] Insight 3: Bundling templates adds maintenance burden
- [x] Insight 4: Git clone is overkill for just copying templates

**Recommendation: Two-Phase Approach**

1. **Phase 1:** Local path reference (`templates.source` config)
2. **Phase 2:** HTTP download from releases as fallback/enhancement

---

## 💡 Recommendations

- [x] **Recommendation 1:** Start with local path reference via `templates.source` config
- [x] **Recommendation 2:** Add HTTP download from releases as future enhancement
- [x] **Recommendation 3:** Do NOT bundle templates in proj-cli package
- [x] **Recommendation 4:** Provide clear error when templates.source not configured

---

## 📋 Requirements Discovered

- [x] **FR-TMPL-1:** Must support local path to templates (`templates.source`)
- [x] **FR-TMPL-2:** Must validate template directory exists
- [x] **FR-TMPL-3:** Must support both template types (standard-project, learning-project)
- [x] **NFR-TMPL-1:** Should work offline when templates.source is configured
- [x] **NFR-TMPL-2:** Should provide clear error if templates not available

---

## 🚀 Next Steps

1. ✅ Template fetching strategy decided
2. 🔜 Implement templates.source config
3. 🔜 Implement template directory validation

---

**Last Updated:** 2025-01-05

