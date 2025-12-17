# Development Guide

**Purpose:** Development setup and contribution guidelines  
**Status:** 🔴 Not Started  
**Last Updated:** 2025-12-16

---

## 📋 Quick Links

- **[Configuration](../configuration/README.md)** - Config reference
- **[Main README](../../README.md)** - Project overview

---

## 🎯 Overview

This guide covers setting up a development environment, running tests, and contributing to proj-cli.

---

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=proj

# Run specific test file
pytest tests/test_cli.py -v
```

---

## 📏 Code Style

```bash
# Lint code
flake8 src/proj

# Check all
flake8 src/proj tests/
```

---

## 📁 Project Structure

```
proj-cli/
├── pyproject.toml       # Package configuration
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── src/
│   └── proj/            # Main package
│       ├── __init__.py
│       ├── __main__.py  # Entry point
│       ├── cli.py       # Typer app
│       ├── config.py    # Pydantic config
│       ├── api_client.py
│       └── commands/    # Command modules
└── tests/
```

---

## 🔄 Git Workflow

- `main` - Production releases (protected)
- `develop` - Ongoing development (protected)
- `feat/*` - Feature branches
- `fix/*` - Bug fixes
- `docs/*` - Documentation (can push directly)

### Commit Format

```
type(scope): brief description

type: feat, fix, docs, chore, test, refactor
scope: cli, config, api, inv, etc.
```

---

## 📚 Related

- [Maintainers Hub](../maintainers/README.md)
- [Architecture Decisions](../maintainers/decisions/)

---

**Last Updated:** 2025-12-16  
**Status:** 🔴 Not Started  
**Next:** Add contribution guidelines

