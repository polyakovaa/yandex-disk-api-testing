from pathlib import Path


class FileUtils:
    __PROJECT_MARKERS = ("pyproject.toml", "requirements.txt")
    RESOURCES_DIR = "resources"

    @classmethod
    def find_project_root(cls, start: Path | None = None) -> Path:
        current = (start or Path(__file__)).resolve()
        if current.is_file():
            current = current.parent
        for parent in [current, *current.parents]:
            if any((parent / marker).exists() for marker in cls.__PROJECT_MARKERS):
                return parent
        raise FileNotFoundError(
            "File not Found by pyproject.toml / requirements.txt")

    @classmethod
    def resource_path(cls, file_name: str) -> Path:
        return cls.find_project_root() / cls.RESOURCES_DIR / file_name

    @classmethod
    def read_resource_bytes(cls, file_name: str) -> bytes:
        with open(cls.resource_path(file_name), "rb") as file:
            return file.read()
