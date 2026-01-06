# Template Generation - Phase 5: Testing & Polish

**Phase:** 5 - Testing & Polish  
**Duration:** ~2-3 hours  
**Status:** ✅ Expanded  
**Prerequisites:** Phase 4 complete (all functionality implemented)  
**Last Updated:** 2026-01-06

---

## 📋 Overview

Final polish phase for the template generation feature. Fix known bugs, verify requirements, update documentation, and ensure the feature is production-ready.

**Success Definition:** All known bugs fixed, >80% test coverage, documentation complete, all manual testing scenarios pass.

---

## 🎯 Goals

1. **Fix Known Bugs** - Address learning-project placeholder issue from Phase 4
2. **Coverage Analysis** - Identify and fill test coverage gaps
3. **Documentation Updates** - Update README with new create options
4. **Requirements Verification** - Verify all requirements are met
5. **Final Testing** - Re-run manual testing guide
6. **Code Quality** - Address deferred issues opportunistically

---

## 📝 Tasks

### Task 1: Fix Learning Project Placeholder (TDD)

**Purpose:** Fix the bug where `[Learning Project Name]` placeholder is not replaced in learning-project templates.

**Reference:** [fix/pr12/issue-1-learning-placeholder.md](fix/pr12/issue-1-learning-placeholder.md)

**TDD Flow:**

