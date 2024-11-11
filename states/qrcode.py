from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateQRCodeState(StatesGroup):
    user_name = State()