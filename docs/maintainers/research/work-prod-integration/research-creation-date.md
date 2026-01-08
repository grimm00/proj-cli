# Research: Project Creation Date Semantics

**Research Topic:** Work-Prod Integration  
**Question:** How should we track when a project actually began vs when we recorded it?  
**Status:** 🔴 Research  
**Priority:** 🟡 Medium  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-08

---

## 🎯 Research Question

How should we track when a project actually began vs when we recorded it?

**Context:** Current `created_at` field only tracks when the record was created in our system (inventory scan, API creation), not when the project itself was started. This limits usefulness for project timeline analysis.

---

## 🔍 Research Goals

- [ ] Goal 1: Distinguish `created_at` (record creation) from `started_at` (project inception)
- [ ] Goal 2: Research methods to obtain actual project start dates
- [ ] Goal 3: Determine if work-prod API schema should be extended
- [ ] Goal 4: Design handling for unknown start dates

---

## 📚 Research Methodology

**Sources:**
- [ ] Web search: Project metadata standards
- [ ] Git API: First commit timestamp methods
- [ ] GitHub API: Repository creation date
- [ ] OS-level: File/directory creation timestamps

---

## 🔑 Sub-Questions

1. **Date Distinction:** Should we distinguish `created_at` (record creation) from `started_at` (project inception)?
2. **Data Sources:** How can we obtain actual project start dates?
   - Git repos: First commit timestamp (`git log --reverse --format=%aI | head -1`)
   - Local directories: File/directory creation time (varies by OS)
   - GitHub API: `created_at` field for repos
3. **Capture Timing:** Should this be captured at scan time or on-demand?
4. **Schema Impact:** Should work-prod API schema be extended with `started_at` field?
5. **Unknown Dates:** How should we handle projects where start date is unknown?

---

## 📊 Findings

### Finding 1: [Title]

[Description of finding]

**Source:** [Source reference]

**Relevance:** [Why this finding matters]

---

## 🔍 Analysis

[Analysis of findings]

**Key Insights:**
- [ ] Insight 1: [Description]
- [ ] Insight 2: [Description]

---

## 💡 Recommendations

- [ ] Recommendation 1: [Description]
- [ ] Recommendation 2: [Description]

---

## 📋 Requirements Discovered

- [ ] Requirement 1: [Description]
- [ ] Requirement 2: [Description]

---

## 🚀 Next Steps

1. Research date sources
2. Evaluate schema extension options
3. Design date handling proposal

---

**Last Updated:** 2026-01-08
