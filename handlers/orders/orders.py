from __future__ import annotations
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import messages
from states.user import OrderStates
router = Router(name="orders")
@router.callback_query(F.data == "buy:stars")
async def ask_stars(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(OrderStates.waiting_stars_count)
    await callback.message.answer(messages.ENTER_STARS_COUNT.format(minimum=50))
    await callback.answer()
@router.message(OrderStates.waiting_stars_count)
async def receive_stars(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit() or int(message.text) < 50:
        await message.answer(messages.INVALID_STARS_COUNT.format(minimum=50)); return
    await state.update_data(quantity=int(message.text)); await state.clear()
    await message.answer(messages.ORDER_CREATED)
