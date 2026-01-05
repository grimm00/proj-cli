# Template Generation - Phase 1: Config Extension

**Phase:** 1 - Config Extension  
**Duration:** ~2 hours  
**Status:** 🟠 In Progress  
**Last Updated:** 2025-01-05  
**Prerequisites:** proj-cli foundation complete (Phases 1-4)

---

## 📋 Overview

Extend the existing Pydantic configuration with new fields for template source, registry path, and API enablement toggle. This provides the foundation for subsequent phases.

**Success Definition:** Configuration supports all new fields with proper defaults and environment variable overrides.

---

## 🎯 Goals

1. **Add `api_enabled` boolean toggle** - Control whether API integration is active
2. **Add `TemplateConfig` nested model** - Configure template source and default type
3. **Add `RegistryConfig` nested model** - Configure registry location
4. **Add `default_project_dir` field** - Default location for new projects
5. **Update `proj init`** - Handle new configuration fields

---

## 📝 Tasks

### Task 1: Add `api_enabled` Field

**Purpose:** Allow users to toggle API integration on/off via config.

**TDD Flow:**

1. **RED - Write failing test:**
   - [x] Add test for `api_enabled` field existence
   - [x] Add test for default value (`True`)
   - [x] Add test for environment variable override (`PROJ_API_ENABLED`)
   - [x] Verify tests fail (no implementation yet)

   **Test code (`tests/test_config.py`):**
   ```python
   def test_config_has_api_enabled():
       """Test that config has api_enabled setting."""
       from proj.config import Config
       config = Config.load()
       assert hasattr(config, 'api_enabled')


   def test_config_api_enabled_default_true():
       """Test default api_enabled is True."""
       from proj.config import Config
       config = Config.load()
       assert config.api_enabled is True


   def test_config_api_enabled_env_override():
       """Test PROJ_API_ENABLED environment variable override."""
       with patch.dict(os.environ, {"PROJ_API_ENABLED": "false"}):
           from proj.config import Config
           config = Config.load()
           assert config.api_enabled is False
   ```

2. **GREEN - Implement minimum code:**
   - [x] Add `api_enabled` field to Config class
   - [x] Set default to `True`
   - [x] Run tests, verify they pass

   **Implementation (`src/proj/config.py`):**
   ```python
   # In Config class, add after api_url:
   api_enabled: bool = Field(
       default=True,
       description="Whether to use the work-prod API",
   )
   ```

3. **REFACTOR - Clean up:**
   - [x] Review field placement (group with other API settings)
   - [x] Ensure docstring is clear
   - [x] Verify tests still pass

**Checklist:**
- [x] Test written and failing
- [x] Implementation passes test
- [x] Code refactored and clean

---

### Task 2: Add `TemplateConfig` Nested Model

**Purpose:** Configure template source path and default template type.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Add test for `templates` nested attribute existence
   - [ ] Add test for `templates.source` field (defaults to `None`)
   - [ ] Add test for `templates.default` field (defaults to `"standard-project"`)
   - [ ] Add test for environment override (`PROJ_TEMPLATES__SOURCE`)
   - [ ] Verify tests fail

   **Test code (`tests/test_config.py`):**
   ```python
   def test_config_has_templates_nested():
       """Test that config has templates nested config."""
       from proj.config import Config
       config = Config.load()
       assert hasattr(config, 'templates')


   def test_config_templates_source_default_none():
       """Test templates.source defaults to None."""
       from proj.config import Config
       config = Config.load()
       assert config.templates.source is None


   def test_config_templates_default_value():
       """Test templates.default is standard-project."""
       from proj.config import Config
       config = Config.load()
       assert config.templates.default == "standard-project"


   def test_config_templates_source_env_override():
       """Test PROJ_TEMPLATES__SOURCE environment variable."""
       with patch.dict(os.environ, {"PROJ_TEMPLATES__SOURCE": "/path/to/templates"}):
           from proj.config import Config
           config = Config.load()
           assert str(config.templates.source) == "/path/to/templates"
   ```

