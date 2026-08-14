from models.test_data import ModelTestData
from providers.file_data_reader import FileDataReader
from utils.file_utils import FileUtils


class ModelTestDataProvider:
    __instance: ModelTestData | None = None
    FILE_NAME = "test_data.json"

    @classmethod
    def __initialize(cls) -> None:
        if cls.__instance is None:
            data_path = FileUtils.resource_path(cls.FILE_NAME)
            cls.__instance = FileDataReader.parse_json(data_path, ModelTestData)

    @classmethod
    def get_instance(cls) -> ModelTestData:
        cls.__initialize()
        assert cls.__instance is not None
        return cls.__instance
