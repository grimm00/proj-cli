# Code Structure Refactoring - Exploration

**Status:** ✅ Decision Made  
**Created:** 2025-01-05  
**Last Updated:** 2026-01-07

---

## 🎯 What Are We Exploring?

How to improve code organization in proj-cli:

**Part 1: Source Code**
- Split `projects.py` (943 lines, 14 functions) into focused modules
- Create `projects/` package with single-responsibility modules

**Part 2: Test Structure**
- Reorganize flat `tests/` directory (24 files, 4312 lines)
- Adopt subdirectory structure matching ecosystem

**Key Questions:**
1. Current flat structure vs subdirectory approach
2. Consistency with sibling projects (dev-infra, work-prod)
3. Python/pytest best practices for CLI tools
4. pytest marker usage vs directory-based test separation
5. Scalability as the project grows

---

## 🤔 Why Explore This?

### Current Issues

**Source Code:**
1. **Large Module** - `projects.py` at 943 lines with 4 different create modes
2. **Hard to Navigate** - 14 functions in one file
3. **Risk** - Changes have large blast radius

**Tests:**
1. **README/Reality Mismatch** - The `tests/README.md` describes a structure (unit/, integration/, e2e/, performance/) that doesn't exist
2. **Inconsistency** - Different from dev-infra (subdirectories) and work-prod (subdirectories)
3. **Commands Flattened Oddly** - Source has `commands/init.py` but test is `test_commands_init.py` instead of mirroring structure
4. **Mixed Concerns** - Unit and integration tests distinguished only by `_integration` suffix
5. **Scattered Create Tests** - 10 `test_create_*.py` files in root directory

### Benefits of Standardization

1. **Consistency** - Align with ecosystem patterns
2. **Navigation** - Easier to find tests by type
3. **Selective Running** - Run only unit tests, only integration tests, etc.
4. **Documentation Accuracy** - README matches reality
5. **Scalability** - Clear place for new tests as project grows

---

## 💡 Initial Thoughts

### Current Ecosystem Patterns

**dev-infra (Bash/BATS):**
```
tests/
├── helpers/        # Test utilities
├── unit/           # Individual function testing
├── integration/    # Multiple functions together
├── regression/     # Bug fix verification
├── smoke/          # End-to-end tests
└── fixtures/       # Test data
```

**work-prod (Python/pytest):**
```
tests/
├── conftest.py     # Shared fixtures
├── unit/
│   └── models/     # Mirrors source structure
├── integration/
│   └── api/        # API endpoint tests
└── performance/    # Performance tests
```

**proj-cli (Current):**
```
tests/
├── conftest.py
├── README.md       # Describes non-existent structure
├── test_api_client.py
├── test_api_client_integration.py
├── test_cli.py
├── test_cli_integration.py
├── test_commands_init.py
├── test_commands_inventory.py
├── test_commands_projects.py
├── test_config.py
├── test_config_integration.py
└── ... (14 files total)
```

### Possible Approaches

**Option A: Keep Flat, Fix README**
- Update README to describe actual structure
- Keep `_integration` suffix convention
- Use pytest markers (`@pytest.mark.integration`)
- Pros: Simple, works well for small project
- Cons: Doesn't match ecosystem, harder to scale

**Option B: Reorganize to Match Ecosystem**
```
tests/
├── conftest.py
├── README.md
├── unit/
│   ├── test_api_client.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_error_handler.py
│   ├── test_package.py
│   ├── test_registry.py
│   ├── test_templates.py
│   └── commands/
│       ├── test_init.py
│       ├── test_inventory.py
│       └── test_projects.py
└── integration/
    ├── test_api_client.py
    ├── test_cli.py
    └── test_config.py
```
- Pros: Matches ecosystem, clear separation, scales well
- Cons: Migration effort, file moves

**Option C: Hybrid - Subdirectories + Markers**
- Use subdirectories for organization
- Use pytest markers for selective running
- Best of both worlds

---

## 🔍 Key Questions

### Source Code
- [x] Q1: When is a module too large? → 943 lines with 14 functions is too large
- [x] Q2: How to split a commands module? → Convert to package with focused submodules
- [x] Q3: What's the right granularity? → By functionality: helpers, list, crud, create, import_export

### Test Structure
- [x] Q4: Flat vs subdirectory structure? → Subdirectory (matches ecosystem)
- [x] Q5: Should tests mirror source structure? → Partial (commands/ mirrors, create/ separate)
- [x] Q6: Markers vs directories? → Both (directories primary, markers for flexibility)
- [x] Q7: How to handle shared fixtures? → Keep root conftest.py, add subdirectory conftest.py as needed
- [x] Q8: Migration path? → Source first (PRs 1-4), then tests (PRs 5-6)

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research code-structure-refactoring --from-explore code-structure-refactoring` to conduct research
3. After research, use `/decision code-structure-refactoring --from-research` to make decisions

---

## 📝 Notes

### Observations from Current Tests

1. **Integration tests use markers** - `@pytest.mark.integration` is already in use
2. **Fixtures are centralized** - `conftest.py` has shared fixtures
3. **Clear separation pattern** - Unit tests check existence, integration tests hit real API
4. **~15 test files** - Small enough to reorganize without major effort

### Migration Considerations

1. Update import paths in test files
2. Update any CI/CD test commands
3. Update pytest.ini if it exists
4. May need multiple conftest.py files (one per subdirectory)

---

## ✅ Decision (2026-01-07)

**Decision:** Proceed with **Option B** (subdirectory reorganization) for tests, combined with source code refactoring.

### Rationale

1. **Ecosystem Consistency** - Both dev-infra and work-prod use subdirectories
2. **Scalability** - Clear place for new tests as project grows
3. **Navigation** - Easy to find tests by type or by source module
4. **Selective Running** - Can run `pytest tests/unit/` or `pytest tests/integration/`
5. **Source + Tests Together** - Refactoring source first creates clean boundaries for test organization

### Implementation

See **[implementation-plan.md](implementation-plan.md)** for:
- 6 PRs totaling ~4-5 hours
- Source refactor first (PRs 1-4)
- Test reorganization second (PRs 5-6)
- All tests pass after each PR

### Deferred Research

The following research topics can be addressed during or after implementation:
- Topic 3: pytest configuration details
- Topic 4: Marker vs directory trade-offs (using both)
- Topic 7: dev-infra template updates

---

**Last Updated:** 2026-01-07

