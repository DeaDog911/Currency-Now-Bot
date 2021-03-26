from aiogram.utils.callback_data import CallbackData

select_currency_callback = CallbackData('choose', 'type', 'name')
select_notification_day = CallbackData('day', 'type', 'name')
select_notification_time = CallbackData('set', 'time', 'count')
delete_notification_time = CallbackData('delete', 'time', 'count')