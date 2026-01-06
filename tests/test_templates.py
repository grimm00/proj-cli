"""Tests for template operations."""
import pytest
from pathlib import Path
from datetime import date
from proj.templates import (
    validate_project_name,
    sanitize_project_name,
    validate_target_directory,
    list_templates,
    validate_template_type,
    copy_template,
    replace_placeholders,
    create_from_template,
    get_templates_source,
    InvalidProjectNameError,
    DirectoryNotFoundError,
    TemplateNotFoundError,
    ProjectExistsError,
    TemplateError,
)
from proj.config import Config


class TestValidateProjectName:
    """Tests for validate_project_name function."""

    def test_valid_name_lowercase(self):
        """Test valid lowercase name passes."""
        result = validate_project_name("my-project")
        assert result == "my-project"

    def test_valid_name_with_numbers(self):
        """Test valid name with numbers passes."""
        result = validate_project_name("project123")
        assert result == "project123"

    def test_valid_name_with_underscores(self):
        """Test valid name with underscores passes."""
        result = validate_project_name("my_project")
        assert result == "my_project"

    def test_valid_name_with_hyphens(self):
        """Test valid name with hyphens passes."""
        result = validate_project_name("my-cool-project")
        assert result == "my-cool-project"

    def test_valid_name_uppercase(self):
        """Test valid uppercase name passes."""
        result = validate_project_name("MyProject")
        assert result == "MyProject"

    def test_empty_name_raises_error(self):
        """Test empty name raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("")
        assert "cannot be empty" in str(exc.value)

    def test_whitespace_only_raises_error(self):
        """Test whitespace-only name raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("   ")
        assert "cannot be empty" in str(exc.value)

    def test_name_with_spaces_raises_error(self):
        """Test name with spaces raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("my project")
        assert "cannot contain whitespace" in str(exc.value)

    def test_name_with_tabs_raises_error(self):
        """Test name with tabs raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("my\tproject")
        assert "cannot contain whitespace" in str(exc.value)

    def test_invalid_characters_raises_error(self):
        """Test name with invalid chars raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("my@project!")
        assert "can only contain" in str(exc.value)

    def test_name_with_dots_raises_error(self):
        """Test name with dots raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("my.project")
        assert "can only contain" in str(exc.value)

    def test_name_with_slashes_raises_error(self):
        """Test name with slashes raises InvalidProjectNameError."""
        with pytest.raises(InvalidProjectNameError) as exc:
            validate_project_name("my/project")
        assert "can only contain" in str(exc.value)


class TestSanitizeProjectName:
    """Tests for sanitize_project_name function."""

    def test_sanitize_spaces_to_hyphens(self):
        """Test spaces are replaced with hyphens."""
        result = sanitize_project_name("my project")
        assert result == "my-project"

    def test_sanitize_multiple_spaces(self):
        """Test multiple spaces become single hyphen."""
        result = sanitize_project_name("my    project")
        assert result == "my-project"

    def test_sanitize_tabs_to_hyphens(self):
        """Test tabs are replaced with hyphens."""
        result = sanitize_project_name("my\tproject")
        assert result == "my-project"

    def test_sanitize_leading_trailing_whitespace(self):
        """Test leading/trailing whitespace is trimmed."""
        result = sanitize_project_name("  my project  ")
        assert result == "my-project"

    def test_sanitize_special_chars_removed(self):
        """Test special characters are removed."""
        result = sanitize_project_name("my@project!")
        assert result == "myproject"

    def test_sanitize_dots_removed(self):
        """Test dots are removed."""
        result = sanitize_project_name("my.project")
        assert result == "myproject"

    def test_sanitize_preserves_valid_name(self):
        """Test valid names are unchanged."""
        result = sanitize_project_name("my-project_123")
        assert result == "my-project_123"

    def test_sanitize_empty_after_sanitization(self):
        """Test returns None if name becomes empty after sanitization."""
        result = sanitize_project_name("@#$%^")
        assert result is None

    def test_sanitize_collapses_consecutive_hyphens(self):
        """Test consecutive hyphens are collapsed."""
        result = sanitize_project_name("my - - project")
        assert result == "my-project"


