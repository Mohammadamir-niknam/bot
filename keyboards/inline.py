"""Inline keyboards."""
from __future__ import annotations
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import messages

def service_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=messages.BUY_STARS, callback_data="buy:stars")],
        [InlineKeyboardButton(text=messages.BUY_PREMIUM, callback_data="buy:premium")],
    ])

def payment_menu(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=messages.PAY_WITH_WALLET, callback_data=f"pay:wallet:{order_id}")],
        [InlineKeyboardButton(text=messages.SEND_RECEIPT, callback_data=f"pay:receipt:{order_id}")],
    ])
