from datetime import datetime, timedelta
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def create_user(self, username, full_name, telegram_id, role='user', joined_at=datetime.now()):
        sql = "INSERT INTO users (username, full_name, telegram_id, role, joined_at) VALUES($1, $2, $3, $4, $5) RETURNING *"
        return await self.execute(sql, username, full_name, telegram_id, role, joined_at, fetchrow=True)

    async def select_user(self, user_id):
        sql = "SELECT * FROM users WHERE id = $1"
        return await self.execute(sql, user_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_users_last_week(self):
        # Hozirgi sanani olish
        today = datetime.now()
        # Bir hafta oldin sanani hisoblash
        one_week_ago = today - timedelta(days=7)

        sql = """
        SELECT * FROM users 
        WHERE joined_at <= $1 
          AND role = 'user'
        """
        return await self.execute(sql, one_week_ago, fetch=True)

    async def update_user(self, user_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE users SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), user_id, fetchrow=True)

    async def delete_user(self, user_id):
        sql = "DELETE FROM users WHERE id = $1 RETURNING *"
        return await self.execute(sql, user_id, fetchrow=True)

    # for qr codes
    async def create_qr_code(self, information, user_name, is_active=True, created_at=datetime.now()):
        sql = """
        INSERT INTO qrcode (information, user_name, is_active, created_at) 
        VALUES ($1, $2, $3, $4) RETURNING *
        """
        return await self.execute(sql, information, user_name, is_active, created_at, fetchrow=True)

    async def select_qr_code(self, qr_code_id):
        sql = "SELECT * FROM qrcode WHERE id = $1"
        return await self.execute(sql, qr_code_id, fetchrow=True)

    async def select_all_qr_codes(self):
        sql = "SELECT * FROM qrcode"
        return await self.execute(sql, fetch=True)

    async def select_qr_codes(self, **kwargs):
        sql = "SELECT * FROM qrcode WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_qr_code(self, qr_code_id, **kwargs):
        set_clause = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(kwargs.keys())])
        sql = f"UPDATE qrcode SET {set_clause} WHERE id = ${len(kwargs) + 1} RETURNING *"
        return await self.execute(sql, *kwargs.values(), qr_code_id, fetchrow=True)

    async def delete_qr_code(self, qr_code_id):
        sql = "DELETE FROM qrcode WHERE id = $1 RETURNING *"
        return await self.execute(sql, qr_code_id, fetchrow=True)