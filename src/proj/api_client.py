"""API client for work-prod backend."""

from typing import Dict, List, Optional

import requests

from proj.config import Config
from proj.error_handler import APIError, BackendConnectionError, TimeoutError


def _raise_api_error(
    error: requests.exceptions.RequestException,
    response=None
) -> None:
    """Convert requests exceptions to APIError or re-raise connection errors.

    Raises BackendConnectionError for connection errors, APIError for HTTP
    errors, or re-raises the original exception.
    """
    if isinstance(error, requests.exceptions.ConnectionError):
        raise BackendConnectionError(str(error)) from error
    elif isinstance(error, requests.exceptions.Timeout):
        raise TimeoutError(str(error)) from error
    elif isinstance(error, requests.exceptions.HTTPError):
        error_msg = str(error)
        if response is not None:
            try:
                error_data = response.json()
                if isinstance(error_data, dict) and 'error' in error_data:
                    error_msg = error_data['error']
            except Exception:
                pass
        raise APIError(
            error_msg,
            status_code=response.status_code if response else None
        ) from error
    else:
        raise error


class APIClient:
    """Client for interacting with work-prod API."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize client with config.

        Args:
            config: Config instance (uses Config.load() if not provided)
        """
        self.config = config or Config.load()
        self.base_url = self.config.api_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _url(self, path: str) -> str:
        """Build full URL for API path."""
        return f"{self.base_url}/api{path}"

    def list_projects(
        self,
        status: Optional[str] = None,
        organization: Optional[str] = None,
        classification: Optional[str] = None,
        search: Optional[str] = None,
    ) -> List[Dict]:
        """List all projects with optional filters.

        Args:
            status: Filter by status (active, paused, completed, cancelled)
            organization: Filter by organization name
            classification: Filter by classification
            search: Search term for name and description

        Returns:
            List of project dictionaries
        """
        params = {}
        if status:
            params["status"] = status
        if organization:
            params["organization"] = organization
        if classification:
            params["classification"] = classification
        if search:
            params["search"] = search

        try:
            response = self.session.get(
                self._url("/projects"),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def get_project(self, project_id: int) -> Dict:
        """Get a single project by ID.

        Args:
            project_id: ID of the project to retrieve

        Returns:
            Project dictionary
        """
        try:
            response = self.session.get(
                self._url(f"/projects/{project_id}"),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def create_project(self, data: Dict) -> Dict:
        """Create a new project.

        Args:
            data: Project data dictionary

        Returns:
            Created project dictionary
        """
        try:
            response = self.session.post(
                self._url("/projects"),
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def update_project(self, project_id: int, data: Dict) -> Dict:
        """Update an existing project.

        Args:
            project_id: ID of the project to update
            data: Fields to update

        Returns:
            Updated project dictionary
        """
        try:
            response = self.session.patch(
                self._url(f"/projects/{project_id}"),
                json=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def delete_project(self, project_id: int) -> None:
        """Delete a project permanently.

        Args:
            project_id: ID of the project to delete
        """
        try:
            response = self.session.delete(
                self._url(f"/projects/{project_id}"),
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def search_projects(self, query: str) -> List[Dict]:
        """Search projects by query.

        Args:
            query: Search query string

        Returns:
            List of matching projects
        """
        try:
            response = self.session.get(
                self._url("/projects"),
                params={"search": query},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def import_projects(self, projects: List[Dict]) -> Dict:
        """Import multiple projects from JSON data.

        Args:
            projects: List of project data dictionaries

        Returns:
            Dictionary with import statistics: imported, skipped, errors
        """
        try:
            response = self.session.post(
                self._url("/projects/import"),
                json={"projects": projects},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)

    def archive_project(self, project_id: int) -> Dict:
        """Archive a project.

        Sets classification to 'archive' and status to 'completed'.

        Args:
            project_id: ID of the project to archive

        Returns:
            Archived project dictionary
        """
        try:
            response = self.session.put(
                self._url(f"/projects/{project_id}/archive"),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            response = getattr(e, 'response', None)
            _raise_api_error(e, response)
