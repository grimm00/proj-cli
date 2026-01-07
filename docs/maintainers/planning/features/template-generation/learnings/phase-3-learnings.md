# Template Generation Learnings - Phase 3: Template Copying

**Project:** proj-cli  
**Feature:** Template Generation Extension  
**Phase:** 3 - Template Copying  
**Date:** 2026-01-05  
**Status:** ✅ Complete  
**Last Updated:** 2026-01-05

---

## 📋 Overview

Phase 3 ported template copying logic from dev-infra's `new-project.sh` Bash script to Python. This included project name validation, directory validation, template discovery, template copying with hidden files, and placeholder replacement.

**PR:** #11 (merged 2026-01-05)  
**Duration:** ~3 hours  
**Tests:** 52 passing  
**Coverage:** 96% for templates.py

---

## ✅ What Worked Exceptionally Well

### 1. Shell-to-Python Porting Pattern

**Why it worked:**
The `new-project.sh` script provided clear, tested logic that could be systematically ported to Python function by function.

**What made it successful:**
- Each shell function mapped to a Python function
- Same validation patterns (regex, path checks)
- Same placeholder replacement logic (sed → str.replace)
- Clear error messages maintained

**Template implications:**
- Document porting patterns for shell-to-Python migrations
- Shell scripts can serve as "executable specifications"

**Key examples:**

**Shell validation:**
```bash
if [[ ! "$project_name" =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]]; then
    echo "Error: Invalid project name"
    exit 1
fi
```

**Python validation:**
```python
PROJECT_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$')

def validate_project_name(name: str) -> str:
    name = name.strip()
    if not PROJECT_NAME_PATTERN.match(name):
        raise InvalidProjectNameError(
            f"Invalid project name: '{name}'. "
            "Must start with alphanumeric and contain only "
            "alphanumeric, hyphens, and underscores."
        )
    return name
```

**Benefits:**
- Proven logic from production use
- Clear migration path
- Test cases derived from shell behavior

---

### 2. Explicit REFACTOR Phase Tracking

**Why it worked:**
Explicitly marking the REFACTOR phase complete in phase documentation ensured we didn't skip code quality improvements.

**What made it successful:**
- Each task had RED, GREEN, REFACTOR checkboxes
- REFACTOR forced review of edge cases and consistency
- User feedback ("That should be a part of our flow from now on")

**Template implications:**
- Include explicit REFACTOR checklist in TDD task templates
- Document REFACTOR as mandatory, not optional

**Key examples:**

```markdown
### Task 3: Directory Validation

**TDD Steps:**

- [x] **RED:** Write tests for validate_target_directory
- [x] **GREEN:** Implement validate_target_directory 
- [x] **REFACTOR:**
  - [x] Review edge cases (empty path, relative paths)
  - [x] Check consistency with other validation functions
  - [x] Run linting and fix any issues
```

**Benefits:**
- Prevents "green and done" mentality
- Catches edge cases during implementation
- Maintains code quality standards

---

### 3. Domain-Specific Exceptions in Module

**Why it worked:**
Keeping `TemplateError` and its subclasses in `templates.py` (not `error_handler.py`) followed Python best practices for module organization.

**What made it successful:**
- Domain exceptions belong with domain logic
- Avoids circular imports
- Module is self-contained and testable
- `error_handler.py` handles *displaying* errors, not *defining* domain errors

**Template implications:**
- Document exception placement patterns
- Domain exceptions stay with domain modules
- Error handler focuses on presentation

**Key examples:**

```python
# templates.py - Domain exceptions
class TemplateError(Exception):
    """Base exception for template operations."""
    pass

class InvalidProjectNameError(TemplateError):
    """Raised when project name is invalid."""
    pass

class DirectoryNotFoundError(TemplateError):
    """Raised when target directory does not exist."""
    pass
```

**Benefits:**
- Clear separation of concerns
- No circular import issues
- Module is independently testable
- Error handler remains generic

---

### 4. shutil.copytree for Template Copying

**Why it worked:**
Python's `shutil.copytree` handles all edge cases that required special handling in Bash (hidden files, directory structure, permissions).

**What made it successful:**
- Single function call replaces complex shell logic
- Automatically includes hidden files (`.gitignore`, `.cursor/`)
- Preserves directory structure
- Handles permissions correctly

**Template implications:**
- Recommend `shutil.copytree` for directory copying
- Document that it handles hidden files by default

**Key examples:**

**Shell (complex):**
```bash
# Must explicitly handle hidden files
cp -r "$template_path/." "$target_path/"
```

**Python (simple):**
```python
shutil.copytree(template_path, project_path)
```

**Benefits:**
- Cleaner code
- Fewer edge cases to handle
- Built-in error handling

---

## 🟡 What Needs Improvement

### 1. Progress Table Synchronization

**What the problem was:**
The progress tracking table in phase-3.md showed all tasks as "🔴 Not Started" even though all tasks were complete.

**Why it occurred:**
- Table created during scaffolding
- Not updated as tasks were completed
- Narrative and checklists were updated, but table was forgotten

