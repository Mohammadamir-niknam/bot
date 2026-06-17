from __future__ import annotations
from aiogram import F, Router
from aiogram.types import Message
import messages
from keyboards.inline import service_menu
router = Router(name="user_menu")
@router.message(F.text == messages.MAIN_MENU_BUY)
async def buy_menu(message: Message) -> None:
    await message.answer(messages.BUY_MENU, reply_markup=service_menu())
@router.message(F.text == messages.MAIN_MENU_TRUST)
async def trust(message: Message) -> None:
    await message.answer(messages.TRUST_TEXT_FALLBACK)
