import asyncio

from aiogram import executor

from loader import db
from utils.notify_admins import on_startup_notify
from utils.notify_users import notify_users

NOTIFICATIONS_DELAY = 60


async def on_startup(dispatcher):
    print('Создание базу данных')
    await db.create()
    print('Готово')

    print('Создание таблицы')
    await db.create_notifications_table()
    print('Готово')

    await on_startup_notify(dispatcher)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(NOTIFICATIONS_DELAY, repeat, coro, loop)


if __name__ == '__main__':
    from loader import dp
    import handlers
    import filters
    loop = asyncio.get_event_loop()
    loop.call_later(NOTIFICATIONS_DELAY, repeat, notify_users, loop)
    executor.start_polling(dp, on_startup=on_startup)