2. **GREEN - Implement minimum code:**
   - [ ] Create `TemplateConfig` nested model class
   - [ ] Add `templates` field to Config class
   - [ ] Configure `env_nested_delimiter` in model_config for `__` separator
   - [ ] Run tests, verify they pass

   **Implementation (`src/proj/config.py`):**
   ```python
   from typing import Optional
   from pathlib import Path

   class TemplateConfig(BaseSettings):
       """Template-related configuration."""

       model_config = SettingsConfigDict(
           env_prefix="PROJ_TEMPLATES_",
           extra="ignore",
       )

       source: Optional[Path] = Field(
           default=None,
           description="Path to dev-infra templates directory",
       )
       default: str = Field(
           default="standard-project",
           description="Default template type",
       )


   class Config(BaseSettings):
       # ... existing fields ...

       model_config = SettingsConfigDict(
           env_prefix="PROJ_",
           env_file=".env",
           extra="ignore",
           env_nested_delimiter="__",  # ADD THIS for nested config
       )

       # Template Settings (NEW)
       templates: TemplateConfig = Field(default_factory=TemplateConfig)
   ```

3. **REFACTOR - Clean up:**
   - [ ] Group template settings logically
   - [ ] Add section comment
   - [ ] Verify tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 3: Add `RegistryConfig` Nested Model

**Purpose:** Configure local registry location (XDG-compliant by default).

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Add test for `registry` nested attribute existence
   - [ ] Add test for `registry.path` defaults to XDG data directory
   - [ ] Add test for environment override (`PROJ_REGISTRY__PATH`)
   - [ ] Verify tests fail

   **Test code (`tests/test_config.py`):**
   ```python
   def test_config_has_registry_nested():
       """Test that config has registry nested config."""
       from proj.config import Config
       config = Config.load()
       assert hasattr(config, 'registry')


   def test_config_registry_path_xdg_default():
       """Test registry.path defaults to XDG data dir."""
       from proj.config import Config, get_data_dir
       config = Config.load()
       expected = get_data_dir() / "registry.json"
       assert config.registry.path == expected


   def test_config_registry_path_env_override():
       """Test PROJ_REGISTRY__PATH environment variable."""
       with patch.dict(os.environ, {"PROJ_REGISTRY__PATH": "/custom/registry.json"}):
           from proj.config import Config
           config = Config.load()
           assert str(config.registry.path) == "/custom/registry.json"
   ```

2. **GREEN - Implement minimum code:**
   - [ ] Create `RegistryConfig` nested model class
   - [ ] Add `registry` field to Config class
   - [ ] Use `default_factory` for XDG path
   - [ ] Run tests, verify they pass

   **Implementation (`src/proj/config.py`):**
   ```python
   class RegistryConfig(BaseSettings):
       """Local registry configuration."""

       model_config = SettingsConfigDict(
           env_prefix="PROJ_REGISTRY_",
           extra="ignore",
       )

       path: Path = Field(
           default_factory=lambda: get_data_dir() / "registry.json",
           description="Path to local project registry",
       )


   class Config(BaseSettings):
       # ... existing fields ...

       # Registry Settings (NEW)
       registry: RegistryConfig = Field(default_factory=RegistryConfig)
   ```

3. **REFACTOR - Clean up:**
   - [ ] Group registry settings logically
   - [ ] Add section comment
   - [ ] Verify tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 4: Add `default_project_dir` Field

**Purpose:** Configure default location for new projects.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Add test for `default_project_dir` field existence
   - [ ] Add test for default value (`~/Projects`)
   - [ ] Add test for path expansion (~ expands to home)
   - [ ] Add test for environment override
   - [ ] Verify tests fail

   **Test code (`tests/test_config.py`):**
   ```python
   def test_config_has_default_project_dir():
       """Test that config has default_project_dir setting."""
       from proj.config import Config
       config = Config.load()
       assert hasattr(config, 'default_project_dir')


   def test_config_default_project_dir_value():
       """Test default_project_dir defaults to ~/Projects."""
       from proj.config import Config
       from pathlib import Path
       config = Config.load()
       expected = Path.home() / "Projects"
       assert config.default_project_dir == expected


   def test_config_default_project_dir_env_override():
       """Test PROJ_DEFAULT_PROJECT_DIR environment variable."""
       with patch.dict(os.environ, {"PROJ_DEFAULT_PROJECT_DIR": "/custom/projects"}):
           from proj.config import Config
           config = Config.load()
           assert str(config.default_project_dir) == "/custom/projects"
   ```

