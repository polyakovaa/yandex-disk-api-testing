import requests
from api.api_client import ApiClient
from enums.routes import Routes
from enums.trash_sort import TrashSort
from enums.query_params import QueryParams


class DiskApi(ApiClient):
    def get_upload_link(self, file_path: str, overwrite: bool = False) -> requests.Response:
        return self._get(
            Routes.UPLOAD,
            params={
                QueryParams.PATH: file_path,
                QueryParams.OVERWRITE: str(overwrite).lower(),
            },
        )

    def upload_to_link(self, href: str, data: bytes | str) -> requests.Response:
        if isinstance(data, str):
            data = data.encode("utf-8")
        return requests.put(href, data=data, timeout=self.timeout)

    def move(self, from_path: str, to_path: str) -> requests.Response:
        return self._post(
            Routes.MOVE,
            params={
                QueryParams.FROM: from_path,
                QueryParams.PATH: to_path,
            },
        )

    def list_trash(self, sort: TrashSort | None = None) -> requests.Response:
        params = {}
        if sort is not None:
            params[QueryParams.SORT] = sort
        return self._get(Routes.TRASH_RESOURCES, params=params)

    def get_trash_resource(self, file_path: str) -> requests.Response:
        return self._get(
            Routes.TRASH_RESOURCES,
            params={QueryParams.PATH: file_path},
        )

    def restore(self, file_path: str) -> requests.Response:
        return self._put(
            Routes.TRASH_RESTORE,
            params={QueryParams.PATH: file_path},
        )

    def delete_resource(self, file_path: str, permanently: bool = False) -> requests.Response:
        return self._delete(
            Routes.RESOURCES,
            params={
                QueryParams.PATH: file_path,
                QueryParams.PERMANENTLY: str(permanently).lower(),
            },
        )
