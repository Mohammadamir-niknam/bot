from __future__ import annotations
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
import messages
from keyboards.reply import main_menu
router = Router(name="common_start")
@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(messages.START.format(name=message.from_user.full_name if message.from_user else ""), reply_markup=main_menu())