2. **GREEN - Implement minimum code:**
   - [ ] Add `default_project_dir` field to Config class
   - [ ] Use `default_factory` for `~/Projects` path
   - [ ] Run tests, verify they pass

   **Implementation (`src/proj/config.py`):**
   ```python
   class Config(BaseSettings):
       # ... existing fields ...

       # Default project location (NEW)
       default_project_dir: Path = Field(
           default_factory=lambda: Path.home() / "Projects",
           description="Default directory for new projects",
       )
   ```

3. **REFACTOR - Clean up:**
   - [ ] Group with other path settings
   - [ ] Ensure Path type handles expansion
   - [ ] Verify tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 5: Update YAML Serialization

**Purpose:** Ensure new fields serialize correctly to YAML config file.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Add test for saving config with new fields
   - [ ] Add test for loading config with nested fields from YAML
   - [ ] Verify tests fail

   **Test code (`tests/test_config.py`):**
   ```python
   def test_config_save_includes_new_fields(tmp_path, monkeypatch):
       """Test that save() includes new configuration fields."""
       # Use temp directory for config
       monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

       from proj.config import Config, get_config_file
       config = Config.load()
       config.save()

       config_file = get_config_file()
       with open(config_file) as f:
           saved = yaml.safe_load(f)

       assert 'api_enabled' in saved
       assert 'templates' in saved
       assert 'registry' in saved
       assert 'default_project_dir' in saved


   def test_config_load_nested_from_yaml(tmp_path, monkeypatch):
       """Test loading nested config from YAML file."""
       monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

       from proj.config import get_config_dir, get_config_file, Config
       
       # Create config directory and file
       config_dir = get_config_dir()
       config_dir.mkdir(parents=True, exist_ok=True)

       config_file = get_config_file()
       config_content = {
           'api_enabled': False,
           'templates': {
               'source': '/custom/templates',
               'default': 'learning-project'
           },
           'registry': {
               'path': '/custom/registry.json'
           },
           'default_project_dir': '/custom/projects'
       }
       with open(config_file, 'w') as f:
           yaml.dump(config_content, f)

       config = Config.load()
       assert config.api_enabled is False
       assert str(config.templates.source) == '/custom/templates'
       assert config.templates.default == 'learning-project'
   ```

2. **GREEN - Implement minimum code:**
   - [ ] Update `model_dump()` to handle nested models
   - [ ] Update `load()` to handle nested YAML structure
   - [ ] Run tests, verify they pass

   **Implementation notes:**
   - Pydantic's `model_dump()` should handle nested models automatically
   - May need to convert Path objects to strings for YAML
   - May need custom serialization for nested configs

3. **REFACTOR - Clean up:**
   - [ ] Extract common serialization logic if needed
   - [ ] Add comments for serialization handling
   - [ ] Verify tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

### Task 6: Update `proj init` Command

**Purpose:** Ensure `proj init` creates config with new fields.

**TDD Flow:**

1. **RED - Write failing test:**
   - [ ] Add test that `proj init` creates config with new fields
   - [ ] Verify tests fail

   **Test code (`tests/test_cli.py` or `tests/test_cli_integration.py`):**
   ```python
   def test_init_creates_config_with_new_fields(tmp_path, monkeypatch):
       """Test that proj init creates config with new fields."""
       monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))

       result = subprocess.run(
           [sys.executable, "-m", "proj", "init"],
           capture_output=True,
           text=True,
       )
       assert result.returncode == 0

       from proj.config import get_config_file
       config_file = get_config_file()
       assert config_file.exists()

       with open(config_file) as f:
           saved = yaml.safe_load(f)

       assert 'api_enabled' in saved
       assert 'templates' in saved
       assert 'registry' in saved
   ```

