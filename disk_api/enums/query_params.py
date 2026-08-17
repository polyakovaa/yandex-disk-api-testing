from enum import Enum


class QueryParams(str, Enum):
    PATH = "path"
    FROM = "from"
    OVERWRITE = "overwrite"
    PERMANENTLY = "permanently"
    SORT = "sort"
    FILENAME = "filename"
