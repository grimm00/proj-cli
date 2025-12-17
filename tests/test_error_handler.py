"""Tests for error handler."""


def test_error_handler_module_exists():
    """Test that error_handler module exists."""
    from proj import error_handler
    assert error_handler is not None


def test_cli_error_exists():
    """Test that CLIError exception exists."""
    from proj.error_handler import CLIError
    assert CLIError is not None
    assert issubclass(CLIError, Exception)


def test_api_error_exists():
    """Test that APIError exception exists."""
    from proj.error_handler import APIError
    assert APIError is not None


def test_api_error_has_status_code():
    """Test that APIError stores status code."""
    from proj.error_handler import APIError
    error = APIError("Test error", status_code=404)
    assert error.status_code == 404


def test_backend_connection_error_exists():
    """Test that BackendConnectionError exception exists."""
    from proj.error_handler import BackendConnectionError
    assert BackendConnectionError is not None


def test_handle_error_exists():
    """Test that handle_error function exists."""
    from proj.error_handler import handle_error
    assert callable(handle_error)
