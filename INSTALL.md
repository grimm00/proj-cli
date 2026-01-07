# Installation Guide

Complete installation instructions for proj-cli.

---

## Prerequisites

### Python Version

proj-cli requires **Python 3.10 or higher**.

Check your Python version:

```bash
python --version
# or
python3 --version
```

### Installing Prerequisites

**macOS:**

```bash
# Install Python via Homebrew (recommended)
brew install python@3.12

# Install pipx (recommended for CLI tools)
brew install pipx
pipx ensurepath
```

**Linux (Debian/Ubuntu):**

```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

**Windows:**

```powershell
# Install Python from python.org or via winget
winget install Python.Python.3.12

# Install pipx
pip install --user pipx
pipx ensurepath
```

### Optional Requirements

- **GitHub Personal Access Token**: Required for `proj inv scan github` to access private repos or avoid rate limits
- **dev-infra repository**: Required for `proj create --template` to create projects from templates

---

## Installation Methods

### Recommended: pipx (Isolated Environment)

[pipx](https://pipx.pypa.io/) installs Python CLI tools in isolated environments while making them globally available. This is the recommended method for end users.

```bash
# Install proj-cli
pipx install git+https://github.com/grimm00/proj-cli.git

# Verify installation
proj --version
```

**Why pipx?**
- Installs in isolated virtual environment (no dependency conflicts)
- Automatically adds `proj` command to PATH
- Easy upgrades and clean uninstalls

### Alternative: uv (Fast Modern Installer)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer that can also install CLI tools.

```bash
# Install uv first (if not already installed)
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install proj-cli as a tool
uv tool install git+https://github.com/grimm00/proj-cli.git

# Verify installation
proj --version
```

### Alternative: pip with Virtual Environment

For users who prefer explicit virtual environment management:

```bash
# Create a dedicated virtual environment
python3 -m venv ~/.local/venvs/proj-cli

# Activate the environment
source ~/.local/venvs/proj-cli/bin/activate  # macOS/Linux

# Windows (PowerShell)
# ~\.local\venvs\proj-cli\Scripts\Activate.ps1
# Windows (cmd)
# %USERPROFILE%\.local\venvs\proj-cli\Scripts\activate.bat

# Install proj-cli
pip install git+https://github.com/grimm00/proj-cli.git

# Verify installation
proj --version
```

> **Note:** With this method, you'll need to activate the virtual environment each time you want to use `proj`, or create a shell alias.

### Developer Install

For contributors who want to modify the code:

```bash
# Clone the repository
git clone https://github.com/grimm00/proj-cli.git
cd proj-cli

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate.bat     # Windows (cmd)
# venv\Scripts\Activate.ps1     # Windows (PowerShell)

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

See [docs/development/README.md](docs/development/README.md) for full development setup.

---

## Verify Installation

After installation, verify that proj-cli is working:

```bash
# Check version
proj --version

# View available commands
proj --help

# Check a specific command
proj list --help
```

Expected output for `proj --version`:

```
proj version 0.2.0
```

---

## Initial Configuration

Run the initialization wizard to configure proj-cli:

```bash
proj init
```

You'll be prompted for:

| Setting | Description | Default |
|---------|-------------|---------|
| **API URL** | work-prod API endpoint | `http://localhost:5000` |
| **GitHub username** | For inventory scanning (optional) | skip |
| **Local scan directories** | Directories to scan for projects | `~/Projects` |
| **Templates source** | Path to dev-infra templates | `~/Projects/dev-infra/templates` |

Configuration is saved to `~/.config/proj/config.yaml`.

### Environment Variables

You can also configure proj-cli via environment variables (these override config file settings):

| Variable | Description |
|----------|-------------|
| `PROJ_API_URL` | work-prod API URL |
| `PROJ_API_ENABLED` | Enable/disable API (`true`/`false`) |
| `PROJ_GITHUB_TOKEN` | GitHub personal access token |
| `PROJ_GITHUB_USERNAME` | GitHub username |
| `PROJ_TEMPLATES__SOURCE` | Path to templates directory |
| `PROJ_REGISTRY__PATH` | Path to local registry file |
| `PROJ_DEFAULT_PROJECT_DIR` | Default directory for new projects |

---

## Upgrading

### pipx

```bash
pipx upgrade proj-cli
```

### uv

```bash
uv tool upgrade proj-cli
```

### pip (in virtual environment)

```bash
# Activate your virtual environment first
source ~/.local/venvs/proj-cli/bin/activate

# Upgrade
pip install --upgrade git+https://github.com/grimm00/proj-cli.git
```

---

## Uninstalling

### pipx

```bash
pipx uninstall proj-cli
```

### uv

```bash
uv tool uninstall proj-cli
```

### pip (in virtual environment)

```bash
pip uninstall proj-cli

# Optionally remove the virtual environment
rm -rf ~/.local/venvs/proj-cli
```

### Cleaning Up Configuration

proj-cli stores configuration and data in these locations:

| Path | Contents |
|------|----------|
| `~/.config/proj/` | Configuration file (`config.yaml`) |
| `~/.local/share/proj/` | Local registry and data |

To remove all proj-cli data:

```bash
rm -rf ~/.config/proj
rm -rf ~/.local/share/proj
```

---

## Troubleshooting

### `proj: command not found`

**Cause:** The `proj` command is not in your PATH.

**Solutions:**

1. **pipx users:** Run `pipx ensurepath` and restart your terminal
2. **uv users:** Run `uv tool update-shell` and restart your terminal
3. **pip users:** Ensure your virtual environment is activated

### Python version mismatch

**Error:** `This package requires Python >=3.10`

**Solution:** Install Python 3.10 or higher:

```bash
# macOS
brew install python@3.12

# Linux
sudo apt install python3.12

# Check version
python3 --version
```

### Permission denied errors

**Cause:** Trying to install globally without proper permissions.

**Solution:** Use pipx or uv (they install to user directories), or use a virtual environment:

```bash
# Don't do this:
pip install ...  # May require sudo

# Do this instead:
pipx install ...  # Installs to ~/.local/
```

### Config file issues

**Symptom:** Unexpected behavior or settings not applying.

**Solution:** Check or reset your configuration:

```bash
# View current config location
cat ~/.config/proj/config.yaml

# Re-run initialization
proj init --force
```

### API connection errors

**Error:** `Cannot connect to API at http://localhost:5000`

**Solutions:**

1. **If using work-prod locally:** Ensure the backend is running
2. **If not using an API:** Disable API integration:
   ```bash
   # In config.yaml, set:
   api_enabled: false
   
   # Or use environment variable:
   export PROJ_API_ENABLED=false
   ```

---

## Next Steps

After installation:

1. **List projects:** `proj list`
2. **Scan GitHub repos:** `proj inv scan github --user YOUR_USERNAME`
3. **Create from template:** `proj create my-app --template standard-project`
4. **View all commands:** `proj --help`

See the [README](README.md) for complete usage documentation.
