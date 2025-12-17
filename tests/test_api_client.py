"""Tests for API client."""


def test_api_client_exists():
    """Test that APIClient class exists."""
    from proj.api_client import APIClient
    assert APIClient is not None


def test_api_client_uses_config_url():
    """Test that client uses URL from config."""
    from proj.api_client import APIClient
    from proj.config import Config

    config = Config(api_url="http://test:8000")
    client = APIClient(config=config)
    assert client.base_url == "http://test:8000"


def test_api_client_list_projects():
    """Test list_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'list_projects')


def test_api_client_get_project():
    """Test get_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'get_project')


def test_api_client_create_project():
    """Test create_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'create_project')


def test_api_client_update_project():
    """Test update_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'update_project')


def test_api_client_delete_project():
    """Test delete_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'delete_project')


def test_api_client_search_projects():
    """Test search_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'search_projects')


def test_api_client_import_projects():
    """Test import_projects method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'import_projects')


def test_api_client_archive_project():
    """Test archive_project method exists."""
    from proj.api_client import APIClient

    client = APIClient()
    assert hasattr(client, 'archive_project')
