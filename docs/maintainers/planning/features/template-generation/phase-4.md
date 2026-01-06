# Template Generation - Phase 4: Create Command Extension

**Phase:** 4 - Create Command Extension  
**Duration:** ~3-4 hours  
**Status:** 🟠 In Progress  
**Prerequisites:** Phase 2 (registry) and Phase 3 (templates) complete  
**Last Updated:** 2026-01-06

---

## 📋 Overview

Extend the existing `proj create` command with template modes, interactive prompts, and integration with the registry and templates modules. This is the user-facing integration phase that brings together all previous work.

**Success Definition:** `proj create` works in all modes (interactive, template, api-only, local-only) with proper backward compatibility. Created projects are registered in the local registry.

---

## 🎯 Goals

1. **Add `--template` flag** - Create project from specified template type
2. **Add `--api-only` flag** - Preserve current behavior (backward compat)
3. **Add `--local-only` flag** - Work without API connectivity
4. **Implement interactive mode** - Default behavior with prompts
5. **Integrate registry** - Register created projects automatically
6. **Integrate templates** - Use templates module for project creation
7. **Support git initialization** - Optional git init for new projects
8. **Add `--dry-run` flag** - Preview creation without side effects

---

## 📝 Tasks

### Task 1: Add Mode Detection Helper

**Purpose:** Determine which create mode to use based on flags and config.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [x] Add test for default mode (interactive when api_enabled=True)
   - [x] Add test for api-only mode detection
   - [x] Add test for local-only mode detection
   - [x] Add test for template mode detection
   - [x] Add test for mode conflicts (api-only + local-only should error)
   - [x] Verify tests fail (no implementation yet)

   **Test code (`tests/test_commands_projects.py`):**

   ```python
   import pytest
   from unittest.mock import MagicMock
   from proj.commands.projects import detect_create_mode

   def test_detect_mode_default_interactive():
       """Test default mode is interactive when no flags."""
       config = MagicMock()
       config.api_enabled = True
       mode = detect_create_mode(
           config=config,
           template=None,
           api_only=False,
           local_only=False,
       )
       assert mode == "interactive"

   def test_detect_mode_api_only():
       """Test api-only mode detection."""
       config = MagicMock()
       mode = detect_create_mode(
           config=config,
           template=None,
           api_only=True,
           local_only=False,
       )
       assert mode == "api-only"

   def test_detect_mode_local_only():
       """Test local-only mode detection."""
       config = MagicMock()
       mode = detect_create_mode(
           config=config,
           template=None,
           api_only=False,
           local_only=True,
       )
       assert mode == "local-only"

   def test_detect_mode_template():
       """Test template mode detection."""
       config = MagicMock()
       mode = detect_create_mode(
           config=config,
           template="standard-project",
           api_only=False,
           local_only=False,
       )
       assert mode == "template"

   def test_detect_mode_conflict_raises():
       """Test conflicting flags raise error."""
       config = MagicMock()
       with pytest.raises(ValueError) as exc:
           detect_create_mode(
               config=config,
               template=None,
               api_only=True,
               local_only=True,
           )
       assert "conflict" in str(exc.value).lower()
   ```

2. **GREEN - Implement minimum code:**

   - [x] Create `detect_create_mode()` function in `projects.py`
   - [x] Handle all mode combinations
   - [x] Raise error on conflicts
   - [x] Run tests, verify they pass

   **Implementation (`src/proj/commands/projects.py`):**

   ```python
   def detect_create_mode(
       config: Config,
       template: Optional[str],
       api_only: bool,
       local_only: bool,
   ) -> str:
       """Detect which create mode to use.

       Args:
           config: proj-cli configuration.
           template: Template type if specified.
           api_only: Force API-only mode.
           local_only: Force local-only mode.

       Returns:
           Mode string: "interactive", "api-only", "local-only", "template"

       Raises:
           ValueError: If conflicting flags provided.
       """
       if api_only and local_only:
           raise ValueError(
               "Cannot use --api-only and --local-only together (conflict)"
           )

       if api_only:
           return "api-only"
       if local_only:
           return "local-only"
       if template:
           return "template"

       # Default: interactive
       return "interactive"
   ```

3. **REFACTOR - Clean up:**
   - [x] Consider adding template + api_only combination
   - [x] Add docstring with all modes explained
   - [x] Run linting

**Checklist:**

- [x] Tests written and failing
- [x] Implementation passes tests
- [x] Code refactored and clean

