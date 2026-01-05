"""Tests for template operations."""
import pytest
from proj.templates import validate_project_name, InvalidProjectNameError


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
