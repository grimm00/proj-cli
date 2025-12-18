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
# Initialize configuration
proj init

# List projects
proj list

# Get project details
proj get 1

# Create a project
proj create "My New Project" --desc "Description here"

# Scan GitHub repos
proj inv scan github --user grimm00

# Scan local projects
proj inv scan local --dir ~/Projects

# Analyze inventory
proj inv analyze

# Export to API
proj inv export api
```

## Commands

### Project Management

| Command                   | Description         |
| ------------------------- | ------------------- |
| `proj list`               | List all projects   |
| `proj get <id>`           | Get project details |
| `proj create <name>`      | Create new project  |
| `proj update <id>`        | Update project      |
| `proj delete <id>`        | Delete project      |
| `proj search <query>`     | Search projects     |
| `proj import-json <file>` | Import from JSON    |
| `proj archive <id>`       | Archive project     |

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
github_username: grimm00
github_token: null # Set via PROJ_GITHUB_TOKEN env var
local_scan_dirs:
  - /home/user/Projects
```

### Environment Variables

| Variable               | Description                  |
| ---------------------- | ---------------------------- |
| `PROJ_API_URL`         | work-prod API URL            |
| `PROJ_GITHUB_TOKEN`    | GitHub personal access token |
| `PROJ_GITHUB_USERNAME` | GitHub username              |

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
