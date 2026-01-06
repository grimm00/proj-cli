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

**Prerequisites:**

- `proj-cli` installed in development mode (`pip install -e .`)
- dev-infra templates available (configured in config or `~/Projects/dev-infra`)
- Terminal access

---

## 🧪 Phase 1: Config Extension

### Scenario 1.1: View Config with Templates Section

**Objective:** Verify config shows templates section

**Steps:**

1. Run config command (if available) or check config file

```bash
# Check config file location
ls ~/.config/proj/config.yaml

# Or verify config loads without error
python -c "from proj.config import Config; c = Config.load(); print(c)"
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
```

**Expected Result:** ✅ Template directories are visible and accessible

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

**Expected Result:** ✅ All new flags appear in help output

---

### Scenario 4.2: Dry-Run Mode Preview

**Objective:** Verify dry-run shows preview without side effects

**Steps:**

```bash
# Create a test directory
mkdir -p /tmp/proj-test

# Run dry-run command
proj create my-test-app \
  --template standard-project \
  --target-dir /tmp/proj-test \
  --dry-run \
  --local-only

# Verify no directory was created
ls /tmp/proj-test/
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
ls /tmp/proj-test/my-test-app
# Expected: No such file or directory
```

**Expected Result:** ✅ Preview shown, no directory created

---

### Scenario 4.3: Template Mode - Create Project from Template

**Objective:** Verify template creation works end-to-end

**Prerequisites:** 

- dev-infra templates available at configured location
- Target directory exists and is writable

**Steps:**

```bash
# Create target directory
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
# Check project was created
ls /tmp/proj-test/my-template-app/

# Check README has placeholder replaced
head -5 /tmp/proj-test/my-template-app/README.md
# Should show "my-template-app" not "[Project Name]"

# Check git was initialized
ls /tmp/proj-test/my-template-app/.git/
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/my-template-app
```

**Expected Result:** ✅ Project created with placeholders replaced, git initialized

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

**Verification:**

```bash
# Check git was NOT initialized
ls /tmp/proj-test/no-git-app/.git/
# Expected: No such file or directory
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/no-git-app
```

**Expected Result:** ✅ Project created without .git directory

---

### Scenario 4.5: Template Mode - Registry Integration

**Objective:** Verify project is registered in local registry

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
✓ Registered project in local registry
```

**Verification:**

```bash
# Check registry contains the project
cat ~/.local/share/proj/registry.json | grep registered-app
```

**Cleanup:**

```bash
rm -rf /tmp/proj-test/registered-app
# Note: Registry entry will remain (can clean manually if needed)
```

**Expected Result:** ✅ Project registered in local registry

---

### Scenario 4.6: Local-Only Mode - No API Call

**Objective:** Verify local-only mode works without API connectivity

**Steps:**

```bash
# Ensure API is NOT running (or use a config with api_enabled=false)

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

**Cleanup:**

```bash
rm -rf /tmp/proj-test/offline-app
```

**Expected Result:** ✅ Project created without API dependency

---

### Scenario 4.7: Local-Only Without Template Shows Error

**Objective:** Verify local-only mode requires template

**Steps:**

```bash
proj create error-app \
  --local-only
```

**Expected Output:**

```
Error: --local-only mode requires --template flag
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
proj create "API Test App" --api-only
```

**Expected Output (if API running):**

```
✓ Created project [id]: API Test App
```

**Expected Result:** ✅ Project created via API (or skip if API not available)

---

### Scenario 4.9: Interactive Mode (Default)

**Objective:** Verify interactive mode prompts for all options

**Steps:**

```bash
# Run create without arguments
proj create --local-only
```

**Expected Behavior:**

1. Prompts for "Project name"
2. Prompts for "Template type" (with choices)
3. Prompts for "Target directory" (with default)
4. Prompts for "Description (optional)"
5. Creates project based on inputs

**Expected Result:** ✅ Interactive prompts appear and work correctly

---

### Scenario 4.10: Interactive Mode - Cancellation

**Objective:** Verify Ctrl+C cancels gracefully

**Steps:**

```bash
proj create --local-only
# When prompted, press Ctrl+C
```

**Expected Output:**

```
Project name: ^C
Cancelled
```

**Expected Result:** ✅ Graceful cancellation, no traceback

---

## ✅ Acceptance Criteria Checklist

### Phase 1: Config Extension

- [ ] Scenario 1.1: Config loads with templates settings

### Phase 2: Local Registry

- [ ] Scenario 2.1: Registry file exists or created

### Phase 3: Template Copying

- [ ] Scenario 3.1: Templates discoverable

### Phase 4: Create Command Extension

- [ ] Scenario 4.1: Help shows all new flags
- [ ] Scenario 4.2: Dry-run shows preview without side effects
- [ ] Scenario 4.3: Template mode creates project end-to-end
- [ ] Scenario 4.4: `--no-git` skips git initialization
- [ ] Scenario 4.5: Registry integration works
- [ ] Scenario 4.6: Local-only works without API
- [ ] Scenario 4.7: Local-only without template shows error
- [ ] Scenario 4.8: API-only mode works (if API available)
- [ ] Scenario 4.9: Interactive mode prompts correctly
- [ ] Scenario 4.10: Ctrl+C cancels gracefully

---

## 🧹 Cleanup After Testing

```bash
# Remove all test directories
rm -rf /tmp/proj-test

# Optionally clean registry entries (manual edit)
# ~/.local/share/proj/registry.json
```

---

**Last Updated:** 2026-01-06

