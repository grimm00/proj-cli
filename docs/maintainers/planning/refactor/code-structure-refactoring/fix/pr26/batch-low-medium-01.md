# Fix Plan: PR #26 Batch LOW MEDIUM - Batch 01

**PR:** #26  
**Batch:** low-medium-01  
**Priority:** 🟢 LOW  
**Effort:** 🟡 MEDIUM  
**Status:** ✅ Complete  
**Created:** 2026-01-08  
**Completed:** 2026-01-08  
**PR:** Pending  
**Issues:** 1 issue

---

## Issues in This Batch

| Issue | Priority | Impact | Effort | Description |
|-------|----------|--------|--------|-------------|
| PR26-Overall-#2 | 🟢 LOW | 🟢 LOW | 🟡 MEDIUM | Parametrize command-existence tests |

---

## Overview

This batch contains 1 LOW priority issue with MEDIUM effort. The issue addresses code repetition in command-existence tests that use nearly identical `subprocess.run([... '--help'])` patterns across multiple files.

**Estimated Time:** ~1-2 hours  
**Files Affected:**
- `tests/unit/test_cli.py` (likely)
- `tests/commands/test_init.py` (likely)
- `tests/commands/test_inventory.py` (likely)
- Other test files with command-existence tests

---

## Issue Details

### Issue PR26-Overall-#2: Parametrize Command-Existence Tests

**Location:** Multiple test files  
**Sourcery Comment:** Overall Comment #2  
**Priority:** 🟢 LOW | **Impact:** 🟢 LOW | **Effort:** 🟡 MEDIUM

**Description:**
Many command-existence tests rely on nearly identical `subprocess.run([... '--help'])` patterns across multiple files. This creates repetition and makes adding new commands require copying boilerplate to multiple places.

**Current Pattern (repeated in multiple files):**
```python
def test_proj_list_exists():
    """Test that proj list --help works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "list", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "list" in result.stdout.lower()

def test_proj_get_exists():
    """Test that proj get --help works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "get", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "get" in result.stdout.lower()
```

**Proposed Solution:**
Use pytest parametrization to reduce repetition:
```python
import pytest

COMMANDS = [
    ("list", ["list"]),
    ("get", ["get"]),
    ("create", ["create"]),
    ("update", ["update"]),
    ("delete", ["delete"]),
    ("archive", ["archive"]),
    ("inv", ["inv"]),
    # Add more commands as needed
]

@pytest.mark.parametrize("command_name,args", COMMANDS)
def test_command_exists(command_name, args):
    """Test that command --help works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj"] + args + ["--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Command {command_name} --help failed"
    assert command_name in result.stdout.lower(), f"Command name not in help output"
```

**Alternative: Helper Function**
```python
def assert_command_exists(args: list[str], command_name: str):
    """Helper to verify a command exists and shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "proj"] + args + ["--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Command {command_name} --help failed"
    assert command_name in result.stdout.lower()

def test_proj_list_exists():
    assert_command_exists(["list"], "list")

def test_proj_get_exists():
    assert_command_exists(["get"], "get")
```

---

## Implementation Steps

1. **Issue PR26-Overall-#2**
   - [ ] Identify all files with command-existence tests
   - [ ] Determine best approach (parametrization vs helper function)
   - [ ] Create shared test utility (in conftest.py or test helper)
   - [ ] Refactor existing tests to use new pattern
   - [ ] Verify all tests still pass
   - [ ] Update any test documentation

---

## Testing

- [ ] All existing tests pass
- [ ] Command-existence tests still cover all commands
- [ ] New parametrized approach works correctly
- [ ] No regressions introduced

---

## Files to Modify

- `tests/conftest.py` - Add helper function or fixture (if using helper approach)
- `tests/unit/test_cli.py` - Refactor command-existence tests
- `tests/commands/test_*.py` - Refactor if command tests exist
- Other test files with similar patterns

---

## Definition of Done

- [x] Command-existence tests use consistent pattern (helper function)
- [x] Repetition reduced across test files (16 tests refactored, ~72 lines removed)
- [x] Easy to add new commands (just call assert_command_exists())
- [x] All 238+ tests passing (4 pre-existing failures unrelated)
- [ ] Code reviewed
- [ ] Ready for PR

---

**Batch Rationale:**
This issue is in its own batch because:
- MEDIUM effort requires focused attention
- Affects multiple files across the test suite
- Code style/DRY improvement (not functionality)
- Can be deferred to a dedicated cleanup PR

---

**Last Updated:** 2026-01-08
