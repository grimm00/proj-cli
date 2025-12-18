# Dev-Infra Template Improvements

**Source:** proj-cli - All Phases (1, 3, 4) + Quick Wins 01  
**Target:** dev-infra template  
**Status:** ✅ Complete  
**Created:** 2025-12-17  
**Last Updated:** 2025-12-17

---

## 📋 Overview

This document consolidates all actionable improvements for the dev-infra template based on learnings from proj-cli development across 4 phases and 1 fix batch. Improvements are organized by category with clear actions, locations, and priorities.

**Total Items:** 33 improvements  
**Categories:** 6

---

## 🎯 Improvement Categories

### 1. CLI Patterns (8 items)

These improvements add CLI-specific patterns and documentation to the dev-infra template.

- [ ] **Add Typer + Pydantic pattern documentation**
  - **Location:** `docs/patterns/cli-patterns.md` (new file)
  - **Action:** Document Typer app setup with Pydantic configuration
  - **Prevents/Enables:** Faster CLI project setup with proven patterns
  - **Content/Example:**
    ```python
    app = typer.Typer(name="[tool]", no_args_is_help=True)
    
    class Config(BaseSettings):
        model_config = SettingsConfigDict(env_prefix="[TOOL]_")
    ```
  - **Expected Impact:** Consistent CLI patterns across projects
  - **Priority:** HIGH
  - **Effort:** LOW
  - **Source:** Phase 1

- [ ] **Document Typer nested subcommand pattern**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Add pattern for nested Typer command groups
  - **Prevents/Enables:** Clean hierarchical CLI structure
  - **Content/Example:**
    ```python
    inv_app = typer.Typer(name="inv", help="Inventory commands.")
    scan_app = typer.Typer(name="scan", help="Scan commands.")
    inv_app.add_typer(scan_app, name="scan")
    ```
  - **Expected Impact:** Intuitive command organization
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Document Rich Progress timing patterns**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Add pattern for correct message timing with Rich Progress
  - **Prevents/Enables:** Confusing progress output with messages appearing mid-spinner
  - **Content/Example:**
    ```python
    with Progress(...) as progress:
        # All progress updates here
        
    # After context exits, spinner is gone
    console.print("[green]✓ Complete[/green]")
    ```
  - **Expected Impact:** Better UX for long-running CLI operations
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Document click.Choice usage in Typer**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Explain Typer/Click relationship and click.Choice pattern
  - **Prevents/Enables:** Confusion when trying to use type constraints in Typer
  - **Content/Example:**
    ```python
    format: str = typer.Option(
        "table", "--format", "-f",
        click_type=click.Choice(["table", "json"], case_sensitive=False),
    )
    ```
  - **Expected Impact:** Enables validation patterns in Typer CLIs
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 3, Quick Wins 01

- [ ] **Document shared option patterns**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Pattern for consistent options across commands (`--wide`, `--format`)
  - **Prevents/Enables:** Inconsistent options between similar commands
  - **Content/Example:**
    ```python
    # Define shared options
    def wide_option():
        return typer.Option(False, "--wide", "-w", help="Show all columns")
    ```
  - **Expected Impact:** Consistent CLI UX
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Add conftest.py template with common fixtures**
  - **Location:** `templates/python/tests/conftest.py` (new file)
  - **Action:** Create template with XDG, temp dir, mock fixtures
  - **Prevents/Enables:** Test code duplication, inconsistent test setup
  - **Content/Example:**
    ```python
    @pytest.fixture
    def mock_xdg_dirs(temp_config_dir, temp_data_dir, monkeypatch):
        """Mock XDG directories to use temp dirs."""
        monkeypatch.setenv("XDG_CONFIG_HOME", str(temp_config_dir.parent.parent))
        monkeypatch.setenv("XDG_DATA_HOME", str(temp_data_dir.parent.parent))
        return {"config": temp_config_dir, "data": temp_data_dir}
    ```
  - **Expected Impact:** Faster test setup for new projects
  - **Priority:** HIGH
  - **Effort:** MEDIUM
  - **Source:** Phase 4

