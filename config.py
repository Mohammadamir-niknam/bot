"""Application configuration for telBotPropo.

Architecture:
    This module is the single typed boundary between environment variables,
    `.env` files, and the application runtime. It is intentionally free of
    aiogram, database, and business-service imports so it can be loaded by all
    layers without creating circular dependencies.

Responsibility:
    - Load and validate production/development settings.
    - Normalize comma-separated values such as admin IDs and proxy URLs.
    - Expose security, logging, database, Redis, and Telegram options.

Dependencies:
    - pydantic-settings for environment-backed settings.
    - python-dotenv is used by pydantic-settings through `env_file`.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings loaded from environment and `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "telBotPropo"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: Path = Path("logs/telbotpropo.log")

    bot_token: SecretStr = Field(..., min_length=20)
    bot_parse_mode: Literal["HTML", "MarkdownV2", "Markdown", ""] = "HTML"
    bot_drop_pending_updates: bool = True
    super_admin_ids: tuple[int, ...] = ()

    proxy_url_1: str | None = None
    proxy_url_2: str | None = None
    proxy_url_3: str | None = None
    proxy_timeout_seconds: int = Field(default=12, ge=3, le=60)
    proxy_healthcheck_enabled: bool = True
    allow_direct_telegram_fallback: bool = False

    database_url: str = "sqlite+aiosqlite:///./telbotpropo.db"
    database_pool_size: int = Field(default=10, ge=1, le=100)
    database_max_overflow: int = Field(default=20, ge=0, le=200)
    database_pool_recycle_seconds: int = Field(default=1800, ge=300, le=86400)

    redis_url: str | None = None
    redis_prefix: str = "telbotpropo"

    rate_limit_max_requests: int = Field(default=5, ge=1, le=100)
    rate_limit_window_seconds: int = Field(default=30, ge=1, le=3600)
    upload_max_bytes: int = Field(default=5 * 1024 * 1024, ge=1024, le=25 * 1024 * 1024)
    allowed_image_extensions: tuple[str, ...] = ("jpg", "jpeg", "png")
    backup_dir: Path = Path("backups")

    @field_validator("super_admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, value: str | int | list[int] | tuple[int, ...] | None) -> tuple[int, ...]:
        if value in (None, ""):
            return ()
        if isinstance(value, int):
            return (value,)
        if isinstance(value, str):
            return tuple(int(item.strip()) for item in value.split(",") if item.strip())
        return tuple(int(item) for item in value)

    @field_validator("allowed_image_extensions", mode="before")
    @classmethod
    def parse_extensions(cls, value: str | list[str] | tuple[str, ...]) -> tuple[str, ...]:
        if isinstance(value, str):
            items = value.split(",")
        else:
            items = value
        return tuple(sorted({item.strip().lower().lstrip(".") for item in items if item.strip()}))

    @field_validator("proxy_url_1", "proxy_url_2", "proxy_url_3", "redis_url", mode="before")
    @classmethod
    def empty_string_to_none(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None

    @property
    def bot_token_value(self) -> str:
        """Return the raw Telegram token only where an API client needs it."""

        return self.bot_token.get_secret_value()

    @property
    def proxy_urls(self) -> tuple[str, ...]:
        """Return configured proxy URLs in failover order."""

        return tuple(url.rstrip("/") for url in (self.proxy_url_1, self.proxy_url_2, self.proxy_url_3) if url)

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance for dependency injection."""

    return Settings()  # type: ignore[call-arg]
