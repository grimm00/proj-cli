# proj-cli

**Purpose:** Unified CLI for project and inventory management  
**Version:** v0.1.0  
**Last Updated:** 2025-12-16  
**Status:** 🟠 In Development

---

## 📋 Overview

A unified command-line tool that consolidates project management and inventory scanning into a single, professional Python package.

### Features

- **Project Management:** Manage projects in the work-prod API (list, get, create, update, delete, search, import)
- **Inventory Scanning:** Scan GitHub repos and local directories for project inventory
- **XDG Compliance:** Configuration stored in standard locations (`~/.config/proj/`)
- **Rich Output:** Beautiful terminal output with progress bars and tables

---

## 🚀 Installation

### From Source (Development)

```bash
# Clone the repository
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode
pip install -e ".[dev]"
```

### From GitHub

```bash
pip install git+https://github.com/grimm00/proj-cli.git
```

---

## 📖 Quick Start

```bash
# Show version
proj --version

# Show help
proj --help

# List projects (requires work-prod API running)
proj list

# Get project details
proj get 1

# Create a project
proj create "My New Project" --desc "Description here"

# Scan GitHub repos for inventory
proj inv scan github --user yourusername

# Scan local projects
proj inv scan local --dir ~/Projects

# Export inventory to work-prod API
proj inv export api
```

---

## ⌨️ Commands

### Project Management

| Command | Description |
|---------|-------------|
| `proj list` | List all projects |
| `proj get <id>` | Get project details |
| `proj create <name>` | Create new project |
| `proj update <id>` | Update project |
| `proj delete <id>` | Delete project |
| `proj search <query>` | Search projects |
| `proj import-json <file>` | Import from JSON |

### Inventory Management

| Command | Description |
|---------|-------------|
| `proj inv scan github` | Scan GitHub repos |
| `proj inv scan local` | Scan local directories |
| `proj inv analyze` | Analyze tech stack |
| `proj inv dedupe` | Remove duplicates |
| `proj inv export json <file>` | Export to JSON |
| `proj inv export api` | Push to work-prod API |
| `proj inv status` | Show inventory status |

---

## ⚙️ Configuration

Configuration is stored at `~/.config/proj/config.yaml`:

```yaml
api_url: http://localhost:5000
github_username: yourusername
github_token: null  # Set via PROJ_GITHUB_TOKEN env var
local_scan_dirs:
  - /Users/you/Projects
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PROJ_API_URL` | work-prod API URL |
| `PROJ_GITHUB_TOKEN` | GitHub personal access token |
| `PROJ_GITHUB_USERNAME` | GitHub username |

---

## 🛠️ Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dev dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=proj

# Lint
flake8 src/proj
```

### Project Structure

```
proj-cli/
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
├── README.md
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

## 📚 Related

- **work-prod:** Backend API for project management
- **ADR-0007:** Architecture decision for unified CLI

---

## 📄 License

MIT

---

**Last Updated:** 2025-12-16  
**Status:** 🟠 In Development  
**Next:** Phase 2 - Migrate project commands from work-prod
