from pydantic import BaseModel, ConfigDict, Field


class ResourceMeta(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    path: str
    type: str | None = None
    mime_type: str | None = None


class TrashEmbedded(BaseModel):
    model_config = ConfigDict(extra="ignore")
    items: list[ResourceMeta] = []
    total: int | None = None


class TrashListResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    embedded: TrashEmbedded = Field(
        default_factory=TrashEmbedded,
        alias="_embedded",
    )