class TestValidateTargetDirectory:
    """Tests for validate_target_directory function."""

    def test_existing_writable_directory(self, tmp_path):
        """Test existing writable directory returns resolved path."""
        result = validate_target_directory(tmp_path)
        assert result == tmp_path.resolve()

    def test_nonexistent_directory_raises_error(self, tmp_path):
        """Test nonexistent directory raises DirectoryNotFoundError."""
        nonexistent = tmp_path / "does-not-exist"
        with pytest.raises(DirectoryNotFoundError) as exc:
            validate_target_directory(nonexistent)
        assert "does not exist" in str(exc.value)

    def test_relative_path_resolved_to_absolute(self, tmp_path, monkeypatch):
        """Test relative path is resolved to absolute."""
        # Create a subdirectory
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        # Change to tmp_path and use relative path
        monkeypatch.chdir(tmp_path)
        result = validate_target_directory(Path("subdir"))
        assert result == subdir.resolve()
        assert result.is_absolute()

    def test_path_with_tilde_expanded(self, monkeypatch, tmp_path):
        """Test path with ~ is expanded to home directory."""
        # Mock home directory
        monkeypatch.setenv("HOME", str(tmp_path))

        # Create test directory in mock home
        test_dir = tmp_path / "Projects"
        test_dir.mkdir()

        result = validate_target_directory(Path("~/Projects"))
        assert result == test_dir.resolve()

    def test_file_path_raises_error(self, tmp_path):
        """Test file path (not directory) raises error."""
        file_path = tmp_path / "file.txt"
        file_path.touch()

        with pytest.raises(DirectoryNotFoundError) as exc:
            validate_target_directory(file_path)
        assert "not a directory" in str(exc.value)

    def test_empty_path_raises_error(self):
        """Test empty path raises error."""
        with pytest.raises(DirectoryNotFoundError):
            validate_target_directory(Path(""))


class TestListTemplates:
    """Tests for list_templates function."""

    def test_list_templates_returns_directories(self, tmp_path):
        """Test list_templates returns template directory names."""
        # Create mock template directories
        (tmp_path / "standard-project").mkdir()
        (tmp_path / "learning-project").mkdir()

        result = list_templates(tmp_path)
        assert "standard-project" in result
        assert "learning-project" in result
        assert len(result) == 2

    def test_list_templates_ignores_files(self, tmp_path):
        """Test list_templates ignores files, only returns directories."""
        (tmp_path / "standard-project").mkdir()
        (tmp_path / "README.md").touch()

        result = list_templates(tmp_path)
        assert result == ["standard-project"]

    def test_list_templates_ignores_hidden(self, tmp_path):
        """Test list_templates ignores hidden directories."""
        (tmp_path / "standard-project").mkdir()
        (tmp_path / ".git").mkdir()

        result = list_templates(tmp_path)
        assert result == ["standard-project"]

    def test_list_templates_empty_source(self, tmp_path):
        """Test list_templates returns empty list for empty source."""
        result = list_templates(tmp_path)
        assert result == []

    def test_list_templates_nonexistent_source_raises(self, tmp_path):
        """Test list_templates raises error for nonexistent source."""
        nonexistent = tmp_path / "does-not-exist"
        with pytest.raises(DirectoryNotFoundError):
            list_templates(nonexistent)


class TestValidateTemplateType:
    """Tests for validate_template_type function."""

    def test_valid_template_type(self, tmp_path):
        """Test valid template type returns path."""
        template_dir = tmp_path / "standard-project"
        template_dir.mkdir()

        result = validate_template_type("standard-project", tmp_path)
        assert result == template_dir

    def test_invalid_template_type_raises(self, tmp_path):
        """Test invalid template type raises TemplateNotFoundError."""
        (tmp_path / "standard-project").mkdir()

        with pytest.raises(TemplateNotFoundError) as exc:
            validate_template_type("nonexistent", tmp_path)
        assert "not found" in str(exc.value)
        assert "standard-project" in str(exc.value)  # Should list available


