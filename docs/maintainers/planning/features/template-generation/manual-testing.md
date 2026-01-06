# Manual Testing Guide - Template Generation Extension

**Feature:** Template Generation Extension  
**Phases Covered:** 1-4  
**Last Updated:** 2026-01-06  
**Status:** ✅ Active

---

## 📋 Overview

This guide provides step-by-step instructions for manually verifying the Template Generation Extension feature.

**Purpose:**

- Verify user-facing CLI functionality works as expected
- Test all create modes (interactive, template, api-only, local-only, dry-run)
- Validate template copying and placeholder replacement
- Test registry integration and git initialization
- Verify error handling for edge cases

**Prerequisites:**

- `proj-cli` installed in development mode (`pip install -e .`)
- dev-infra templates available (configured in config or `~/Projects/dev-infra`)
- Terminal access
- Git installed (for git initialization tests)

---

## 🔧 Setup Verification

**Run these checks before testing to ensure environment is ready:**

```bash
# 1. Verify proj-cli installed and accessible
proj --version
# Expected: 0.1.0 or similar version number

# 2. Initialize proj configuration (first-time setup)
proj init
# This creates ~/.config/proj/config.yaml with:
# - API URL (default: http://localhost:5000)
# - GitHub username (for inventory scanning)
# - Local scan directories (default: ~/Projects)
# - Templates source (if configured)
#
# If config already exists, it will ask to overwrite.
# Use `proj init --force` to overwrite without prompt.

# 3. Verify proj create command exists
proj create --help | head -5
# Expected: Shows "Create a new project" help text

# 4. Verify templates location exists
ls ~/Projects/dev-infra/templates/
# Expected: standard-project/ learning-project/

# 5. Verify both template types exist
ls ~/Projects/dev-infra/templates/standard-project/
ls ~/Projects/dev-infra/templates/learning-project/
# Expected: Both directories have README.md and other files

# 6. Create clean test directory
rm -rf /tmp/proj-test && mkdir -p /tmp/proj-test
echo "Test directory ready: /tmp/proj-test"

# 7. Verify git is available (for git init tests)
git --version
# Expected: git version X.X.X
```

**If any check fails:**

- Check 1 fails: Run `pip install -e .` from proj-cli directory
- Check 2 fails: Run `proj init` to create initial config
- Check 3 fails: Verify installation, check PATH
- Check 4-5 fails: Clone dev-infra or update config with templates location
- Check 6 fails: Check filesystem permissions
- Check 7 fails: Install git

**Note:** `proj init` is required before using most proj commands. It creates the configuration file that stores API URL, templates location, and other settings.

---

## 🧪 Phase 1: Config Extension

### Scenario 1.1: View Config with Templates Section

**Objective:** Verify config shows templates section

**Steps:**

```bash
# Check config file location
ls ~/.config/proj/config.yaml

# Or verify config loads without error
python -c "from proj.config import Config; c = Config.load(); print('Config loaded successfully'); print(f'Templates source: {c.templates.source if hasattr(c, \"templates\") else \"default\"}')"
```

**Expected Result:** ✅ Config loads successfully with templates settings available

---

## 🧪 Phase 2: Local Registry

### Scenario 2.1: Registry File Creation

**Objective:** Verify registry file is created on first use

**Steps:**

```bash
# Check if registry file exists
ls ~/.local/share/proj/registry.json

# If not exists, it will be created on first project registration
```

**Expected Result:** ✅ Registry file exists or will be created when needed

---

## 🧪 Phase 3: Template Copying

### Scenario 3.1: Template Discovery

**Objective:** Verify templates can be discovered from source

**Steps:**

```bash
# Verify templates exist in dev-infra (or configured location)
ls ~/Projects/dev-infra/templates/
# Expected: standard-project/ learning-project/

# Check standard-project has key files
ls ~/Projects/dev-infra/templates/standard-project/
# Expected: README.md, .gitignore, docs/, backend/, frontend/, etc.

# Check learning-project has key files
ls ~/Projects/dev-infra/templates/learning-project/
# Expected: README.md, .gitignore, stage0-fundamentals/, etc.
```

**Expected Result:** ✅ Template directories are visible and accessible with expected structure

---

## 🧪 Phase 4: Create Command Extension

### Scenario 4.1: Help Output Shows New Flags

**Objective:** Verify `proj create --help` shows all new flags

**Steps:**

```bash
proj create --help
```

**Expected Output Should Include:**

- `--template`, `-t` - Template type option
- `--api-only` - API-only mode flag
- `--local-only` - Local-only mode flag
- `--target-dir` - Target directory option
- `--no-git` - Skip git initialization flag
- `--register/--no-register` - Registry option
- `--dry-run` - Dry-run preview flag
- `--desc`, `-d` - Description option

