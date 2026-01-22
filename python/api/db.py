import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "3306")

ASYNC_DB_URL = (
    f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/demo?charset=utf8"
)

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)

async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