class TestCopyTemplate:
    """Tests for copy_template function."""

    def test_copy_template_creates_directory(self, tmp_path):
        """Test copy_template creates project directory."""
        # Create mock template
        template_dir = tmp_path / "templates" / "standard-project"
        template_dir.mkdir(parents=True)
        (template_dir / "README.md").write_text("# Test")

        target = tmp_path / "projects"
        target.mkdir()

        result = copy_template(
            template_path=template_dir,
            target_dir=target,
            project_name="my-project",
        )

        assert result == target / "my-project"
        assert result.exists()
        assert (result / "README.md").exists()

    def test_copy_template_includes_hidden_files(self, tmp_path):
        """Test copy_template includes hidden files like .gitignore."""
        template_dir = tmp_path / "templates" / "standard-project"
        template_dir.mkdir(parents=True)
        (template_dir / ".gitignore").write_text("*.pyc")
        (template_dir / "README.md").write_text("# Test")

        target = tmp_path / "projects"
        target.mkdir()

        result = copy_template(
            template_path=template_dir,
            target_dir=target,
            project_name="my-project",
        )

        assert (result / ".gitignore").exists()
        assert (result / ".gitignore").read_text() == "*.pyc"

    def test_copy_template_includes_hidden_directories(self, tmp_path):
        """Test copy_template includes hidden directories like .cursor/."""
        template_dir = tmp_path / "templates" / "standard-project"
        template_dir.mkdir(parents=True)
        cursor_dir = template_dir / ".cursor" / "commands"
        cursor_dir.mkdir(parents=True)
        (cursor_dir / "status.md").write_text("# Status")

        target = tmp_path / "projects"
        target.mkdir()

        result = copy_template(
            template_path=template_dir,
            target_dir=target,
            project_name="my-project",
        )

        assert (result / ".cursor").exists()
        assert (result / ".cursor" / "commands" / "status.md").exists()

    def test_copy_template_preserves_directory_structure(self, tmp_path):
        """Test copy_template preserves nested directory structure."""
        template_dir = tmp_path / "templates" / "standard-project"
        template_dir.mkdir(parents=True)
        nested = template_dir / "docs" / "maintainers" / "planning"
        nested.mkdir(parents=True)
        (nested / "README.md").write_text("# Planning")

        target = tmp_path / "projects"
        target.mkdir()

        result = copy_template(
            template_path=template_dir,
            target_dir=target,
            project_name="my-project",
        )

        planning_readme = (
            result / "docs" / "maintainers" / "planning" / "README.md"
        )
        assert planning_readme.exists()

    def test_copy_template_project_exists_raises(self, tmp_path):
        """Test copy_template raises error if project directory exists."""
        template_dir = tmp_path / "templates" / "standard-project"
        template_dir.mkdir(parents=True)

        target = tmp_path / "projects"
        target.mkdir()
        (target / "my-project").mkdir()  # Already exists

        with pytest.raises(ProjectExistsError) as exc:
            copy_template(
                template_path=template_dir,
                target_dir=target,
                project_name="my-project",
            )
        assert "already exists" in str(exc.value)


class TestReplacePlaceholders:
    """Tests for replace_placeholders function."""

    def test_replace_project_name_in_readme(self, tmp_path):
        """Test [Project Name] is replaced in README.md."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        readme.write_text("# [Project Name]\n\nWelcome to [Project Name]!")

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
        )

        content = readme.read_text()
        assert "# my-project" in content
        assert "Welcome to my-project!" in content
        assert "[Project Name]" not in content

    def test_replace_description_in_readme(self, tmp_path):
        """Test description placeholder is replaced in README.md."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        readme.write_text(
            "# Project\n\n"
            "[Brief description of what this project does]"
        )

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
            description="A cool project for testing",
        )

        content = readme.read_text()
        assert "A cool project for testing" in content
        assert "[Brief description" not in content

    def test_replace_date_in_readme(self, tmp_path):
        """Test [Date] is replaced with current date."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        readme.write_text("Created: [Date]")

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
        )

        content = readme.read_text()
        today = date.today().strftime("%Y-%m-%d")
        assert today in content
        assert "[Date]" not in content

    def test_replace_in_start_txt(self, tmp_path):
        """Test placeholders are replaced in start.txt."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        start = project_dir / "start.txt"
        start.write_text("Project: [Project Name]\nAuthor: [Author]")

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
            author="Test Author",
        )

        content = start.read_text()
        assert "Project: my-project" in content
        assert "Author: Test Author" in content

    def test_handles_missing_files_gracefully(self, tmp_path):
        """Test function doesn't fail if files don't exist."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()

        # Should not raise - just skip missing files
        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
        )

    def test_preserves_files_without_placeholders(self, tmp_path):
        """Test files without placeholders are unchanged."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        original = "# Simple README\n\nNo placeholders here."
        readme.write_text(original)

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
        )

        assert readme.read_text() == original

    def test_default_description_when_not_provided(self, tmp_path):
        """Test default description when not provided."""
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        readme.write_text("[Brief description of what this project does]")

        replace_placeholders(
            project_path=project_dir,
            project_name="my-project",
            # No description provided
        )

        content = readme.read_text()
        # Should replace with empty or project name
        assert "[Brief description" not in content

    def test_replace_learning_project_name_placeholder(self, tmp_path):
        """Test that [Learning Project Name] placeholder is replaced."""
        project_dir = tmp_path / "my-learning-app"
        project_dir.mkdir()
        readme = project_dir / "README.md"
        readme.write_text("# [Learning Project Name]\n\n**Purpose:** Learning")

        replace_placeholders(
            project_path=project_dir,
            project_name="my-learning-app",
        )

        content = readme.read_text()
        assert "# my-learning-app" in content
        assert "[Learning Project Name]" not in content


