from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="YANDEX_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str
    timeout: int
    oauth_token: str
    email: str
    password: str
