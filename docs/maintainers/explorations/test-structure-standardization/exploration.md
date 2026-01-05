# Test Structure Standardization - Exploration

**Status:** 🔴 Exploration  
**Created:** 2025-01-05  
**Last Updated:** 2025-01-05

---

## 🎯 What Are We Exploring?

How to best organize the `tests/` directory for proj-cli, taking into account:

1. Current flat structure vs subdirectory approach
2. Consistency with sibling projects (dev-infra, work-prod)
3. Python/pytest best practices for CLI tools
4. pytest marker usage vs directory-based test separation
5. Scalability as the project grows

---

## 🤔 Why Explore This?

### Current Issues

1. **README/Reality Mismatch** - The `tests/README.md` describes a structure (unit/, integration/, e2e/, performance/) that doesn't exist
2. **Inconsistency** - Different from dev-infra (subdirectories) and work-prod (subdirectories)
3. **Commands Flattened Oddly** - Source has `commands/init.py` but test is `test_commands_init.py` instead of mirroring structure
4. **Mixed Concerns** - Unit and integration tests distinguished only by `_integration` suffix

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

- [ ] Question 1: What is the pytest best practice for CLI projects - flat or subdirectory structure?
- [ ] Question 2: How do other popular Python CLI tools (like Typer, Click examples) organize their tests?
- [ ] Question 3: Should tests mirror source structure (commands/ → commands/) or flatten?
- [ ] Question 4: What pytest configuration is needed to support subdirectory organization?
- [ ] Question 5: How to handle shared fixtures across unit and integration tests?
- [ ] Question 6: Should we add regression tests directory for proj-cli?
- [ ] Question 7: What is the migration path with minimal disruption?

---

## 🚀 Next Steps

1. Review research topics in `research-topics.md`
2. Use `/research test-structure-standardization --from-explore test-structure-standardization` to conduct research
3. After research, use `/decision test-structure-standardization --from-research` to make decisions

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

**Last Updated:** 2025-01-05

