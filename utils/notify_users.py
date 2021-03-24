import asyncio
from loader import db, dp
from datetime import datetime

from utils.currency import get_currency


def get_date() -> dict:
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    day = int(datetime.now().day)
    month = int(datetime.now().month)
    year = int(datetime.now().year)
    weekday = weekdays[datetime.now().weekday()]
    hour = datetime.now().hour
    minute = datetime.now().minute
    return {
        'day': day,
        'month': month,
        'year': year,
        'weekday': weekday,
        'hour': hour,
        'minute': minute,
    }


async def notify_users():
    notifications = await db.select_notifications()
    date = get_date()
    for notification in notifications:
        if date.get("weekday") == notification.get('weekday') or notification.get('weekday') == 'all':
            if notification.get('time_hour') == date.get('hour') and notification.get('time_minutes') == date.get('minute'):
                currency_char_code = notification.get('currency_char_code')
                currency = get_currency(currency_char_code, date.get('day'), date.get('month'), date.get('year'))
                currency_val = currency.get("value")
                currency_name = currency.get('name')
                telegram_id = notification.get('telegram_id')
                text = f"Курс {currency_name} на {date.get('day')}.{date.get('month')}.{date.get('year')} - {currency_val} руб"
                await dp.bot.send_message(chat_id=telegram_id, text=text)