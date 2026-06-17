"""In-memory anti-spam middleware."""
from __future__ import annotations
import time
from collections import defaultdict, deque
from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from config import Settings
import messages

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, settings: Settings) -> None:
        self.max_requests = settings.rate_limit_max_requests; self.window = settings.rate_limit_window_seconds
        self.bucket: dict[int, deque[float]] = defaultdict(deque)
    async def __call__(self, handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: dict[str, Any]) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
        now = time.monotonic(); q = self.bucket[user.id]
        while q and now - q[0] > self.window: q.popleft()
        if len(q) >= self.max_requests:
            if isinstance(event, Message): await event.answer(messages.RATE_LIMITED)
            return None
        q.append(now); return await handler(event, data)
