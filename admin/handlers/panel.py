from __future__ import annotations
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import messages
from admin.filters.roles import SuperAdminFilter
from admin.keyboards.panel import admin_panel
router = Router(name="admin_panel")
@router.message(Command("admin"), SuperAdminFilter())
async def panel(message: Message) -> None:
    await message.answer(messages.ADMIN_PANEL, reply_markup=admin_panel())
