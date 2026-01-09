# Field Enrichment - Exploration

**Status:** 🔴 Exploration  
**Created:** 2026-01-09  
**Last Updated:** 2026-01-09

---

## 🎯 What Are We Exploring?

How to populate and manage project metadata fields across the entire project lifecycle:

1. **Initial creation** - Setting fields at project creation time
2. **Inventory scanning** - Populating fields from discovered projects
3. **Ongoing enrichment** - Updating fields as projects evolve
4. **File-system integration** - Using directory structure as metadata source

The goal is a cohesive, usability-focused approach where field population feels natural and integrated rather than a separate "data entry" task.

---

## 🤔 Why Explore This?

### Current Problem

After projects are created or scanned, several API fields remain empty:

| Field | `inv scan` | `create --template` | `update` | Notes |
|-------|------------|---------------------|----------|-------|
| `name` | ✅ | ✅ | ✅ | Works |
| `description` | ✅ (GitHub) | ✅ | ✅ | Works |
| `path` | ✅ | ✅ | ✅ | Works |
| `remote_url` | ✅ | ❌ | ✅ | Not synced from template |
| `status` | ⚠️ hardcoded | ⚠️ hardcoded | ✅ | Always "active" |
| `organization` | ❌ | ❌ | ✅ | No source |
| `classification` | ❌ | ❌ | ✅ | No source |
| **`project_type`** | ❌ | ❌ | ❌ | **Cannot be set at all!** |

### Underlying Issues

1. **No unified mental model** - Fields are scattered across API, registry, inventory
2. **No config-driven defaults** - User can't configure default values
3. **No file-system awareness** - Directory structure (~/Projects/work/ vs ~/Projects/personal/) is ignored
4. **Missing CLI options** - `project_type` not in create/update commands
5. **No bulk operations** - Must update projects one at a time

---

## 💡 Initial Thoughts

### Thought 1: File-System as Metadata Source

Directory structure could imply metadata:

```
~/Projects/
├── work/                  # project_type = "Work", organization = "employer"
│   ├── project-a/
│   └── project-b/
├── personal/              # project_type = "Personal"
│   ├── hobby-1/
│   └── hobby-2/
└── learning/              # project_type = "Learning"
    ├── course-1/
    └── tutorials/
```

**Benefits:**
- Natural organization that developers already use
- Metadata derived from existing structure, not manual entry
- File system is the "source of truth" for local organization

**Questions:**
- How do we map directory structure to fields?
- What if someone doesn't use this structure?
- Should we enforce it or just suggest it?

---

### Thought 2: Config-Driven Defaults

Users could configure default field values in `~/.config/proj/config.yaml`:

```yaml
# Field defaults based on parent directory patterns
path_patterns:
  "~/Projects/work/*":
    project_type: "Work"
    organization: "my-company"
    classification: "primary"
  "~/Projects/personal/*":
    project_type: "Personal"
    organization: null
    classification: "secondary"
  "~/Projects/learning/*":
    project_type: "Learning"
    classification: "secondary"

# Default for projects not matching any pattern
defaults:
  status: "active"
  classification: "secondary"
```

**Benefits:**
- User controls their own conventions
- Flexible - works with any directory structure
- Explicit - no magic inference

---

### Thought 3: Enrichment at Creation Time

When running `proj create`, prompt for or infer fields:

```bash
$ proj create my-project --template standard-project --target-dir ~/Projects/work/

# Could auto-detect:
# - project_type: "Work" (from ~/Projects/work/)
# - organization: "my-company" (from config pattern match)
# - status: "active" (from config default)
```

Or interactive mode:

```bash
$ proj create
Project name: my-project
Template: standard-project
Target directory [~/Projects]: ~/Projects/work/

# Auto-populated from path:
Project type [Work]: 
Organization [my-company]: 
Classification [primary]: 
Description: My new work project
```

---

### Thought 4: Enrichment After Scan

After `proj inv scan`, run enrichment:

```bash
$ proj inv scan local --dir ~/Projects
✓ Found 42 local projects

$ proj enrich --from-inventory
Found 42 projects with empty fields:
- 38 missing project_type
- 42 missing organization
- 40 missing classification

Options:
1. Infer from directory structure (uses config patterns)
2. Interactive mode (prompt for each)
3. Batch mode (apply same values to selection)
4. Skip

Choice [1]: 1

✓ Enriched 38 projects with project_type
✓ Enriched 42 projects with organization
✓ Enriched 40 projects with classification
```

---

### Thought 5: Registry as Enrichment Store

The local registry (`~/.local/share/proj/registry.json`) could store field overrides:

```json
{
  "projects": [
    {
      "path": "/Users/me/Projects/work/project-a",
      "template": "standard-project",
      "template_version": "0.7.0",
      "work_prod_id": 42,
      "enrichment": {
        "project_type": "Work",
        "organization": "my-company",
        "classification": "primary"
      }
    }
  ]
}
```

**Benefits:**
- Local storage for fields that may not be in API
- Survives API data loss
- Can be synced to API selectively

---

## 🔍 Key Questions

- [ ] **Q1: File-system implications** - Should metadata influence directory structure, or should directory structure influence metadata?
- [ ] **Q2: Config vs conventions** - Should we use explicit config patterns or implicit conventions (~/work = Work)?
- [ ] **Q3: Single source of truth** - Where should enriched data live? API? Registry? Both?
- [ ] **Q4: Enrichment timing** - When should enrichment happen? At creation? After scan? On-demand?
- [ ] **Q5: Bulk operations** - What's the best UX for updating many projects at once?
- [ ] **Q6: project_type gap** - Should we fix this first as a quick win before the larger feature?

---

## 🎨 Concept Sketches

### Concept A: "Opinionated Defaults"

Enforce a specific directory convention:

```
~/Projects/
├── work/       → project_type=Work
├── personal/   → project_type=Personal
├── learning/   → project_type=Learning
└── archive/    → classification=archive
```

**Pros:** Simple, consistent, no config needed  
**Cons:** Inflexible, assumes directory structure

---

### Concept B: "Config-First"

Everything driven by config patterns:

```yaml
path_patterns:
  "*/work/*": { project_type: "Work" }
  "*/personal/*": { project_type: "Personal" }
```

**Pros:** Flexible, user controls conventions  
**Cons:** More setup, config complexity

---

### Concept C: "Interactive Enrichment"

No assumptions - always prompt:

```bash
$ proj create my-project
# ... prompts for all fields ...
```

**Pros:** Explicit, user controls everything  
**Cons:** Tedious, many prompts

---

### Concept D: "Hybrid Approach"

Combine all approaches:

1. **Config patterns** - First priority
2. **Directory conventions** - Second priority (optional)
3. **Interactive prompts** - Fallback for missing fields
4. **Defaults** - Last resort

**Pros:** Flexible, progressive disclosure  
**Cons:** More complex implementation

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research [topic] --from-explore field-enrichment` to conduct research
3. After research, use `/decision [topic] --from-research` to make decisions

---

## 📝 Notes

### From Initial Discovery

- `project_type` is **completely missing** from create and update commands - this is a bug/gap
- The project-type-support feature only added filtering, not setting
- Inventory export hardcodes `status: "active"` - no way to change
- Registry already has `work_prod_id` linking - could extend with enrichment fields

### User's Key Insights

> "This is where configs, init, and initial project creation can really be helpful to set the stage for how projects' fields are populated later on"

> "Maybe we can think about if it's necessary to have project subdirectories of work/personal"

> "The metadata of these fields could have file-system implications, and I think this is where the 'enriching' truly shines"

---

**Last Updated:** 2026-01-09
