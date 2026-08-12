from http import HTTPStatus
import requests
from api.api_client import ApiClient
from api.routes import Routes
from models.upload_link import UploadLink
from models.query_params import QueryParams
from models.resource_meta import ResourceMeta, TrashListResponse


class DiskApi(ApiClient):

    def get_upload_link(self, file_path: str, overwrite: bool = False) -> requests.Response:
        return self.get(
            Routes.UPLOAD,
            params={
                QueryParams.PATH: file_path,
                QueryParams.OVERWRITE: str(overwrite).lower(),
            },
        )

    def upload_to_link(self, href: str, data: bytes) -> requests.Response:
        response = requests.put(href, data=data, timeout=self.timeout)
        return response

    def upload_file(self, file_path: str, data: bytes | str, overwrite: bool) -> requests.Response:
        if isinstance(data, str):
            data = data.encode("utf-8")

        link_response = self.get_upload_link(file_path, overwrite=overwrite)
        if link_response.status_code != HTTPStatus.OK:
            return link_response

        upload_link = UploadLink.model_validate(link_response.json())
        return self.upload_to_link(upload_link.href, data)

    def move(self, from_path: str, to_path: str) -> requests.Response:
        return self.post(
            Routes.MOVE,
            params={
                QueryParams.FROM: from_path,
                QueryParams.PATH: to_path,
            },
        )

    def get_resource(self, file_path: str) -> requests.Response:
        return self.get(
            Routes.RESOURCES,
            params={QueryParams.PATH: file_path},
        )

    def list_trash(self, limit: int, offset: int, sort: str | None = None) -> requests.Response:
        params = {
            QueryParams.LIMIT: limit,
            QueryParams.OFFSET: offset,
        }
        if sort is not None:
            params[QueryParams.SORT] = sort
        return self.get(Routes.TRASH_RESOURCES, params=params)

    def find_in_trash(self, file_name: str, page_size: int, sort: str) -> ResourceMeta | None:
        offset = 0
        while True:
            response = self.list_trash(
                limit=page_size, offset=offset, sort=sort)
            if response.status_code != HTTPStatus.OK:
                return None

            body = TrashListResponse.model_validate(response.json())
            for item in body.embedded.items:
                if item.name == file_name:
                    return item

            if not body.embedded.items or len(body.embedded.items) < page_size:
                return None

            total = body.embedded.total
            offset += len(body.embedded.items)
            if total is not None and offset >= total:
                return None

    def get_trash_resource(self, file_path: str) -> requests.Response:
        return self.get(
            Routes.TRASH_RESOURCES,
            params={QueryParams.PATH: file_path},
        )

    def restore(self, file_path: str) -> requests.Response:
        return self.put(
            Routes.TRASH_RESTORE,
            params={QueryParams.PATH: file_path},
        )

    def delete_resource(self, file_path: str, permanently: bool = False) -> requests.Response:
        return self.delete(
            Routes.RESOURCES,
            params={
                QueryParams.PATH: file_path,
                QueryParams.PERMANENTLY: str(permanently).lower(),
            },
        )
