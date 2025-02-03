from aiogram.fsm.state import StatesGroup, State


class TakeImageFromUser(StatesGroup):
    image = State()