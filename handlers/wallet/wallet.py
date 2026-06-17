from __future__ import annotations
from aiogram import F, Router
from aiogram.types import Message
import messages
router = Router(name="wallet")
@router.message(F.text == messages.MAIN_MENU_WALLET)
async def wallet_menu(message: Message) -> None:
    await message.answer(messages.WALLET_BALANCE.format(balance=0))
