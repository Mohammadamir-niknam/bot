from __future__ import annotations
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import messages

def admin_panel() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=messages.ADMIN_ORDERS, callback_data="admin:orders"), InlineKeyboardButton(text=messages.ADMIN_USERS, callback_data="admin:users")],
        [InlineKeyboardButton(text=messages.ADMIN_WALLET, callback_data="admin:wallet"), InlineKeyboardButton(text=messages.ADMIN_TICKETS, callback_data="admin:tickets")],
        [InlineKeyboardButton(text=messages.ADMIN_SETTINGS, callback_data="admin:settings"), InlineKeyboardButton(text=messages.ADMIN_STATS, callback_data="admin:stats")],
    ])
