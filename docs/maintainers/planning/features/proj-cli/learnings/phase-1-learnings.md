# proj-cli Learnings - Phase 1: Repository Setup

**Project:** proj-cli  
**Phase:** 1 - Repository Setup  
**Date:** 2025-12-17  
**Status:** ✅ Complete  
**Last Updated:** 2025-12-17

---

## 📋 Overview

Phase 1 established the proj-cli repository by adapting the dev-infra template for a CLI-only Python package. Key work included restructuring for `src/proj/` layout, setting up Typer + Pydantic, implementing XDG-compliant configuration, and establishing the test foundation.

---

## ✅ What Worked Exceptionally Well

### 1. dev-infra Template as Starting Point

**Why it worked:**
The dev-infra template provided a solid foundation with pre-configured docs structure, workflows, and maintainer documentation patterns.

**What made it successful:**
- Hub-and-spoke documentation pattern already established
- CI/CD workflows ready to adapt
- Cursor commands available for workflow automation

**Template implications:**
- dev-infra template works well even for CLI-only projects
- Removing unused directories (backend/, frontend/) was straightforward

**Benefits:**
- Saved hours of boilerplate setup
- Consistent documentation structure from day one
- GitHub Actions CI already configured

---

### 2. Typer + Pydantic Combination

**Why it worked:**
Typer provides modern CLI with type hints, Pydantic provides validated configuration - both use Python's type system consistently.

**What made it successful:**
- Typer's `no_args_is_help=True` provides good UX out of the box
- Pydantic Settings handles environment variable overrides automatically
- Rich output comes free with `typer[all]`

**Key examples:**

```python
# Typer app with version callback
app = typer.Typer(name="proj", no_args_is_help=True)

# Pydantic config with env prefix
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROJ_")
    api_url: str = Field(default="http://localhost:5000")
```

**Benefits:**
- Type-safe CLI and configuration
- Automatic `--help` generation
- Environment variable support without boilerplate

---

### 3. XDG Base Directory Compliance

**Why it worked:**
Using standard XDG paths (`~/.config/proj/`, `~/.local/share/proj/`) makes the tool portable and follows Unix conventions.

**What made it successful:**
- Simple helper functions (`get_config_dir()`, `get_data_dir()`)
- Environment variable overrides respected
- Easy to test with mocked XDG vars

**Template implications:**
- XDG compliance pattern should be standard for all CLI tools
- Helper functions are reusable

---

### 4. Sourcery Review Integration

**Why it worked:**
Running `dt-review` during PR validation caught real issues (coverage regex bug) and provided actionable feedback.

**What made it successful:**
- Priority matrix assessment helped triage 8 comments efficiently
- 2 HIGH items fixed immediately, 6 deferred appropriately
- Deferred issues documented in fix tracking

**Benefits:**
- Quality improvement without blocking progress
- Clear documentation of what to address later (Phase 4)

---

## 🟡 What Needs Improvement

### 1. Template Cleanup During Adaptation

**What the problem was:**
The dev-infra template includes full-app structure (backend/, frontend/) that needed manual removal for CLI-only project.

**Why it occurred:**
Template is designed for full-stack apps, not specialized for CLI tools.

**Impact:**
Minor - took ~10 minutes to remove unneeded directories and update docs.

**How to prevent:**
- Consider dev-infra template variants (full-app, cli-only, library)
- Or document "CLI-only adaptation" steps in template README

**Template changes needed:**
- Add CLI-only project variant or adaptation guide to dev-infra

---

### 2. Test Return Code Brittleness

**What the problem was:**
Test asserts `returncode == 2` for Typer's `no_args_is_help`, which is implementation-dependent.

**Why it occurred:**
Quick implementation without considering Typer version differences.

**Impact:**
Test may break with Typer updates (deferred to Phase 4).

**How to prevent:**
- Test behavior (help text shown) not implementation details (exit code)
- Use Typer's `CliRunner` for more robust testing

---

### 3. Documentation Placeholders from Template

**What the problem was:**
Template files had `{{CURRENT_DATE}}` placeholders and references to non-existent directories.

**Why it occurred:**
Template uses placeholders that should be replaced during `new-project.sh` but weren't fully processed.

**Impact:**
Required manual cleanup of docs/README.md and other template files.

**Template changes needed:**
- Ensure all placeholders are replaced by new-project.sh
- Or document manual cleanup steps clearly

---

## 💡 Unexpected Discoveries

### 1. Cursor Commands Transfer Easily

**Finding:**
The `.cursor/commands/` from dev-infra (via work-prod) transferred to proj-cli with minimal adaptation needed.

**Why it's valuable:**
Commands like `/pr`, `/pr-validation`, `/post-pr` work immediately in new projects.

**How to leverage:**
- Cursor commands should be part of dev-infra template
- Project-specific paths auto-detected by commands

---

### 2. Migration Reference Doc is Valuable

**Finding:**
Creating `migration-reference.md` to document work-prod's CLI structure proved very useful for planning Phase 2.

**Why it's valuable:**
- Captures source code patterns before migration
- Documents key differences (Click → Typer, INI → YAML)
- Serves as checklist for migration completeness

**How to leverage:**
- Consider adding "migration reference" as standard practice when splitting/migrating functionality between projects

---

## ⏱️ Time Investment Analysis

**Breakdown:**
- Repository restructuring: ~30 minutes
- Package setup (pyproject.toml, src/): ~20 minutes
- Typer CLI basic setup: ~15 minutes
- Pydantic configuration: ~30 minutes
- Tests: ~30 minutes
- Documentation cleanup: ~30 minutes
- PR validation + review: ~30 minutes
- Post-PR documentation: ~15 minutes

**Total:** ~3 hours (within 2-3 hour estimate)

**What took longer:**
- Documentation cleanup - template had more placeholders than expected

**What was faster:**
- Typer setup - simpler than expected, good defaults
- Tests - straightforward subprocess-based approach

**Estimation lessons:**
- Phase 1 estimates were accurate
- Include buffer for template cleanup when using dev-infra

---

## 📊 Metrics & Impact

**Code metrics:**
- Source files: 6 Python files in `src/proj/`
- Test files: 3 test files
- Lines of code: ~200 (excluding tests)
- Test coverage: 67%

**Quality metrics:**
- Tests: 13 passing
- Linter: Clean (flake8)
- Sourcery issues: 8 found, 2 fixed, 6 deferred

**Developer experience:**
- `proj --version` and `proj --help` work immediately
- Configuration via environment variables or YAML
- XDG-compliant paths

---

## 🎯 Actionable Items for dev-infra

Based on these learnings, potential improvements for dev-infra template:

1. **Add CLI-only variant or adaptation guide**
   - Document which directories to remove
   - Provide CLI-specific pyproject.toml example

2. **Improve placeholder processing**
   - Ensure `{{CURRENT_DATE}}` replaced everywhere
   - Validate all placeholder replacements

3. **Include XDG helpers as standard pattern**
   - Add to template's utility patterns
   - Document XDG compliance approach

4. **Add learnings/ directory to feature structure**
   - Make capturing learnings standard practice
   - Include learnings hub template

---

## 📚 Related

- [Phase 1 Document](../phase-1.md)
- [Migration Reference](../migration-reference.md)
- [PR #1 Sourcery Review](../../../feedback/sourcery/pr1.md)

---

**Last Updated:** 2025-12-17

