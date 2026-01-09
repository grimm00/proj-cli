# Research: Inventory Integration

**Research Topic:** Work-Prod Integration  
**Question:** How does the registry relate to inventory scanning?  
**Status:** ✅ Complete  
**Priority:** 🟢 Low  
**Created:** 2026-01-08  
**Last Updated:** 2026-01-09  
**Completed:** 2026-01-09

---

## 🎯 Research Question

How does the registry relate to inventory scanning?

**Context:** Both registry and inventory track local projects; need to understand overlap and distinction.

---

## 🔍 Research Goals

- [x] Goal 1: Clarify distinction between registry and inventory
- [x] Goal 2: Determine if inventory scanning should update registry
- [x] Goal 3: Decide if registry entries should appear in inventory
- [x] Goal 4: Identify and eliminate any duplication

---

## 📚 Research Methodology

**Sources:**
- [x] Codebase: `src/proj/registry.py` (259 lines)
- [x] Codebase: `src/proj/commands/inventory.py` (inventory functions)
- [x] Documentation: Existing docstrings and design comments
- [x] User workflows: How users use both features

---

## 🔑 Sub-Questions

1. **Inventory → Registry:** Should inventory scanning update the registry?
2. **Registry → Inventory:** Should registry entries appear in inventory results?
3. **Duplication:** Is there duplication between these concepts?

---

## 📊 Findings

### Finding 1: Clear Separation of Concerns Already Exists

**Current Architecture:**

| Aspect | Registry | Inventory |
|--------|----------|-----------|
| **Purpose** | Track template-created projects for sync | Catalog all local projects |
| **Data Source** | `proj create` (template mode) | File system scan (`proj inv scan`) |
| **Storage** | `~/.local/share/proj/registry.json` | `~/.local/share/proj/inventory.json` |
| **API Sync** | Yes (work_prod_id linking) | Yes (export to API) |
| **User Action** | Automatic on create | Manual scan command |
| **Schema** | Minimal (sync-only fields) | Rich (metadata, languages, markers) |

**Source:** Codebase analysis (`src/proj/registry.py`, `src/proj/commands/inventory.py`)

**Relevance:** The two systems are intentionally separate with different purposes. Registry is a "sync overlay", inventory is a "project catalog".

---

### Finding 2: Registry Already Cross-References Inventory

**Explicit design documented in code:**

```python
# From registry.py:
@dataclass
class RegistryProject:
    """A project tracked in the registry for template sync.

    Minimal schema - only sync-related fields.
    Project metadata lives in inventory.json.
    Cross-references inventory via path field.
    """
```

**Design Intent:**
- Registry uses `path` as cross-reference key to inventory
- Registry is intentionally minimal (template, template_version, work_prod_id)
- Full project metadata (description, languages, etc.) lives in inventory

**Source:** `src/proj/registry.py` lines 12-25

**Relevance:** The cross-reference design already exists but is one-way (registry → inventory). Inventory doesn't know about registry.

---

### Finding 3: No Automatic Registration from Inventory Scan

**Current Behavior:**

| Operation | Updates Registry? | Updates Inventory? |
|-----------|-------------------|-------------------|
| `proj create` | Yes (if --register) | No (manual) |
| `proj inv scan local` | No | Yes |
| `proj inv scan github` | No | Yes |
| `proj delete` | Gap (should yes) | No |

**Source:** Codebase analysis

**Relevance:** Registry only tracks template-created projects, not all projects. This is intentional - registry is for "sync overlay" of template projects only.

---

### Finding 4: Field Name Already Aligned

**Both systems use `path` for consistency:**

| System | Internal Field | API Export |
|--------|---------------|------------|
| Registry | `path` (Path) | `path` (string) |
| Inventory | `local_path` (string) | `path` (transformed) |

**Export transformation:**
```python
# inventory.py - transforms on export
"path": item.get("local_path", ""),  # work-prod API expects "path"
```

**Source:** `src/proj/commands/inventory.py` lines 489, 563 (after BUG-001 fix)

**Relevance:** Field consistency is handled through transformation. Internal naming difference is acceptable.

---

### Finding 5: Two Valid Use Patterns

**Pattern 1: Template-First (Registry-Tracked)**
```
User → proj create → Creates project + Registers → API sync
                  ↓
              Registry tracks template sync state
```

