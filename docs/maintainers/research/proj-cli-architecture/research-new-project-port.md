# Research: new-project.sh Port

**Research Topic:** proj-cli Architecture
**Question:** What logic from new-project.sh needs to be ported to Python?
**Status:** ✅ Complete
**Created:** 2025-01-05
**Completed:** 2025-01-05

---

## 🎯 Research Question

What functionality from dev-infra's `new-project.sh` needs to be ported to proj-cli, and how should it be adapted for the Python/Typer environment?

---

## 🔍 Research Goals

- [x] Goal 1: Identify key functions in new-project.sh
- [x] Goal 2: Map Bash functions to Python equivalents
- [x] Goal 3: Identify interactive prompt requirements

---

## 📚 Research Methodology

**Sources:**

- [x] dev-infra new-project.sh: Source script (924 lines)
- [x] Typer documentation: CLI framework patterns
- [x] Rich library: Terminal output and prompts

---

## 📊 Findings

### Finding 1: Core Functions to Port

| Bash Function | Purpose | Python Equivalent |
|---------------|---------|-------------------|
| `validate_project_name()` | Name validation, sanitization | Custom validator |
| `validate_target_directory()` | Path resolution, permissions | pathlib + os |
| `copy_template()` | Copy template with hidden files | shutil.copytree |
| `customize_project()` | Placeholder replacement | String templates |
| `init_git_repo()` | Git init + optional GitHub | subprocess/GitPython |
| `prompt_yes_no()` | Interactive prompts | typer.confirm() |
| `prompt_input()` | Text input prompts | typer.prompt() |

**Source:** dev-infra/scripts/new-project.sh

**Relevance:** These are the essential functions to implement.

---

### Finding 2: Validation Rules

Project name validation from new-project.sh:
- Cannot be empty
- Cannot contain whitespace (offer sanitization)
- Can only contain letters, numbers, hyphens, underscores
- Cannot already exist in target directory

**Source:** `validate_project_name()` in new-project.sh

**Relevance:** Must implement same validation in Python.

---

### Finding 3: Template Customization

Placeholders replaced during customization:
- `[Project Name]` → actual project name
- `[Brief description...]` → user description
- `[Date]` → current date

Files customized:
- `README.md`
- `start.txt`
- `package.json` (if present)

**Source:** `customize_project()` in new-project.sh

**Relevance:** Need template customization logic.

---

### Finding 4: Interactive Flow

new-project.sh flow:
1. Get target directory (prompt with default)
2. Get project name (prompt, validate)
3. Get description (prompt)
4. Get author (prompt with git config default)
5. Select project type (numbered choice)
6. Confirm settings
7. Create project
8. Optionally init git
9. Optionally create GitHub repo

**Source:** `main()` in new-project.sh

**Relevance:** Interactive mode should follow this flow.

---

## 🔍 Analysis

**Key Insights:**

- [x] Insight 1: Most Bash logic has direct Python equivalents
- [x] Insight 2: Typer/Rich provide superior interactive UX
- [x] Insight 3: Non-interactive mode needs all flags to avoid prompts
- [x] Insight 4: GitHub repo creation is optional (skip in Phase 1)

---

## 💡 Recommendations

- [x] **Recommendation 1:** Implement validation as separate module
- [x] **Recommendation 2:** Use Rich prompts for better UX than Bash
- [x] **Recommendation 3:** Skip GitHub repo creation in Phase 1 (defer)
- [x] **Recommendation 4:** Support `--dry-run` flag for testing

---

## 📋 Requirements Discovered

- [x] **FR-PORT-1:** Must validate project name (no spaces, valid chars)
- [x] **FR-PORT-2:** Must validate target directory (exists, writable)
- [x] **FR-PORT-3:** Must copy template including hidden files (.gitignore)
- [x] **FR-PORT-4:** Must replace placeholders in README.md and start.txt
- [x] **FR-PORT-5:** Must support git initialization (optional)
- [x] **FR-PORT-6:** Must support interactive prompts
- [x] **FR-PORT-7:** Must support non-interactive mode via flags
- [x] **NFR-PORT-1:** Should offer name sanitization for invalid names

---

## 📝 Module Structure

```python
# proj/commands/create/
#   __init__.py
#   validators.py      # Name and directory validation
#   templates.py       # Template copying and customization
#   git_ops.py         # Git initialization
#   prompts.py         # Interactive prompt helpers
```

---

## 🚀 Next Steps

1. ✅ Port requirements identified
2. 🔜 Implement validators first (testable in isolation)
3. 🔜 Implement template copying
4. 🔜 Wire into interactive flow

---

**Last Updated:** 2025-01-05