- [ ] **Document CliRunner testing patterns**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Add Typer CliRunner examples for fast CLI testing
  - **Prevents/Enables:** Slow subprocess-based tests
  - **Content/Example:**
    ```python
    from typer.testing import CliRunner
    runner = CliRunner()
    
    @patch("module.APIClient")
    def test_command(mock_client):
        result = runner.invoke(app, ["command"])
        assert result.exit_code == 0
    ```
  - **Expected Impact:** Faster, more reliable CLI tests
  - **Priority:** HIGH
  - **Effort:** LOW
  - **Source:** Phase 4

- [ ] **Include init command pattern**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Document first-run experience pattern with Rich
  - **Prevents/Enables:** Poor onboarding experience for CLI tools
  - **Content/Example:**
    ```python
    console.print(Panel.fit(
        "[bold green]Welcome to tool![/bold green]\n\n"
        "Let's set up your configuration.",
        title="🚀 tool-cli",
    ))
    ```
  - **Expected Impact:** Professional CLI onboarding
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 4

---

### 2. Test Patterns (6 items)

These improvements add testing patterns and fixtures for CLI projects.

- [ ] **Document behavior testing vs existence testing**
  - **Location:** `docs/patterns/test-patterns.md` (new file)
  - **Action:** Explain difference and when to use each
  - **Prevents/Enables:** Tests that check `--help` but not actual behavior
  - **Content/Example:**
    ```markdown
    ## Existence Testing
    Tests that command exists: `--help` returns 0
    Good for: TDD command structure, registration verification
    
    ## Behavior Testing
    Tests actual command behavior with mocked dependencies
    Good for: Regression protection, logic verification
    ```
  - **Expected Impact:** Better test coverage guidance
  - **Priority:** HIGH
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Add fixture patterns for filesystem testing**
  - **Location:** `docs/patterns/test-patterns.md`
  - **Action:** Document `tmp_path` and file system test fixtures
  - **Prevents/Enables:** Tests polluting real filesystem
  - **Content/Example:**
    ```python
    def test_scan_local(tmp_path):
        # Create test project structure
        (tmp_path / "project" / ".git").mkdir(parents=True)
        (tmp_path / "project" / "package.json").write_text('{}')
        # Test against tmp_path
    ```
  - **Expected Impact:** Reliable filesystem tests
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Add mocking patterns for external APIs**
  - **Location:** `docs/patterns/test-patterns.md`
  - **Action:** Document strategies for mocking API calls
  - **Prevents/Enables:** Tests depending on external services
  - **Content/Example:**
    ```python
    @patch("module.requests.get")
    def test_api_call(mock_get):
        mock_get.return_value.json.return_value = {"data": []}
        # Test API client
    ```
  - **Expected Impact:** Reliable, fast unit tests
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Document integration test exception handling**
  - **Location:** `docs/patterns/test-patterns.md`
  - **Action:** Warn against broad `except Exception` in integration tests
  - **Prevents/Enables:** Silent test failures when assertions are caught
  - **Content/Example:**
    ```python
    # BAD - hides assertion failures
    except Exception:
        pytest.skip("API unavailable")
    
    # GOOD - specific exceptions only
    except requests.ConnectionError:
        pytest.skip("API unavailable")
    ```
  - **Expected Impact:** More reliable test results
  - **Priority:** HIGH
  - **Effort:** LOW
  - **Source:** Phase 4

- [ ] **Document PackageNotFoundError handling**
  - **Location:** `docs/patterns/test-patterns.md`
  - **Action:** Pattern for handling metadata unavailability in dev
  - **Prevents/Enables:** Test failures in development environments
  - **Content/Example:**
    ```python
    try:
        version = importlib.metadata.version("package")
    except importlib.metadata.PackageNotFoundError:
        pytest.skip("Package not installed")
    ```
  - **Expected Impact:** Tests work in all environments
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 4

- [ ] **Document realistic coverage expectations**
  - **Location:** `docs/patterns/test-patterns.md`
  - **Action:** Set coverage targets by module type
  - **Prevents/Enables:** Unrealistic coverage goals causing frustration
  - **Content/Example:**
    ```markdown
    ## Coverage Expectations
    - Config/utils modules: 80%+
    - CLI commands: 50-70%
    - Integration code: 30-50%
    - Overall initial target: 30-40%
    ```
  - **Expected Impact:** Realistic planning, less frustration
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 4

