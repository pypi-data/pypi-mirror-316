"""Base class for ICMD API clients."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import requests

from .session import Session


class BaseClient:
    """Client to facilitate user workflows with QuesTek IDE APIs."""

    app_name = ""  # app name in Django urls, provide in subclasses

    def __init__(self):
        self.session: Session = Session()
        self.response: requests.Response | None = None

    def send_request(self, method: str, endpoint: str, data: dict | None = None, **kwargs):
        """Send a request to the ICMD API."""
        url = self._get_url(endpoint)
        self.response = self.session.checked_request(method, url, json=data, **kwargs)

    def _get_url(self, endpoint: str) -> str:
        """Get the full url for a request with app-specific endpoint."""
        _app_name = self.app_name.strip("/")
        _endpoint = endpoint.strip("/")
        return f"{_app_name}/{_endpoint}/"
