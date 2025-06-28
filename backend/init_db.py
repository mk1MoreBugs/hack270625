#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""
import sys
import os
import asyncio
from sqlmodel import SQLModel
from app.database import create_db_and_tables, AsyncSessionLocal, async_engine
from app.mock_data import create_all_mock_data

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def init_db():
    """Инициализирует базу данных и создает тестовые данные"""
    # Удаляем все таблицы
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    
    # Создаем таблицы заново
    await create_db_and_tables()
    
    # Создаем тестовые данные
    async with AsyncSessionLocal() as session:
        await create_all_mock_data(session)


if __name__ == "__main__":
    print("Инициализация базы данных...")
    asyncio.run(init_db())
    print("База данных успешно инициализирована!") 