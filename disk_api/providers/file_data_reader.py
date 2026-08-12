import json
from pathlib import Path
from typing import TypeVar
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class FileDataReader:
    @staticmethod
    def parse_json(file_path: Path | str, model: type[T]) -> T:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as err:
            raise FileNotFoundError(
                f"File {file_path} not found: {err}") from err
        except json.JSONDecodeError as err:
            raise ValueError(f"Error in JSON encoding: {err}") from err
        try:
            return model.model_validate(data)
        except ValidationError as err:
            raise ValueError(
                f"File doesn't match model {model.__name__}: {err}"
            ) from err
