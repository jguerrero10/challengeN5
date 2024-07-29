from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_url: str = "http://backend:8000"

    model_config = SettingsConfigDict(env_file=".env")
