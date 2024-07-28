from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str = "S3gtd2fcIJYtp_TJoMcKUyksWl9kXtr8ssiwzH9HTQM"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    db_url: str = "mongodb://mongo:27017"

    model_config = SettingsConfigDict(env_file=".env")
