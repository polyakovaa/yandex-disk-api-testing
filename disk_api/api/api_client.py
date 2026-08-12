import logging
import requests
from abc import ABC
from urllib.parse import urljoin
from http import HTTPMethod

logger = logging.getLogger(__name__)


class ApiClient(ABC):
    AUTHORIZATION = "Authorization"
    OAUTH_PREFIX = "OAuth"

    def __init__(self, base_url: str, timeout: int, oauth_token: str):
        self.base_url = base_url
        self.timeout = timeout
        self.oauth_token = oauth_token

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        headers = kwargs.pop("headers", {})
        headers.setdefault(self.AUTHORIZATION,
                           f"{self.OAUTH_PREFIX} {self.oauth_token}")
        response = requests.request(
            method=method,
            url=urljoin(self.base_url, str(path)),
            timeout=self.timeout,
            headers=headers,
            **kwargs,
        )
        logger.info(
            "%s %s code: %s",
            response.request.method,
            response.request.url,
            response.status_code,
        )
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request(HTTPMethod.GET, path, **kwargs)

    def post(self, path: str, json=None, **kwargs) -> requests.Response:
        return self.request(HTTPMethod.POST, path, json=json, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request(HTTPMethod.PUT, path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request(HTTPMethod.DELETE, path, **kwargs)
