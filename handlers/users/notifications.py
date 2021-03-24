from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
import asyncio

from keyboards.inline.callback_datas import select_currency_callback, select_notification_day, select_notification_time
from keyboards.inline.notifications import keyboard_currencies, days_keyboard, get_hours_keyboard, get_minutes_keyboard
from loader import dp, db
from states.notifications import Notification
from utils.misc.logging import logging


@dp.message_handler(Command('set_notifications', prefixes='!/'), state=None)
async def set_notifications(message: types.Message):
    await message.answer('Выберите валюту', reply_markup=keyboard_currencies)
    await Notification.currency.set()


@dp.callback_query_handler(select_currency_callback.filter(type='currency'), state=Notification.currency)
async def set_currency_notify(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    currency = callback_data.get('name')
    await state.update_data(currency=currency)

    await call.message.answer(f'Выберите день для уведомления', reply_markup=days_keyboard)
    await Notification.weekday.set()


@dp.callback_query_handler(select_notification_day.filter(type='weekday'), state=Notification.weekday)
async def set_notification_day(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    weekday = callback_data.get('name')
    await state.update_data(weekday=weekday)

    await call.message.answer(f'Выберите время для уведомления', reply_markup=get_hours_keyboard())
    await Notification.time_hour.set()


@dp.callback_query_handler(select_notification_time.filter(time='hour'), state=Notification.time_hour)
async def set_notification_hour(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    time_hour = int(callback_data.get('count'))
    await state.update_data(time_hour=time_hour)

    await call.message.answer(f'Выберите время для уведомления', reply_markup=get_minutes_keyboard(time_hour))
    await Notification.time_minutes.set()


@dp.callback_query_handler(select_notification_time.filter(time='minute'), state=Notification.time_minutes)
async def set_notification_minute(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)

    time_minutes = int(callback_data.get('count'))
    notification_dict = await state.get_data()
    await state.finish()

    await db.add_notification(telegram_id=call.from_user.id,
                              currency_char_code=notification_dict.get('currency'),
                              weekday=notification_dict.get('weekday'),
                              time_hour=notification_dict.get('time_hour'),
                              time_minutes=time_minutes)

    logging.log(logging.INFO, f'Добавлена запись {notification_dict}')


@dp.async_task
async def print_hello():
    await asyncio.sleep(5)
    print('hello')