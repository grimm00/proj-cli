# Research: Project Creation Date Semantics

**Research Topic:** Work-Prod Integration  
**Question:** How should we track when a project actually began vs when we recorded it?  
**Status:** ✅ Complete  
**Priority:** 🟡 Medium  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09  
**Completed:** 2026-01-09

---

## 🎯 Research Question

How should we track when a project actually began vs when we recorded it?

**Context:** Current `created_at` field only tracks when the record was created in our system (inventory scan, API creation), not when the project itself was started. This limits usefulness for project timeline analysis.

---

## 🔍 Research Goals

- [x] Goal 1: Distinguish `created_at` (record creation) from `started_at` (project inception)
- [x] Goal 2: Research methods to obtain actual project start dates
- [x] Goal 3: Determine if work-prod API schema should be extended
- [x] Goal 4: Design handling for unknown start dates

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase: Current implementation in proj-cli and work-prod
- [x] Git: First commit timestamp commands
- [x] OS: File/directory creation timestamps
- [x] Database patterns: Audit trail and entity lifecycle patterns

---

## 🔑 Sub-Questions

1. **Date Distinction:** Should we distinguish `created_at` (record creation) from `started_at` (project inception)?
2. **Data Sources:** How can we obtain actual project start dates?
3. **Capture Timing:** Should this be captured at scan time or on-demand?
4. **Schema Impact:** Should work-prod API schema be extended with `started_at` field?
5. **Unknown Dates:** How should we handle projects where start date is unknown?

---

## 📊 Findings

### Finding 1: Current Date Handling is System-Centric

**Current implementation:**

| System | Field | Meaning | Source |
|--------|-------|---------|--------|
| proj-cli registry | `created_at` | When project was registered | `datetime.now()` |
| work-prod API | `created_at` | When API record was created | `func.now()` (DB) |
| work-prod API | `updated_at` | When API record was modified | `func.now()` (DB) |

All current dates track **system events** (when records were created), not **project events** (when the project actually started).

**Source:** Codebase analysis (`src/proj/registry.py`, `backend/app/models/project.py`)

**Relevance:** Limits usefulness for project timeline analysis ("How long has this project existed?")

---

### Finding 2: Multiple Date Sources Available for Git Projects

**Methods to obtain project inception dates:**

| Method | Command/API | Reliability | Notes |
|--------|-------------|-------------|-------|
| Git first commit | `git log --reverse --format=%aI \| head -1` | High | Accurate for git repos |
| Git repo creation | `git log --reverse --format=%cI \| head -1` | High | Commit date (not author date) |
| GitHub API | `GET /repos/{owner}/{repo}` → `created_at` | High | Only for GitHub repos |
| macOS birthtime | `stat -f %SB` | Medium | File creation (may not exist) |
| Linux | `stat --printf=%W` | Low | Many filesystems don't track this |

**Git command (most reliable):**
```bash
git log --reverse --format='%aI' | head -1
# Returns: 2024-03-15T10:30:00-07:00
```

**Source:** Git documentation, OS file system capabilities

**Relevance:** Git first commit is the most reliable source for actual project start date.

---

### Finding 3: Database Patterns Support Entity vs Record Dates

**Common database pattern:**

| Field | Purpose | Example |
|-------|---------|---------|
| `created_at` | When record was inserted | System-managed, immutable |
| `updated_at` | When record was modified | System-managed, auto-updated |
| `started_at` or `inception_date` | When entity began existing | User/system-provided |
| `ended_at` | When entity ceased (soft delete) | Optional |

**Best practice:** Separate **system timestamps** (record lifecycle) from **entity timestamps** (business/domain dates).

**Examples:**
- Employee record: `created_at` (hired into system) vs `start_date` (actual job start)
- Project record: `created_at` (added to tracker) vs `started_at` (first commit)

**Source:** Database design patterns, audit trail implementations

**Relevance:** Adding `started_at` follows established patterns without breaking existing `created_at` semantics.

---

### Finding 4: Null/Unknown Start Dates Need Strategy

**Scenarios where start date is unknown:**

1. **Non-git directories:** No commit history to query
2. **Moved/copied projects:** Original timestamps lost
3. **Legacy projects:** Created before tracking was implemented
4. **Network filesystems:** May not preserve creation time

**Options for handling unknown dates:**

| Strategy | Behavior | Pros | Cons |
|----------|----------|------|------|
| **Allow null** | `started_at: null` | Simple, honest | Complicates queries |
| **Default to created_at** | `started_at = created_at` | No nulls | Misleading data |
| **Explicit "unknown"** | Special marker value | Clear intent | More complexity |
| **Estimate from path** | Extract year from path pattern | Data available | Unreliable |