**Verification:**

```bash
# Check for specific flags
proj create --help | grep -E "(--template|--api-only|--local-only|--target-dir|--no-git|--register|--dry-run|--desc)"
# Should show all flags listed
```

**Expected Result:** ✅ All new flags appear in help output

---

### Scenario 4.2: Dry-Run Mode Preview

**Objective:** Verify dry-run shows preview without side effects

**Steps:**

```bash
# Ensure test directory is clean
rm -rf /tmp/proj-test && mkdir -p /tmp/proj-test

# Run dry-run command
proj create my-test-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --dry-run \
  --local-only
```

**Expected Output:**

```
🔍 Dry-run mode: Preview only

Would create project: my-test-app
Template: standard-project
Target directory: /tmp/proj-test/my-test-app
Git initialization: Yes
Registry: Yes

No changes made (dry-run mode)
```

**Verification:**

```bash
# Directory should NOT exist
ls /tmp/proj-test/my-test-app 2>&1
# Expected: "No such file or directory"

# Test directory should still be empty
ls /tmp/proj-test/
# Expected: empty (no output)
```

**Expected Result:** ✅ Preview shown, no directory created, no side effects

---

### Scenario 4.3: Template Mode - Create Project from Template

**Objective:** Verify template creation works end-to-end with correct file structure

**Prerequisites:**

- dev-infra templates available at configured location
- Target directory exists and is writable

**Steps:**

```bash
# Ensure test directory exists
mkdir -p /tmp/proj-test

# Create project from template (local-only to avoid API)
proj create my-template-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register
```

**Expected Output:**

```
✓ Initialized git repository
✓ Created project from template: /tmp/proj-test/my-template-app
```

**Verification:**

```bash
# 1. Check project directory was created
ls /tmp/proj-test/my-template-app/
# Expected: README.md, .gitignore, docs/, backend/, frontend/, etc.

# 2. Check README has placeholder replaced with project name
head -3 /tmp/proj-test/my-template-app/README.md
# Should show "my-template-app" NOT "[Project Name]" or "[PROJECT_NAME]"

# 3. Check .gitignore was copied (including hidden files)
ls -la /tmp/proj-test/my-template-app/.gitignore
# Should exist

# 4. Check git was initialized
ls /tmp/proj-test/my-template-app/.git/
# Should show: HEAD, config, objects/, refs/, etc.

# 5. Check docs directory structure exists
ls /tmp/proj-test/my-template-app/docs/
# Should have subdirectories from template
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/my-template-app
```

**Expected Result:** ✅ Project created with:

- All template files copied (including hidden files)
- Placeholders replaced with project name
- Git repository initialized
- Correct directory structure

---

### Scenario 4.4: Template Mode - Skip Git Initialization

**Objective:** Verify `--no-git` skips git initialization

**Steps:**

```bash
proj create no-git-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-git \
  --no-register
```

**Expected Output:**

```
✓ Created project from template: /tmp/proj-test/no-git-app
```

**Note:** Should NOT show "Initialized git repository" message.

**Verification:**

```bash
# Check git was NOT initialized
ls /tmp/proj-test/no-git-app/.git/ 2>&1
# Expected: "No such file or directory"

# Check project files exist (template was still copied)
ls /tmp/proj-test/no-git-app/README.md
# Should exist
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/no-git-app
```

**Expected Result:** ✅ Project created without .git directory

---

### Scenario 4.5: Template Mode - Registry Integration

**Objective:** Verify project is registered in local registry with correct data

**Steps:**

```bash
proj create registered-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --register
```

**Expected Output Should Include:**

```
✓ Initialized git repository
✓ Registered project in local registry
✓ Created project from template: /tmp/proj-test/registered-app
```

**Verification:**

```bash
# Check registry contains the project
cat ~/.local/share/proj/registry.json | python -m json.tool | grep -A 10 "registered-app"
```

**Expected Registry Entry Format:**

```json
{
  "path": "/tmp/proj-test/registered-app",
  "template": "standard-project",
  "template_version": "unknown",
  "created_at": "2026-01-06T10:30:00.000000"
}
```

**Key Fields to Verify:**

- `path` - Full path to created project
- `template` - Template type used
- `template_version` - Version (currently "unknown" - will be set from dev-infra in future)
- `created_at` - ISO timestamp of creation

**Cleanup:**

```bash
rm -rf /tmp/proj-test/registered-app
# Note: Registry entry will remain (can clean manually if needed)
```

**Expected Result:** ✅ Project registered in local registry with correct metadata

---

### Scenario 4.6: Local-Only Mode - No API Call

