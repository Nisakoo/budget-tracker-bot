from typing import Any, Coroutine, Iterable
from abc import ABC, abstractmethod
import enum


class Period(enum.Enum):
    ALLTIME = 0
    DAY = 1
    WEEK = 2
    MONTH = 3


class BaseDataBase(ABC):
    @abstractmethod
    def __enter__(self) -> "BaseDataBase":
        raise NotImplementedError()
    
    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def add(
            self, user_id: int, is_income: bool,
            category_name: str, value: int) -> Coroutine[None, None, None]:
        raise NotImplementedError()
    
    @abstractmethod
    async def fetch(
            self, user_id: int, is_income: bool, period: Period) -> Coroutine[Iterable, None, None]:
        raise NotImplementedError()
    
    @abstractmethod
    async def get_categories(
            self, user_id: int, is_income: bool) -> Coroutine[Iterable, None, None]:
        raise NotImplementedError()