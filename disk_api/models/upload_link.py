from pydantic import BaseModel, ConfigDict


class UploadLink(BaseModel):
    model_config = ConfigDict(extra="ignore")
    href: str
