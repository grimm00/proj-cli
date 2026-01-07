# Fix Plan: PR #11 Batch LOW LOW - Batch 01

**PR:** #11  
**Batch:** low-low-01  
**Priority:** 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** ✅ Complete  
**Created:** 2026-01-05  
**Completed:** 2026-01-07  
**Merged:** PR #18  
**Issues:** 3 issues

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR11-#1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Add whitespace strip test |
| PR11-#3 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Strengthen default description test |
| PR11-#4 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Add ProjectExistsError test for create_from_template |

---

## Overview

This batch contains 3 LOW priority issues with LOW effort. All issues are test improvements that strengthen test assertions and add missing test coverage.

**Estimated Time:** 45 minutes  
**Files Affected:** `tests/test_templates.py`

---

## Issue Details

### Issue PR11-#1: Add Whitespace Strip Test

**Location:** `tests/test_templates.py:42-47`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Since `validate_project_name` calls `name.strip()` before validation, add a test case that asserts the returned value is the trimmed name to protect against regressions in the stripping behavior.

**Proposed Solution:**

```python
def test_valid_name_with_whitespace_is_stripped(self):
    """Test leading/trailing whitespace is stripped for valid names."""
    result = validate_project_name("  my-project  ")
    assert result == "my-project"
```

---

### Issue PR11-#3: Strengthen Default Description Test

**Location:** `tests/test_templates.py:463-401`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
`test_default_description_when_not_provided` currently only verifies that the placeholder is removed. Update the test to assert the exact replacement value (`f"{project_name} project"`) to catch unintended changes.

**Current Code:**

```python
def test_default_description_when_not_provided(self, tmp_path):
    """Test default description is used when not provided."""
    # ... creates project and calls replace_placeholders
    # Only verifies placeholder is removed
```

**Proposed Solution:**

```python
def test_default_description_when_not_provided(self, tmp_path):
    """Test default description is used when not provided."""
    project_path = tmp_path / "my-project"
    project_path.mkdir()
    readme = project_path / "README.md"
    readme.write_text("[Brief description of what this project does]")

    replace_placeholders(project_path, "my-project")

    content = readme.read_text()
    assert "[Brief description of what this project does]" not in content
    assert "my-project project" in content  # Assert actual replacement value
```

---

### Issue PR11-#4: Add ProjectExistsError Test for create_from_template

**Location:** `tests/test_templates.py:545-502`  
**Sourcery Comment:** Comment #4  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Since `create_from_template` is the orchestration entry point, verify it surfaces `ProjectExistsError` just like `copy_template`. Add a test that creates a project directory that already exists and asserts the error is raised.

**Proposed Solution:**

```python
def test_create_from_template_project_exists_raises(self, tmp_path):
    """Test project already exists raises ProjectExistsError."""
    templates_source = tmp_path / "templates"
    templates_source.mkdir()
    template_dir = templates_source / "standard-project"
    template_dir.mkdir()
    (template_dir / "README.md").write_text("[Project Name]")

    target_dir = tmp_path / "target"
    target_dir.mkdir()

    # Create project directory that already exists
    existing_project = target_dir / "my-app"
    existing_project.mkdir()

    with pytest.raises(ProjectExistsError):
        create_from_template(
            project_name="my-app",
            template_type="standard-project",
            target_dir=target_dir,
            templates_source=templates_source,
        )
```

---

## Implementation Steps

1. **Issue PR11-#1: Whitespace strip test**
   - [x] Add `test_valid_name_with_whitespace_is_stripped` to `TestValidateProjectName`
   - [x] Verify test passes

2. **Issue PR11-#3: Default description test**
   - [x] Update `test_default_description_when_not_provided` in `TestReplacePlaceholders`
   - [x] Add assertion for exact replacement value
   - [x] Verify test passes

3. **Issue PR11-#4: ProjectExistsError test**
   - [x] Add `test_create_from_template_project_exists_raises` to `TestCreateFromTemplate`
   - [x] Set up template structure
   - [x] Create existing project directory
   - [x] Assert `ProjectExistsError` is raised
   - [x] Verify test passes

---

## Testing

- [x] All existing tests pass
- [x] 3 new/updated tests added
- [x] No regressions introduced

---

## Files to Modify

- `tests/test_templates.py` - Add/update 3 tests across different test classes

---

## Definition of Done

- [x] All 3 issues fixed
- [x] All tests passing
- [x] Code reviewed
- [x] Ready for PR

---

**Batch Rationale:**
These issues are batched together because they:
- Share the same priority (LOW) and effort (LOW)
- All are test improvements in the same file
- Can be implemented together efficiently in a single session

