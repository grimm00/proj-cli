# Project Type Support - Phase 2: Integration Testing

**Feature:** Add `project_type` parameter support  
**Phase:** 2 of 2  
**Status:** 🔴 Not Started  
**Estimated Effort:** ~1 hour  
**Created:** 2025-12-23  
**Last Updated:** 2025-12-23  
**Dependencies:** Phase 1 complete

---

## 📋 Phase Overview

Verify proj-cli integration with work-prod API for `project_type` filtering.

**Goal:** Confirm all filtering commands work correctly against live API.

---

## 🎯 Phase Goals

- [ ] Test against running work-prod instance
- [ ] Verify all type filters work
- [ ] Verify combined filters work
- [ ] Verify error handling
- [ ] Update documentation

---

## 📝 Tasks

### Task 1: Setup Test Environment (~10 min)

**Prerequisites:**
1. work-prod server running with `project_type` support
2. proj-cli installed with Phase 1 changes
3. Database has projects with `project_type` populated

**Start work-prod:**
```bash
cd ~/Projects/work-prod/backend
source venv/bin/activate
flask run
```

**Verify API is ready:**
```bash
curl "http://localhost:5000/api/projects?project_type=Work"
```

**Acceptance Criteria:**
- [ ] work-prod server running
- [ ] API responds to project_type parameter

---

### Task 2: Test Type Filters (~20 min)

**Test Commands:**

```bash
# Test each type individually
proj list --type Work
proj list --type Personal
proj list --type Learning
proj list --type Inactive

# Verify output shows only projects of that type
```

**Expected Behavior:**
- Each command should return only projects matching the type
- Output should include project_type column
- Empty results are OK if no projects of that type exist

**Verification:**
```bash
# Check a specific type has correct filtering
proj list --type Work --format json | jq '.[].project_type' | sort | uniq
# Should output only: "Work"
```

**Acceptance Criteria:**
- [ ] `--type Work` returns only Work projects
- [ ] `--type Personal` returns only Personal projects
- [ ] `--type Learning` returns only Learning projects
- [ ] `--type Inactive` returns only Inactive projects

---

### Task 3: Test Combined Filters (~15 min)

**Test Commands:**

```bash
# Combine type with classification
proj list --type Work --classification primary
proj list --type Learning --classification secondary

# Combine type with search
proj list --type Work --search "api"
proj list --type Personal --search "python"

# Combine all filters
proj list --type Work --classification primary --search "test" --limit 10
```

**Expected Behavior:**
- Filters should be additive (AND logic)
- Should return projects matching ALL criteria

**Acceptance Criteria:**
- [ ] Type + classification works
- [ ] Type + search works
- [ ] Multiple filters combined work

---

### Task 4: Test Error Handling (~10 min)

**Test Commands:**

```bash
# Invalid type value
proj list --type Invalid
# Expected: Error message about valid types

# Mixed case (should this work?)
proj list --type work
proj list --type WORK
# Document behavior
```

**Expected Behavior:**
- Invalid type shows clear error message
- Error message lists valid values

**Acceptance Criteria:**
- [ ] Invalid type shows error
- [ ] Error message is helpful
- [ ] Case sensitivity documented

---

### Task 5: Update Documentation (~15 min)

**Files to Update:**

1. **CLI Help** - Verify `proj list --help` shows `--type` option
2. **README.md** - Add `--type` to examples if not present

**Example Documentation:**

```markdown
## Filtering Projects

### By Type
```bash
proj list --type Work      # Show only Work projects
proj list --type Personal  # Show only Personal projects
proj list --type Learning  # Show only Learning projects
proj list --type Inactive  # Show only Inactive projects
```

### Combined Filters
```bash
proj list --type Work --classification primary
proj list --type Learning --search "python"
```
```

**Acceptance Criteria:**
- [ ] CLI help is accurate
- [ ] README includes type filter examples

---

## ✅ Phase Completion Criteria

- [ ] All type filters tested and working
- [ ] Combined filters tested and working
- [ ] Error handling tested
- [ ] Documentation updated
- [ ] Ready for PR

---

## 🚀 Post-Phase Actions

After Phase 2 completion:
1. Create PR for feature
2. Update dev-infra requirements to mark FR-2d complete
3. Close any related issues

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Phase 1: Client Update](phase-1.md)
- [work-prod: project-type-field](../../../../../work-prod/docs/maintainers/planning/features/project-type-field/)

---

**Last Updated:** 2025-12-23