---

### Task 2: Add New Command Flags

**Purpose:** Add `--template`, `--api-only`, `--local-only`, `--target-dir`, `--no-git`, `--register`, and `--dry-run` flags to create command.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [x] Add test for `--template` flag parsing
   - [x] Add test for `--api-only` flag parsing
   - [x] Add test for `--local-only` flag parsing
   - [x] Add test for `--target-dir` flag parsing
   - [x] Add test for `--no-git` flag parsing
   - [x] Add test for `--register` flag parsing
   - [x] Add test for `--dry-run` flag parsing
   - [x] Verify tests fail

   **Test code (`tests/test_cli_create_flags.py`):**

   ```python
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   def test_create_template_flag_recognized():
       """Test --template flag is recognized."""
       # Dry run to avoid side effects
       result = runner.invoke(app, [
           "create", "test-app",
           "--template", "standard-project",
           "--dry-run"
       ])
       # Should not fail with "unrecognized option"
       assert "unrecognized" not in result.output.lower()

   def test_create_api_only_flag_recognized():
       """Test --api-only flag is recognized."""
       result = runner.invoke(app, [
           "create", "test-app",
           "--api-only",
           "--dry-run"
       ])
       assert "unrecognized" not in result.output.lower()

   def test_create_local_only_flag_recognized():
       """Test --local-only flag is recognized."""
       result = runner.invoke(app, [
           "create", "test-app",
           "--local-only",
           "--dry-run"
       ])
       assert "unrecognized" not in result.output.lower()

   def test_create_target_dir_flag_recognized():
       """Test --target-dir flag is recognized."""
       result = runner.invoke(app, [
           "create", "test-app",
           "--template", "standard-project",
           "--target-dir", "/tmp",
           "--dry-run"
       ])
       assert "unrecognized" not in result.output.lower()

   def test_create_no_git_flag_recognized():
       """Test --no-git flag is recognized."""
       result = runner.invoke(app, [
           "create", "test-app",
           "--template", "standard-project",
           "--no-git",
           "--dry-run"
       ])
       assert "unrecognized" not in result.output.lower()
   ```

2. **GREEN - Implement minimum code:**

   - [x] Update `create_project` function signature with new flags
   - [x] Add all new Typer options
   - [x] Run tests, verify they pass

   **Implementation (`src/proj/commands/projects.py`):**

   ```python
   def create_project(
       name: Optional[str] = typer.Argument(
           None, help="Project name (required for non-interactive)"
       ),
       description: Optional[str] = typer.Option(
           None, "--desc", "-d", help="Description"
       ),
       status: str = typer.Option("active", "--status", "-s", help="Status"),
       organization: Optional[str] = typer.Option(
           None, "--org", "-o", help="Organization"
       ),
       classification: Optional[str] = typer.Option(
           None, "--class", "-c", help="Classification"
       ),
       path: Optional[str] = typer.Option(
           None, "--path", "-p", help="Local path (for API mode)"
       ),
       remote_url: Optional[str] = typer.Option(
           None, "--url", "-u", help="Remote URL"
       ),
       # New flags for template generation
       template: Optional[str] = typer.Option(
           None, "--template", "-t",
           help="Template type (e.g., standard-project, learning-project)"
       ),
       api_only: bool = typer.Option(
           False, "--api-only",
           help="Create in API only (original behavior)"
       ),
       local_only: bool = typer.Option(
           False, "--local-only",
           help="Create locally only (no API, requires --template)"
       ),
       target_dir: Optional[Path] = typer.Option(
           None, "--target-dir",
           help="Target directory for template (default: config.default_project_dir)"
       ),
       no_git: bool = typer.Option(
           False, "--no-git",
           help="Skip git initialization"
       ),
       register: bool = typer.Option(
           True, "--register/--no-register",
           help="Register project in local registry (default: True)"
       ),
       dry_run: bool = typer.Option(
           False, "--dry-run",
           help="Preview creation without side effects"
       ),
   ):
       """Create a new project.

       MODES:
       - Interactive (default): Prompts for all options
       - Template: Creates from dev-infra template
       - API-only: Original behavior (backward compatible)
       - Local-only: Template creation without API
       """
       # Implementation in later tasks...
   ```

3. **REFACTOR - Clean up:**
   - [x] Group related flags together
   - [x] Ensure help text is clear
   - [x] Run linting

**Checklist:**

- [x] Tests written and failing
- [x] Implementation passes tests
- [x] Code refactored and clean

