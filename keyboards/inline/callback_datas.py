from aiogram.utils.callback_data import CallbackData

select_currency_callback = CallbackData('choose', 'type', 'name')
select_notification_day = CallbackData('day', 'type', 'name')
select_notification_time = CallbackData('time', 'time', 'count')