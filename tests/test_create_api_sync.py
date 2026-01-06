"""Tests for API sync functionality."""
from pathlib import Path
from unittest.mock import Mock

from proj.commands.projects import sync_to_api
from proj.error_handler import APIError, BackendConnectionError, TimeoutError


def test_sync_to_api_success():
    """Test sync_to_api returns work_prod_id on success."""
    mock_client = Mock()
    mock_client.create_project.return_value = {"id": 42, "name": "test"}

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
        description="Test description",
    )

    assert result == 42
    mock_client.create_project.assert_called_once()
    call_args = mock_client.create_project.call_args[0][0]
    assert call_args["name"] == "test-project"
    assert call_args["path"] == "/tmp/test"
    assert call_args["description"] == "Test description"
    assert call_args["status"] == "active"


def test_sync_to_api_connection_error():
    """Test sync_to_api returns None on connection error."""
    mock_client = Mock()
    mock_client.create_project.side_effect = BackendConnectionError(
        "No connection"
    )

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result is None  # No exception raised


def test_sync_to_api_api_error():
    """Test sync_to_api returns None on API error."""
    mock_client = Mock()
    mock_client.create_project.side_effect = APIError("Server error", 500)

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result is None  # No exception raised


def test_sync_to_api_timeout_error():
    """Test sync_to_api returns None on timeout error."""
    mock_client = Mock()
    mock_client.create_project.side_effect = TimeoutError("Request timeout")

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result is None  # No exception raised


def test_sync_to_api_default_description():
    """Test sync_to_api uses default description when not provided."""
    mock_client = Mock()
    mock_client.create_project.return_value = {"id": 123}

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
    )

    assert result == 123
    call_args = mock_client.create_project.call_args[0][0]
    assert "description" in call_args
    assert "standard-project" in call_args["description"]


def test_sync_to_api_with_console_output():
    """Test sync_to_api prints error message when console provided."""
    mock_client = Mock()
    mock_client.create_project.side_effect = APIError("Server error", 500)
    mock_console = Mock()

    result = sync_to_api(
        client=mock_client,
        name="test-project",
        path=Path("/tmp/test"),
        template="standard-project",
        console=mock_console,
    )

    assert result is None
    mock_console.print.assert_called_once()
    # Verify error message contains warning
    call_args = mock_console.print.call_args[0][0]
    assert "Could not sync" in call_args or "⚠" in call_args
