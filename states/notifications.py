from aiogram.dispatcher.filters.state import StatesGroup, State


class Notification(StatesGroup):
    currency = State()
    weekday = State()
    time_hour = State()
    time_minutes = State()
