"""Reply keyboards."""
from __future__ import annotations
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
import messages

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=messages.MAIN_MENU_BUY), KeyboardButton(text=messages.MAIN_MENU_REFERRAL)],
        [KeyboardButton(text=messages.MAIN_MENU_WALLET), KeyboardButton(text=messages.MAIN_MENU_TRUST)],
        [KeyboardButton(text=messages.MAIN_MENU_SUPPORT)],
    ], resize_keyboard=True, input_field_placeholder=messages.APP_STARTED)