---

### 3. Configuration (5 items)

These improvements add configuration patterns for CLI tools.

- [ ] **Include XDG helpers as standard pattern**
  - **Location:** `templates/python/src/[package]/config.py`
  - **Action:** Add XDG Base Directory helper functions
  - **Prevents/Enables:** Non-standard config file locations
  - **Content/Example:**
    ```python
    def get_xdg_config_home() -> Path:
        return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    
    def get_config_dir() -> Path:
        return get_xdg_config_home() / "tool"
    ```
  - **Expected Impact:** Unix-standard CLI tools
  - **Priority:** HIGH
  - **Effort:** LOW
  - **Source:** Phase 1

- [ ] **Document Pydantic Settings precedence**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Explain env var vs file vs kwarg precedence
  - **Prevents/Enables:** Confusing configuration behavior
  - **Content/Example:**
    ```markdown
    ## Pydantic Settings Precedence
    1. Keyword arguments (highest)
    2. Environment variables
    3. Config file values
    4. Defaults (lowest)
    
    Note: Config.load() passes file values as kwargs
    ```
  - **Expected Impact:** Clear config loading behavior
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 4

- [ ] **Add local cache pattern for remote APIs**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Document local JSON cache → sync to API pattern
  - **Prevents/Enables:** CLI tools requiring constant connectivity
  - **Content/Example:**
    ```markdown
    ## Local Cache Pattern
    1. Store data locally in XDG data dir
    2. Work offline with local data
    3. Sync to remote API when ready
    
    Example: ~/.local/share/tool/data.json
    ```
  - **Expected Impact:** Better offline CLI experience
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Document GitHub API pagination**
  - **Location:** `docs/patterns/api-patterns.md` (new file)
  - **Action:** Document Link header pagination for GitHub API
  - **Prevents/Enables:** Incomplete data fetching from paginated APIs
  - **Content/Example:**
    ```python
    while url:
        response = requests.get(url, headers=headers, params=params)
        data.extend(response.json())
        url = response.links.get("next", {}).get("url")
        params = {}  # Clear for subsequent requests
    ```
  - **Expected Impact:** Correct API pagination handling
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 3

- [ ] **Document project identification patterns**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Pattern for identifying projects vs subdirectories
  - **Prevents/Enables:** False positives from subdirectory scanning
  - **Content/Example:**
    ```python
    # Check if inside existing git repo
    for parent in root.parents:
        if (parent / ".git").exists():
            # This is a subdirectory, not a separate project
            break
    ```
  - **Expected Impact:** Accurate project scanning
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 3

---

### 4. Fix Workflow (5 items)

These improvements enhance the fix management workflow.

- [ ] **Add cross-PR directory pattern**
  - **Location:** `docs/workflows/fix-workflow.md`
  - **Action:** Document `fix/cross-pr/` directory for batched fixes
  - **Prevents/Enables:** Confusion about where cross-PR fixes go
  - **Content/Example:**
    ```
    fix/
    ├── cross-pr/
    │   ├── README.md          # Cross-PR batches hub
    │   └── quick-wins-01.md   # Batch plan
    ├── pr1/
    └── pr2/
    ```
  - **Expected Impact:** Clear fix organization
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Quick Wins 01

- [ ] **Document batch-based fix planning**
  - **Location:** `docs/workflows/fix-workflow.md`
  - **Action:** Add guidance on grouping fixes by effort level
  - **Prevents/Enables:** Inefficient one-fix-per-PR approach
  - **Content/Example:**
    ```markdown
    ## Batching Strategy
    - Quick Wins: All LOW effort, <2 hours total
    - Medium Batch: MEDIUM effort, related changes
    - Complex Fix: Single HIGH/CRITICAL issue
    ```
  - **Expected Impact:** More efficient fix management
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Quick Wins 01

