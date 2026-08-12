from models.config import Config
from utils.file_utils import FileUtils


class ConfigProvider:
    __instance: Config | None = None
    FILE_PATH = ".env"

    @classmethod
    def get_instance(cls) -> Config:
        if cls.__instance is None:
            root = FileUtils.find_project_root()
            cls.__instance = Config(_env_file=root / cls.FILE_PATH)
        return cls.__instance
