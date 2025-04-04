from aiogram.fsm.state import State, StatesGroup

class UserRateStates(StatesGroup):
    rate = State()
    phone_number = State()
    confirmed = State()