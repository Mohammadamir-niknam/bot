from __future__ import annotations
from aiogram import F, Router
from aiogram.types import Message
import messages
router = Router(name="support")
@router.message(F.text == messages.MAIN_MENU_SUPPORT)
async def support_menu(message: Message) -> None:
    await message.answer(messages.SUPPORT_MENU)
