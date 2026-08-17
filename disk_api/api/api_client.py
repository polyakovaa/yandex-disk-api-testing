import logging
import requests
from abc import ABC
from urllib.parse import urljoin
from http import HTTPMethod
from api.headers import Headers

logger = logging.getLogger(__name__)


class ApiClient(ABC):
    __HEADERS = "headers"

    def __init__(self, base_url: str, timeout: int, oauth_token: str):
        self.base_url = base_url
        self.timeout = timeout
        self.oauth_token = oauth_token

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        headers = {**Headers.default(self.oauth_token),
                   **kwargs.pop(self.__HEADERS, {})}
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

    def _get(self, path: str, **kwargs) -> requests.Response:
        return self._request(HTTPMethod.GET, path, **kwargs)

    def _post(self, path: str, json=None, **kwargs) -> requests.Response:
        return self._request(HTTPMethod.POST, path, json=json, **kwargs)

    def _put(self, path: str, **kwargs) -> requests.Response:
        return self._request(HTTPMethod.PUT, path, **kwargs)

    def _delete(self, path: str, **kwargs) -> requests.Response:
        return self._request(HTTPMethod.DELETE, path, **kwargs)
