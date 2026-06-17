from __future__ import annotations
from aiogram import F, Router
from aiogram.types import Message
import messages
router = Router(name="referral")
@router.message(F.text == messages.MAIN_MENU_REFERRAL)
async def referral_info(message: Message) -> None:
    username = (await message.bot.get_me()).username
    await message.answer(messages.REFERRAL_INFO.format(link=f"https://t.me/{username}?start=ref_{message.from_user.id}", points=0))
