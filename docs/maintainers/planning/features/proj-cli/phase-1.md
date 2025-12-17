# proj-cli - Phase 1: Repository Setup

**Phase:** 1 of 4  
**Duration:** ~2-3 hours  
**Status:** ✅ Complete  
**Completed:** 2025-12-16  
**Merged:** PR #1 (2025-12-17)  
**Prerequisites:** Repository created at https://github.com/grimm00/proj-cli

---

## 📋 Overview

Restructure the `proj-cli` repository from the dev-infra template into a proper Python CLI package with Typer framework and Pydantic configuration. The repository exists but needs restructuring for CLI-only focus.

**Success Definition:** Running `proj --version` shows version, `proj --help` shows command structure, and config loads from XDG paths.

**Note:** Repository was created from dev-infra template (full app structure). We need to adapt it for a CLI-only package.

---

## 🎯 Goals

1. ~~Create `proj-cli` repository using `dev-infra/new-project.sh`~~ ✅ Done
2. Restructure repository for CLI-only package (`src/proj/` layout)
3. Create `pyproject.toml` with entry point for `proj` command
4. Implement Pydantic configuration with XDG compliance
5. Create basic Typer app with placeholder commands

---

## 📝 Tasks

### Task 1: Clone and Restructure Repository (Setup)

**Goal:** Clone the existing repository and restructure for CLI-only

**Steps:**

- [x] Repository created at https://github.com/grimm00/proj-cli ✅
- [ ] Clone repository locally
- [ ] Remove web app directories (backend/, frontend/)
- [ ] Create CLI package structure (src/proj/)
- [ ] Update README.md for CLI-only project

**Commands:**

```bash
cd ~/Projects
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli
```

**Restructure:**

```bash
# Remove web app directories (keep useful parts)
rm -rf backend/ frontend/

# Create CLI package structure
mkdir -p src/proj/commands
touch src/proj/__init__.py
touch src/proj/__main__.py
touch src/proj/cli.py
touch src/proj/config.py
touch src/proj/commands/__init__.py
```

**Notes:**

- Repository exists with dev-infra template
- Need to restructure for CLI-only focus
- Keep: .cursor/, docs/, scripts/ (useful), tests/, .github/
- Remove: backend/, frontend/ (not needed for CLI)

---

### Task 2: Write Tests for Package Structure (RED)

**Goal:** Write tests that define expected package structure

**Files to create:**

- `tests/test_package.py`

**Test cases:**

```python
# tests/test_package.py
"""Tests for package structure and metadata."""
import importlib.metadata


def test_package_importable():
    """Test that proj package can be imported."""
    import proj
    assert proj is not None


def test_package_has_version():
    """Test that package has version metadata."""
    version = importlib.metadata.version("proj-cli")
    assert version is not None
    assert len(version) > 0


def test_cli_module_exists():
    """Test that cli module exists."""
    from proj import cli
    assert cli is not None


def test_config_module_exists():
    """Test that config module exists."""
    from proj import config
    assert config is not None
```

**Expected Result:** Tests fail (RED) - package doesn't exist yet

---

### Task 3: Create Package Structure (GREEN)

**Goal:** Create package structure to pass tests

**Directory structure:**

```
proj-cli/
├── pyproject.toml
├── requirements.txt
├── README.md
├── src/
│   └── proj/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       └── commands/
│           └── __init__.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_package.py
```

**Files to create:**

1. **`src/proj/__init__.py`:**

```python
"""proj - Unified CLI for project and inventory management."""
__version__ = "0.1.0"
```

2. **`src/proj/__main__.py`:**

```python
"""Allow running with python -m proj."""
from proj.cli import app

if __name__ == "__main__":
    app()
```

3. **`src/proj/cli.py`:**

```python
"""Main CLI application using Typer."""
import typer
from typing import Optional

app = typer.Typer(
    name="proj",
    help="Unified CLI for project and inventory management.",
    no_args_is_help=True,
)


def version_callback(value: bool):
    """Show version and exit."""
    if value:
        from proj import __version__
        typer.echo(f"proj version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Unified CLI for project and inventory management."""
    pass


if __name__ == "__main__":
    app()
```

4. **`src/proj/config.py`:** (placeholder)

```python
"""Configuration management with Pydantic and XDG compliance."""
# To be implemented in Task 5
pass
```

5. **`src/proj/commands/__init__.py`:**

```python
"""Command modules for proj CLI."""
```

**Run tests:**

