"""Application entrypoint for telBotPropo.

Architecture:
    The entrypoint wires configuration, logging, the Telegram Bot, and the
    aiogram Dispatcher. Business routers, database lifecycle, Redis storage,
    middleware, and background jobs will be attached from their own modules in
    the next project stages.

Responsibility:
    - Configure structured logging and rotating file output.
    - Start long polling safely with proxy-aware Bot creation.
    - Close Telegram HTTP sessions on shutdown.

Dependencies:
    - asyncio for process lifecycle.
    - aiogram for polling.
    - structlog and stdlib logging for production logs.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from logging.handlers import RotatingFileHandler

import structlog

from bot import create_bot, create_dispatcher
from config import Settings, get_settings
from handlers import setup_routers
from admin import setup_admin_routers
from middlewares.rate_limit import RateLimitMiddleware
from middlewares.audit import AuditMiddleware


def configure_logging(settings: Settings) -> None:
    """Configure JSON structured logging with rotating file persistence."""

    settings.log_file.parent.mkdir(parents=True, exist_ok=True)
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    structlog.configure(
        processors=[*shared_processors, structlog.processors.JSONRenderer()],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, settings.log_level)),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = logging.Formatter("%(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    file_handler = RotatingFileHandler(
        settings.log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        handlers=[stream_handler, file_handler],
        force=True,
    )


async def run() -> None:
    """Run bot polling until interrupted by the process manager."""

    settings = get_settings()
    configure_logging(settings)
    logger = structlog.get_logger(__name__)
    logger.info("application_starting", app=settings.app_name, env=settings.app_env)

    bot = await create_bot(settings)
    dispatcher = create_dispatcher(routers=[*setup_routers(), *setup_admin_routers()])
    dispatcher.message.middleware(RateLimitMiddleware(settings))
    dispatcher.callback_query.middleware(AuditMiddleware())

    try:
        await dispatcher.start_polling(bot, drop_pending_updates=settings.bot_drop_pending_updates)
    finally:
        await bot.session.close()
        logger.info("application_stopped")


def main() -> None:
    """Synchronous console-script compatible entrypoint."""

    asyncio.run(run())


if __name__ == "__main__":
    main()