**Objective:** Verify local-only mode works without API connectivity

**Steps:**

```bash
# Ensure API is NOT running (or use a config with api_enabled=false)
# This test should succeed even without API

proj create offline-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register
```

**Expected Output:**

```
✓ Initialized git repository
✓ Created project from template: /tmp/proj-test/offline-app
```

**Verification:**

- Command should succeed even without API running
- No connection errors should appear
- No timeout errors should appear

```bash
# Verify project was created
ls /tmp/proj-test/offline-app/README.md
# Should exist
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/offline-app
```

**Expected Result:** ✅ Project created without API dependency

---

### Scenario 4.7: Local-Only Without Template Shows Error

**Objective:** Verify local-only mode requires template flag

**Steps:**

```bash
proj create error-app --local-only
```

**Expected Output:**

```
Error: --local-only mode requires --template flag
```

**Verification:**

```bash
# Check exit code (should be non-zero)
proj create error-app --local-only; echo "Exit code: $?"
# Expected: Exit code: 1
```

**Expected Result:** ✅ Clear error message, exit code 1

---

### Scenario 4.8: API-Only Mode (Backward Compatibility)

**Objective:** Verify api-only mode works (requires running API)

**Prerequisites:**

- work-prod API running at localhost:5000 (optional - skip if not available)

**Steps:**

```bash
# Only run if API is available
# Check API health first:
curl -s http://localhost:5000/api/health 2>/dev/null && echo "API available" || echo "API not available - skip this test"

# If API available:
proj create "API Test App" --api-only
```

**Expected Output (if API running):**

```
✓ Created project [id]: API Test App
```

**Expected Result:** ✅ Project created via API (or skip if API not available)

---

### Scenario 4.9: Interactive Mode - Complete Walkthrough

**Objective:** Verify interactive mode prompts for all options and creates project

**Steps:**

```bash
# Run create with --local-only but no name or template
proj create --local-only
```

**Interactive Prompts (provide these inputs):**

```
Project name: interactive-test-app
Template type [standard-project]: standard-project
Target directory [/Users/.../Projects]: /tmp/proj-test
Description (optional): Test project from interactive mode
```

**Expected Behavior:**

1. Prompts for "Project name" - Enter: `interactive-test-app`
2. Prompts for "Template type" with choices - Enter: `standard-project` (or press Enter for default)
3. Prompts for "Target directory" with default - Enter: `/tmp/proj-test`
4. Prompts for "Description (optional)" - Enter: `Test project from interactive mode` or press Enter to skip

**Expected Output After Inputs:**

```
✓ Initialized git repository
✓ Created project from template: /tmp/proj-test/interactive-test-app
```

**Verification:**

```bash
# Check project was created
ls /tmp/proj-test/interactive-test-app/
# Should show project files

# Check README has correct name
head -3 /tmp/proj-test/interactive-test-app/README.md
# Should show "interactive-test-app"
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/interactive-test-app
```

**Expected Result:** ✅ Interactive prompts appear, accept input, and create project correctly

---

### Scenario 4.10: Interactive Mode - Cancellation

**Objective:** Verify Ctrl+C cancels gracefully without traceback

**Steps:**

```bash
proj create --local-only
# When prompted for "Project name:", press Ctrl+C
```

**Expected Output:**

```
Project name: ^C
Cancelled
```

**Verification:**

- Should NOT show Python traceback
- Should NOT show "KeyboardInterrupt" exception
- Should show clean "Cancelled" message
- Exit code should be non-zero

```bash
proj create --local-only  # Then press Ctrl+C immediately
echo "Exit code: $?"
# Expected: Exit code: 1 (not 0)
```

**Expected Result:** ✅ Graceful cancellation, no traceback, clean exit

---

### Scenario 4.11: Learning Project Template

**Objective:** Verify learning-project template works (tests both template types)

**Steps:**

```bash
proj create my-learning-app \
  --template learning-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register
```

**Expected Output:**

```
✓ Initialized git repository
✓ Created project from template: /tmp/proj-test/my-learning-app
```

**Verification:**

```bash
# Check learning-project specific structure
ls /tmp/proj-test/my-learning-app/
# Expected: README.md, stage0-fundamentals/, practice-apps/, reference/, etc.

# Check README has placeholder replaced
head -3 /tmp/proj-test/my-learning-app/README.md
# Should show "my-learning-app" NOT "[Project Name]"

# Check stage directories exist
ls /tmp/proj-test/my-learning-app/stage0-fundamentals/
# Should have content from template
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/my-learning-app
```

**Expected Result:** ✅ Learning project template works with correct structure

---

### Scenario 4.12: Invalid Template Name Shows Error

