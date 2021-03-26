import xmltodict
import requests
from aiogram import types

from utils.dates import get_today

CURRENCIES = {
        "AUD": "R01010",
        "GBP": "R01035",
        "BYR": "R01090",
        "DKK": "R01215",
        "USD": "R01235",
        "EUR": "R01239",
        "ISK": "R01310",
        "KZT": "R01335",
        "CAD": "R01350",
        "NOK": "R01535",
        "XDR": "R01589",
        "SGD": "R01625",
        "TRL": "R01700",
        "UAH": "R01720",
        "SEK": "R01770",
        "CHF": "R01775",
        "JPY": "R01820",
}


def get_currency(char_code: str, day: int, month: int, year: int) -> dict:
    if month < 10:
        month = '0' + str(month)
    if day < 10:
        day = '0' + str(day)

    req_url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'
    response = requests.get(req_url)
    xml_dict = xmltodict.parse(response.content)
    valutes = xml_dict['ValCurs']['Valute']

    for valute in valutes:
        if valute['@ID'] == CURRENCIES.get(char_code.upper()):
            return {'value': valute['Value'], 'name': valute['Name']}


def get_currencies_names():
    req_url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req=17/08/2003'
    response = requests.get(req_url)
    xml_dict = xmltodict.parse(response.content)
    valutes = xml_dict['ValCurs']['Valute']
    currencies = []
    for valute in valutes:
        currencies.append({'CharCode': valute['CharCode'], 'Name': valute['Name']})
    return currencies


async def get_rate(message: types.Message, char_code: str, date=None):
    if date is None:
        day = get_today().get('day')
        month = get_today().get('month')
        year = get_today().get('year')
    else:
        day, month, year = date.split('.')
    currency = get_currency(char_code, int(day), int(month), int(year))
    value = currency.get('value')
    name = currency.get('name')
    await message.answer(f'Курс {name} на {day}.{month}.{year} - {value} руб')

