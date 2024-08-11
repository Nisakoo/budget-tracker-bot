from typing import Coroutine, Callable, Iterable
import asyncio
from datetime import datetime, timedelta

import aiosqlite
from aiosqlite import Row

from db.base_database import BaseDataBase, Period


class SqliteDB(BaseDataBase):
    def __init__(self, database_path: str) -> None:
        self._database_path = database_path

    @staticmethod
    def ensure_connection(func) -> Callable:
        async def inner(self: "SqliteDB", *args, **kwargs) -> Coroutine[None, None, None]:
            if not hasattr(self, "_conn"):
                self._conn = await aiosqlite.connect(self._database_path)
                await self._create_table()

            return await func(self, *args, **kwargs)

        return inner

    def __enter__(self) -> BaseDataBase:
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if hasattr(self, "_conn"):
            asyncio.run(self._conn.close())

    @ensure_connection
    async def add(
            self, user_id: int, is_income: bool,
            category_name: str, amount: int) -> Coroutine[None, None, None]:
        await self._conn.execute_insert(
            """INSERT INTO data
            (user_id, created, is_income, category, amount)
            VALUES (?, ?, ?, ?, ?)""",
            (user_id, datetime.now().date(), is_income, category_name, amount)
        )
        await self._conn.commit()

    @ensure_connection
    async def fetch(
            self, user_id: int, is_income: bool, period: Period) -> Coroutine[Iterable[Row], None, None]:
        if period == Period.ALLTIME:
            return await self._conn.execute_fetchall(
                "SELECT created, is_income, category, amount FROM data WHERE user_id = ?",
                (user_id,)
            )

        start_date = datetime.now().date()
        offset = "+1 day"

        if period == Period.WEEK:
            start_date = start_date - timedelta(days=start_date.weekday())
            offset = "+7 days"
        elif period == Period.MONTH:
            start_date = datetime(start_date.year, start_date.month, 1)
            offset = "+1 month"

        return await self._conn.execute_fetchall(
            """SELECT category, SUM(amount) FROM data
            WHERE user_id = ? AND is_income = ? AND created >= date(?) AND created < date(?, ?)
            GROUP BY category""",
            (user_id, is_income, start_date, start_date, offset)
        )
        
    
    @ensure_connection
    async def get_categories(
            self, user_id: int, is_income: bool) -> Coroutine[Iterable, None, None]:
        categories = await self._conn.execute_fetchall(
            "SELECT DISTINCT category FROM data WHERE user_id = ? AND is_income = ?",
            (user_id, is_income)
        )

        return [i[0] for i in categories]

    @ensure_connection
    async def _create_table(self) -> Coroutine[None, None, None]:
        await self._conn.execute(
            """CREATE TABLE IF NOT EXISTS data
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, created TEXT,
            is_income BOOLEAN, category TEXT, amount REAL)"""
        )