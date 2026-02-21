# Pre-Phase Review Command

Reviews phase planning documents before implementation begins. Ensures phase plans are complete, dependencies are identified, and implementation is ready to proceed.

---

## Configuration

**Path Detection:**

This command supports multiple project organization patterns:

1. **Feature-Specific Structure (default):**
   - Phase documents: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
   - Feature plan: `docs/maintainers/planning/features/[feature-name]/feature-plan.md`
   - Status: `docs/maintainers/planning/features/[feature-name]/status-and-next-steps.md`

2. **Project-Wide Structure:**
   - Phase documents: `docs/maintainers/planning/phases/phase-N.md`
   - Status: `docs/maintainers/planning/status-and-next-steps.md` (if exists)

**Feature Detection:**

- Use `--feature` option if provided
- Otherwise, auto-detect:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for phase documents in each
  - If no features exist, use project-wide structure

---

## Workflow Overview

**When to use:**

- Before starting phase implementation
- After phase planning is complete
- To validate phase readiness
- To identify missing dependencies
- To ensure phase plan completeness

**Key principle:** Review phase planning documents to ensure implementation readiness before beginning work.

---

## Usage

**Command:** `/pre-phase-review [phase-number] [options]`

**Examples:**

- `/pre-phase-review 4` - Review Phase 4 before implementation
- `/pre-phase-review 3 --feature my-feature` - Review Phase 3 for specific feature
- `/pre-phase-review 5 --dry-run` - Show review without creating files
- `/pre-phase-review 2 --check-dependencies` - Focus on dependency validation

**Options:**

- `--phase NUMBER` - Phase number to review (required)
- `--feature [name]` - Specify feature name (overrides auto-detection)
- `--check-dependencies` - Focus on dependency validation
- `--check-tests` - Focus on test plan validation
- `--dry-run` - Show review without creating files

---

## Step-by-Step Process

### 1. Identify Phase Document

**Detect feature name:**

- Use `--feature` option if provided
- Otherwise, auto-detect:
  - Check if `docs/maintainers/planning/features/` exists
  - If single feature exists, use that feature name
  - If multiple features exist, search for phase documents in each
  - If no features exist, use project-wide structure

**Load phase document:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

**Verify document exists:**

```bash
# Feature-specific
ls docs/maintainers/planning/features/[feature-name]/phase-N.md

# Project-wide
ls docs/maintainers/planning/phases/phase-N.md
```

**Checklist:**

- [ ] Feature name detected or specified
- [ ] Phase document found
- [ ] Document is readable
- [ ] Phase number valid

---

### 2. Review Phase Plan Completeness

**Check for required sections:**

1. **Phase Overview:**
   - [ ] Phase name/description present
   - [ ] Goals clearly stated
   - [ ] Success criteria defined

2. **Task Breakdown:**
   - [ ] Tasks clearly defined
   - [ ] Task dependencies identified
   - [ ] Task order logical
   - [ ] Effort estimates provided

3. **Test Plan:**
   - [ ] Test scenarios defined
   - [ ] Test cases identified
   - [ ] Test data requirements specified
   - [ ] Test coverage goals stated

4. **Dependencies:**
   - [ ] Prerequisites listed
   - [ ] External dependencies identified
   - [ ] Blocking issues noted
   - [ ] Resource requirements specified

5. **Implementation Details:**
   - [ ] Technical approach described
   - [ ] Architecture decisions documented
   - [ ] Design patterns specified
   - [ ] Code structure outlined

**Checklist:**

- [ ] All required sections present
- [ ] Sections are complete
- [ ] Information is actionable
- [ ] Plan is ready for implementation

---

### 3. Validate Dependencies

**Check prerequisites:**

1. **Previous Phases:**
   - [ ] Previous phases complete
   - [ ] Dependencies from previous phases met
   - [ ] Required functionality available

2. **External Dependencies:**
   - [ ] External libraries/tools available
   - [ ] API dependencies ready
   - [ ] Infrastructure ready
   - [ ] Third-party services configured

3. **Internal Dependencies:**
   - [ ] Related features complete
   - [ ] Shared components ready
   - [ ] Database schema updated (if needed)
   - [ ] Configuration changes made (if needed)

4. **Resource Dependencies:**
   - [ ] Team members available
   - [ ] Development environment ready
   - [ ] Testing environment ready
   - [ ] Documentation resources available

**Checklist:**

- [ ] All dependencies identified
- [ ] Dependencies are available
- [ ] Blocking dependencies resolved
- [ ] Phase can proceed

---

### 4. Review Test Plan

**Validate test coverage:**

1. **Test Scenarios:**
   - [ ] Happy path scenarios defined
   - [ ] Edge cases identified
   - [ ] Error cases covered
   - [ ] Integration scenarios specified

2. **Test Cases:**
   - [ ] Unit tests planned
   - [ ] Integration tests planned
   - [ ] Manual tests identified
   - [ ] Test data requirements clear

3. **Test Coverage:**
   - [ ] Coverage goals defined
   - [ ] Critical paths covered
   - [ ] Test strategy appropriate
   - [ ] Test tools selected

**Checklist:**

- [ ] Test plan is comprehensive
- [ ] Test scenarios are clear
- [ ] Test coverage goals are realistic
- [ ] Test plan is implementable

---

### 5. Identify Issues and Gaps

**Look for:**

1. **Missing Information:**
   - Incomplete task descriptions
   - Missing dependencies
   - Unclear requirements
   - Undefined success criteria

2. **Potential Problems:**
   - Ambiguous tasks
   - Unrealistic estimates
   - Missing test scenarios
   - Unidentified risks

