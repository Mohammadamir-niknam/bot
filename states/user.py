from aiogram.fsm.state import State, StatesGroup
class OrderStates(StatesGroup):
    waiting_stars_count = State(); waiting_receipt = State()
class WalletStates(StatesGroup):
    waiting_charge_amount = State()
class SupportStates(StatesGroup):
    waiting_subject = State(); waiting_message = State()
