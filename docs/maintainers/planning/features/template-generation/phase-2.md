# Template Generation - Phase 2: Local Registry

**Phase:** 2 - Local Registry  
**Duration:** ~2 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** Phase 1 complete (registry.path in config)

---

## 📋 Overview

Create a local registry module to track template-created projects. The registry stores project metadata in a JSON file at the XDG-compliant location, enabling future sync features.

**Success Definition:** Can add, remove, and lookup projects in the registry with proper JSON persistence.

---

## 🎯 Goals

1. **Create `registry.py` module** - New module for registry operations
2. **Implement read/write functions** - Load and save registry JSON
3. **Implement project lookup** - Find projects by path or name
4. **Handle first-use creation** - Create registry file if it doesn't exist
5. **Support API linkage** - Store `work_prod_id` for linked projects

---

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan template-generation --expand --phase 2` to add detailed TDD tasks.

### Task Categories

- [ ] **Registry Module** - Create `src/proj/registry.py` with core functions
- [ ] **Data Model** - Define RegistryProject dataclass/model
- [ ] **CRUD Operations** - Add, update, remove, list projects
- [ ] **Lookup Functions** - Find by path, name, or work_prod_id
- [ ] **File Management** - Handle missing file, atomic writes
- [ ] **Tests** - Comprehensive tests for all operations

---

## ✅ Completion Criteria

- [ ] Registry module exists at `src/proj/registry.py`
- [ ] Can add project to registry
- [ ] Can remove project from registry
- [ ] Can lookup project by path
- [ ] Can lookup project by name
- [ ] Registry file is valid JSON and human-readable
- [ ] Registry created on first use at XDG data directory
- [ ] All tests pass

---

## 📦 Deliverables

- New `src/proj/registry.py` module
- New `tests/test_registry.py` test file
- Registry schema matching ADR-0008 specification

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-REG-1 | Project tracking | 🔴 Pending |
| FR-REG-2 | Project path storage | 🔴 Pending |
| FR-REG-3 | Template info (type, version) | 🔴 Pending |
| FR-REG-4 | API linkage (work_prod_id) | 🔴 Pending |
| NFR-REG-1 | Human-readable (JSON) | 🔴 Pending |
| NFR-REG-2 | XDG-compliant location | 🔴 Pending |

---

## 📄 Registry Schema (from ADR-0008)

```json
{
  "version": "1.0",
  "projects": [
    {
      "id": "uuid",
      "name": "my-app",
      "path": "/Users/me/Projects/my-app",
      "template": "standard-project",
      "template_version": "0.8.0",
      "created_at": "2025-01-05T10:30:00Z",
      "work_prod_id": 42,
      "metadata": {
        "description": "My awesome app",
        "author": "me"
      }
    }
  ]
}
```

---

## 🔗 Dependencies

### Prerequisites

- Phase 1 complete (registry.path in config)

### Blocks

- Phase 4 (registry integration in create command)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 1 - Config Extension](phase-1.md)
- [Next Phase: Phase 3 - Template Copying](phase-3.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan template-generation --expand --phase 2`