**Impact:**
- Confusing documentation
- Identified by Sourcery review (Comment #5)
- Fixed before merge

**How to prevent:**
- Update progress table during REFACTOR phase
- Add reminder in task completion template
- Consider automating table updates

**Template changes needed:**
- Add "Update progress table" to REFACTOR checklist
- Consider removing redundant tracking (narrative OR table, not both)

---

### 2. Exception Path Test Coverage

**What the problem was:**
Several exception paths were not tested:
- `DirectoryNotWritableError` path in `validate_target_directory`
- Whitespace stripping behavior in `validate_project_name`
- `ProjectExistsError` path in `create_from_template`

**Why it occurred:**
- Focus on happy path during TDD
- Exception paths harder to trigger in tests
- Some require monkeypatching (os.access)

**Impact:**
- 4 deferred issues from Sourcery review
- Test coverage gaps (96% instead of ~100%)
- Fix batches created for later

**How to prevent:**
- Add exception path tests during RED phase
- Use monkeypatching proactively for error paths
- Review coverage report during REFACTOR phase

**Template changes needed:**
- Include exception path testing in TDD task templates
- Document monkeypatching patterns for error paths

---

## 💡 Unexpected Discoveries

### 1. Path("") Resolves to Path(".")

**Finding:**
In Python, `Path("")` resolves to `Path(".")` and `path.exists()` returns `True` for it (current directory).

**Why it's valuable:**
This edge case caused test failures during Task 3 (Directory Validation). The fix required explicit empty path checking.

**How to leverage:**
Document this behavior for path validation functions. Always check for empty paths explicitly before other validations.

**Code example:**

```python
def validate_target_directory(path: Path) -> Path:
    # Empty path check FIRST
    if not path.parts or str(path) == ".":
        raise DirectoryNotFoundError("Target directory path cannot be empty")
    
    # Then expand and resolve
    path = path.expanduser().resolve()
    
    # Then check existence
    if not path.exists():
        raise DirectoryNotFoundError(f"Target directory does not exist: {path}")
```

---

### 2. str.replace() Sufficient for Placeholders

**Finding:**
Simple `str.replace()` calls were sufficient for placeholder replacement - no regex needed.

**Why it's valuable:**
The shell script used `sed` with regex, but since placeholders are literal strings like `[Project Name]`, simple string replacement works perfectly.

**How to leverage:**
Keep it simple. Don't use regex when string replacement suffices.

**Code example:**

```python
def replace_placeholders(project_path, project_name, description=None, author=None):
    content = content.replace("[Project Name]", project_name)
    content = content.replace("[Date]", current_date)
    # No regex needed!
```

---

### 3. Test Organization by Function

**Finding:**
Organizing tests into classes by function (`TestValidateProjectName`, `TestSanitizeProjectName`, etc.) made the test file highly navigable despite 52 tests.

**Why it's valuable:**
- Easy to find tests for specific functions
- pytest output groups by class
- Adding new tests is straightforward

**How to leverage:**
Always organize test files by function/class under test, especially for utility modules.

---

## ⏱️ Time Investment Analysis

**Breakdown:**
- Task 1 (Name Validation): ~25 minutes
- Task 2 (Name Sanitization): ~20 minutes
- Task 3 (Directory Validation): ~30 minutes (debugging Path("") edge case)
- Task 4 (Template Discovery): ~20 minutes
- Task 5 (Template Copying): ~25 minutes
- Task 6 (Placeholder Replacement): ~25 minutes
- Task 7 (High-Level Function): ~20 minutes
- Task 8 (Config Integration): ~15 minutes
- **Total Implementation:** ~3 hours

**What took longer:**
- Task 3: Path validation edge cases took extra debugging
- Sourcery review and progress table fix added ~15 minutes

**What was faster:**
- Tasks 7-8: High-level orchestration built on solid foundations
- Having shell script as reference made implementation straightforward

**Estimation lessons:**
- TDD with clear specifications is predictable
- Edge cases in validation add ~20% time
- Having reference implementation (shell script) speeds up work

---

## 📊 Metrics & Impact

**Code metrics:**
- Lines of code: ~370 (templates.py)
- Test code: ~607 (test_templates.py)
- Test coverage: 96%
- Functions created: 9
- Exception classes: 6

**Quality metrics:**
- Sourcery review: 5 comments
- Fixed before merge: 1
- Deferred (LOW/MEDIUM): 4
- All tests passing: 52

**Developer experience:**
- Module is self-contained and testable
- Clear error messages for all failure modes
- Matches familiar shell script behavior
- Ready for CLI integration in Phase 4

---

## 🔗 Related

- [Phase 3 Plan](../phase-3.md)
- [PR #11](https://github.com/grimm00/proj-cli/pull/11)
- [Sourcery Review](../../../feedback/sourcery/pr11.md)
- [Fix Batches](../fix/pr11/README.md)
- [dev-infra new-project.sh](https://github.com/grimm00/dev-infra/blob/main/scripts/new-project.sh)

---

**Last Updated:** 2026-01-05

