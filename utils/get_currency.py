import xmltodict
import requests


def get_currency(char_code, day, month, year) -> dict:
    currencies = {
        'usd': 'R01235',
        'eur': 'R01239',
        'aud': 'R01010',
    }
    req_url = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{year}'
    response = requests.get(req_url)
    xml_dict = xmltodict.parse(response.content)
    valutes = xml_dict['ValCurs']['Valute']
    for valute in valutes:
        if valute['@ID'] == currencies.get(char_code):
            return {'value': valute['Value'], 'name': valute['Name']}