class TestCreateFromTemplate:
    """Tests for create_from_template function."""

    def test_create_from_template_full_workflow(self, tmp_path):
        """Test full workflow: validate, copy, replace."""
        # Set up mock template source
        templates_source = tmp_path / "templates"
        templates_source.mkdir()
        template_dir = templates_source / "standard-project"
        template_dir.mkdir()
        (template_dir / "README.md").write_text("# [Project Name]")
        (template_dir / ".gitignore").write_text("*.pyc")

        # Target directory
        target = tmp_path / "projects"
        target.mkdir()

        result = create_from_template(
            project_name="my-app",
            template_type="standard-project",
            target_dir=target,
            templates_source=templates_source,
            description="My awesome app",
        )

        assert result.exists()
        assert result.name == "my-app"
        assert (result / "README.md").read_text() == "# my-app"
        assert (result / ".gitignore").exists()

    def test_create_from_template_invalid_name_raises(self, tmp_path):
        """Test invalid project name raises error."""
        templates_source = tmp_path / "templates"
        templates_source.mkdir()
        (templates_source / "standard-project").mkdir()

        target = tmp_path / "projects"
        target.mkdir()

        with pytest.raises(InvalidProjectNameError):
            create_from_template(
                project_name="my project",  # Invalid - has space
                template_type="standard-project",
                target_dir=target,
                templates_source=templates_source,
            )

    def test_create_from_template_invalid_template_raises(self, tmp_path):
        """Test invalid template type raises error."""
        templates_source = tmp_path / "templates"
        templates_source.mkdir()
        (templates_source / "standard-project").mkdir()

        target = tmp_path / "projects"
        target.mkdir()

        with pytest.raises(TemplateNotFoundError):
            create_from_template(
                project_name="my-app",
                template_type="nonexistent",
                target_dir=target,
                templates_source=templates_source,
            )

    def test_create_from_template_invalid_target_raises(self, tmp_path):
        """Test invalid target directory raises error."""
        templates_source = tmp_path / "templates"
        templates_source.mkdir()
        (templates_source / "standard-project").mkdir()

        nonexistent = tmp_path / "does-not-exist"

        with pytest.raises(DirectoryNotFoundError):
            create_from_template(
                project_name="my-app",
                template_type="standard-project",
                target_dir=nonexistent,
                templates_source=templates_source,
            )


class TestGetTemplatesSource:
    """Tests for get_templates_source function."""

    def test_get_templates_source_from_config(self, tmp_path, monkeypatch):
        """Test getting templates source from config."""
        # Mock XDG paths for isolation
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
        monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))

        # Create config with templates source
        config_dir = tmp_path / "config" / "proj"
        config_dir.mkdir(parents=True)

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()

        config_file = config_dir / "config.yaml"
        config_file.write_text(f"""
api_url: http://localhost:5000
templates:
  source: {templates_dir}
""")

        config = Config.load()
        result = get_templates_source(config)
        assert result == templates_dir.resolve()

    def test_get_templates_source_not_configured_raises(
        self, tmp_path, monkeypatch
    ):
        """Test error when templates source not configured."""
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
        monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "data"))

        config_dir = tmp_path / "config" / "proj"
        config_dir.mkdir(parents=True)

        config_file = config_dir / "config.yaml"
        config_file.write_text("api_url: http://localhost:5000")

        config = Config.load()

        with pytest.raises(TemplateError) as exc:
            get_templates_source(config)
        assert "not configured" in str(exc.value)
