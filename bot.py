"""Telegram bot factory with Cloudflare proxy failover.

Architecture:
    Bot creation is isolated behind a factory so the rest of the application
    receives an already validated aiogram Bot instance. Proxy selection is
    runtime-aware and can later be backed by database settings from the admin
    panel without changing handlers.

Responsibility:
    - Build aiogram Bot instances with AiohttpSession.
    - Try PROXY_URL_1, PROXY_URL_2, and PROXY_URL_3 in order.
    - Optionally verify endpoints through `getMe` before selecting one.
    - Fall back to direct Telegram only when explicitly enabled.

Dependencies:
    - aiogram 3.x for Bot, Dispatcher, sessions, and default properties.
    - aiogram AiohttpSession timeout controls for strict network timeouts.
    - structlog for structured operational logs.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from config import Settings

logger = structlog.get_logger(__name__)


@dataclass(frozen=True, slots=True)
class BotEndpoint:
    """A Telegram API endpoint candidate."""

    name: str
    base_url: str | None


class TelegramProxyUnavailable(RuntimeError):
    """Raised when no configured Telegram API endpoint can be used."""


class BotFactory:
    """Create a healthy aiogram Bot using ordered Cloudflare proxy failover."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def endpoints(self) -> tuple[BotEndpoint, ...]:
        configured = [
            BotEndpoint(name=f"proxy_url_{index}", base_url=url)
            for index, url in enumerate(self.settings.proxy_urls, start=1)
        ]
        if self.settings.allow_direct_telegram_fallback:
            configured.append(BotEndpoint(name="direct_telegram", base_url=None))
        return tuple(configured)

    def build_session(self, endpoint: BotEndpoint) -> AiohttpSession:
        if endpoint.base_url:
            return AiohttpSession(base_url=endpoint.base_url, timeout=self.settings.proxy_timeout_seconds)
        return AiohttpSession(timeout=self.settings.proxy_timeout_seconds)

    def build_bot(self, endpoint: BotEndpoint) -> Bot:
        parse_mode = ParseMode(self.settings.bot_parse_mode) if self.settings.bot_parse_mode else None
        return Bot(
            token=self.settings.bot_token_value,
            session=self.build_session(endpoint),
            default=DefaultBotProperties(parse_mode=parse_mode),
        )

    async def _is_healthy(self, bot: Bot, endpoint: BotEndpoint) -> bool:
        if not self.settings.proxy_healthcheck_enabled:
            return True
        try:
            me = await bot.get_me()
            logger.info("telegram_endpoint_healthy", endpoint=endpoint.name, bot_id=me.id, username=me.username)
            return True
        except Exception as exc:  # noqa: BLE001 - every transport/API error should trigger failover.
            logger.warning("telegram_endpoint_unhealthy", endpoint=endpoint.name, error=str(exc))
            await bot.session.close()
            return False

    async def create(self) -> Bot:
        endpoints = self.endpoints()
        if not endpoints:
            raise TelegramProxyUnavailable(
                "No Telegram proxy is configured. Set PROXY_URL_1 or enable ALLOW_DIRECT_TELEGRAM_FALLBACK."
            )

        for endpoint in endpoints:
            bot = self.build_bot(endpoint)
            logger.info("telegram_endpoint_try", endpoint=endpoint.name)
            if await self._is_healthy(bot, endpoint):
                logger.info("telegram_endpoint_selected", endpoint=endpoint.name)
                return bot

        raise TelegramProxyUnavailable("All configured Telegram API endpoints failed health checks.")


async def create_bot(settings: Settings) -> Bot:
    """Create the production Bot instance."""

    return await BotFactory(settings).create()


def create_dispatcher(*, routers: Iterable[object] = ()) -> Dispatcher:
    """Create Dispatcher and include routers when later application layers exist."""

    dispatcher = Dispatcher()
    for router in routers:
        dispatcher.include_router(router)  # type: ignore[arg-type]
    return dispatcher
