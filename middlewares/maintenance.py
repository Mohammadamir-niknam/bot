"""Maintenance mode middleware."""
from __future__ import annotations
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from config import Settings
import messages

class MaintenanceMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        if self.settings.debug:
            return await handler(event, data)
        if isinstance(event, Message) and event.text and event.text.startswith("/admin"):
            return await handler(event, data)
        return await handler(event, data)