---

### Task 3: Implement API-Only Mode

**Purpose:** Preserve backward compatibility with original `proj create` behavior.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for API-only mode creates via API
   - [ ] Add test for API-only mode does NOT create local directory
   - [ ] Add test for API-only mode does NOT register
   - [ ] Add test for API-only mode matches original behavior
   - [ ] Verify tests fail

   **Test code (`tests/test_create_api_only.py`):**

   ```python
   import pytest
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   @patch('proj.commands.projects.get_client')
   def test_create_api_only_calls_api(mock_get_client):
       """Test api-only mode creates project via API."""
       mock_client = MagicMock()
       mock_client.create_project.return_value = {"id": 1, "name": "Test"}
       mock_get_client.return_value = mock_client

       result = runner.invoke(app, [
           "create", "Test Project", "--api-only"
       ])

       assert result.exit_code == 0
       mock_client.create_project.assert_called_once()

   @patch('proj.commands.projects.get_client')
   def test_create_api_only_does_not_create_directory(mock_get_client, tmp_path):
       """Test api-only mode does NOT create local directory."""
       mock_client = MagicMock()
       mock_client.create_project.return_value = {"id": 1, "name": "test-app"}
       mock_get_client.return_value = mock_client

       result = runner.invoke(app, [
           "create", "test-app", "--api-only"
       ])

       # No local directory should be created
       assert not (tmp_path / "test-app").exists()

   @patch('proj.commands.projects.get_client')
   @patch('proj.registry.add_project')
   def test_create_api_only_does_not_register(
       mock_add_project, mock_get_client
   ):
       """Test api-only mode does NOT register locally."""
       mock_client = MagicMock()
       mock_client.create_project.return_value = {"id": 1, "name": "test-app"}
       mock_get_client.return_value = mock_client

       result = runner.invoke(app, [
           "create", "test-app", "--api-only"
       ])

       mock_add_project.assert_not_called()
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Add mode detection call in create_project
   - [ ] Implement API-only branch (existing behavior)
   - [ ] Run tests, verify they pass

3. **REFACTOR - Clean up:**
   - [ ] Extract API creation to helper function
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 4: Implement Template Mode

**Purpose:** Create project from template with optional API registration.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for template mode creates local directory
   - [ ] Add test for template mode copies template files
   - [ ] Add test for template mode replaces placeholders
   - [ ] Add test for template mode registers project
   - [ ] Add test for template mode with --no-register skips registry
   - [ ] Add test for template mode initializes git (default)
   - [ ] Add test for template mode with --no-git skips git
   - [ ] Verify tests fail

   **Test code (`tests/test_create_template.py`):**

   ```python
   import pytest
   from pathlib import Path
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   @pytest.fixture
   def mock_templates_source(tmp_path):
       """Create mock templates directory."""
       templates = tmp_path / "templates"
       templates.mkdir()
       standard = templates / "standard-project"
       standard.mkdir()
       (standard / "README.md").write_text("[Project Name]")
       (standard / "start.txt").write_text("[Project Name]")
       return templates

   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_template_creates_directory(
       mock_config_load, mock_get_source, mock_templates_source, tmp_path
   ):
       """Test template mode creates local directory."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = mock_templates_source

       target_dir = tmp_path / "projects"
       target_dir.mkdir()

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--target-dir", str(target_dir),
           "--local-only",
           "--no-register",
       ])

       assert result.exit_code == 0
       assert (target_dir / "my-app").exists()

   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_template_replaces_placeholders(
       mock_config_load, mock_get_source, mock_templates_source, tmp_path
   ):
       """Test template mode replaces placeholders."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = mock_templates_source

       target_dir = tmp_path / "projects"
       target_dir.mkdir()

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--target-dir", str(target_dir),
           "--local-only",
           "--no-register",
       ])

       readme = (target_dir / "my-app" / "README.md").read_text()
       assert "my-app" in readme
       assert "[Project Name]" not in readme

   @patch('proj.commands.projects.add_project')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_template_registers_project(
       mock_config_load, mock_get_source, mock_add_project,
       mock_templates_source, tmp_path
   ):
       """Test template mode registers project by default."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config.registry.path = tmp_path / "registry.json"
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = mock_templates_source

       target_dir = tmp_path / "projects"
       target_dir.mkdir()

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--target-dir", str(target_dir),
           "--local-only",
       ])

       mock_add_project.assert_called_once()
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Import templates module functions
   - [ ] Import registry module functions
   - [ ] Implement template mode branch
   - [ ] Call `create_from_template()`
   - [ ] Call `add_project()` to registry
   - [ ] Run tests, verify they pass

3. **REFACTOR - Clean up:**
   - [ ] Extract template creation to helper function
   - [ ] Handle errors gracefully
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 5: Implement Local-Only Mode

**Purpose:** Template creation without any API interaction.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for local-only mode requires template
   - [ ] Add test for local-only mode does NOT call API
   - [ ] Add test for local-only mode works when api_enabled=False
   - [ ] Add test for local-only mode registers locally
   - [ ] Verify tests fail

   **Test code (`tests/test_create_local_only.py`):**

   ```python
   import pytest
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   def test_create_local_only_requires_template():
       """Test local-only mode requires --template."""
       result = runner.invoke(app, [
           "create", "my-app",
           "--local-only",
           # No --template
       ])

       assert result.exit_code != 0
       assert "template" in result.output.lower()

   @patch('proj.commands.projects.get_client')
   @patch('proj.commands.projects.create_from_template')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_local_only_does_not_call_api(
       mock_config_load, mock_get_source, mock_create, mock_get_client, tmp_path
   ):
       """Test local-only mode does NOT call API."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = tmp_path / "templates"
       mock_create.return_value = tmp_path / "my-app"

       target = tmp_path / "projects"
       target.mkdir()

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--target-dir", str(target),
           "--local-only",
           "--no-register",
       ])

       mock_get_client.assert_not_called()
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Add validation: local-only requires template
   - [ ] Implement local-only branch
   - [ ] Skip API client initialization
   - [ ] Run tests, verify they pass