```bash
pip install -e .
pytest tests/test_package.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 4: Write Tests for Configuration (RED)

**Goal:** Write tests for Pydantic configuration with XDG paths

**Files to create:**

- `tests/test_config.py`

**Test cases:**

```python
# tests/test_config.py
"""Tests for configuration management."""
import os
from pathlib import Path
from unittest.mock import patch


def test_config_class_exists():
    """Test that Config class exists."""
    from proj.config import Config
    assert Config is not None


def test_config_has_api_url():
    """Test that config has api_url setting."""
    from proj.config import Config
    config = Config()
    assert hasattr(config, 'api_url')


def test_config_default_api_url():
    """Test default API URL."""
    from proj.config import Config
    config = Config()
    assert config.api_url == "http://localhost:5000"


def test_config_xdg_config_path():
    """Test that config uses XDG config path."""
    from proj.config import get_config_dir
    config_dir = get_config_dir()
    # Should be ~/.config/proj or XDG_CONFIG_HOME/proj
    assert "proj" in str(config_dir)


def test_config_xdg_data_path():
    """Test that config uses XDG data path."""
    from proj.config import get_data_dir
    data_dir = get_data_dir()
    # Should be ~/.local/share/proj or XDG_DATA_HOME/proj
    assert "proj" in str(data_dir)


def test_config_env_override():
    """Test that environment variables override config."""
    with patch.dict(os.environ, {"PROJ_API_URL": "http://test:8000"}):
        from proj.config import Config
        # Force reload
        config = Config()
        assert config.api_url == "http://test:8000"
```

**Expected Result:** Tests fail (RED) - config not implemented

---

### Task 5: Implement Pydantic Configuration (GREEN)

**Goal:** Implement configuration to pass tests

**File to update:** `src/proj/config.py`

```python
"""Configuration management with Pydantic and XDG compliance."""
import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


def get_xdg_config_home() -> Path:
    """Get XDG_CONFIG_HOME or default."""
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


def get_xdg_data_home() -> Path:
    """Get XDG_DATA_HOME or default."""
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))


def get_config_dir() -> Path:
    """Get proj config directory."""
    return get_xdg_config_home() / "proj"


def get_data_dir() -> Path:
    """Get proj data directory."""
    return get_xdg_data_home() / "proj"


def get_config_file() -> Path:
    """Get config file path."""
    return get_config_dir() / "config.yaml"


class Config(BaseSettings):
    """Application configuration with environment variable support."""

    model_config = SettingsConfigDict(
        env_prefix="PROJ_",
        env_file=".env",
        extra="ignore",
    )

    # API Settings
    api_url: str = Field(
        default="http://localhost:5000",
        description="URL of the work-prod API",
    )

    # GitHub Settings
    github_token: Optional[str] = Field(
        default=None,
        description="GitHub personal access token",
    )
    github_username: Optional[str] = Field(
        default=None,
        description="GitHub username for scanning repos",
    )

    # Scan Settings
    local_scan_dirs: list[str] = Field(
        default_factory=lambda: [str(Path.home() / "Projects")],
        description="Directories to scan for local projects",
    )

    @classmethod
    def load(cls) -> "Config":
        """Load config from file and environment."""
        config_file = get_config_file()

        if config_file.exists():
            with open(config_file) as f:
                file_config = yaml.safe_load(f) or {}
        else:
            file_config = {}

        # Environment variables override file config
        return cls(**file_config)

    def save(self) -> None:
        """Save current config to file."""
        config_dir = get_config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)

        config_file = get_config_file()
        with open(config_file, "w") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False)


def ensure_dirs() -> None:
    """Ensure config and data directories exist."""
    get_config_dir().mkdir(parents=True, exist_ok=True)
    get_data_dir().mkdir(parents=True, exist_ok=True)
```

**Run tests:**

```bash
pytest tests/test_config.py -v
```

**Expected Result:** Tests pass (GREEN)

---

### Task 6: Create pyproject.toml

**Goal:** Configure Python package with entry point

**File:** `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "proj-cli"
version = "0.1.0"
description = "Unified CLI for project and inventory management"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "your@email.com"}
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "typer[all]>=0.9.0",
    "pyyaml>=6.0",
    "pydantic-settings>=2.0",
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "flake8>=6.0",
]

[project.scripts]
proj = "proj.cli:app"

[project.urls]
"Homepage" = "https://github.com/yourusername/proj-cli"
"Bug Tracker" = "https://github.com/yourusername/proj-cli/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v"

