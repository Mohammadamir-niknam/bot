from __future__ import annotations
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import get_settings

class SuperAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return bool(message.from_user and message.from_user.id in get_settings().super_admin_ids)
