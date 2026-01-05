# Research: Unified Create Command

**Research Topic:** proj-cli Architecture
**Question:** Should we add `proj new` or extend `proj create` for template generation?
**Status:** ✅ Complete
**Created:** 2025-01-05
**Completed:** 2025-01-05

---

## 🎯 Research Question

How should proj-cli expose template generation functionality - as a new command (`proj new`) or by extending the existing `proj create` command with modes?

---

## 🔍 Research Goals

- [x] Goal 1: Evaluate UX of separate command vs extended command
- [x] Goal 2: Assess backward compatibility implications
- [x] Goal 3: Compare with dev-infra new-project.sh interactive behavior

---

## 📚 Research Methodology

**Sources:**

- [x] dev-infra new-project.sh: Interactive project creation script
- [x] Current proj-cli create command: API-only project creation
- [x] CLI design patterns: Industry practices for multi-mode commands

---

## 📊 Findings

### Finding 1: new-project.sh is Interactive by Default

dev-infra's `new-project.sh` runs interactively, prompting for:
- Project name
- Project type (standard/learning)
- Description
- Target directory
- Git initialization
- GitHub repository creation

**Source:** `dev-infra/scripts/new-project.sh`

**Relevance:** proj-cli should match this interactive-first UX.

---

### Finding 2: Current `proj create` is API-Only

Current behavior:
```bash
proj create "My Project" --desc "Description"
```
Creates only an API record in work-prod, no local files.

**Source:** `proj-cli/src/proj/commands/projects.py`

**Relevance:** Need to preserve this behavior for backward compatibility.

---

### Finding 3: Naming Tension Between API and Template

- **API creation** uses display name: `"My Cool Project"`
- **Template creation** uses directory name: `my-cool-project`

These are different inputs that need to be handled by the same command.

**Source:** Exploration discussion

**Relevance:** Command design must accommodate both use cases.

---

### Finding 4: Single Command Pattern in Industry

Many CLIs use a single command with modes rather than separate commands:
- `git init` vs `git clone` (separate - but create different things)
- `docker create` vs `docker run` (separate - different lifecycles)
- `npm init` (single with interactive mode)
- `cargo new` (single with options)

Most project scaffolding tools use interactive prompts by default.

**Source:** Industry CLI patterns

**Relevance:** Interactive-first, single command is a valid pattern.

---

## 🔍 Analysis

**Key Insights:**

- [x] Insight 1: Users expect "create" to create projects, not "new"
- [x] Insight 2: Interactive mode by default matches user expectations
- [x] Insight 3: Modes via flags (`--api-only`, `--template`, `--local-only`) provide flexibility
- [x] Insight 4: Config-driven defaults reduce flag verbosity

**Trade-offs:**

| Approach | Pros | Cons |
|----------|------|------|
| Separate `proj new` | Clear separation | Two mental models |
| Extend `proj create` | Single command | More complex logic |

---

## 💡 Recommendations

- [x] **Recommendation 1:** Extend `proj create` with modes instead of adding `proj new`
- [x] **Recommendation 2:** Make interactive mode the default behavior
- [x] **Recommendation 3:** Preserve `--api-only` for backward compatibility
- [x] **Recommendation 4:** Use config to control default behaviors

---

## 📋 Requirements Discovered

- [x] **FR-CREATE-1:** `proj create` must support interactive mode (default)
- [x] **FR-CREATE-2:** `proj create` must support template-based project creation
- [x] **FR-CREATE-3:** `proj create --api-only` must preserve current behavior
- [x] **FR-CREATE-4:** `proj create --local-only` must work without API
- [x] **NFR-CREATE-1:** Command must be backward compatible

---

## 🚀 Next Steps

1. ✅ Design validated through exploration
2. 🔜 Create ADR documenting this decision
3. 🔜 Implement config extension first

---

**Last Updated:** 2025-01-05

