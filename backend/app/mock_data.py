from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Developer, Project, Building, Apartment, User,
    PropertyClass, ApartmentStatus, UserRole
)
from app.crud import developer, project, building, apartment, user


async def create_mock_data(session: AsyncSession):
    """Создает тестовые данные в базе данных"""
    
    # Создаем застройщика
    dev_data = {
        "name": "ПИК",
        "description": "Крупнейший застройщик России",
        "website": "https://pik.ru",
        "phone": "+7 (495) 123-45-67",
        "email": "info@pik.ru",
        "logo_url": "https://pik.ru/logo.png",
        "inn": "7713011336"
    }
    dev = await developer.create(session, dev_data)
    
    # Создаем проект
    project_data = {
        "name": "ЖК Зеленый парк",
        "description": """Жилой комплекс бизнес-класса в экологически чистом районе.
        Собственный парк, подземный паркинг, развитая инфраструктура.""",
        "city": "Москва",
        "region_code": "77",
        "address": "г. Москва, ул. Лесная, 25",
        "class_type": PropertyClass.BUSINESS,
        "completion_date": datetime.now() + timedelta(days=365),
        "developer_id": dev.id,
        "total_apartments": 450,
        "available_apartments": 150
    }
    proj = await project.create(session, project_data)
    
    # Создаем здание
    building_data = {
        "name": "Корпус 1",
        "floors": 25,
        "completion_date": datetime.now() + timedelta(days=365),
        "project_id": proj.id
    }
    build = await building.create(session, building_data)
    
    # Создаем квартиры
    apartments_data = [
        {
            "building_id": build.id,
            "number": "101",
            "floor": 10,
            "rooms": 2,
            "area_total": 65.5,
            "area_living": 45.2,
            "area_kitchen": 12.3,
            "base_price": 15_500_000,
            "current_price": 15_500_000,
            "status": ApartmentStatus.AVAILABLE,
            "balcony": True,
            "loggia": False,
            "parking": True
        },
        {
            "building_id": build.id,
            "number": "102",
            "floor": 10,
            "rooms": 3,
            "area_total": 85.7,
            "area_living": 60.3,
            "area_kitchen": 15.4,
            "base_price": 19_800_000,
            "current_price": 19_800_000,
            "status": ApartmentStatus.AVAILABLE,
            "balcony": True,
            "loggia": True,
            "parking": True
        },
        {
            "building_id": build.id,
            "number": "103",
            "floor": 10,
            "rooms": 1,
            "area_total": 42.3,
            "area_living": 28.1,
            "area_kitchen": 10.2,
            "base_price": 9_900_000,
            "current_price": 9_900_000,
            "status": ApartmentStatus.AVAILABLE,
            "balcony": False,
            "loggia": True,
            "parking": False
        }
    ]
    
    for apt_data in apartments_data:
        await apartment.create(session, apt_data)
    
    # Создаем тестового пользователя
    user_data = {
        "email": "test@example.com",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGpJ4vZKkOS",  # пароль: test123
        "full_name": "Тестов Тест Тестович",
        "role": UserRole.BUYER,
        "phone": "+7 (999) 123-45-67",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    await user.create(session, user_data)
    
    await session.commit()
    print("✅ Тестовые данные успешно созданы") 