from urllib.parse import parse_qs, urlparse

from enums.query_params import QueryParams


class ImageUtils:
    @staticmethod
    def _get_query_value(image_url: str, param_name: str) -> str:
        query = parse_qs(urlparse(image_url).query)
        values = query.get(param_name, [])
        return values[0] if values else ""

    @classmethod
    def get_filename(cls, image_url: str) -> str:
        return cls._get_query_value(image_url, QueryParams.FILENAME)

    @classmethod
    def matches_filename(cls, image_url: str, expected_name: str) -> bool:
        return cls.get_filename(image_url) == expected_name
