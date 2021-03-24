from typing import Union

import asyncpg
from asyncpg import Connection, Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False, ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_notifications_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Notifications(
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL,
            currency_char_code VARCHAR(3) NOT NULL,
            weekday VARCHAR(10) NULL,
            time_hour INT NULL,
            time_minutes INT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def select_notifications(self):
        sql = "SELECT * FROM Notifications"
        return await self.execute(sql, fetch=True)

    async def count_notifications(self):
        sql = "SELECT COUNT(*) FROM Notifications"
        return await self.execute(sql, fetchval=True)

    async def select_user_notifications(self, telegram_id, currency_char_code=None):
        if currency_char_code:
            sql = "SELECT * FROM Notifications WHERE telegram_id = $1 AND currency_char_code = $2"
            return await self.execute(sql, telegram_id, currency_char_code, fetch=True)
        else:
            sql = "SELECT * FROM Notifications WHERE telegram_id = $1"
            return await self.execute(sql, telegram_id, fetch=True)

    async def add_notification(self, telegram_id: int, currency_char_code: str, weekday: str = None,
                               time_hour: int = None, time_minutes: int = None):
        sql = "INSERT INTO Notifications (telegram_id, currency_char_code, weekday, time_hour, time_minutes) " \
              "VALUES ($1, $2, $3, $4, $5) returning *"
        return await self.execute(sql, telegram_id, currency_char_code, weekday, time_hour, time_minutes, fetchrow=True)

    async def update_notification_hour(self, telegram_id: int, currency_char_code: str, weekday: str, time_hour: int):
        sql = "UPDATE Notifications SET time_hour=$1 WHERE telegram_id=$2 AND weekday=$3 AND currency_char_code=$4"
        await self.execute(sql, time_hour, telegram_id, weekday, currency_char_code, execute=True)

    async def update_notification_minute(self, telegram_id: int, weekday: str, time_hour: int, time_minutes: int,
                                         currency_char_code: str):
        sql = "UPDATE Notifications SET time_minutes = $1 WHERE telegram_id = $2 AND time_hour = $3 AND weekday = $4" \
              "AND currency_char_code = $5"
        await self.execute(sql, time_minutes, telegram_id, time_hour, weekday, currency_char_code, execute=True)

    async def delete_notification(self, id: int):
        await self.execute("DELETE FROM Notifications WHERE id = $1", id, execute=True)

    async def delete_all_notifications(self):
        await self.execute("DELETE FROM Notifications WHERE TRUE", execute=True)

    async def drop_notifications(self):
        await self.execute("DROP TABLE Notifications", execute=True)
