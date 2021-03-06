from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.currency import get_currencies_names, get_rate


@dp.message_handler(Command('all_currencies', prefixes='!/'))
async def get_all_currencies(message: types.Message):
    s = 'Все валюты, которые поддерживает бот: \n \n'
    for currency in get_currencies_names():
        s += f'{currency.get("Name")} - {currency.get("CharCode")} \n'
    await message.answer(s)


@dp.message_handler(Command('currency_usd', prefixes='!/'))
async def get_dollar_rate(message: types.Message):
    if len(message.text.split(' ')) == 2:
        date = message.text.split(' ')[1]
    else:
        date = None
    await get_rate(message, 'usd', date)


@dp.message_handler(Command('currency_eur', prefixes='!/'))
async def get_euro_rate(message: types.Message):
    if len(message.text.split(' ')) == 2:
        date = message.text.split(' ')[1]
    else:
        date = None
    await get_rate(message, 'eur', date)


@dp.message_handler(Command('currency', prefixes='!/'))
async def get_currency_rate(message: types.Message):
    try:
        if len(message.text.split(' ')) == 3:
            date = message.text.split(' ')[2]
        else:
            date = None
        currency = message.text.split(' ')[1].lower()
        await get_rate(message, currency, date)
    except IndexError:
        await message.answer('Укажите валюту - /currency aud [date]')

