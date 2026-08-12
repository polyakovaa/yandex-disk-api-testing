from pydantic import BaseModel


class ModelTestData(BaseModel):
    text_content_length: int
    ext_before: str
    ext_after: str
    img_file: str
    trash_page_size: int
    trash_sort: str
