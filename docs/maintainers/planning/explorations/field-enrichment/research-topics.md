# Research Topics - Field Enrichment

**Purpose:** List of research topics/questions to investigate  
**Status:** 🔴 Pending Research  
**Created:** 2026-01-09  
**Last Updated:** 2026-01-09

---

## 📋 Research Topics

This document lists research topics and questions that need investigation before making decisions about field enrichment.

---

### Research Topic 1: File-System to Metadata Mapping

**Question:** How should directory structure map to project metadata fields?

**Sub-questions:**
- Should `~/Projects/work/` automatically set `project_type: "Work"`?
- Should we support nested patterns like `~/Projects/work/client-a/` → `organization: "client-a"`?
- How do we handle projects that don't fit the pattern?
- Should this mapping be bidirectional (metadata → directory suggestions)?

**Why:** Directory structure is a natural way developers organize projects. Leveraging this for metadata could eliminate manual data entry.

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 2: Config Pattern Design

**Question:** What's the best pattern/syntax for path-based config rules?

**Sub-questions:**
- Glob patterns vs regex vs simple prefix matching?
- Precedence: What if multiple patterns match?
- Validation: How do we validate pattern syntax?
- Migration: How do we help users set up initial patterns?

**Potential approaches:**
```yaml
# Approach A: Simple glob
path_patterns:
  "~/Projects/work/*":
    project_type: "Work"

# Approach B: Named rules with priority
rules:
  - name: work-projects
    pattern: "*/work/*"
    priority: 10
    fields:
      project_type: "Work"

# Approach C: Directory-based (special directories)
special_dirs:
  work: { project_type: "Work" }
  personal: { project_type: "Personal" }
```

**Why:** Config patterns are the core mechanism for automation. The design affects usability and flexibility.

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 3: Enrichment Timing and Triggers

**Question:** When should field enrichment happen?

**Options to investigate:**
1. **At creation time** - `proj create` infers/prompts for fields
2. **After scan** - `proj inv scan` followed by `proj enrich`
3. **On-demand** - `proj enrich [project-id]` explicitly
4. **Automatic sync** - Background process keeps fields up-to-date
5. **Pre-export** - Enrich before `proj inv export api`

**Trade-offs:**
- Early enrichment (creation) = less data entry later, but more prompts upfront
- Late enrichment (on-demand) = flexible, but fields stay empty longer
- Automatic = magic, but unexpected changes

**Why:** Timing affects user experience and data consistency.

**Priority:** High

**Status:** 🔴 Not Started

---

### Research Topic 4: Bulk Update UX Patterns

**Question:** What's the best UX for updating many projects at once?

**Options to investigate:**
1. **Multi-ID update** - `proj update --type Work 1 2 3 4`
2. **Filter-based update** - `proj bulk-update --filter "org=null" --set-org "my-company"`
3. **Interactive wizard** - `proj enrich` walks through projects
4. **CSV/JSON import** - `proj import-fields projects.csv`
5. **Editor-based** - Open list in $EDITOR, save changes

**Why:** Bulk operations are essential for managing many projects (59+ discovered).

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 5: Source of Truth Architecture

**Question:** Where should enriched field data live?

**Options:**
1. **API only** - All data in work-prod API
2. **Registry only** - All data in local registry.json
3. **Hybrid** - Registry stores overrides, API is canonical
4. **Inventory** - Inventory.json stores all local data

**Considerations:**
- API availability (offline scenarios)
- Data sync complexity
- Conflict resolution
- Performance

**Why:** Architecture affects sync behavior, offline support, and data consistency.

**Priority:** Medium

**Status:** 🔴 Not Started

**Related:** [Research: Source of Truth](../../research/work-prod-integration/research-source-of-truth.md)

---

### Research Topic 6: Quick Win - project_type in CLI

**Question:** Should we fix the `project_type` gap first as a quick win?

**Current state:**
- `proj list --type Work` works (filtering)
- `proj create --type Work` does NOT work (can't set)
- `proj update --type Work 42` does NOT work (can't set)

**Fix scope:**
- Add `--type` to `create_project()` in create.py
- Add `--type` to `update_project()` in crud.py
- Add validation for valid enum values
- Tests

**Effort:** ~2-3 hours

**Why:** This is a clear gap that should exist. Quick win before larger feature.

**Priority:** High (but separate from main feature)

**Status:** 🔴 Not Started

---

### Research Topic 7: Init Command Enhancements

**Question:** How should `proj init` set up field enrichment configuration?

**Current state:**
- `proj init` creates config.yaml with API settings
- No path pattern configuration
- No default field values

**Potential enhancements:**
- Interactive setup: "Do you organize projects by type? (work/personal/learning)"
- Auto-detect existing structure: "Found ~/Projects/work/ - map to Work type?"
- Suggest standard structure: "Recommended: ~/Projects/{work,personal,learning}/"

**Why:** Init is the natural place to set up conventions before projects are created.

**Priority:** Medium

**Status:** 🔴 Not Started

---

### Research Topic 8: Template Integration

**Question:** Should templates influence field defaults?

**Current state:**
- Templates don't set any API fields except name, path, description
- `--template standard-project` doesn't imply `project_type: "Work"`

**Options:**
1. **Template metadata** - Templates define default fields
   ```yaml
   # In template.yaml
   defaults:
     project_type: "Work"
     classification: "primary"
   ```

2. **Template-to-type mapping** - Config maps templates to types
   ```yaml
   template_defaults:
     standard-project:
       project_type: "Work"
     learning-project:
       project_type: "Learning"
   ```

3. **No coupling** - Keep templates and fields separate

**Why:** Templates are already used to create projects. Could be natural integration point.

**Priority:** Low

**Status:** 🔴 Not Started

---

## 🎯 Research Workflow

1. Use `/research [topic] --from-explore field-enrichment` to conduct research
2. Research will create documents in `docs/maintainers/research/field-enrichment/`
3. After research complete, use `/decision [topic] --from-research` to make decisions

---

## 📊 Priority Summary

| Priority | Topic | Effort | Notes |
|----------|-------|--------|-------|
| 🔴 High | project_type Quick Win | ~2-3h | Clear gap, should fix first |
| 🔴 High | File-System Mapping | ~4h | Core concept |
| 🔴 High | Config Pattern Design | ~4h | Core implementation |
| 🔴 High | Enrichment Timing | ~2h | UX decision |
| 🟡 Medium | Bulk Update UX | ~3h | Important for usability |
| 🟡 Medium | Source of Truth | ~2h | Architecture decision |
| 🟡 Medium | Init Enhancements | ~3h | Setup experience |
| 🟢 Low | Template Integration | ~2h | Nice-to-have |

---

**Last Updated:** 2026-01-09
