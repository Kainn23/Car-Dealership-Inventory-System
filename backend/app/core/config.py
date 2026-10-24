"""Application settings and configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/dealership"
    TEST_DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/dealership_test"
    JWT_SECRET: str = "dev-insecure-secret-key-change-in-production-min-32-chars-long"
    JWT_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:8080"]


settings = Settings()
