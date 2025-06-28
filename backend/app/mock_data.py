from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    Developer, Project, Building, Apartment, User,
    PropertyClass, ApartmentStatus, UserRole, Promotion,
    Booking, ViewsLog, ApartmentStats, ViewEvent
)
from app.crud import (
    developer, project, building, apartment, user,
    promotion, booking, views_log, apartment_stats
)


async def create_mock_data(session: AsyncSession):
    """Создает тестовые данные в базе данных"""
    
    # Создаем пользователей разных ролей
    users_data = [
        {
            "email": "buyer@example.com",
            "hashed_password": "hashed_password",
            "role": UserRole.BUYER,
            "display_name": "Иван Покупателев",
            "phone": "+7 (999) 123-45-67"
        },
        {
            "email": "developer@pik.ru",
            "hashed_password": "hashed_password",
            "role": UserRole.DEVELOPER,
            "display_name": "ПИК Менеджер",
            "phone": "+7 (495) 123-45-67"
        },
        {
            "email": "admin@association.ru",
            "hashed_password": "hashed_password",
            "role": UserRole.ADMIN,
            "display_name": "Администратор Системы",
            "phone": "+7 (495) 765-43-21"
        }
    ]
    
    for user_data in users_data:
        await user.create(session, user_data)
    
    # Создаем первого застройщика (ПИК)
    pik_data = {
        "name": "ПИК",
        "description": "Крупнейший застройщик России",
        "website": "https://pik.ru",
        "logo_url": "https://pik.ru/logo.png",
        "inn": "7713011336",
        "verified": True
    }
    pik = await developer.create(session, pik_data)
    
    # Создаем проект ПИК
    pik_project_data = {
        "name": "ПИК Парк",
        "city": "Москва",
        "region_code": "77",
        "address": "ул. Парковая, 15",
        "description": "Современный жилой комплекс бизнес-класса",
        "class_type": PropertyClass.BUSINESS,
        "developer_id": pik.id,
        "completion_date": datetime(2024, 12, 1),
        "total_apartments": 500,
        "available_apartments": 350
    }
    pik_project = await project.create(session, pik_project_data)
    
    # Создаем корпус в проекте ПИК
    pik_building_data = {
        "name": "Корпус А",
        "project_id": pik_project.id,
        "floors": 25,
        "completion_date": datetime(2024, 12, 1)
    }
    pik_building = await building.create(session, pik_building_data)
    
    # Создаем квартиры в корпусе ПИК
    pik_apartments_data = [
        {
            "number": "101",
            "floor": 10,
            "rooms": 2,
            "area_total": 60.5,
            "area_living": 40.0,
            "area_kitchen": 15.0,
            "base_price": 15000000.0,
            "current_price": 15000000.0,
            "building_id": pik_building.id,
            "status": ApartmentStatus.AVAILABLE,
            "balcony": True,
            "loggia": False,
            "parking": False
        },
        {
            "number": "102",
            "floor": 10,
            "rooms": 3,
            "area_total": 85.5,
            "area_living": 60.0,
            "area_kitchen": 18.0,
            "base_price": 20000000.0,
            "current_price": 20000000.0,
            "building_id": pik_building.id,
            "status": ApartmentStatus.AVAILABLE,
            "balcony": True,
            "loggia": True,
            "parking": True
        }
    ]
    
    for apt_data in pik_apartments_data:
        await apartment.create(session, apt_data)
    
    # Создаем второго застройщика (СтройИнвест)
    stroyinvest_data = {
        "name": "СтройИнвест",
        "description": "Надежный застройщик",
        "website": "https://stroyinvest.ru",
        "inn": "7701234567",
        "logo_url": "https://stroyinvest.ru/logo.png",
        "verified": False
    }
    stroyinvest = await developer.create(session, stroyinvest_data)
    
    # Создаем проект СтройИнвест
    stroyinvest_project_data = {
        "name": "Зеленый квартал",
        "city": "Москва",
        "region_code": "77",
        "address": "ул. Ленина, 123",
        "description": "Современный жилой комплекс",
        "class_type": PropertyClass.COMFORT,
        "developer_id": stroyinvest.id,
        "completion_date": datetime(2025, 6, 1),
        "total_apartments": 300,
        "available_apartments": 250
    }
    stroyinvest_project = await project.create(session, stroyinvest_project_data)
    
    # Создаем корпус в проекте СтройИнвест
    stroyinvest_building_data = {
        "name": "Корпус 1",
        "project_id": stroyinvest_project.id,
        "floors": 25,
        "completion_date": datetime(2025, 6, 1)
    }
    stroyinvest_building = await building.create(session, stroyinvest_building_data)
    
    # Создаем квартиру в корпусе СтройИнвест
    stroyinvest_apartment_data = {
        "number": "123",
        "floor": 12,
        "rooms": 2,
        "area_total": 65.5,
        "area_living": 45.0,
        "area_kitchen": 12.0,
        "base_price": 8500000.0,
        "current_price": 8500000.0,
        "building_id": stroyinvest_building.id,
        "status": ApartmentStatus.AVAILABLE,
        "balcony": True,
        "loggia": False,
        "parking": True
    }
    stroyinvest_apartment = await apartment.create(session, stroyinvest_apartment_data)
    
    # Создаем акции
    promotions_data = [
        {
            "name": "Скидка 5% при 100% оплате",
            "discount_percent": 5.0,
            "starts_at": datetime.utcnow(),
            "ends_at": datetime.utcnow() + timedelta(days=30),
            "conditions": '{"payment_type": "full"}'
        },
        {
            "name": "Паркинг в подарок",
            "discount_percent": 100.0,
            "starts_at": datetime.utcnow(),
            "ends_at": datetime.utcnow() + timedelta(days=60),
            "conditions": '{"min_rooms": 3}'
        }
    ]
    
    for promo_data in promotions_data:
        await promotion.create(session, promo_data)
    
    # Создаем статистику просмотров и бронирований
    views_data = [
        {
            "apartment_id": stroyinvest_apartment.id,
            "user_id": 1,  # buyer
            "event": ViewEvent.VIEW,
            "occurred_at": datetime.utcnow() - timedelta(hours=12)
        },
        {
            "apartment_id": stroyinvest_apartment.id,
            "user_id": 1,  # buyer
            "event": ViewEvent.FAVOURITE,
            "occurred_at": datetime.utcnow() - timedelta(hours=11)
        }
    ]
    
    for view_data in views_data:
        await views_log.create(session, view_data)
    
    # Создаем статистику квартир
    stats_data = [
        {
            "apartment_id": stroyinvest_apartment.id,
            "views_24h": 10,
            "leads_24h": 2,
            "bookings_24h": 1,
            "days_on_site": 30
        }
    ]
    
    for stat_data in stats_data:
        await apartment_stats.create(session, stat_data)
    
    await session.commit()
    print("✅ Тестовые данные успешно созданы") 