# proj-cli

Unified CLI for project and inventory management.

## Installation

```bash
# From local source
pip install -e .

# From GitHub
pip install git+https://github.com/grimm00/proj-cli.git
```

## Quick Start

```bash
# Initialize configuration (sets API URL, templates source, etc.)
proj init

# List projects
proj list

# Get project details
proj get 1

# Create a project from template (recommended)
proj create my-app --template standard-project --local-only

# Or use interactive mode
proj create

# Scan GitHub repos
proj inv scan github --user grimm00

# Scan local projects
proj inv scan local --dir ~/Projects

# Analyze inventory
proj inv analyze

# Export to API
proj inv export api
```

## Creating Projects from Templates

The `proj create` command supports creating projects from dev-infra templates.

### Interactive Mode (Default)

Simply run `proj create` without arguments to enter interactive mode:

```bash
proj create
```

You'll be prompted for:
- **Project name** - Name for your new project
- **Template type** - Choose from available templates (standard-project, learning-project)
- **Description** - Brief description of the project
- **Target directory** - Where to create the project (default: ~/Projects)

### Template Mode

Create a project directly from a template:

```bash
# Standard project (full structure)
proj create my-app --template standard-project --local-only

# Learning project (stage-based structure)
proj create my-learning --template learning-project --local-only

# With custom target directory
proj create my-app --template standard-project --target-dir ~/Projects

# With description
proj create my-app --template standard-project --desc "My awesome app"
```

### Available Templates

| Template | Description |
| -------- | ----------- |
| `standard-project` | Full project structure with backend/frontend, tests, CI/CD |
| `learning-project` | Stage-based learning structure with fundamentals and practice apps |

### Create Command Options

| Option | Short | Description |
| ------ | ----- | ----------- |
| `--template` | `-t` | Template to use (standard-project, learning-project) |
| `--target-dir` | `-d` | Directory to create project in (default: ~/Projects) |
| `--desc` | | Project description |
| `--local-only` | | Create locally without API registration |
| `--api-only` | | Create API record only (no local files) |
| `--dry-run` | | Preview what would be created |
| `--no-git` | | Skip Git repository initialization |
| `--register/--no-register` | | Control local registry registration |

### Examples

```bash
# Preview what would be created (dry-run)
proj create my-app --template standard-project --dry-run

# Create without Git initialization
proj create my-app --template standard-project --local-only --no-git

# API-only mode (backward compatible with work-prod)
proj create "My Project" --api-only --desc "Created via CLI"
```

## Commands

### Project Management

| Command                   | Description                              |
| ------------------------- | ---------------------------------------- |
| `proj list`               | List all projects                        |
| `proj get <id>`           | Get project details                      |
| `proj create`             | Create project (interactive mode)        |
| `proj create <name> -t`   | Create project from template             |
| `proj update <id>`        | Update project                           |
| `proj delete <id>`        | Delete project                           |
| `proj search <query>`     | Search projects                          |
| `proj import-json <file>` | Import from JSON                         |
| `proj archive <id>`       | Archive project                          |
| `proj init`               | Initialize/update configuration          |

### Inventory Management

| Command                       | Description            |
| ----------------------------- | ---------------------- |
| `proj inv scan github`        | Scan GitHub repos      |
| `proj inv scan local`         | Scan local directories |
| `proj inv analyze`            | Analyze tech stack     |
| `proj inv dedupe`             | Remove duplicates      |
| `proj inv export json <file>` | Export to JSON         |
| `proj inv export api`         | Push to work-prod API  |
| `proj inv status`             | Show inventory status  |

## Configuration

Configuration is stored at `~/.config/proj/config.yaml`:

```yaml
api_url: http://localhost:5000
api_enabled: true
github_username: grimm00
github_token: null # Set via PROJ_GITHUB_TOKEN env var
local_scan_dirs:
  - /home/user/Projects

# Template configuration
templates:
  source: ~/Projects/dev-infra/templates  # Path to dev-infra templates
  default: standard-project               # Default template type

# Local registry
registry:
  path: ~/.local/share/proj/registry.json  # Local project registry
```

### Setting Up Templates

Run `proj init` to configure the template source:

```bash
proj init
# Prompts for:
# - API URL (default: http://localhost:5000)
# - GitHub username (optional)
# - Local scan directories
# - Templates source (default: ~/Projects/dev-infra/templates)
```

The templates source should point to your local clone of the dev-infra repository's `templates/` directory.

### Environment Variables

| Variable                  | Description                           |
| ------------------------- | ------------------------------------- |
| `PROJ_API_URL`            | work-prod API URL                     |
| `PROJ_API_ENABLED`        | Enable/disable API (true/false)       |
| `PROJ_GITHUB_TOKEN`       | GitHub personal access token          |
| `PROJ_GITHUB_USERNAME`    | GitHub username                       |
| `PROJ_TEMPLATES__SOURCE`  | Path to templates directory           |
| `PROJ_REGISTRY__PATH`     | Path to local registry file           |
| `PROJ_DEFAULT_PROJECT_DIR`| Default directory for new projects    |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=proj

# Lint
flake8 src/proj
```

## License

MIT