- [ ] **Add fix-specific manual testing guidance**
  - **Location:** `docs/workflows/manual-testing.md`
  - **Action:** Document adding fix verification scenarios
  - **Prevents/Enables:** Fixes not being verified
  - **Content/Example:**
    ```markdown
    ## Fix Verification (FX.N)
    For each fix batch, add scenarios:
    - FX.1: Verify fix works as expected
    - FX.2: Verify edge cases don't regress
    ```
  - **Expected Impact:** Better fix verification
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Quick Wins 01

- [ ] **Update fix statistics guidance**
  - **Location:** `docs/workflows/fix-workflow.md`
  - **Action:** Add when/how to update fix statistics
  - **Prevents/Enables:** Inconsistent or stale statistics
  - **Content/Example:**
    ```markdown
    ## Statistics Updates
    Update fix/README.md statistics:
    - After fixing issues (increment resolved)
    - After deferring issues (increment deferred)
    - At end of each PR cycle
    ```
  - **Expected Impact:** Accurate tracking
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Quick Wins 01

- [ ] **Document iterative improvement expectation**
  - **Location:** `docs/workflows/fix-workflow.md`
  - **Action:** Set expectation that fix PRs generate new issues
  - **Prevents/Enables:** Surprise when Sourcery finds issues in fix PRs
  - **Content/Example:**
    ```markdown
    ## Iterative Improvement
    Expect fix PRs to generate new Sourcery issues.
    This is normal - each improvement reveals more opportunities.
    Plan for deferred issues to grow during fix batches.
    ```
  - **Expected Impact:** Realistic expectations
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Quick Wins 01

---

### 5. Documentation (5 items)

These improvements enhance documentation patterns.

- [ ] **Add learnings/ directory to feature structure**
  - **Location:** `templates/docs/features/[feature]/learnings/README.md`
  - **Action:** Include learnings hub in feature template
  - **Prevents/Enables:** Learnings being forgotten or unorganized
  - **Content/Example:**
    ```
    features/[feature]/
    ├── learnings/
    │   ├── README.md          # Learnings hub
    │   └── phase-N-learnings.md
    ```
  - **Expected Impact:** Standard learnings capture
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 1

- [ ] **Add improvements/ directory to feature structure**
  - **Location:** `templates/docs/features/[feature]/improvements/README.md`
  - **Action:** Include improvements hub in feature template
  - **Prevents/Enables:** Actionable items being lost in learnings
  - **Content/Example:**
    ```
    features/[feature]/
    ├── improvements/
    │   ├── README.md          # Improvements hub
    │   └── [target]-improvements.md
    ```
  - **Expected Impact:** Actionable improvement tracking
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** This document

- [ ] **Improve placeholder processing**
  - **Location:** `scripts/new-project.sh`
  - **Action:** Ensure all placeholders replaced, validate after
  - **Prevents/Enables:** `{{CURRENT_DATE}}` appearing in generated docs
  - **Content/Example:**
    ```bash
    # Validate no placeholders remain
    if grep -r '{{' "$PROJECT_DIR"; then
        echo "Warning: Unreplaced placeholders found"
    fi
    ```
  - **Expected Impact:** Cleaner project generation
  - **Priority:** LOW
  - **Effort:** MEDIUM
  - **Source:** Phase 1

- [ ] **Document documentation overhead estimate**
  - **Location:** `docs/workflows/planning.md`
  - **Action:** Add guidance on documentation time
  - **Prevents/Enables:** Underestimating time for docs updates
  - **Content/Example:**
    ```markdown
    ## Documentation Overhead
    Plan for ~30% overhead for documentation:
    - Phase docs: 15% of phase time
    - Fix docs: 30% of fix time
    - Learnings: 10-15 min per phase
    ```
  - **Expected Impact:** Better time estimates
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Quick Wins 01

- [ ] **Add migration reference pattern**
  - **Location:** `docs/patterns/migration-patterns.md` (new file)
  - **Action:** Document creating migration-reference.md when moving code
  - **Prevents/Enables:** Lost context during code migration
  - **Content/Example:**
    ```markdown
    ## Migration Reference
    When migrating functionality between projects:
    1. Create migration-reference.md
    2. Document source structure
    3. Map source → target patterns
    4. Track migration completeness
    ```
  - **Expected Impact:** Smoother code migrations
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 1

---

