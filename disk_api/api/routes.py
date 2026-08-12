from enum import Enum


class Routes(str, Enum):
    UPLOAD = "resources/upload"
    MOVE = "resources/move"
    RESOURCES = "resources"
    TRASH_RESOURCES = "trash/resources"
    TRASH_RESTORE = "trash/resources/restore"

    def __str__(self) -> str:
        return self.value