3. **REFACTOR - Clean up:**
   - [ ] Add clear error message for missing template
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 6: Implement Dry-Run Mode

**Purpose:** Preview what would be created without side effects.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for dry-run shows what would be created
   - [ ] Add test for dry-run does NOT create directory
   - [ ] Add test for dry-run does NOT call API
   - [ ] Add test for dry-run does NOT register
   - [ ] Verify tests fail

   **Test code (`tests/test_create_dry_run.py`):**

   ```python
   import pytest
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   @patch('proj.commands.projects.create_from_template')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_dry_run_shows_preview(
       mock_config_load, mock_get_source, mock_create, tmp_path
   ):
       """Test dry-run shows preview."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = tmp_path / "templates"

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--dry-run",
       ])

       assert "would create" in result.output.lower() or "preview" in result.output.lower()
       mock_create.assert_not_called()

   @patch('proj.commands.projects.get_client')
   def test_create_dry_run_api_shows_preview(mock_get_client):
       """Test dry-run with api-only shows preview."""
       result = runner.invoke(app, [
           "create", "Test App",
           "--api-only",
           "--dry-run",
       ])

       assert "would create" in result.output.lower() or "preview" in result.output.lower()
       mock_get_client.assert_not_called()
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Add dry-run check at start of create_project
   - [ ] Show preview output
   - [ ] Return early without side effects
   - [ ] Run tests, verify they pass

3. **REFACTOR - Clean up:**
   - [ ] Make preview output Rich-formatted
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 7: Implement Git Initialization

**Purpose:** Initialize git repository in created project.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for git init runs by default
   - [ ] Add test for --no-git skips git init
   - [ ] Add test for git init handles errors gracefully
   - [ ] Verify tests fail

   **Test code (`tests/test_create_git.py`):**

   ```python
   import pytest
   import subprocess
   from pathlib import Path
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   @patch('subprocess.run')
   @patch('proj.commands.projects.create_from_template')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_git_init_runs_by_default(
       mock_config_load, mock_get_source, mock_create, mock_subprocess,
       tmp_path
   ):
       """Test git init runs by default."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = tmp_path / "templates"
       mock_create.return_value = tmp_path / "my-app"
       mock_subprocess.return_value = MagicMock(returncode=0)

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--local-only",
           "--no-register",
       ])

       # git init should be called
       mock_subprocess.assert_called()
       call_args = mock_subprocess.call_args_list
       assert any("git" in str(c) and "init" in str(c) for c in call_args)

   @patch('subprocess.run')
   @patch('proj.commands.projects.create_from_template')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_no_git_skips_init(
       mock_config_load, mock_get_source, mock_create, mock_subprocess,
       tmp_path
   ):
       """Test --no-git skips git init."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = tmp_path / "templates"
       mock_create.return_value = tmp_path / "my-app"

       result = runner.invoke(app, [
           "create", "my-app",
           "--template", "standard-project",
           "--local-only",
           "--no-git",
           "--no-register",
       ])

       # git init should NOT be called
       if mock_subprocess.called:
           call_args = mock_subprocess.call_args_list
           assert not any("git" in str(c) and "init" in str(c) for c in call_args)
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Add `init_git()` helper function
   - [ ] Call `subprocess.run(["git", "init"])`
   - [ ] Skip if --no-git flag
   - [ ] Run tests, verify they pass

   **Implementation:**

   ```python
   def init_git(project_path: Path) -> bool:
       """Initialize git repository in project.

       Args:
           project_path: Path to project directory.

       Returns:
           True if successful, False otherwise.
       """
       try:
           result = subprocess.run(
               ["git", "init"],
               cwd=project_path,
               capture_output=True,
               text=True,
           )
           return result.returncode == 0
       except Exception:
           return False
   ```

