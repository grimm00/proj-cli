# Research: Local Registry

**Research Topic:** proj-cli Architecture
**Question:** How should proj-cli track locally created projects?
**Status:** ✅ Complete
**Created:** 2025-01-05
**Completed:** 2025-01-05

---

## 🎯 Research Question

What format and location should be used for a local registry of projects created from templates?

---

## 🔍 Research Goals

- [x] Goal 1: Determine registry file format
- [x] Goal 2: Define registry schema
- [x] Goal 3: Determine XDG-compliant location

---

## 📚 Research Methodology

**Sources:**

- [x] XDG Base Directory Specification: Standard paths
- [x] dev-infra research: Previous local registry research
- [x] Industry patterns: How other tools track projects

---

## 📊 Findings

### Finding 1: XDG Data Directory is Appropriate

Per XDG spec:
- Config (`~/.config/`) → User configuration files
- Data (`~/.local/share/`) → User data files

Registry is data, not configuration.

**Source:** XDG Base Directory Specification

**Relevance:** Registry should be in `~/.local/share/proj/`

---

### Finding 2: JSON Format for Simplicity

JSON is:
- Human-readable
- Easily parseable
- Compatible with jq for CLI manipulation
- Standard format used by many tools

**Source:** Industry patterns

**Relevance:** Use JSON for registry format.

---

### Finding 3: Required Registry Fields

Minimum fields needed:
- `id`: Unique identifier (UUID)
- `name`: Project directory name
- `path`: Absolute path to project
- `template`: Template used (standard-project, learning-project)
- `template_version`: dev-infra version when created
- `created_at`: Creation timestamp
- `work_prod_id`: Link to API record (nullable)

**Source:** dev-infra research, exploration discussion

**Relevance:** Schema must support all use cases.

---

## 🔍 Analysis

**Key Insights:**

- [x] Insight 1: Registry is separate from work-prod API data
- [x] Insight 2: work_prod_id links local and remote records when registered
- [x] Insight 3: Version field enables future sync feature

---

## 💡 Recommendations

- [x] **Recommendation 1:** Store registry at `~/.local/share/proj/registry.json`
- [x] **Recommendation 2:** Use JSON format with schema versioning
- [x] **Recommendation 3:** Include `work_prod_id` for API linkage
- [x] **Recommendation 4:** Include `template_version` for sync support

---

## 📋 Requirements Discovered

- [x] **FR-REG-1:** Registry must track all template-created projects
- [x] **FR-REG-2:** Registry must include project path
- [x] **FR-REG-3:** Registry must include template info and version
- [x] **FR-REG-4:** Registry must support linking to work-prod API records
- [x] **NFR-REG-1:** Registry must be human-readable (JSON)
- [x] **NFR-REG-2:** Registry must be XDG-compliant location

---

## 📝 Proposed Registry Schema

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "my-app",
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z",
      "work_prod_id": 42,
      "metadata": {
        "description": "My awesome application",
        "author": "me"
      }
    }
  ]
}
```

---

## 🚀 Next Steps

1. ✅ Registry design validated
2. 🔜 Implement registry read/write functions
3. 🔜 Integrate with `proj create` template mode

---

**Last Updated:** 2025-01-05

