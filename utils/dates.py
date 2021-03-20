import datetime


def get_today() -> dict:
    today = datetime.datetime.today()
    day = today.day
    if day < 10:
        day = f'0{day}'
    month = today.month
    if month < 10:
        month = f'0{month}'
    year = today.year
    return {'day': day, 'month': month, 'year': year}

get_today()