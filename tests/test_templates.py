"""Tests for template operations."""
import pytest
from pathlib import Path
from proj.templates import (
    validate_project_name,
    sanitize_project_name,
    validate_target_directory,
    list_templates,
    validate_template_type,
    copy_template,
    InvalidProjectNameError,
    DirectoryNotFoundError,
    TemplateNotFoundError,
    ProjectExistsError,
)


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

        assert (result / "docs" / "maintainers" / "planning" / "README.md").exists()

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
