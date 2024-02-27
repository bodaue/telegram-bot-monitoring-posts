from aiogram.fsm.state import StatesGroup, State


class ChannelState(StatesGroup):
    waiting_add = State()
    waiting_delete = State()


class KeywordState(StatesGroup):
    waiting_add = State()
    waiting_delete = State()
