# proj-cli

**Your command center for project and inventory management.**

A unified CLI tool that eliminates the friction of starting new projects and managing your portfolio. Create projects from battle-tested templates, scan your GitHub and local repos, and keep everything synced with your project database.

---

## ✨ Why proj-cli?

| Problem | Solution |
|---------|----------|
| 🔄 Starting projects from scratch every time | **One command** creates fully-structured projects from proven templates |
| 📂 Projects scattered across GitHub and local dirs | **Unified inventory** that scans and consolidates everything |
| 📝 Manual tracking in spreadsheets or docs | **Automatic sync** to your project database (work-prod API) |
| 🤔 Forgetting your project portfolio | **Rich filtering** by type, status, and tech stack |
| ⚙️ Different setup steps for each project | **Consistent structure** across all your projects |

---

## 🚀 Key Features

### 📦 Template-Powered Project Creation
Create new projects instantly from dev-infra templates with all the scaffolding you need:

```bash
# Interactive mode - guided prompts
proj create

# Direct creation - one command
proj create my-app --template standard-project --local-only
```

**Available Templates:**
- **`standard-project`** - Full structure with backend/frontend, tests, CI/CD, and documentation
- **`learning-project`** - Stage-based learning structure with fundamentals and practice apps

**What you get:**
- ✅ Pre-configured directory structure
- ✅ Git initialization
- ✅ Placeholder replacement (project name, dates, etc.)
- ✅ Local registry tracking
- ✅ Optional API sync

### 🔍 Intelligent Inventory Scanning

Discover and catalog all your projects from multiple sources:

```bash
# Scan your GitHub repos
proj inv scan github --user yourname

# Scan local project directories
proj inv scan local --dir ~/Projects

# Analyze tech stacks across all projects
proj inv analyze
```

**Detected project markers:** `.git`, `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`

**Auto-detected frameworks:** React, Vue, Express, and more

### 📊 Powerful Project Management

Full CRUD operations with rich filtering:

```bash
# Filter by project type
proj list --type Work
proj list --type Learning --search "python"

# Combine filters
proj list --type Personal --class primary --wide
```

**Output formats:** Beautiful tables with status emojis or JSON for scripting

### 🔄 Seamless API Integration

Keep your local projects synced with work-prod:

```bash
# Export inventory to API
proj inv export api

# Import projects from JSON
proj import-json projects.json
```

**Graceful degradation:** Works offline, syncs when API is available

---

## 📥 Installation

**Quick install with pipx (recommended):**

```bash
pipx install git+https://github.com/grimm00/proj-cli.git
proj init
```

See [INSTALL.md](INSTALL.md) for alternative methods and troubleshooting.

---

## ⚡ Quick Start

```bash
# 1. Initialize configuration
proj init

# 2. Create your first project
proj create my-app --template standard-project --local-only

# 3. Build your inventory
proj inv scan github --user yourname
proj inv scan local --dir ~/Projects
proj inv analyze

# 4. View your portfolio
proj list --wide
```

---

## 📋 Command Reference

### Project Management

| Command | Description |
|---------|-------------|
| `proj list` | List projects with filtering |
| `proj get <id>` | Get project details |
| `proj create` | Create project (interactive or template) |
| `proj update <id>` | Update project fields |
| `proj delete <id>` | Delete project |
| `proj search <query>` | Search projects |
| `proj import-json <file>` | Bulk import from JSON |
| `proj archive <id>` | Archive project |
| `proj init` | Initialize/update configuration |

### Inventory Management

| Command | Description |
|---------|-------------|
| `proj inv scan github` | Scan GitHub repositories |
| `proj inv scan local` | Scan local directories |
| `proj inv analyze` | Analyze tech stacks |
| `proj inv dedupe` | Remove duplicates |
| `proj inv export json <file>` | Export to JSON |
| `proj inv export api` | Push to work-prod API |
| `proj inv status` | Show inventory statistics |

---

## 🎨 Creating Projects from Templates

### Interactive Mode (Default)

Run `proj create` without arguments for guided prompts:

```bash
proj create
# Prompts for: project name, template type, target directory, description
```

### Template Mode

Create directly with flags:

```bash
# Standard project (full structure)
proj create my-app --template standard-project --local-only

# Learning project (stage-based)
proj create my-learning --template learning-project --local-only

# With custom options
proj create my-app -t standard-project --target-dir ~/Work --desc "My app"

# Preview without creating (dry-run)
proj create my-app --template standard-project --dry-run
```

### Create Command Options

| Option | Short | Description |
|--------|-------|-------------|
| `--template` | `-t` | Template type (standard-project, learning-project) |
| `--target-dir` | `-d` | Directory to create project in |
| `--desc` | | Project description |
| `--local-only` | | Create locally without API sync |
| `--api-only` | | Create API record only (no local files) |
| `--dry-run` | | Preview what would be created |
| `--no-git` | | Skip Git repository initialization |
| `--register/--no-register` | | Control local registry registration |

---

## 🔎 Filtering Projects

### By Project Type

```bash
proj list --type Work       # Work projects
proj list --type Personal   # Personal projects
proj list --type Learning   # Learning projects
proj list --type Inactive   # Inactive projects
```

### Combined Filters

```bash
proj list --type Work --class primary
proj list --type Personal --search "python"
proj list --type Work --status active --org personal
```

### Filter Options

| Option | Short | Description |
|--------|-------|-------------|
| `--type` | `-t` | Filter by project type |
| `--status` | `-s` | Filter by status |
| `--org` | `-o` | Filter by organization |
| `--class` | `-c` | Filter by classification |
| `--search` | | Search in names and descriptions |
| `--wide` | `-w` | Show all columns |
| `--format` | `-f` | Output format: table, json |

---

## ⚙️ Configuration

Configuration is stored at `~/.config/proj/config.yaml`:

```yaml
# API Settings
api_url: http://localhost:5000
api_enabled: true

# GitHub Settings
github_username: yourname
github_token: null  # Set via PROJ_GITHUB_TOKEN env var

# Scanning
local_scan_dirs:
  - ~/Projects

# Templates
templates:
  source: ~/Projects/dev-infra/templates
  default: standard-project

# Local Registry
registry:
  path: ~/.local/share/proj/registry.json

# Defaults
default_project_dir: ~/Projects
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PROJ_API_URL` | work-prod API URL |
| `PROJ_API_ENABLED` | Enable/disable API (true/false) |
| `PROJ_GITHUB_TOKEN` | GitHub personal access token |
| `PROJ_GITHUB_USERNAME` | GitHub username |
| `PROJ_TEMPLATES__SOURCE` | Path to templates directory |
| `PROJ_REGISTRY__PATH` | Path to local registry file |
| `PROJ_DEFAULT_PROJECT_DIR` | Default directory for new projects |

---

## 🔄 API Synchronization

### Default Behavior

Template creation syncs to work-prod API when:
- `api_enabled: true` in config
- `--local-only` flag is NOT used

### Offline Mode

Use `--local-only` for offline development:

```bash
proj create my-app --template standard-project --local-only
```

### Handling API Errors

If the API is unavailable, local creation continues successfully:

```
✓ Initialized git repository
✓ Registered project in local registry
⚠ Could not sync to API: Connection refused
✓ Created project from template: /path/to/my-app
```

---

## 🛠️ Development

```bash
# Clone and install
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=proj

# Lint
flake8 src/proj
```

---

## 📄 License

MIT

---

**Version:** 0.3.2 • [Changelog](CHANGELOG.md) • [Installation](INSTALL.md)