3. **REFACTOR - Clean up:**
   - [ ] Add logging for git init result
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 8: Implement Interactive Mode

**Purpose:** Default mode with Rich prompts for all options.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add test for interactive mode prompts for project name
   - [ ] Add test for interactive mode prompts for template type
   - [ ] Add test for interactive mode prompts for target directory
   - [ ] Add test for interactive mode handles cancellation
   - [ ] Verify tests fail

   **Test code (`tests/test_create_interactive.py`):**

   ```python
   import pytest
   from unittest.mock import MagicMock, patch
   from typer.testing import CliRunner
   from proj.cli import app

   runner = CliRunner()

   @patch('proj.commands.projects.Prompt.ask')
   @patch('proj.commands.projects.create_from_template')
   @patch('proj.commands.projects.get_templates_source')
   @patch('proj.commands.projects.Config.load')
   def test_create_interactive_prompts_for_name(
       mock_config_load, mock_get_source, mock_create, mock_prompt, tmp_path
   ):
       """Test interactive mode prompts for project name."""
       mock_config = MagicMock()
       mock_config.default_project_dir = tmp_path
       mock_config.api_enabled = False
       mock_config.templates.default = "standard-project"
       mock_config_load.return_value = mock_config
       mock_get_source.return_value = tmp_path / "templates"
       mock_create.return_value = tmp_path / "my-app"

       # Simulate user input
       mock_prompt.side_effect = [
           "my-app",           # Project name
           "standard-project", # Template type
           str(tmp_path),      # Target directory
       ]

       result = runner.invoke(app, [
           "create",
           "--local-only",
           "--no-register",
       ])

       # Should have prompted for name
       assert mock_prompt.called
   ```

2. **GREEN - Implement minimum code:**

   - [ ] Import Rich Prompt
   - [ ] Add prompts when name is None
   - [ ] Add prompts for template selection
   - [ ] Add prompts for target directory
   - [ ] Run tests, verify they pass

   **Implementation:**

   ```python
   from rich.prompt import Prompt, Confirm

   def prompt_for_create_options(config: Config) -> dict:
       """Prompt user for create options interactively.

       Args:
           config: proj-cli configuration.

       Returns:
           Dict with user choices.
       """
       name = Prompt.ask("Project name")

       # List available templates
       templates_source = get_templates_source(config)
       available = list_templates(templates_source)
       template = Prompt.ask(
           "Template type",
           choices=available,
           default=config.templates.default,
       )

       target_dir = Prompt.ask(
           "Target directory",
           default=str(config.default_project_dir or Path.home() / "Projects"),
       )

       description = Prompt.ask("Description (optional)", default="")

       return {
           "name": name,
           "template": template,
           "target_dir": Path(target_dir),
           "description": description or None,
       }
   ```

3. **REFACTOR - Clean up:**
   - [ ] Add validation for prompts
   - [ ] Make prompts visually appealing
   - [ ] Run linting

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean

---

### Task 9: Integration Test - Full Workflow

**Purpose:** End-to-end test of all modes working together.

**TDD Flow:**

1. **RED - Write failing tests:**

   - [ ] Add integration test for template + register + git
   - [ ] Add integration test for api-only backward compatibility
   - [ ] Add integration test for local-only + template
   - [ ] Verify tests fail

2. **GREEN - Implement any remaining code:**

   - [ ] Wire together all components
   - [ ] Ensure error handling is complete
   - [ ] Run tests, verify they pass

