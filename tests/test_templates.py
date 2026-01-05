"""Tests for template operations."""
import pytest
from proj.templates import (
    validate_project_name,
    sanitize_project_name,
    InvalidProjectNameError,
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