1. **RED - Write failing test:**

   - [ ] Add test for learning-project placeholder replacement
   - [ ] Verify test fails (placeholder not replaced)

   **Test code (`tests/test_templates.py`):**

   ```python
   def test_replace_placeholders_learning_project_name(tmp_path):
       """Test that [Learning Project Name] placeholder is replaced."""
       test_file = tmp_path / "README.md"
       test_file.write_text("# [Learning Project Name]\n\n**Purpose:** Learning")

       replace_placeholders(tmp_path, "my-learning-app")

       content = test_file.read_text()
       assert "# my-learning-app" in content
       assert "[Learning Project Name]" not in content
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Add `[Learning Project Name]` to `replace_placeholders()` in `src/proj/templates.py`
   - [ ] Run test, verify it passes

   **Implementation (line ~281 in templates.py):**

   ```python
   # Add after existing [Project Name] replacement
   content = content.replace("[Learning Project Name]", project_name)
   ```

3. **REFACTOR:**

   - [ ] Check for other learning-project-specific placeholders
   - [ ] Run all tests to ensure no regressions
   - [ ] Run linting

**Checklist:**

- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] No regressions in existing tests
- [ ] Manual verification: `proj create test-learn --template learning-project --local-only --target-dir /tmp/test`

---

### Task 2: Coverage Gap Analysis

**Purpose:** Identify and fill any significant test coverage gaps.

**Steps:**

1. **Run coverage report:**

   - [ ] Run: `pytest --cov=proj --cov-report=html tests/`
   - [ ] Open `htmlcov/index.html` to review
   - [ ] Document any modules below 80%

2. **Identify priority gaps:**

   - [ ] Check `src/proj/templates.py` coverage
   - [ ] Check `src/proj/registry.py` coverage
   - [ ] Check `src/proj/commands/projects.py` coverage
   - [ ] Focus on error handling paths

3. **Add tests for critical gaps (if any):**

   - [ ] Add tests for uncovered error paths
   - [ ] Add tests for edge cases identified
   - [ ] Ensure new tests follow existing patterns

**Coverage Targets:**
| Module | Target | Notes |
|--------|--------|-------|
| templates.py | >90% | Core module |
| registry.py | >90% | Core module |
| commands/projects.py | >85% | Complex, some interactive code |
| config.py | >90% | Already well-tested |

**Checklist:**

- [ ] Coverage report generated
- [ ] Gaps identified and documented
- [ ] Critical gaps addressed (if any)
- [ ] Overall coverage >80%

---

### Task 3: README Documentation Update

**Purpose:** Update project README with new `proj create` options.

**File:** `README.md` (project root)

**Updates to make:**

1. **Update Create Command Section:**

   - [ ] Document `--template` option with available templates
   - [ ] Document `--local-only` for offline use
   - [ ] Document `--target-dir` for custom location
   - [ ] Document `--dry-run` for preview
   - [ ] Document `--no-git` option
   - [ ] Document `--register/--no-register` options

2. **Add Template Creation Examples:**

   ````markdown
   ## Creating Projects from Templates

   Create a new project from a template:

   ```bash
   # Standard project
   proj create my-app --template standard-project --local-only

   # Learning project
   proj create my-learning --template learning-project --local-only

   # With custom target directory
   proj create my-app --template standard-project --target-dir ~/Projects

   # Preview without creating
   proj create my-app --template standard-project --dry-run
   ```
   ````

3. **Document Interactive Mode:**

   - [ ] Explain that running `proj create` without args enters interactive mode
   - [ ] List the prompts and options

4. **Update Configuration Section:**

   - [ ] Document `templates.source` config option
   - [ ] Document `registry.enabled` and `registry.path` options
   - [ ] Note that `proj init` configures template source

**Checklist:**

- [ ] Create command section updated
- [ ] Template examples added
- [ ] Interactive mode documented
- [ ] Configuration section updated
- [ ] Help text matches documentation

---

### Task 4: Requirements Verification

**Purpose:** Verify all functional and non-functional requirements are met.

**Reference:** [Requirements Document](../../research/proj-cli-architecture/requirements.md)

**Verification Process:**

1. **Functional Requirements:**

   | Requirement | Description             | Verified | Notes                                      |
   | ----------- | ----------------------- | -------- | ------------------------------------------ |
   | FR-CREATE-1 | Template selection      | [ ]      | `--template` flag                          |
   | FR-CREATE-2 | Project name validation | [ ]      | `validate_project_name()`                  |
   | FR-CREATE-3 | Directory creation      | [ ]      | `create_from_template()`                   |
   | FR-CREATE-4 | Git initialization      | [ ]      | `init_git()` helper                        |
   | FR-CONFIG-1 | api_enabled field       | [ ]      | Config model                               |
   | FR-CONFIG-2 | templates.source        | [ ]      | TemplateConfig                             |
   | FR-CONFIG-3 | registry config         | [ ]      | RegistryConfig                             |
   | FR-CONFIG-4 | default_project_dir     | [ ]      | Config model                               |
   | FR-TMPL-1   | Template discovery      | [ ]      | `list_templates()`                         |
   | FR-TMPL-2   | Template validation     | [ ]      | `validate_template()`                      |
   | FR-TMPL-3   | Placeholder replacement | [ ]      | `replace_placeholders()`                   |
   | FR-REG-1    | Project registration    | [ ]      | `add_project()`                            |
   | FR-REG-2    | Registry storage        | [ ]      | `save_registry()`                          |
   | FR-REG-3    | Registry query          | [ ]      | `is_registered()`, `get_project_by_path()` |
   | FR-REG-4    | Registry listing        | [ ]      | `list_projects()`                          |

2. **Non-Functional Requirements:**

   | Requirement  | Description            | Verified | Notes               |
   | ------------ | ---------------------- | -------- | ------------------- |
   | NFR-CREATE-1 | Clear error messages   | [ ]      | Custom exceptions   |
   | NFR-CONFIG-1 | Backward compatibility | [ ]      | api_enabled default |
   | NFR-CONFIG-2 | XDG compliance         | [ ]      | Config paths        |
   | NFR-TMPL-1   | Fast template copy     | [ ]      | shutil.copytree     |
   | NFR-TMPL-2   | Preserve permissions   | [ ]      | copy_function arg   |
   | NFR-REG-1    | Atomic writes          | [ ]      | Write to temp first |
   | NFR-REG-2    | JSON format            | [ ]      | Human-readable      |
   | NFR-PORT-1   | dev-infra parity       | [ ]      | Same behavior       |

**Checklist:**

- [ ] All FR requirements verified
- [ ] All NFR requirements verified
- [ ] Any gaps documented
- [ ] Requirements tracking updated

---

### Task 5: Final Manual Testing

**Purpose:** Re-run manual testing guide to verify all scenarios pass.

**Reference:** [Manual Testing Guide](manual-testing.md)

**Testing Process:**

1. **Setup Verification:**

   - [ ] `proj --version` shows correct version
   - [ ] Templates directory accessible
   - [ ] Clean test directory created
   - [ ] `proj init` completed (with templates source)

2. **Core Scenarios:**

   - [ ] 4.1: Help Output - All flags shown
   - [ ] 4.2: Dry-Run Mode - Preview without creation
   - [ ] 4.3: Template Mode - Standard project created
   - [ ] 4.4: Skip Git - No .git directory
   - [ ] 4.5: Registry Integration - Entry in registry.json
   - [ ] 4.6: Local-Only Mode - Works offline
   - [ ] 4.7: Local-Only Error - Requires --template

3. **Template Variations:**

   - [ ] 4.11: Learning Project - **Now with fixed placeholder**
   - [ ] 4.12: Invalid Template - Clear error message
   - [ ] 4.13: Project Exists - Conflict error

4. **Options:**

   - [ ] 4.14: Description Option - --desc flag works

5. **Update Testing Guide (if needed):**
   - [ ] Add any new scenarios discovered
   - [ ] Update expected results if changed
   - [ ] Check off completed scenarios

**Checklist:**

- [ ] Setup verification complete
- [ ] All core scenarios pass
- [ ] Template variations tested (including fixed learning-project)
- [ ] Testing guide updated with results

---

### Task 6: Code Quality Polish (Optional)

**Purpose:** Address any remaining code quality issues opportunistically.

**Scope:** LOW priority items only - do not block release for these.

**Potential Items:**

1. **From Sourcery Reviews (if time permits):**

   - [ ] Review pr8/batch-low-low-01.md for quick wins
   - [ ] Review pr11/batch-low-low-01.md for quick wins
   - [ ] Skip any item requiring significant refactoring

2. **Linting Check:**

   - [ ] Run `flake8 src/proj/` - 0 errors
   - [ ] Run `flake8 tests/` - 0 errors

3. **Type Hints (if missing):**
   - [ ] Check critical functions have type hints
   - [ ] Add any obviously missing hints

**Note:** This task is optional. The feature is complete without these improvements.

**Checklist:**

- [ ] Quick wins addressed (if any)
- [ ] No linting errors
- [ ] No blocking issues remain

---

## 📊 Progress Tracking

| Task                              | Status         | Notes                  |
| --------------------------------- | -------------- | ---------------------- |
| Task 1: Learning Placeholder Fix  | 🔴 Not Started | TDD - estimated 20 min |
| Task 2: Coverage Analysis         | 🔴 Not Started | ~30 min                |
| Task 3: README Update             | 🔴 Not Started | ~30 min                |
| Task 4: Requirements Verification | 🔴 Not Started | ~20 min                |
| Task 5: Final Manual Testing      | 🔴 Not Started | ~30 min                |
| Task 6: Code Quality (Optional)   | 🔴 Not Started | ~30 min if done        |

---

## ✅ Completion Criteria

- [ ] Learning-project placeholder bug fixed
- [ ] Test coverage >80% overall
- [ ] README.md updated with new create options
- [ ] All requirements verified
- [ ] All manual testing scenarios pass
- [ ] No linting errors
- [ ] All CI checks pass
- [ ] PR ready for review

---

## 📦 Deliverables

- Fixed `templates.py` with learning-project placeholder support
- Updated integration test suite (if gaps found)
- Updated `README.md` documentation
- Completed requirements verification checklist
- Manual testing checklist completed
- PR branch ready for review

---

## 📊 Requirements Summary

**After Phase 5 Completion:**

| Category            | Total  | Verified |
| ------------------- | ------ | -------- |
| Command (FR-CREATE) | 4      | 4        |
| Config (FR-CONFIG)  | 4      | 4        |
| Template (FR-TMPL)  | 3      | 3        |
| Registry (FR-REG)   | 4      | 4        |
| NFR                 | 8      | 8        |
| **Total**           | **23** | **23**   |

---

## 🔗 Dependencies

### Prerequisites

- Phase 4 complete (all functionality implemented)

### Blocks

- Feature completion and release

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 4 - Create Command Extension](phase-4.md)
- [Manual Testing Guide](manual-testing.md)
- [Fix Tracking](fix/README.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)
- [Requirements](../../research/proj-cli-architecture/requirements.md)

---

**Last Updated:** 2026-01-06  
**Status:** ✅ Expanded  
**Next:** Begin implementation with Task 1 (`/task-phase 5 1`)
