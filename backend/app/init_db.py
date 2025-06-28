import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, create_db_and_tables
from app.mock_data import create_mock_data


async def main():
    """Инициализирует базу данных и создает тестовые данные"""
    # Создаем таблицы
    await create_db_and_tables()
    print("✅ Таблицы созданы")
    
    # Создаем тестовые данные
    async with AsyncSessionLocal() as session:
        await create_mock_data(session)
    
    print("✅ Тестовые данные созданы")


if __name__ == "__main__":
    asyncio.run(main()) 