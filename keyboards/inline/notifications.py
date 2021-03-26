from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_currencies = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="USD", callback_data='choose:currency:USD'),
            InlineKeyboardButton(text="EUR", callback_data='choose:currency:EUR'),
        ],
        [
            InlineKeyboardButton(text="AUD", callback_data="choose:currency:AUD"),
            InlineKeyboardButton(text="GBP", callback_data="choose:currency:GBP"),
            InlineKeyboardButton(text="BYR", callback_data="choose:currency:BYR"),
            InlineKeyboardButton(text="DKK", callback_data="choose:currency:DKK"),
        ],
        [
            InlineKeyboardButton(text="ISK", callback_data="choose:currency:ISK"),
            InlineKeyboardButton(text="KZT", callback_data="choose:currency:KZT"),
            InlineKeyboardButton(text="CAD", callback_data="choose:currency:CAD"),
            InlineKeyboardButton(text="NOK", callback_data="choose:currency:NOK"),
        ],
        [

            InlineKeyboardButton(text="XDR", callback_data="choose:currency:XDR"),
            InlineKeyboardButton(text="SGD", callback_data="choose:currency:SGD"),
            InlineKeyboardButton(text="TRL", callback_data="choose:currency:TRL"),
            InlineKeyboardButton(text="UAH", callback_data="choose:currency:UAH"),
        ],
        [

            InlineKeyboardButton(text="SEK", callback_data="choose:currency:SEK"),
            InlineKeyboardButton(text="CHF", callback_data="choose:currency:CHF"),
            InlineKeyboardButton(text="JPY", callback_data="choose:currency:JPY"),
        ],
    ]
)

days_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Каждый день', callback_data='day:weekday:all'),
        ],
        [
            InlineKeyboardButton(text='Понедельник', callback_data='day:weekday:monday'),
            InlineKeyboardButton(text='Вторник', callback_data='day:weekday:tuesday'),
        ],
        [
            InlineKeyboardButton(text='Среда', callback_data='day:weekday:wednesday'),
            InlineKeyboardButton(text='Четверг', callback_data='day:weekday:thursday'),
        ],
        [
            InlineKeyboardButton(text='Пятница', callback_data='day:weekday:friday'),
            InlineKeyboardButton(text='Суббота', callback_data='day:weekday:saturday'),
            InlineKeyboardButton(text='Воскресенье', callback_data='day:weekday:sunday'),
        ]
    ]
)


def get_hours_keyboard(except_hours: list = None):
    hours_keyboard = InlineKeyboardMarkup(row_width=4)
    for i in range(24):
        if i not in except_hours:
            t = str(i)
            t_int = i
            if i < 10:
                t = '0' + str(i)
            button = InlineKeyboardButton(text=f'❌ {t}:00', callback_data=f'set:hour:{t_int}')
        else:
            t = str(i)
            t_int = i
            if i < 10:
                t = '0' + str(i)
            button = InlineKeyboardButton(text=f'✅ {t}:00', callback_data=f'set:hour:{t_int}')
        hours_keyboard.insert(button)
    return hours_keyboard


def get_minutes_keyboard(hour: int, except_minutes: list = None):
    hour_str = str(hour)
    if hour < 10:
        hour_str = '0' + str(hour)
    minutes_keyboard = InlineKeyboardMarkup(row_width=5)
    for i in range(0, 60, 5):
        if i not in except_minutes:
            t_int = i
            t = str(i)
            if i < 10:
                t = '0' + str(i)
            button = InlineKeyboardButton(text=f'❌ {hour_str}:{t}', callback_data=f'set:minute:{t_int}')
        else:
            t_int = i
            t = str(i)
            if i < 10:
                t = '0' + str(i)
            button = InlineKeyboardButton(text=f'✅ {hour_str}:{t}', callback_data=f'delete:minute:{t_int}')
        minutes_keyboard.insert(button)
    return minutes_keyboard
