# Template Generation - Phase 3: Template Copying

**Phase:** 3 - Template Copying  
**Duration:** ~3 hours  
**Status:** 🔴 Scaffolding (needs expansion)  
**Prerequisites:** Phase 1 complete (templates.source in config)

---

## 📋 Overview

Port template copying logic from dev-infra's `new-project.sh` to Python. This includes project name validation, directory validation, template copying with hidden files, and placeholder replacement.

**Success Definition:** Can copy a template to target directory with proper validation, hidden files, and placeholder replacement.

---

## 🎯 Goals

1. **Create `templates.py` module** - New module for template operations
2. **Port name validation** - Validate project names (no spaces, valid chars)
3. **Port directory validation** - Check target exists and is writable
4. **Implement template copying** - Copy including hidden files (.gitignore, .cursor/)
5. **Implement placeholder replacement** - Replace placeholders in README.md, start.txt
6. **Provide clear error messages** - User-friendly errors for invalid inputs

---

## 📝 Tasks

> ⚠️ **Scaffolding:** Run `/transition-plan template-generation --expand --phase 3` to add detailed TDD tasks.

### Task Categories

- [ ] **Template Module** - Create `src/proj/templates.py` with core functions
- [ ] **Name Validation** - Validate project name format
- [ ] **Directory Validation** - Validate target directory
- [ ] **Template Discovery** - List available templates from source
- [ ] **Template Copying** - Copy template including hidden files
- [ ] **Placeholder Replacement** - Replace [PROJECT_NAME] etc. in files
- [ ] **Tests** - Comprehensive tests for all operations

---

## ✅ Completion Criteria

- [ ] Template module exists at `src/proj/templates.py`
- [ ] Name validation rejects spaces and invalid characters
- [ ] Directory validation checks existence and writability
- [ ] Can list available templates from source path
- [ ] Can copy template to target directory
- [ ] Hidden files (.gitignore, .cursor/) are copied
- [ ] Placeholders replaced in README.md and start.txt
- [ ] Clear error messages for invalid inputs
- [ ] Works offline (no network required)
- [ ] All tests pass

---

## 📦 Deliverables

- New `src/proj/templates.py` module
- New `tests/test_templates.py` test file
- Functions matching `new-project.sh` behavior

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-TMPL-1 | Local template source | 🔴 Pending |
| FR-TMPL-2 | Template validation | 🔴 Pending |
| FR-TMPL-3 | Template types (standard/learning) | 🔴 Pending |
| FR-PORT-1 | Name validation | 🔴 Pending |
| FR-PORT-2 | Directory validation | 🔴 Pending |
| FR-PORT-3 | Template copying with hidden files | 🔴 Pending |
| FR-PORT-4 | Placeholder replacement | 🔴 Pending |
| NFR-TMPL-1 | Offline operation | 🔴 Pending |
| NFR-TMPL-2 | Clear error messages | 🔴 Pending |
| NFR-PORT-1 | Name sanitization (optional) | 🔴 Pending |

---

## 📄 Reference: new-project.sh Logic

Key functions to port from `dev-infra/scripts/new-project.sh`:

```bash
# Name validation
validate_project_name() {
    if [[ ! "$1" =~ ^[a-zA-Z][a-zA-Z0-9_-]*$ ]]; then
        # Invalid name
    fi
}

# Template copying
copy_template() {
    cp -r "$TEMPLATE_DIR/$TYPE" "$TARGET_DIR/$NAME"
    # Include hidden files
}

# Placeholder replacement
customize_project() {
    sed -i '' "s/\[PROJECT_NAME\]/$NAME/g" README.md
    sed -i '' "s/\[PROJECT_NAME\]/$NAME/g" start.txt
}
```

**Placeholders to support:**
- `[PROJECT_NAME]` - Project name
- `[PROJECT_DESCRIPTION]` - Project description (optional)
- `[AUTHOR]` - Author name (optional)

---

## 🔗 Dependencies

### Prerequisites

- Phase 1 complete (templates.source in config)

### Blocks

- Phase 4 (template integration in create command)

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 2 - Local Registry](phase-2.md)
- [Next Phase: Phase 4 - Create Command Extension](phase-4.md)
- [new-project.sh](https://github.com/grimm00/dev-infra/blob/develop/scripts/new-project.sh)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** 🔴 Scaffolding  
**Next:** Expand with `/transition-plan template-generation --expand --phase 3`