3. **Improvement Opportunities:**
   - Better task breakdown
   - Clearer dependencies
   - More comprehensive tests
   - Better documentation

**Checklist:**

- [ ] Issues identified
- [ ] Gaps documented
- [ ] Recommendations provided
- [ ] Action items created

---

### 6. Generate Review Report

**Create review document:**

**Location:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N-review.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N-review.md`

**Report structure:**

```markdown
# Phase N Review - [Phase Name]

**Phase:** Phase N  
**Feature:** [Feature Name] (if applicable)
**Status:** 🔴 Not Ready / 🟡 Needs Work / ✅ Ready  
**Reviewed:** YYYY-MM-DD

---

## 📋 Phase Plan Completeness

### Overview
- [x] Phase name/description present
- [x] Goals clearly stated
- [x] Success criteria defined

### Task Breakdown
- [x] Tasks clearly defined
- [x] Task dependencies identified
- [x] Task order logical
- [x] Effort estimates provided

### Test Plan
- [x] Test scenarios defined
- [x] Test cases identified
- [x] Test data requirements specified
- [x] Test coverage goals stated

### Dependencies
- [x] Prerequisites listed
- [x] External dependencies identified
- [x] Blocking issues noted
- [x] Resource requirements specified

### Implementation Details
- [x] Technical approach described
- [x] Architecture decisions documented
- [x] Design patterns specified
- [x] Code structure outlined

---

## ✅ Dependencies Validation

### Previous Phases
- [x] Previous phases complete
- [x] Dependencies from previous phases met
- [x] Required functionality available

### External Dependencies
- [x] External libraries/tools available
- [x] API dependencies ready
- [x] Infrastructure ready
- [x] Third-party services configured

### Internal Dependencies
- [x] Related features complete
- [x] Shared components ready
- [x] Database schema updated (if needed)
- [x] Configuration changes made (if needed)

### Resource Dependencies
- [x] Team members available
- [x] Development environment ready
- [x] Testing environment ready
- [x] Documentation resources available

---

## 🧪 Test Plan Validation

### Test Scenarios
- [x] Happy path scenarios defined
- [x] Edge cases identified
- [x] Error cases covered
- [x] Integration scenarios specified

### Test Cases
- [x] Unit tests planned
- [x] Integration tests planned
- [x] Manual tests identified
- [x] Test data requirements clear

### Test Coverage
- [x] Coverage goals defined
- [x] Critical paths covered
- [x] Test strategy appropriate
- [x] Test tools selected

---

## 🔴 Issues and Gaps

### Missing Information
- [Issue 1]
- [Issue 2]

### Potential Problems
- [Problem 1]
- [Problem 2]

### Improvement Opportunities
- [Opportunity 1]
- [Opportunity 2]

---

## 💡 Recommendations

### Before Implementation
1. [Recommendation 1]
2. [Recommendation 2]

### During Implementation
1. [Recommendation 1]
2. [Recommendation 2]

---

## ✅ Readiness Assessment

**Overall Status:** [Not Ready / Needs Work / Ready]

**Blockers:**
- [Blocker 1]
- [Blocker 2]

**Action Items:**
- [ ] Action 1
- [ ] Action 2

---

**Last Updated:** YYYY-MM-DD
```

**Checklist:**

- [ ] Review document created
- [ ] All sections completed
- [ ] Issues documented
- [ ] Recommendations provided
- [ ] Readiness assessed

---

### 7. Update Phase Document

**If issues found:**

- Add review findings to phase document
- Update phase status
- Add action items
- Document blockers

**Checklist:**

- [ ] Phase document updated (if needed)
- [ ] Status updated
- [ ] Action items added
- [ ] Blockers documented

---

### 8. Summary Report

**Present to user:**

```markdown
## Pre-Phase Review Complete

**Phase:** Phase N - [Phase Name]
**Status:** [Not Ready / Needs Work / Ready]

### Review Summary

- [X] sections complete
- [Y] issues identified
- [Z] recommendations provided

### Key Findings

- Finding 1
- Finding 2

### Blockers

- [Blocker 1] (if any)
- [Blocker 2] (if any)

### Next Steps

1. Address identified issues
2. Update phase plan as needed
3. Resolve blockers
4. Re-run review if needed
5. Begin implementation when ready
```

---

## Common Issues

### Issue: Phase Document Missing

**Solution:**

- Check phase document location
- Verify phase number
- Create phase document if needed
- Use `/task-phase` to create phase plan first

### Issue: Dependencies Not Met

**Solution:**

- Complete prerequisite phases
- Resolve blocking dependencies
- Update phase plan with dependency status
- Document blockers

### Issue: Test Plan Incomplete

**Solution:**

- Add missing test scenarios
- Define test cases
- Specify test data requirements
- Set test coverage goals

---

## Tips

### Before Review

- Ensure phase plan is complete
- Review previous phase completions
- Check dependency status
- Verify test plan exists

### During Review

- Be thorough in checking completeness
- Identify all dependencies
- Validate test coverage
- Document all issues

### After Review

- Address identified issues
- Update phase plan
- Resolve blockers
- Re-run review if needed

---

## Reference

**Phase Documents:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N.md`

**Review Documents:**

- Feature-specific: `docs/maintainers/planning/features/[feature-name]/phase-N-review.md`
- Project-wide: `docs/maintainers/planning/phases/phase-N-review.md`

**Related Commands:**

- `/task-phase` - Create phase plans
- `/pr` - Create PRs for completed phases

---

**Last Updated:** 2025-12-07  
**Status:** ✅ Active  
**Next:** Use before starting phase implementation to ensure readiness (supports feature-specific and project-wide structures)

