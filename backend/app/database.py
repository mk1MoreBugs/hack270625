from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Создаем асинхронный движок для PostgreSQL
async_engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,
    future=True
)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_and_tables():
    """Создает таблицы в базе данных"""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    """Получает асинхронную сессию для работы с базой данных"""
    async with AsyncSessionLocal() as session:
        yield session 