**Recommendation:** Allow null with explicit semantics.

**Source:** Data quality best practices

**Relevance:** Null is honest - we don't know the date. Forcing a value creates misleading data.

---

### Finding 5: Capture Timing Trade-offs

**When to capture `started_at`:**

| Timing | Method | Pros | Cons |
|--------|--------|------|------|
| **Scan time** | Run git command during `proj inv scan` | Automatic, complete data | Slower scan |
| **On-demand** | Separate command or lazy loading | Fast scan | Extra user action |
| **Create time** | During `proj create` | Accurate for new projects | Doesn't help existing |
| **API sync time** | When syncing to work-prod | Centralized logic | Late capture |

**Recommendation:** Capture at **scan time** for git repos (fast, reliable). Use null for non-git.

**Source:** UX analysis, performance considerations

**Relevance:** Scan time is the natural moment to gather project metadata.

---

### Finding 6: Schema Extension is Low-Risk

**Current work-prod API Project model:**
```python
class Project(db.Model):
    # Existing fields
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Proposed addition
    started_at = db.Column(db.DateTime, nullable=True)  # Project inception date
```

**Migration impact:**
- New nullable column - no data migration required
- Existing records: `started_at = null` (correct - we don't know)
- New records: populated if available

**Source:** Work-prod API schema analysis

**Relevance:** Safe, non-breaking change that follows existing patterns.

---

## 🔍 Analysis

### Core Insight: Two Different Questions

| Question | Field | Who Sets It |
|----------|-------|-------------|
| "When did we start tracking this project?" | `created_at` | System (automatic) |
| "When did this project actually begin?" | `started_at` | User/scan (extracted) |

Both questions are valid and useful - they shouldn't share a single field.

### Semantic Clarity

| Field | Semantic | Set By | Nullable | Mutable |
|-------|----------|--------|----------|---------|
| `created_at` | Record creation | System | No | No |
| `updated_at` | Record modification | System | No | Yes (auto) |
| `started_at` | Project inception | User/scan | Yes | Yes |

**Key Insights:**
- [x] Insight 1: `created_at` and `started_at` answer different questions - both are needed
- [x] Insight 2: Git first commit is the most reliable source for `started_at`
- [x] Insight 3: Allow null for unknown dates - honest is better than misleading
- [x] Insight 4: Capture at scan time for inventory, at create time for new projects

---

## 💡 Recommendations

### Recommendation 1: Add `started_at` to work-prod API Schema

**Change:**
```python
# backend/app/models/project.py
started_at = db.Column(db.DateTime, nullable=True)
```

**Rationale:** Separates record lifecycle from project lifecycle. Low-risk nullable addition.

---

### Recommendation 2: Capture `started_at` During Inventory Scan

**For git repositories:**
```bash
# Extract first commit date
git log --reverse --format='%aI' 2>/dev/null | head -1
```

**For non-git directories:**
- Set `started_at = null`
- User can manually set via API if known

---

### Recommendation 3: Set `started_at` During `proj create`

**For new projects:**
```python
# src/proj/commands/projects/create.py
started_at = datetime.now()  # Project starts now
```

**Rationale:** New projects created via template have a known start date.

---

### Recommendation 4: Allow User Override via API

**Enable manual setting:**
```bash
proj update <project> --started-at 2024-03-15
```

**Rationale:** User may know the actual start date even when system can't detect it.

---

## 📋 Requirements Discovered

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-DATE-1 | Add `started_at` field to work-prod API Project model | High |
| FR-DATE-2 | Extract first commit date during `proj inv scan` for git repos | Medium |
| FR-DATE-3 | Set `started_at` to current time during `proj create` | High |
| FR-DATE-4 | Allow manual `started_at` override via update command | Low |
| FR-DATE-5 | Preserve `created_at` semantics (record creation only) | High |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-DATE-1 | Git first-commit extraction should add <100ms to scan per repo | Medium |
| NFR-DATE-2 | Allow null `started_at` - don't force inaccurate data | High |

### Constraints

| ID | Constraint |
|----|------------|
| C-DATE-1 | `started_at` must be nullable (unknown dates are valid) |
| C-DATE-2 | `created_at` semantics must not change (backward compatible) |

---

## 🚀 Next Steps

1. ✅ Research complete
2. Add `started_at` to work-prod API schema (migration)
3. Update inventory scan to extract git first-commit
4. Update `proj create` to set `started_at`
5. Add `--started-at` option to update command

---

**Last Updated:** 2026-01-09
