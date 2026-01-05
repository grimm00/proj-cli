# Template Generation Learnings - Phase 2: Local Registry

**Project:** proj-cli  
**Feature:** Template Generation Extension  
**Phase:** 2 - Local Registry  
**Date:** 2026-01-05  
**Status:** ✅ Complete  
**Last Updated:** 2026-01-05

---

## 📋 Overview

Phase 2 created a local registry module to track template-created projects for sync purposes. The registry acts as a minimal overlay that cross-references `inventory.json` (the primary project store). This phase involved significant architectural refinement mid-implementation.

**PR:** #10 (merged 2026-01-05)
**Duration:** ~3 hours (including architectural refinement)
**Tests:** 22 passing

---

## ✅ What Worked Exceptionally Well

### 1. Dataclasses for Simple Models

**Why it worked:**
Using Python dataclasses (instead of Pydantic) for `RegistryProject` and `Registry` kept the models lightweight and focused.

**What made it successful:**
- No validation overhead needed (data comes from trusted sources)
- Clear, simple data structures
- Easy JSON serialization with custom functions

**Template implications:**
- Recommend dataclasses for internal data models
- Reserve Pydantic for user-facing configuration

**Key examples:**

```python
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

@dataclass
class RegistryProject:
    """Minimal schema - only sync-related fields."""
    path: Path  # Cross-reference key to inventory
    template: str  # Template type used
    template_version: str  # Template version for sync
    created_at: datetime  # When created

@dataclass
class Registry:
    """Sync overlay, not a project store."""
    version: str = "1.0"
    projects: list[RegistryProject] = field(default_factory=list)
```

**Benefits:**
- Simple, readable code
- No external dependencies for models
- Easy to test

---

### 2. Pre-Merge Fix Pattern (Sourcery Workflow)

**Why it worked:**
Fixing all HIGH priority Sourcery issues before merge resulted in cleaner code and no deferred technical debt.

**What made it successful:**
- PR validation identified 5 issues (4 HIGH, 1 MEDIUM)
- All HIGH issues were LOW effort to fix
- Fixed on the same branch before merge

**Template implications:**
- Document pre-merge fix pattern in workflow docs
- Encourage fixing HIGH priority, LOW effort issues before merge

**Key examples:**
- #1: Updated docstring (removed misleading "atomic write" claim)
- #2: Added path normalization (`.resolve()`)
- #3: Added round-trip test
- Overall-#2: Added Z suffix handling for datetime

**Benefits:**
- No deferred HIGH priority issues
- Cleaner merge
- Better code quality from start

---

### 3. Architectural Refinement Pattern

**Why it worked:**
Identifying overlap between `registry.json` and `inventory.json` mid-phase and refining the architecture before proceeding prevented future rework.

**What made it successful:**
- Paused implementation to analyze overlap
- Used `/transition-plan --update-adr` to document decision
- Simplified `RegistryProject` to minimal schema (4 fields instead of 8)
- Updated phase plan to reflect new architecture

**Template implications:**
- Document architectural refinement workflow
- ADR updates should be part of normal development

**Key decisions:**
- `inventory.json` = Primary project store (all projects, rich metadata)
- `registry.json` = Sync overlay (template projects only, minimal fields)
- Cross-reference via `path` field

**Benefits:**
- Cleaner separation of concerns
- No duplication between files
- Simpler implementation

---

### 4. Functional Module Design

**Why it worked:**
Using pure functions (`load_registry()`, `save_registry()`, `add_project()`, etc.) instead of a class made the module easy to test and use.

**What made it successful:**
- Each function has single responsibility
- No shared state (loads registry fresh each time)
- Easy to test in isolation

**Template implications:**
- Consider functional design for data persistence modules
- Document functional vs class-based patterns

**Key examples:**

```python
def load_registry() -> Registry:
    """Load registry from disk, creating empty if not exists."""
    ...

def save_registry(registry: Registry) -> None:
    """Save registry to disk."""
    ...

def add_project(path: Path, template: str, template_version: str) -> RegistryProject:
    """Add a new project to the registry."""
    registry = load_registry()
    # ... add project ...
    save_registry(registry)
    return project
```

**Benefits:**
- Clear function contracts
- Easy to test each function
- No hidden state

---

## 🟡 What Needs Improvement

### 1. Path Normalization Oversight

**What the problem was:**
Initial implementation didn't normalize paths with `.resolve()`, causing potential duplicate detection issues with relative vs absolute paths.

**Why it occurred:**
Assumed callers would always pass consistent path formats.

**Impact:**
- Sourcery flagged as HIGH priority
- Required fix before merge

**How to prevent:**
- Always normalize paths at entry points
- Add path format tests (relative, absolute, symlinks)

**Template changes needed:**
- Document path normalization pattern in data modules
- Include path format tests in test templates

**Fix:**

```python
def add_project(path: Path, ...) -> RegistryProject:
    # Normalize path for consistent comparisons
    path = path.resolve()
    ...
```

---

### 2. ISO 8601 Z Suffix Handling

**What the problem was:**
`datetime.fromisoformat()` doesn't accept the `Z` suffix (ISO 8601 UTC indicator) that many JSON APIs use.

**Why it occurred:**
Didn't test with Z-suffix timestamps in test data.

