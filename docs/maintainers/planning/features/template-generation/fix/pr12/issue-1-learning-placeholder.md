# Issue #1: Learning Project Placeholder Not Replaced

**Source:** Manual Testing (Scenario 4.11)  
**Priority:** MEDIUM 🟡  
**Impact:** MEDIUM 🟡  
**Effort:** LOW 🟢  
**Status:** ✅ Complete  
**Fixed In:** PR #13 (Phase 5)  
**Completed:** 2026-01-06

---

## 📋 Problem

When creating a project from the `learning-project` template, the README.md placeholder `[Learning Project Name]` is not replaced with the actual project name.

**Expected:**
```markdown
# my-learning-app

**Purpose:** my-learning-app project
```

**Actual:**
```markdown
# [Learning Project Name]

**Purpose:** [Brief description of what this learning project covers]
```

---

## 🔍 Root Cause

The `replace_placeholders()` function in `src/proj/templates.py` only handles:
- `[Project Name]` → project_name
- `[project-name]` → project_name (kebab-case)
- `[Date]` → current date
- `[Author]` → author

The `learning-project` template uses `[Learning Project Name]` which is not in the replacement list.

---

## 🛠️ Solution Options

### Option 1: Fix in proj-cli (Recommended)

Add `[Learning Project Name]` to the placeholder replacements in `replace_placeholders()`:

```python
content = content.replace("[Learning Project Name]", project_name)
```

**Pros:**
- Quick fix, single file change
- Handles existing templates as-is

**Cons:**
- Template-specific logic in CLI tool

### Option 2: Fix in dev-infra

Standardize all templates to use `[Project Name]` instead of template-specific placeholders.

**Pros:**
- Consistent placeholder format
- CLI stays template-agnostic

**Cons:**
- Requires changes in dev-infra repo
- Cross-repo coordination needed

---

## 📝 Implementation Notes

**Affected File:** `src/proj/templates.py`

**Line ~281:**
```python
# Current
content = content.replace("[Project Name]", project_name)

# Add
content = content.replace("[Learning Project Name]", project_name)
```

**Testing:**
- Add test case for learning-project placeholder replacement
- Verify manual test scenario 4.11 passes

---

## 🔗 Related

- **Manual Testing Guide:** Scenario 4.11
- **Template File:** `dev-infra/templates/learning-project/README.md`

---

**Created:** 2026-01-06  
**Last Updated:** 2026-01-06