### 6. Template Structure (4 items)

These improvements modify the template's project structure.

- [ ] **Add CLI-only variant or adaptation guide**
  - **Location:** `docs/guides/cli-adaptation.md` (new file)
  - **Action:** Document which directories to remove for CLI-only projects
  - **Prevents/Enables:** Confusion when adapting template for CLI tools
  - **Content/Example:**
    ```markdown
    ## CLI-Only Adaptation
    Remove these directories:
    - backend/
    - frontend/
    
    Update these files:
    - README.md (remove web app references)
    - .github/workflows/ (simplify to Python-only)
    ```
  - **Expected Impact:** Faster CLI project setup
  - **Priority:** HIGH
  - **Effort:** MEDIUM
  - **Source:** Phase 1

- [ ] **Add CLI-specific pyproject.toml example**
  - **Location:** `templates/python/pyproject.cli.toml`
  - **Action:** Create CLI-focused pyproject.toml template
  - **Prevents/Enables:** Incorrect package setup for CLIs
  - **Content/Example:**
    ```toml
    [project.scripts]
    tool = "package.cli:app"
    
    [tool.setuptools.packages.find]
    where = ["src"]
    ```
  - **Expected Impact:** Correct CLI package configuration
  - **Priority:** MEDIUM
  - **Effort:** LOW
  - **Source:** Phase 1

- [ ] **Include Cursor commands in template**
  - **Location:** `.cursor/commands/` (copy from work-prod or standardize)
  - **Action:** Make Cursor commands part of dev-infra template
  - **Prevents/Enables:** Manual command copying between projects
  - **Content/Example:**
    ```
    .cursor/commands/
    ├── pr.md
    ├── pr-validation.md
    ├── post-pr.md
    ├── task-phase.md
    └── ... (other workflow commands)
    ```
  - **Expected Impact:** Consistent workflow across projects
  - **Priority:** HIGH
  - **Effort:** MEDIUM
  - **Source:** Phase 1

- [ ] **Add status emoji pattern**
  - **Location:** `docs/patterns/cli-patterns.md`
  - **Action:** Document status emoji as shared constant pattern
  - **Prevents/Enables:** Emoji duplication across commands
  - **Content/Example:**
    ```python
    # In cli/common.py
    STATUS_EMOJI = {
        "active": "🟢",
        "inactive": "⚪",
        "archived": "📦",
        "completed": "✅",
    }
    ```
  - **Expected Impact:** Consistent, maintainable status display
  - **Priority:** LOW
  - **Effort:** LOW
  - **Source:** Phase 4

---

## 📊 Priority Summary

| Priority | Count | Est. Effort |
|----------|-------|-------------|
| HIGH | 7 | ~4 hrs |
| MEDIUM | 14 | ~5 hrs |
| LOW | 12 | ~3 hrs |
| **Total** | **33** | **~12 hrs** |

---

## 🎯 Recommended Implementation Order

### Quick Wins (Day 1: ~2-3 hrs)

These can be done quickly with immediate value:

1. CLI Patterns Documentation (create `docs/patterns/cli-patterns.md`)
   - Typer + Pydantic pattern
   - click.Choice usage
   - CliRunner testing
   - XDG helpers

2. Test Patterns Documentation (create `docs/patterns/test-patterns.md`)
   - Behavior vs existence testing
   - Integration test exception handling

### Phase 2 (Day 2: ~3-4 hrs)

Foundation improvements:

3. Add conftest.py template
4. CLI-only adaptation guide
5. Include Cursor commands in template
6. Add learnings/ and improvements/ to feature structure

### Phase 3 (Day 3: ~4-5 hrs)

Complete documentation:

7. Remaining CLI patterns
8. Fix workflow improvements
9. Migration patterns
10. Remaining test patterns

---

## 📚 References

**Source Documents:**
- [Phase 1 Learnings](../learnings/phase-1-learnings.md)
- [Phase 3 Learnings](../learnings/phase-3-learnings.md)
- [Phase 4 Learnings](../learnings/phase-4-learnings.md)
- [Quick Wins 01 Learnings](../learnings/quick-wins-01-learnings.md)

---

**Last Updated:** 2025-12-17

