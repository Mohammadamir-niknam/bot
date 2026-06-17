from aiogram.fsm.state import State, StatesGroup
class AdminStates(StatesGroup):
    waiting_broadcast = State(); waiting_setting_value = State(); waiting_wallet_amount = State()
