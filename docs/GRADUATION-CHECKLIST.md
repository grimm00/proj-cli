# Command Graduation Checklist

**Purpose:** Criteria for graduating commands from Experimental (🟠) to Stable (🟢)  
**Last Updated:** 2025-12-15  
**Based On:** [ADR-004: Graduation Process](https://github.com/grimm00/dev-infra/blob/main/admin/decisions/dev-infra-identity-and-focus/adr-004-graduation-process.md)

---

## Overview

This checklist defines the criteria for graduating commands and features from **Experimental (🟠)** to **Stable (🟢)**. All experimental features must pass this checklist before being added to the standard template.

**Why this matters:**

- Ensures quality and stability
- Validates user need
- Prevents premature graduation
- Documents decision rationale

---

## Required Criteria

**ALL must be met for graduation**

| Criterion | Threshold | How to Verify |
| --------- | --------- | ------------- |
| **Time in dev-infra** | ≥1 release cycle | Check when feature was introduced |
| **Stability** | No major changes in 2+ weeks | Review commit history |
| **Documentation** | 100% complete | Check all sections filled |
| **Demonstrated use** | Used successfully in dev-infra | Link to evidence |
| **No critical bugs** | No open critical issues | Check issue tracker |

### Checklist Template

```markdown
## Required Criteria (ALL must pass)

- [ ] In dev-infra for ≥1 release: [version introduced: vX.Y.Z]
- [ ] No major changes in last 2 weeks: [last change: YYYY-MM-DD]
- [ ] Documentation is 100% complete: [docs location]
- [ ] Used successfully in dev-infra: [evidence link]
- [ ] No open critical issues: [issue search link]
```

---

## Recommended Criteria

**Majority (3 of 4) should be met**

| Criterion | Threshold | How to Verify |
| --------- | --------- | ------------- |
| **User request** | Evidence of demand | Issue, discussion, feedback |
| **Low complexity** | Newcomers can understand | Code review, docs clarity |
| **Self-contained** | No dev-infra dependencies | Dependency analysis |
| **Testing defined** | Manual testing guide exists | Check for test docs |

### Checklist Template

```markdown
## Recommended Criteria (3/4 should pass)

- [ ] User/project has requested this feature: [evidence]
- [ ] Complexity is low (newcomer can understand): [reviewer assessment]
- [ ] No dev-infra-specific dependencies: [verified]
- [ ] Manual testing approach is documented: [guide location]
```

---

## Optional Criteria

**Nice to have (bonus points)**

| Criterion | Threshold | How to Verify |
| --------- | --------- | ------------- |
| **Multiple use cases** | >1 project type | Usage examples |
| **External validation** | Used in real project | Project reference |
| **Positive feedback** | Users report it works | Feedback collection |

### Checklist Template

```markdown
## Optional Criteria (nice to have)

- [ ] Applies to multiple project types: [which types]
- [ ] Validated in external project: [project link]
- [ ] Positive user feedback received: [feedback summary]
```

---

## Graduation Process

### 1. Identify Candidate

When you believe a command is ready for graduation:

- [ ] Command has been in experimental template for ≥1 release
- [ ] You have used the command successfully
- [ ] You can document its value

### 2. Create Graduation Proposal

**File:** Create issue or discussion with this template:

```markdown
## Graduation Proposal: [Command Name]

**Command:** /command-name
**Introduced:** vX.Y.Z (YYYY-MM-DD)
**Proposer:** [Your name]

### Required Criteria (ALL must pass)

- [ ] In dev-infra for ≥1 release: vX.Y.Z
- [ ] No major changes in last 2 weeks: last change YYYY-MM-DD
- [ ] Documentation 100% complete: [link]
- [ ] Used successfully in dev-infra: [evidence]
- [ ] No open critical issues: [search link]

### Recommended Criteria (3/4 should pass)

- [ ] User request: [evidence or N/A]
- [ ] Low complexity: [assessment]
- [ ] Self-contained: [verified]
- [ ] Testing documented: [guide link]

### Rationale

[Why this command should graduate]

### Evidence of Value

[Examples, metrics, feedback]
```

### 3. Review Period

**Duration:** 1 week minimum

- [ ] Proposal reviewed by maintainer
- [ ] Any final changes implemented
- [ ] Tests pass
- [ ] Documentation updated

### 4. Graduation PR

Create PR with the following changes:

**PR Title:** `feat(templates): graduate [command-name] to stable`

**Changes:**

- [ ] Move command to standard template
- [ ] Update stability indicator: 🟠 → 🟢
- [ ] Update command header (remove experimental warning)
- [ ] Update template README (move from Experimental to Stable)
- [ ] Add to release notes

**PR Body:**

```markdown
## Command Graduation: [Command Name]

Graduates /command-name from Experimental (🟠) to Stable (🟢).

### Graduation Checklist ✅

- [x] Required criteria: 5/5 passed
- [x] Recommended criteria: X/4 passed
- [x] Review period: completed YYYY-MM-DD

### Changes

- Moved command from experimental to standard template
- Updated stability indicator
- Updated documentation

### Evidence

[Link to graduation proposal/discussion]
```

### 5. Post-Graduation

After merge:

- [ ] Update CHANGELOG.md
- [ ] Highlight in release notes
- [ ] Update experimental template docs (remove graduated command)
- [ ] Notify users (if applicable)

---

## Graduation Decision Tree

```
Command is experimental
        │
        ▼
All REQUIRED criteria met?
        │
   NO ◄─┴─► YES
   │         │
   ▼         ▼
DEFER    3/4 RECOMMENDED met?
             │
        NO ◄─┴─► YES
        │         │
        ▼         ▼
     DEFER    GRADUATE ✅
     (with     
     reasons)  
```

---

## Decision Outcomes

### ✅ GRADUATE

Command moves to standard template.

**Action:** Create graduation PR

### ⏸️ DEFER

Command needs more time or refinement.

**Action:** Document what's needed, set timeline for re-review

### ❌ REJECT

Command is not suitable for templates.

**Action:** Document reasons, consider alternative approaches

---

## Examples

### Example: Successful Graduation

**Command:** `/status`

| Criterion | Met | Evidence |
| --------- | --- | -------- |
| Time in dev-infra | ✅ | v1.5.0 (3 months ago) |
| Stability | ✅ | No changes in 4 weeks |
| Documentation | ✅ | Complete with examples |
| Used in dev-infra | ✅ | Used in 15 PRs |
| User request | ✅ | 3 issues requesting |
| Low complexity | ✅ | Simple single-file command |
| Self-contained | ✅ | No external deps |
| Testing documented | ✅ | Manual testing guide exists |

**Decision:** GRADUATE

### Example: Deferred Graduation

**Command:** `/complex-workflow`

| Criterion | Met | Evidence |
| --------- | --- | -------- |
| Time in dev-infra | ✅ | v1.5.0 |
| Stability | ❌ | Changed 3 days ago |
| Documentation | ⚠️ | 80% complete |
| Used in dev-infra | ✅ | Used successfully |

**Decision:** DEFER - Wait 2 weeks, complete documentation

---

## Related Documents

- **[Stability Levels](STABILITY-LEVELS.md)** - Understanding stability indicators
- **[Experimental Features](EXPERIMENTAL.md)** - Overview of experimental template
- **[ADR-004](https://github.com/grimm00/dev-infra/blob/main/admin/decisions/dev-infra-identity-and-focus/adr-004-graduation-process.md)** - Graduation process decision

---

**Last Updated:** 2025-12-15