2. **GREEN - Implement minimum code:**
   - [ ] Update `proj init` to use new Config class
   - [ ] Ensure new fields are included in saved config
   - [ ] Run tests, verify they pass

   **Implementation notes:**
   - `proj init` already uses `Config.save()`, so new fields should be included automatically
   - May need to verify the command handles nested configs correctly

3. **REFACTOR - Clean up:**
   - [ ] Ensure output message mentions new config options
   - [ ] Verify tests still pass

**Checklist:**
- [ ] Test written and failing
- [ ] Implementation passes test
- [ ] Code refactored and clean

---

## 📊 Progress Tracking

| Task | Status | Notes |
|------|--------|-------|
| Task 1: api_enabled field | ✅ Complete | Tests and implementation complete |
| Task 2: TemplateConfig nested model | 🔴 Not Started | |
| Task 3: RegistryConfig nested model | 🔴 Not Started | |
| Task 4: default_project_dir field | 🔴 Not Started | |
| Task 5: YAML serialization | 🔴 Not Started | |
| Task 6: proj init update | 🔴 Not Started | |

---

## ✅ Completion Criteria

- [x] `api_enabled` field works with default `True`
- [ ] `templates.source` and `templates.default` fields accessible
- [ ] `registry.path` field defaults to XDG data directory
- [ ] `default_project_dir` defaults to `~/Projects`
- [ ] Environment variables override: `PROJ_API_ENABLED`, `PROJ_TEMPLATES__SOURCE`
- [ ] `proj init` creates valid config with new fields
- [ ] All tests pass

---

## 📦 Deliverables

- Updated `src/proj/config.py` with new configuration fields
- Tests in `tests/test_config.py` for new fields
- Updated `proj init` command

---

## 📊 Requirements Addressed

| Requirement | Description | Status |
|-------------|-------------|--------|
| FR-CONFIG-1 | api_enabled toggle | ✅ Complete |
| FR-CONFIG-2 | templates.source path | 🔴 Pending |
| FR-CONFIG-3 | registry.path setting | 🔴 Pending |
| FR-CONFIG-4 | Environment overrides | 🔴 Pending |
| NFR-CONFIG-1 | XDG registry location | 🔴 Pending |
| NFR-CONFIG-2 | YAML format maintained | 🔴 Pending |

---

## 🔗 Dependencies

### Prerequisites

- proj-cli foundation complete (existing `Config` class works)
- Pydantic settings framework in place

### Blocks

- Phase 2 (registry.path configuration)
- Phase 3 (templates.source configuration)
- Phase 4 (api_enabled toggle)

---

## 🧪 Testing Commands

```bash
# Run all config tests
pytest tests/test_config.py -v

# Run specific test
pytest tests/test_config.py::test_config_has_api_enabled -v

# Run with coverage
pytest tests/test_config.py --cov=proj.config --cov-report=term-missing
```

---

## 📝 Implementation Notes

### Pydantic Nested Config Pattern

```python
# Nested configs require env_nested_delimiter for env var support
class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="PROJ_",
        env_nested_delimiter="__",  # PROJ_TEMPLATES__SOURCE
    )

    templates: TemplateConfig = Field(default_factory=TemplateConfig)
```

### Path Handling

```python
# Pydantic automatically converts strings to Path objects
# For YAML serialization, convert Path to str:
def model_dump(self, **kwargs):
    data = super().model_dump(**kwargs)
    # Convert Path objects for YAML compatibility
    if data.get('default_project_dir'):
        data['default_project_dir'] = str(data['default_project_dir'])
    return data
```

### YAML Nested Structure

```yaml
# Expected config.yaml format:
api_url: http://localhost:5000
api_enabled: true
templates:
  source: ~/.dev-infra/templates
  default: standard-project
registry:
  path: ~/.local/share/proj/registry.json
default_project_dir: ~/Projects
```

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Transition Plan](transition-plan.md)
- [Next Phase: Phase 2 - Local Registry](phase-2.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)

---

**Last Updated:** 2025-01-05  
**Status:** ✅ Expanded  
**Next:** Begin implementation with Task 1

