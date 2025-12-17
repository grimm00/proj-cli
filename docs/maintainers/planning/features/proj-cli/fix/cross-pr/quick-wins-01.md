# Fix Plan: Cross-PR Quick Wins Batch

**Batch:** quick-wins-01  
**Priority:** 🟡 MEDIUM / 🟢 LOW  
**Effort:** 🟢 LOW  
**Status:** 🔴 Not Started  
**Created:** 2025-12-17  
**Source:** fix-review-report-2025-12-17.md  
**Issues:** 7 issues from 3 PRs

---

## Issues in This Batch

| Issue | PR | Priority | Impact | Effort | Description |
|-------|-----|----------|--------|--------|-------------|
| PR1-#1 | #1 | 🟡 MEDIUM | 🟢 LOW | 🟢 LOW | Add explicit encoding for config file |
| PR1-#3 | #1 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Fix brittle return code test |
| PR1-#7 | #1 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Add test for __version__ matching metadata |
| PR2-OC1 | #2 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | API URL validation in APIClient constructor |
| PR2-OC2 | #2 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Format option validation with typer.Choice |
| PR3-#3 | #3 | 🟡 MEDIUM | 🟡 MEDIUM | 🟢 LOW | Defensive JSON parsing for inventory.json |
| PR3-Overall | #3 | 🟢 LOW | 🟢 LOW | 🟢 LOW | Dedupe logic docs alignment |

---

## Overview

This batch contains 7 LOW effort issues from 3 PRs. These are quick wins that can be fixed in ~1-1.5 hours total.

**Estimated Time:** ~1-1.5 hours  
**Files Affected:**
- `src/proj/config.py`
- `src/proj/api_client.py`
- `src/proj/commands/inventory.py`
- `src/proj/commands/projects.py`
- `tests/test_cli.py`
- `tests/test_package.py`
- `docs/maintainers/planning/features/proj-cli/phase-3.md`

**Source PRs:**
- PR #1: Phase 1 - Repository Setup
- PR #2: Phase 2 - Migrate Project Commands
- PR #3: Phase 3 - Add Inventory Commands

---

## Issue Details

### Issue PR1-#1: Add explicit encoding for config file

**Source PR:** #1 - Phase 1: Repository Setup  
**Location:** `src/proj/config.py:74-75`  
**Sourcery Comment:** Comment #1  
**Priority:** 🟡 MEDIUM | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Using `config_file.open(encoding="utf-8")` avoids platform-dependent default encodings and makes the intended charset explicit.

**Current Code:**
```python
if config_file.exists():
    with open(config_file) as f:
        file_config = yaml.safe_load(f) or {}
```

**Proposed Solution:**
```python
if config_file.exists():
    with open(config_file, encoding="utf-8") as f:
        file_config = yaml.safe_load(f) or {}
```

Also update `save()` method to use explicit encoding:
```python
with open(config_file, "w", encoding="utf-8") as f:
    yaml.safe_dump(...)
```

---

### Issue PR1-#3: Fix brittle return code test

**Source PR:** #1 - Phase 1: Repository Setup  
**Location:** `tests/test_cli.py:36`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
With `no_args_is_help=True`, the conventional behavior is to print help with exit code 0, while 2 is typically for usage errors. Asserting a fixed code of 2 is brittle.

**Current Code:**
```python
# no_args_is_help=True means it shows help (Typer exits with code 2 but shows help)
assert result.returncode == 2  # Typer exits with 2 when no args provided
assert "Usage" in result.stdout or "usage" in result.stdout.lower()
```

**Proposed Solution:**
```python
# no_args_is_help=True shows help; exit code may vary by Typer version
assert result.returncode in (0, 2)  # Accept both codes
assert "Usage" in result.stdout or "usage" in result.stdout.lower()
```

---

### Issue PR1-#7: Add test for __version__ matching metadata

**Source PR:** #1 - Phase 1: Repository Setup  
**Location:** `tests/test_package.py:11-15`  
**Sourcery Comment:** Comment #7  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
Add a test that imports `proj.__version__` and asserts it equals `importlib.metadata.version("proj-cli")`.

**Current Code:**
```python
def test_package_has_version():
    """Test that package has version metadata."""
    version = importlib.metadata.version("proj-cli")
    assert version is not None
    assert len(version) > 0
```

**Proposed Solution:**
Add new test after existing version test:
```python
def test_version_matches_metadata():
    """Test that __version__ matches installed package metadata."""
    from proj import __version__
    metadata_version = importlib.metadata.version("proj-cli")
    assert __version__ == metadata_version
```

---

### Issue PR2-OC1: API URL validation in APIClient constructor

**Source PR:** #2 - Phase 2: Migrate Project Commands  
**Location:** `src/proj/api_client.py` (constructor)  
**Sourcery Comment:** Overall Comment  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
In `APIClient.__init__`, normalize/validate `Config.api_url` similarly to `_get_health_url` (handling `None`, whitespace, and missing scheme) so the client behaves predictably when the config is unset or malformed.

**Current Code:**
```python
def __init__(self, config: Config = None):
    self.config = config or Config.load()
    self.base_url = self.config.api_url.rstrip("/")
    ...
```

**Proposed Solution:**
```python
def __init__(self, config: Config = None):
    self.config = config or Config.load()
    self.base_url = self._normalize_url(self.config.api_url)
    ...

def _normalize_url(self, url: str) -> str:
    """Normalize API URL, handling None, whitespace, and missing scheme."""
    if not url or not url.strip():
        return 'http://localhost:5000'
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://localhost:5000'
    return url.rstrip('/')
```