**Pattern 2: Inventory-First (Catalog-Only)**
```
User → proj inv scan → Catalogs all projects → API export
                    ↓
                No registry entry (not template-created)
```

**Both patterns are valid and complementary:**
- Registry is for **template lifecycle management** (sync detection, upgrades)
- Inventory is for **project discovery and cataloging** (all projects)

**Source:** User workflow analysis

**Relevance:** Don't force integration - the separation is intentional.

---

### Finding 6: Potential Enhancement - Registry Awareness in Inventory

**Current Gap:**
```
Inventory scan → finds template-created project → no registry info shown
```

**Potential Enhancement:**
```
Inventory scan → finds template-created project → shows "✓ Registered" indicator
```

**Implementation:**
```python
# Hypothetical inventory enhancement
from proj.registry import is_registered

for project in inventory:
    if is_registered(Path(project["local_path"])):
        project["registered"] = True
```

**Source:** Analysis

**Relevance:** Nice-to-have for visibility, but not essential for core functionality.

---

## 🔍 Analysis

### Core Insight: Separation is Intentional and Correct

| Question | Answer | Rationale |
|----------|--------|-----------|
| Should inventory update registry? | **No** | Registry is for template projects only |
| Should registry appear in inventory? | **Optional** | Nice for visibility, not required |
| Is there duplication? | **No** | Different purposes, minimal overlap |

### The Two Systems Serve Different Needs

**Registry:** "Which projects did I create from templates, and what's their sync state?"
- Subset of projects (template-created only)
- Sync-focused fields (template version, work_prod_id)
- API integration purpose

**Inventory:** "What projects exist on my system?"
- All projects (GitHub, local, any source)
- Discovery-focused fields (languages, markers, source)
- Cataloging purpose

**Key Insights:**
- [x] Insight 1: Separation is architectural - don't merge
- [x] Insight 2: Cross-reference via `path` is sufficient linkage
- [x] Insight 3: Inventory can optionally show registry status for visibility
- [x] Insight 4: Both can push to API independently (registry via sync, inventory via export)

---

## 💡 Recommendations

### Recommendation 1: Keep Systems Separate

**Don't integrate inventory scan with registry.**

**Rationale:**
- Registry is for template-created projects only
- Inventory scans all projects (GitHub, local, any source)
- Merging would blur purpose of each system

---

### Recommendation 2: Add Optional Registry Indicator to Inventory (Low Priority)

**When listing inventory, optionally show if project is registered:**

```bash
proj inv list
# Could show:
# ✓ my-template-project (registered)
#   other-project
```

**Priority:** Low (visibility enhancement only)

---

### Recommendation 3: Document the Architecture

**Add clear documentation explaining:**
- Registry = sync overlay for template projects
- Inventory = catalog for all projects
- Path is the cross-reference key
- Both can sync to API independently

---

### Recommendation 4: No Changes Needed for Core Integration

**Current architecture is correct:**
- Registry tracks template sync state
- Inventory catalogs all projects
- Path provides linkage when needed
- API export works from both sources

---

## 📋 Requirements Discovered

### Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-INV-1 | Inventory scan shall NOT update registry (registry is template-only) | High |
| FR-INV-2 | Inventory list may optionally show registry status indicator | Low |
| FR-INV-3 | Inventory and registry shall both use `path` as linkage key | High |

### Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-INV-1 | Systems shall remain architecturally separate | High |
| NFR-INV-2 | Documentation shall clarify registry vs inventory purpose | Medium |

### Constraints

| ID | Constraint |
|----|------------|
| C-INV-1 | Registry only tracks template-created projects |
| C-INV-2 | Inventory catalogs all projects regardless of origin |

---

## 🚀 Next Steps

1. ✅ Research complete - architecture is correct
2. Optionally add registry indicator to inventory list (low priority)
3. Add documentation clarifying the two systems
4. No core changes needed

---

## 📊 Summary

**Key Finding:** The registry and inventory systems are intentionally separate with different purposes. This is correct architecture, not a gap.

| System | Purpose | Scope | API Integration |
|--------|---------|-------|-----------------|
| Registry | Template sync tracking | Template projects only | `work_prod_id` linking |
| Inventory | Project cataloging | All projects | Export to API |

**Recommendation:** Keep systems separate. The only potential enhancement is adding a registry indicator to inventory display for visibility.

---

**Last Updated:** 2026-01-09
