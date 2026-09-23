from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")
    openai_api_key: SecretStr = SecretStr("")
    openai_model: str = "gpt-6-sol"
    openai_timeout_seconds: float = Field(default=180, gt=0, le=300)