**Impact:**
- Registry files with Z timestamps would fail to load
- Required fix before merge

**How to prevent:**
- Test datetime parsing with various formats
- Document datetime format expectations

**Template changes needed:**
- Include Z suffix test case in datetime parsing examples
- Document datetime format handling

**Fix:**

```python
# Handle Z suffix (ISO 8601 UTC) - fromisoformat doesn't accept it
created_at_str = proj_data["created_at"]
if created_at_str.endswith("Z"):
    created_at_str = created_at_str[:-1] + "+00:00"
created_at = datetime.fromisoformat(created_at_str)
```

---

### 3. Atomic Write Documentation

**What the problem was:**
Docstring claimed "atomic write" but implementation wasn't actually atomic (no temp file pattern).

**Why it occurred:**
Copied docstring pattern without implementing the behavior.

**Impact:**
- Misleading documentation
- Sourcery flagged as HIGH priority

**How to prevent:**
- Review docstrings for accuracy
- Only claim behaviors that are implemented

**Template changes needed:**
- Remove "atomic" from file write docstrings unless implemented
- Or implement temp file + rename pattern

**Fix (simple):**

```python
def save_registry(registry: Registry) -> None:
    """Save registry to disk.
    
    Note: This is not an atomic write. If the process is interrupted,
    the file may be left in a partial state. For this use case (small
    registry files, low-frequency writes), this is acceptable.
    """
```

---

## 💡 Unexpected Discoveries

### 1. Inventory vs Registry Overlap Analysis

**Finding:**
Stopping to analyze the overlap between `inventory.json` and `registry.json` before completing implementation saved significant rework.

**Why it's valuable:**
- Original plan had registry storing full project metadata
- Analysis revealed registry should only store sync-specific fields
- Simplified `RegistryProject` from 8 fields to 4

**How to leverage:**
- Before implementing data models, analyze existing stores
- Use ADR updates to document architectural refinements
- Don't be afraid to pause and refine architecture

---

### 2. Cross-Reference Pattern Effectiveness

**Finding:**
Using `path` as the cross-reference key between registry and inventory works well because:
- Paths are unique identifiers for local projects
- No need for synthetic IDs
- Easy to verify and debug

**Why it's valuable:**
- Simpler than managing separate ID systems
- Natural key that users understand
- Works with existing inventory structure

**How to leverage:**
- Use natural keys when possible for cross-references
- Document the cross-reference pattern in data model docs

---

### 3. Round-Trip Testing Value

**Finding:**
The round-trip test (`save → load → assert equal`) caught subtle serialization issues that unit tests missed.

**Why it's valuable:**
- Tests full serialization cycle
- Catches datetime format issues
- Catches path format issues
- Verifies real-world usage pattern

**How to leverage:**
- Always add round-trip tests for data persistence
- Test with edge case data (timestamps, paths, unicode)

---

## ⏱️ Time Investment Analysis

**Breakdown:**
- Tasks 1-2 (Models): 30 minutes
- Architectural analysis: 20 minutes
- ADR update: 15 minutes
- Tasks 3-8 (Functions): 60 minutes
- Sourcery fixes: 30 minutes
- Documentation: 15 minutes

**What took longer:**
- Architectural analysis: Stopped implementation to analyze overlap
- Sourcery fixes: 5 issues required addressing before merge

**What was faster:**
- Individual functions: Clear patterns, quick implementation
- Tests: Straightforward with isolated fixtures

**Estimation lessons:**
- Budget time for mid-phase architectural reviews
- Pre-merge fixes are faster than post-merge (same context)

---

## 📊 Metrics & Impact

**Code metrics:**
- Lines added: ~220 (registry.py) + ~350 (tests)
- Test coverage: 22 tests passing
- Files created: 2 (registry.py, test_registry.py)

**Quality metrics:**
- Sourcery issues: 5 total (all fixed before merge)
- Deferred issues: 0

**Developer experience:**
- Effective TDD workflow
- Clean architectural refinement
- Pre-merge fix pattern worked well

---

## 🎯 Template Recommendations

### For dev-infra Template

1. **Add dataclass examples** for internal data models
2. **Document path normalization pattern** for data modules
3. **Include round-trip test template** for persistence modules
4. **Add datetime Z suffix handling** to datetime parsing examples
5. **Document pre-merge fix pattern** in workflow docs

### For Future Template Generation Phases

1. Continue functional module design pattern
2. Test with varied input formats (paths, timestamps)
3. Consider atomic write implementation for critical files
4. Keep architectural refinement as normal practice

---

## 🔗 Key Architectural Decision

**ADR-0008 Refinement:**

```
inventory.json (Primary Store)         registry.json (Sync Overlay)
├── All projects                       ├── Template-created only
├── Rich metadata                      ├── Minimal fields:
├── Multiple sources                   │   ├── path (cross-ref key)
└── Full project info                  │   ├── template
                                       │   ├── template_version
                                       │   └── created_at
                                       └── Cross-references inventory
```

---

## 🔗 Related

- [Phase 2 Document](../phase-2.md)
- [Fix Tracking](../fix/pr10/README.md)
- [Sourcery Review PR #10](../../../../feedback/sourcery/pr10.md)
- [ADR-0008](../../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2026-01-05

