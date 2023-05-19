from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    env: str = Field(
        default="prod",
        description="Current environment",
    )
    postgres_url: str = Field(
        default="postgresql://aiohttp_app:aiohttp_app@localhost:5432/aiohttp_app",
        description="URL of postgresql",
    )
    nats_urls: str = Field(
        default="nats://localhost:4222/",
        description="List of nats urls, separated by comma",
    )
    redis_url: str = Field(
        default="redis://localhost",
        description="Redis DB url",
    )

    class Config:
        env_file = ".env"
        env_prefix = "AIOHTTP_APP_"


settings = Settings()