---

### Issue PR2-OC2: Format option validation with typer.Choice

**Source PR:** #2 - Phase 2: Migrate Project Commands  
**Location:** `src/proj/commands/projects.py` (list_projects, get_project, search_projects)  
**Sourcery Comment:** Overall Comment  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
For project commands that take a `format` option, use `click.Choice(['table', 'json'])` to avoid silently ignoring unexpected values.

**Current Code:**
```python
format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
```

**Proposed Solution:**
```python
import click

format: str = typer.Option(
    "table", "--format", "-f", 
    help="Output format: table, json",
    click_type=click.Choice(["table", "json"], case_sensitive=False),
),
```

**Commands to update:**
- `list_projects`
- `get_project`
- `search_projects`

---

### Issue PR3-#3: Defensive JSON parsing for inventory.json

**Source PR:** #3 - Phase 3: Add Inventory Commands  
**Location:** `src/proj/commands/inventory.py:56-60`  
**Sourcery Comment:** Comment #3  
**Priority:** 🟡 MEDIUM | **Impact:** 🟡 MEDIUM | **Effort:** 🟢 LOW

**Description:**
If `inventory.json` is partially written or corrupted, `json.load` will raise and crash the CLI. Catch `json.JSONDecodeError` and treat it as an empty inventory with a warning.

**Current Code:**
```python
def load_inventory() -> list[dict]:
    """Load inventory from data file."""
    inv_file = get_inventory_file()
    if inv_file.exists():
        with open(inv_file, encoding="utf-8") as f:
            return json.load(f)
    return []
```

**Proposed Solution:**
```python
def load_inventory() -> list[dict]:
    """Load inventory from data file."""
    inv_file = get_inventory_file()
    if inv_file.exists():
        with open(inv_file, encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                console.print(
                    "[yellow]Warning: inventory.json is corrupted. "
                    "Starting with empty inventory.[/yellow]"
                )
                return []
    return []
```

---

### Issue PR3-Overall: Dedupe logic docs alignment

**Source PR:** #3 - Phase 3: Add Inventory Commands  
**Location:** `docs/maintainers/planning/features/proj-cli/phase-3.md`  
**Sourcery Comment:** Overall Comment  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟢 LOW

**Description:**
The dedupe logic only uses `remote_url` and `local_path` as keys, whereas the phase plan mentions `name+local_path` as a secondary key. Align the documentation with the implementation.

**Current Documentation (phase-3.md lines ~559-586):**
```markdown
# Dedupe by remote_url (primary) or name+local_path (secondary)
```

**Proposed Solution:**
Update documentation to reflect actual implementation:
```markdown
# Dedupe by remote_url (primary) or local_path (secondary)
# Note: name is not used as a key because it may not be unique
```

---

## Implementation Steps

### 1. PR1-#1: Explicit encoding
- [ ] Update `Config.load()` to use `encoding="utf-8"`
- [ ] Update `Config.save()` to use `encoding="utf-8"`
- [ ] Run tests to verify

### 2. PR1-#3: Brittle return code
- [ ] Update test to accept both exit codes 0 and 2
- [ ] Add comment explaining why

### 3. PR1-#7: Version metadata test
- [ ] Add `test_version_matches_metadata()` function
- [ ] Run test to verify

### 4. PR2-OC1: API URL validation
- [ ] Add `_normalize_url()` method to `APIClient`
- [ ] Update constructor to use it
- [ ] Add test for URL normalization

### 5. PR2-OC2: Format option validation
- [ ] Add `import click` to `projects.py`
- [ ] Update `list_projects` format option with `click.Choice`
- [ ] Update `get_project` format option with `click.Choice`
- [ ] Update `search_projects` format option with `click.Choice`

### 6. PR3-#3: Defensive JSON parsing
- [ ] Add try/except for `json.JSONDecodeError` in `load_inventory()`
- [ ] Add warning message output
- [ ] Run tests to verify

### 7. PR3-Overall: Docs alignment
- [ ] Update phase-3.md dedupe documentation
- [ ] Verify docs match implementation

---

## Testing

- [ ] All existing tests pass
- [ ] New tests added for:
  - [ ] Version metadata match
  - [ ] API URL normalization
- [ ] Manual testing completed:
  - [ ] `proj list --format invalid` shows error
  - [ ] Config loads with explicit encoding
  - [ ] Corrupted inventory.json shows warning
- [ ] No regressions introduced

---

## Files to Modify

| File | Changes |
|------|---------|
| `src/proj/config.py` | Add `encoding="utf-8"` to open calls |
| `src/proj/api_client.py` | Add `_normalize_url()` method |
| `src/proj/commands/projects.py` | Add `click.Choice` for format options |
| `src/proj/commands/inventory.py` | Add `json.JSONDecodeError` handling |
| `tests/test_cli.py` | Update return code assertion |
| `tests/test_package.py` | Add version metadata test |
| `docs/.../phase-3.md` | Update dedupe documentation |

---

## Definition of Done

- [ ] All 7 issues fixed
- [ ] All existing tests passing
- [ ] New tests added where applicable
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This batch was created from fix-review report recommendations. These issues are batched together because they:
- All have LOW effort (~10-15 minutes each)
- Are low-risk improvements
- Can be implemented independently
- Provide immediate value (better error handling, cross-platform safety)

---

**Last Updated:** 2025-12-17