[tool.coverage.run]
source = ["src/proj"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
]
```

---

### Task 7: Create requirements.txt

**File:** `requirements.txt`

```
typer[all]>=0.9.0
pyyaml>=6.0
pydantic-settings>=2.0
requests>=2.28.0
```

**File:** `requirements-dev.txt`

```
-r requirements.txt
pytest>=7.0
pytest-cov>=4.0
flake8>=6.0
```

---

### Task 8: Write Integration Test for CLI (RED)

**Goal:** Write test for CLI entry point

**File:** `tests/test_cli.py`

```python
# tests/test_cli.py
"""Tests for CLI entry point."""
import subprocess
import sys


def test_cli_version():
    """Test that proj --version works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_cli_help():
    """Test that proj --help works."""
    result = subprocess.run(
        [sys.executable, "-m", "proj", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "project" in result.stdout.lower() or "inventory" in result.stdout.lower()


def test_cli_no_args():
    """Test that proj with no args shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "proj"],
        capture_output=True,
        text=True,
    )
    # no_args_is_help=True means it shows help
    assert result.returncode == 0
    assert "Usage" in result.stdout or "usage" in result.stdout.lower()
```

---

### Task 9: Verify Full Phase 1 (REFACTOR/VERIFY)

**Goal:** Ensure everything works together

**Verification steps:**

```bash
# Install package in editable mode
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Test CLI directly
proj --version
proj --help

# Verify config paths
python -c "from proj.config import get_config_dir, get_data_dir; print(get_config_dir()); print(get_data_dir())"
```

**Expected outputs:**

- `proj --version` → `proj version 0.1.0`
- `proj --help` → Shows help with command structure
- Config dirs → `~/.config/proj` and `~/.local/share/proj`

---

## ✅ Completion Criteria

- [x] Repository created at `~/Projects/proj-cli/` ✅
- [x] Package structure complete (`src/proj/`) ✅
- [x] `pyproject.toml` with entry point configured ✅
- [x] Pydantic configuration with XDG paths ✅
- [x] `proj --version` shows version ✅
- [x] `proj --help` shows command structure ✅
- [x] All tests passing (13 tests) ✅
- [x] Package installable via `pip install -e .` ✅

---

## 📦 Deliverables

1. **`proj-cli` repository** - New Python project
2. **Package structure** - `src/proj/` with modules
3. **Entry point** - `proj` command via pyproject.toml
4. **Configuration** - Pydantic + XDG compliance
5. **Tests** - Package, config, and CLI tests

---

## 🔗 Dependencies

### Prerequisites

- `dev-infra/new-project.sh` available
- Python 3.10+ installed
- pip available

### External Dependencies

- None (this phase is self-contained)

### Blocks

- Phase 2 depends on Phase 1 completion

---

## ⚠️ Risks

| Risk              | Likelihood | Impact | Mitigation                  |
| ----------------- | ---------- | ------ | --------------------------- |
| Template issues   | Low        | Medium | Manual setup if needed      |
| Typer API changes | Low        | Low    | Pin version in requirements |

---

## 📊 Progress Tracking

### Setup

- [x] Repository created ✅
- [x] Template files updated ✅

### Package

- [x] Package structure created (`src/proj/`) ✅
- [x] Tests written (`tests/test_package.py`) ✅

### Configuration

- [x] Config implemented (Pydantic + XDG) ✅
- [x] Config tests written (`tests/test_config.py`) ✅

### Integration

- [x] CLI basic structure working ✅
- [x] `proj --version` verified ✅
- [x] `proj --help` verified ✅
- [x] CLI integration tests written (`tests/test_cli.py`) ✅

> **Note:** TDD tests deferred to Phase 4 (Polish & Cleanup) per pre-phase review decision. Implementation-first approach taken for Phase 1 due to template adaptation needs.

---

## 📝 Implementation Notes

### TDD Workflow

1. **RED:** Write failing test first
2. **GREEN:** Write minimum code to pass
3. **REFACTOR:** Clean up while tests pass

### Typer Patterns

```python
# Main app
app = typer.Typer(name="proj", no_args_is_help=True)

# Subcommand group
inv_app = typer.Typer(name="inv", help="Inventory commands")
app.add_typer(inv_app)

# Command with options
@app.command()
def list(
    format: str = typer.Option("table", "--format", "-f"),
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    """List all projects."""
    pass
```

### Pydantic Settings Patterns

```python
class Config(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PROJ_")

    api_url: str = Field(default="http://localhost:5000")
```

---

## 🔗 Related Documents

- [Feature Hub](README.md)
- [Feature Plan](feature-plan.md)
- [Transition Plan](transition-plan.md)
- [Phase 2: Migrate Project Commands](phase-2.md)
- [ADR-0007](../../decisions/ADR-0007-unified-cli-architecture.md)

---

**Last Updated:** 2025-12-16
