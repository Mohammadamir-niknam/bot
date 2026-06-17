"""Mandatory channel membership middleware placeholder with Bot API check hook."""
from __future__ import annotations
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message
import messages

class ChannelCheckMiddleware(BaseMiddleware):
    def __init__(self, enabled: bool = False, channel_id: str | None = None) -> None:
        self.enabled = enabled; self.channel_id = channel_id
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        if not self.enabled or not self.channel_id:
            return await handler(event, data)
        user = data.get("event_from_user"); bot: Bot | None = data.get("bot")
        if not user or not bot:
            return await handler(event, data)
        member = await bot.get_chat_member(self.channel_id, user.id)
        if member.status in {"left", "kicked"}:
            if isinstance(event, Message): await event.answer(messages.CHANNEL_REQUIRED)
            return None
        return await handler(event, data)
