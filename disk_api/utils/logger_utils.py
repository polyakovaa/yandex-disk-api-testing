import logging
from pathlib import Path

from utils.file_utils import FileUtils


class LoggerUtils:
    __configured = False
    __log_file: Path | None = None
    LOG_DIR = "logs"
    DEFAULT_FILENAME = "disk_api.log"

    @classmethod
    def setup(cls, filename: str = DEFAULT_FILENAME) -> Path:
        if cls.__configured:
            return cls.__log_file

        log_dir = FileUtils.find_project_root() / cls.LOG_DIR
        log_dir.mkdir(exist_ok=True)
        cls.__log_file = log_dir / filename

        handler = logging.FileHandler(cls.__log_file, mode="w", encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        root = logging.getLogger()
        root.setLevel(logging.INFO)
        root.addHandler(handler)

        cls.__configured = True
        logging.getLogger(__name__).info("Logging to file: %s", cls.__log_file)
        return cls.__log_file
