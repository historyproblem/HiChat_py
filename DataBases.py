from typing import Annotated
import asyncio
from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL, text
from Config import settings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    # echo=True
)
async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

str_50 = Annotated[str, 50]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_50: String(50)
    }

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше
            finally:
                await session.close()  # Закрываем сессию

    return wrapper