**Objective:** Verify error handling for non-existent template

**Steps:**

```bash
proj create invalid-template-app \
  --template nonexistent-template \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register
```

**Expected Output:**

```
Error: Template 'nonexistent-template' not found
```

Or similar error message indicating template doesn't exist.

**Verification:**

```bash
# Check exit code
proj create invalid-app --template fake-template --target-dir /tmp/proj-test --local-only --no-register; echo "Exit code: $?"
# Expected: Exit code: 1

# Check no directory was created
ls /tmp/proj-test/invalid-template-app 2>&1
# Expected: "No such file or directory"
```

**Expected Result:** ✅ Clear error message, no partial project created, exit code 1

---

### Scenario 4.13: Project Already Exists - Conflict Handling

**Objective:** Verify error handling when target project directory already exists

**Steps:**

```bash
# First, create a project
proj create conflict-test-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register

# Then try to create same project again
proj create conflict-test-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register
```

**Expected Output (second run):**

```
Error: Target directory already exists: /tmp/proj-test/conflict-test-app
```

Or similar error indicating the directory already exists.

**Verification:**

- Original project should remain intact (not overwritten)
- Exit code should be non-zero

```bash
# Check original project still has original content
ls /tmp/proj-test/conflict-test-app/README.md
# Should still exist with original content
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/conflict-test-app
```

**Expected Result:** ✅ Clear error message, original project not modified, exit code 1

---

### Scenario 4.14: Description Option

**Objective:** Verify `--desc` flag works for setting project description

**Steps:**

```bash
proj create described-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --local-only \
  --no-register \
  --desc "My custom project description"
```

**Expected Output:**

```
✓ Initialized git repository
✓ Created project from template: /tmp/proj-test/described-app
```

**Verification:**

```bash
# Check if description appears in README or project files
# (depends on how description is used in template)
cat /tmp/proj-test/described-app/README.md | head -10
# May show description if template uses it

# Or check project was created successfully
ls /tmp/proj-test/described-app/
```

**Note:** Description handling depends on template implementation. The key test is that the flag is accepted and doesn't cause errors.

**Cleanup:**

```bash
rm -rf /tmp/proj-test/described-app
```

**Expected Result:** ✅ `--desc` flag accepted, project created successfully

---

## ✅ Acceptance Criteria Checklist

### Phase 1: Config Extension

- [ ] Scenario 1.1: Config loads with templates settings

### Phase 2: Local Registry

- [ ] Scenario 2.1: Registry file exists or created

### Phase 3: Template Copying

- [ ] Scenario 3.1: Templates discoverable with expected structure

### Phase 4: Create Command Extension

**Core Functionality:**

- [ ] Scenario 4.1: Help shows all new flags
- [ ] Scenario 4.2: Dry-run shows preview without side effects
- [ ] Scenario 4.3: Template mode creates project end-to-end
- [ ] Scenario 4.4: `--no-git` skips git initialization
- [ ] Scenario 4.5: Registry integration works with correct metadata
- [ ] Scenario 4.6: Local-only works without API

**Error Handling:**

- [ ] Scenario 4.7: Local-only without template shows error
- [ ] Scenario 4.12: Invalid template name shows error
- [ ] Scenario 4.13: Project already exists shows error

**Interactive Mode:**

- [ ] Scenario 4.9: Interactive mode prompts correctly and creates project
- [ ] Scenario 4.10: Ctrl+C cancels gracefully

**Additional Templates & Options:**

- [ ] Scenario 4.8: API-only mode works (if API available)
- [ ] Scenario 4.11: Learning project template works
- [ ] Scenario 4.14: Description option accepted

---

## 🧹 Cleanup After Testing

```bash
# Remove all test directories
rm -rf /tmp/proj-test

# Optionally clean registry entries (manual edit)
# Edit: ~/.local/share/proj/registry.json
# Remove entries with paths starting with "/tmp/proj-test"

# Or remove entire registry to start fresh (if desired)
# rm ~/.local/share/proj/registry.json
```

---

## 🐛 Troubleshooting

### Common Issues

**"proj: command not found"**

- Solution: Ensure proj-cli is installed (`pip install -e .`) and venv is activated

**"Template not found"**

- Solution: Check templates location in config or verify `~/Projects/dev-infra/templates/` exists

**"Permission denied"**

- Solution: Check write permissions on target directory

**"git: command not found"**

- Solution: Install git or use `--no-git` flag

**Interactive mode hangs**

- Solution: Ensure terminal supports input; try different terminal emulator

**Registry file permission error**

- Solution: Check permissions on `~/.local/share/proj/` directory

---

**Last Updated:** 2026-01-06
