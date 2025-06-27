import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, create_db_and_tables
from app.models import (
    User, Developer, Project, Building, Apartment, 
    ApartmentStats, PriceHistory, ViewsLog, Booking,
    Promotion, WebhookInbox, DynamicPricingConfig,
    UserRole, PropertyClass, ApartmentStatus, BookingStatus,
    ViewEvent, PriceChangeReason
)
from app.crud import (
    user, developer, project, building, apartment,
    apartment_stats, price_history, views_log, booking,
    dynamic_pricing_config
)
from datetime import datetime, timedelta
import random


async def create_sample_data():
    """Создает тестовые данные в базе данных"""
    async with AsyncSessionLocal() as session:
        print("🏗️ Создание тестовых данных...")
        
        # Создаем пользователей
        print("👥 Создание пользователей...")
        users_data = [
            {
                "email": "admin@example.com",
                "hashed_password": "hashed_password_123",
                "full_name": "Администратор",
                "role": UserRole.ADMIN,
                "phone": "+7 (999) 123-45-67"
            },
            {
                "email": "developer@example.com",
                "hashed_password": "hashed_password_123",
                "full_name": "Застройщик",
                "role": UserRole.DEVELOPER,
                "phone": "+7 (999) 234-56-78"
            },
            {
                "email": "buyer@example.com",
                "hashed_password": "hashed_password_123",
                "full_name": "Покупатель",
                "role": UserRole.BUYER,
                "phone": "+7 (999) 345-67-89"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            user_obj = await user.create(session, user_data)
            created_users.append(user_obj)
            print(f"✅ Создан пользователь: {user_obj.email}")
        
        # Создаем застройщиков
        print("🏢 Создание застройщиков...")
        developers_data = [
            {
                "name": "ПИК",
                "inn": "7736207543",
                "description": "Крупнейший застройщик России",
                "verified": True,
                "logo_url": "https://example.com/pik-logo.png",
                "website": "https://www.pik.ru"
            },
            {
                "name": "Самолет",
                "inn": "7705031674",
                "description": "Строительная компания",
                "verified": True,
                "logo_url": "https://example.com/samolet-logo.png",
                "website": "https://www.samolet.ru"
            },
            {
                "name": "Донстрой",
                "inn": "7705031675",
                "description": "Премиальный застройщик",
                "verified": False,
                "logo_url": "https://example.com/donstroy-logo.png",
                "website": "https://www.donstroy.ru"
            }
        ]
        
        created_developers = []
        for dev_data in developers_data:
            dev_obj = await developer.create(session, dev_data)
            created_developers.append(dev_obj)
            print(f"✅ Создан застройщик: {dev_obj.name}")
        
        # Создаем проекты
        print("🏗️ Создание проектов...")
        projects_data = [
            {
                "name": "ЖК ПИК-1",
                "developer_id": created_developers[0].id,
                "city": "Москва",
                "region_code": "77",
                "address": "ул. Тверская, 1",
                "description": "Современный жилой комплекс в центре Москвы",
                "class_type": PropertyClass.COMFORT,
                "completion_date": datetime.now() + timedelta(days=365),
                "total_apartments": 500,
                "available_apartments": 50
            },
            {
                "name": "ЖК Самолет-1",
                "developer_id": created_developers[1].id,
                "city": "Санкт-Петербург",
                "region_code": "78",
                "address": "Невский пр., 100",
                "description": "Жилой комплекс в историческом центре",
                "class_type": PropertyClass.BUSINESS,
                "completion_date": datetime.now() + timedelta(days=730),
                "total_apartments": 300,
                "available_apartments": 30
            },
            {
                "name": "ЖК Донстрой-1",
                "developer_id": created_developers[2].id,
                "city": "Москва",
                "region_code": "77",
                "address": "Кутузовский пр., 50",
                "description": "Премиальный жилой комплекс",
                "class_type": PropertyClass.PREMIUM,
                "completion_date": datetime.now() + timedelta(days=1095),
                "total_apartments": 200,
                "available_apartments": 20
            }
        ]
        
        created_projects = []
        for proj_data in projects_data:
            proj_obj = await project.create(session, proj_data)
            created_projects.append(proj_obj)
            print(f"✅ Создан проект: {proj_obj.name}")
        
        # Создаем корпуса
        print("🏢 Создание корпусов...")
        buildings_data = []
        for project_obj in created_projects:
            for i in range(1, 4):  # 3 корпуса на проект
                building_data = {
                    "project_id": project_obj.id,
                    "name": f"Корпус {i}",
                    "floors": random.randint(15, 25),
                    "completion_date": project_obj.completion_date + timedelta(days=30 * i)
                }
                buildings_data.append(building_data)
        
        created_buildings = []
        for building_data in buildings_data:
            building_obj = await building.create(session, building_data)
            created_buildings.append(building_obj)
        
        print(f"✅ Создано {len(created_buildings)} корпусов")
        
        # Создаем квартиры
        print("🏠 Создание квартир...")
        apartments_data = []
        for building_obj in created_buildings:
            for floor in range(1, building_obj.floors + 1):
                for apartment_num in range(1, 5):  # 4 квартиры на этаж
                    rooms = random.choice([1, 2, 3, 4])
                    area_total = random.uniform(30 + rooms * 10, 50 + rooms * 15)
                    area_living = area_total * 0.7
                    area_kitchen = area_total * 0.15
                    
                    base_price = area_total * random.uniform(150000, 300000)
                    current_price = base_price * random.uniform(0.95, 1.05)
                    
                    apartment_data = {
                        "building_id": building_obj.id,
                        "number": f"{floor}{apartment_num:02d}",
                        "floor": floor,
                        "rooms": rooms,
                        "area_total": round(area_total, 2),
                        "area_living": round(area_living, 2),
                        "area_kitchen": round(area_kitchen, 2),
                        "base_price": round(base_price, 2),
                        "current_price": round(current_price, 2),
                        "status": random.choice([ApartmentStatus.AVAILABLE, ApartmentStatus.RESERVED, ApartmentStatus.SOLD]),
                        "balcony": random.choice([True, False]),
                        "loggia": random.choice([True, False]),
                        "parking": random.choice([True, False])
                    }
                    apartments_data.append(apartment_data)
        
        created_apartments = []
        for apartment_data in apartments_data:
            apartment_obj = await apartment.create(session, apartment_data)
            created_apartments.append(apartment_obj)
        
        print(f"✅ Создано {len(created_apartments)} квартир")
        
        # Создаем статистику квартир
        print("📊 Создание статистики квартир...")
        for apartment_obj in created_apartments:
            stats_data = {
                "apartment_id": apartment_obj.id,
                "views_24h": random.randint(0, 50),
                "leads_24h": random.randint(0, 10),
                "bookings_24h": random.randint(0, 3),
                "days_on_site": random.randint(1, 365)
            }
            await apartment_stats.create(session, stats_data)
        
        print(f"✅ Создана статистика для {len(created_apartments)} квартир")
        
        # Создаем историю цен
        print("💰 Создание истории цен...")
        for apartment_obj in created_apartments:
            if random.random() < 0.3:  # 30% квартир имеют историю цен
                price_changes = random.randint(1, 5)
                current_price = apartment_obj.current_price
                
                for i in range(price_changes):
                    old_price = current_price
                    change_percent = random.uniform(-5, 5)
                    current_price = old_price * (1 + change_percent / 100)
                    
                    price_history_data = {
                        "apartment_id": apartment_obj.id,
                        "old_price": round(old_price, 2),
                        "new_price": round(current_price, 2),
                        "reason": random.choice([PriceChangeReason.DYNAMIC, PriceChangeReason.MANUAL]),
                        "description": f"Изменение цены на {change_percent:.1f}%",
                        "changed_at": datetime.now() - timedelta(days=random.randint(1, 30))
                    }
                    await price_history.create(session, price_history_data)
        
        print("✅ Создана история цен")
        
        # Создаем логи просмотров
        print("👀 Создание логов просмотров...")
        for apartment_obj in created_apartments:
            views_count = random.randint(0, 20)
            for _ in range(views_count):
                view_data = {
                    "apartment_id": apartment_obj.id,
                    "user_id": random.choice(created_users).id if random.random() < 0.7 else None,
                    "event": ViewEvent.VIEW,
                    "occurred_at": datetime.now() - timedelta(hours=random.randint(1, 168))
                }
                await views_log.create(session, view_data)
        
        print("✅ Созданы логи просмотров")
        
        # Создаем бронирования
        print("📅 Создание бронирований...")
        for apartment_obj in created_apartments:
            if apartment_obj.status == ApartmentStatus.RESERVED and random.random() < 0.5:
                booking_data = {
                    "apartment_id": apartment_obj.id,
                    "user_id": random.choice(created_users).id,
                    "status": BookingStatus.ACTIVE,
                    "booked_at": datetime.now() - timedelta(days=random.randint(1, 30))
                }
                await booking.create(session, booking_data)
        
        print("✅ Созданы бронирования")
        
        # Создаем конфигурацию динамического ценообразования
        print("⚙️ Создание конфигурации динамического ценообразования...")
        config_data = {
            "k1": 0.5,  # коэффициент просмотров
            "k2": 2.0,  # коэффициент лидов
            "k3": 5.0,  # коэффициент бронирований
            "enabled": True
        }
        await dynamic_pricing_config.create(session, config_data)
        
        print("✅ Создана конфигурация динамического ценообразования")
        
        print("🎉 Тестовые данные успешно созданы!")


async def main():
    """Основная функция"""
    print("🚀 Инициализация базы данных...")
    
    # Создаем таблицы
    await create_db_and_tables()
    print("✅ Таблицы созданы")
    
    # Создаем тестовые данные
    await create_sample_data()
    
    print("🎯 Инициализация завершена!")


if __name__ == "__main__":
    asyncio.run(main()) 