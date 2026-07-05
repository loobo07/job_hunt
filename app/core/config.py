from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://job_hunt:job_hunt@localhost:5432/job_hunt"


def get_settings() -> Settings:
    return Settings()