3. **REFACTOR - Clean up:**
   - [ ] Review overall code organization
   - [ ] Extract common code to helpers
   - [ ] Run linting
   - [ ] Run full test suite

**Checklist:**

- [ ] Tests written and failing
- [ ] Implementation passes tests
- [ ] Code refactored and clean
- [ ] All modes working together

---

## ✅ Completion Criteria

- [ ] `proj create` (no args) launches interactive mode
- [ ] `proj create my-app --template standard-project` creates from template
- [ ] `proj create "My App" --api-only` works (backward compat)
- [ ] `proj create my-app --template standard-project --local-only` works without API
- [ ] `proj create my-app --template standard-project --dry-run` previews without creating
- [ ] Projects automatically registered in local registry (by default)
- [ ] Git initialized by default (--no-git to skip)
- [ ] All modes work correctly
- [ ] Backward compatibility verified
- [ ] All tests pass (target: >80% coverage)

---

## 📦 Deliverables

- Extended `src/proj/commands/projects.py` create command (~200+ lines added)
- New test files:
  - `tests/test_commands_projects.py` (mode detection)
  - `tests/test_cli_create_flags.py` (flag parsing)
  - `tests/test_create_api_only.py` (API-only mode)
  - `tests/test_create_template.py` (template mode)
  - `tests/test_create_local_only.py` (local-only mode)
  - `tests/test_create_dry_run.py` (dry-run mode)
  - `tests/test_create_git.py` (git integration)
  - `tests/test_create_interactive.py` (interactive mode)
- Updated `proj --help` documentation

---

## 📊 Requirements Addressed

| Requirement  | Description                | Status     |
| ------------ | -------------------------- | ---------- |
| FR-CREATE-1  | Interactive mode (default) | 🔴 Pending |
| FR-CREATE-2  | Template-based creation    | 🔴 Pending |
| FR-CREATE-3  | API-only mode              | 🔴 Pending |
| FR-CREATE-4  | Local-only mode            | 🔴 Pending |
| FR-PORT-5    | Git initialization         | 🔴 Pending |
| FR-PORT-6    | Interactive prompts        | 🔴 Pending |
| FR-PORT-7    | Non-interactive mode       | 🔴 Pending |
| NFR-CREATE-1 | Backward compatibility     | 🔴 Pending |

---

## 📄 Command Usage (from ADR-0008)

```bash
# Interactive mode (default) - prompts for all options
proj create

# Non-interactive with template
proj create my-app --template standard-project

# Full non-interactive (for CI/scripts)
proj create my-app \
  --template standard-project \
  --desc "My app" \
  --target-dir ~/Projects \
  --no-git \
  --register

# API-only mode (backward compatible)
proj create "My Application" --api-only

# Local-only mode (offline)
proj create my-app --template standard-project --local-only

# Dry-run to preview
proj create my-app --template standard-project --dry-run
```

---

## 🔗 Dependencies

### Prerequisites

- Phase 2 complete (registry module) ✅
- Phase 3 complete (templates module) ✅

### External Dependencies

- `rich` (prompts) - Already installed
- `subprocess` (git init) - Standard library

### Blocks

- Phase 5 (integration testing)

---

## 📊 Progress Tracking

| Task                          | Status         | Notes |
| ----------------------------- | -------------- | ----- |
| Task 1: Mode Detection Helper | 🔴 Not Started |       |
| Task 2: Command Flags         | 🔴 Not Started |       |
| Task 3: API-Only Mode         | 🔴 Not Started |       |
| Task 4: Template Mode         | 🔴 Not Started |       |
| Task 5: Local-Only Mode       | 🔴 Not Started |       |
| Task 6: Dry-Run Mode          | 🔴 Not Started |       |
| Task 7: Git Integration       | 🔴 Not Started |       |
| Task 8: Interactive Mode      | 🔴 Not Started |       |
| Task 9: Integration Tests     | 🔴 Not Started |       |

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Previous Phase: Phase 3 - Template Copying](phase-3.md)
- [Next Phase: Phase 5 - Testing & Polish](phase-5.md)
- [ADR-0008](../../decisions/ADR-0008-template-generation-extension.md)
- [Templates Module](../../../../src/proj/templates.py)
- [Registry Module](../../../../src/proj/registry.py)

---

**Last Updated:** 2026-01-05  
**Status:** 🔴 Expanded (Ready for implementation)  
**Next:** Begin implementation with `/task-phase 4 1`
