import asyncio
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import (
    crud_developer, crud_project, crud_building, crud_property,
    crud_property_address, crud_property_price, crud_residential_property,
    crud_property_features, crud_property_analytics, crud_commercial_property,
    crud_house_land, crud_property_media, crud_promo_tag, crud_mortgage_program,
    crud_promotion, crud_views_log, crud_booking
)
from app.models import (
    PropertyType, PropertyCategory, PropertyStatus, PropertyFeatures
)


async def create_mock_data(session: AsyncSession):
    """Создает тестовые данные для Краснодарского края"""
    
    print("🏗️ Создание застройщиков...")
    
    # Создаем 5 застройщиков Краснодарского края
    developers_data = [
        {"name": "Краснодарстрой"},
        {"name": "ЮгСтройИнвест"},
        {"name": "КубаньДомСтрой"},
        {"name": "СочиСтройГрупп"},
        {"name": "АнапаСтрой"}
    ]
    
    developers = []
    for dev_data in developers_data:
        developer = await crud_developer.create(session, dev_data)
        developers.append(developer)
        print(f"✅ Создан застройщик: {developer.name}")
    
    print("🏢 Создание проектов...")
    
    # Создаем 6 проектов для каждого застройщика
    projects_data = [
        # Краснодарстрой
        {"name": "ЖК Краснодарский", "developer_id": developers[0].id},
        {"name": "ЖК Центральный", "developer_id": developers[0].id},
        {"name": "ЖК Западный", "developer_id": developers[0].id},
        {"name": "ЖК Восточный", "developer_id": developers[0].id},
        {"name": "ЖК Северный", "developer_id": developers[0].id},
        {"name": "ЖК Южный", "developer_id": developers[0].id},
        
        # ЮгСтройИнвест
        {"name": "ЖК Морской", "developer_id": developers[1].id},
        {"name": "ЖК Приморский", "developer_id": developers[1].id},
        {"name": "ЖК Парковый", "developer_id": developers[1].id},
        {"name": "ЖК Садовый", "developer_id": developers[1].id},
        {"name": "ЖК Лесной", "developer_id": developers[1].id},
        {"name": "ЖК Речной", "developer_id": developers[1].id},
        
        # КубаньДомСтрой
        {"name": "ЖК Кубань", "developer_id": developers[2].id},
        {"name": "ЖК Донской", "developer_id": developers[2].id},
        {"name": "ЖК Азовский", "developer_id": developers[2].id},
        {"name": "ЖК Черноморский", "developer_id": developers[2].id},
        {"name": "ЖК Кавказский", "developer_id": developers[2].id},
        {"name": "ЖК Степной", "developer_id": developers[2].id},
        
        # СочиСтройГрупп
        {"name": "ЖК Сочи Центр", "developer_id": developers[3].id},
        {"name": "ЖК Адлер", "developer_id": developers[3].id},
        {"name": "ЖК Хоста", "developer_id": developers[3].id},
        {"name": "ЖК Лазаревское", "developer_id": developers[3].id},
        {"name": "ЖК Красная Поляна", "developer_id": developers[3].id},
        {"name": "ЖК Олимпийский", "developer_id": developers[3].id},
        
        # АнапаСтрой
        {"name": "ЖК Анапа Центр", "developer_id": developers[4].id},
        {"name": "ЖК Витязево", "developer_id": developers[4].id},
        {"name": "ЖК Джемете", "developer_id": developers[4].id},
        {"name": "ЖК Сукко", "developer_id": developers[4].id},
        {"name": "ЖК Благовещенская", "developer_id": developers[4].id},
        {"name": "ЖК Утриш", "developer_id": developers[4].id}
    ]
    
    projects = []
    for proj_data in projects_data:
        project = await crud_project.create(session, proj_data)
        projects.append(project)
        print(f"✅ Создан проект: {project.name}")
    
    print("🏠 Создание зданий...")
    
    # Создаем 5 зданий для каждого проекта
    buildings = []
    for project in projects:
        for i in range(5):
            building_data = {
                "name": f"Дом {i+1}",
                "project_id": project.id,
                "floors": 9 + (i % 5),  # 9-13 этажей
                "completion_year": 2023 + (i % 3),  # 2023-2025
                "completion_status": 'completed' if i < 3 else 'in_progress'
            }
            building = await crud_building.create(session, building_data)
            buildings.append(building)
            print(f"✅ Создано здание: {building.id} в проекте {project.name}")
    
    print("🏘️ Создание объектов недвижимости...")
    
    # Создаем 6 объектов недвижимости для каждого здания
    properties = []
    for building in buildings:
        for i in range(6):
            property_data = {
                "building_id": building.id,
                "project_id": building.project_id,
                "developer_id": next(p.developer_id for p in projects if p.id == building.project_id),
                "property_type": PropertyType.RESIDENTIAL,
                "category": PropertyCategory.primary,
                "status": PropertyStatus.available,
                "property_class": 'comfort',
                "total_area": 45.0 + (i * 15),  # 45-120 м²
                "living_area": 35.0 + (i * 12),  # 35-95 м²
                "rooms": 1 + (i % 4),  # 1-4 комнаты
                "floor": 1 + (i % 9),  # 1-9 этаж
                "balcony": i % 2 == 0,  # чередуем
                "loggia": i % 3 == 0,  # каждый третий
                "heating_type": 'central',
                "parking_type": 'underground' if i % 2 == 0 else 'open'
            }
            property_obj = await crud_property.create(session, property_data)
            properties.append(property_obj)
            print(f"✅ Создан объект: {property_obj.id} в здании {building.id}")
    
    print("📍 Создание адресов...")
    
    # Адреса в Краснодарском крае
    krasnodar_addresses = [
        {"city": "Краснодар", "street": "ул. Красная", "house": "1", "lat": 45.0448, "lng": 38.9760},
        {"city": "Краснодар", "street": "ул. Северная", "house": "15", "lat": 45.0522, "lng": 38.9725},
        {"city": "Краснодар", "street": "ул. Западная", "house": "25", "lat": 45.0489, "lng": 38.9687},
        {"city": "Краснодар", "street": "ул. Восточная", "house": "8", "lat": 45.0567, "lng": 38.9812},
        {"city": "Краснодар", "street": "ул. Южная", "house": "12", "lat": 45.0412, "lng": 38.9745},
        {"city": "Краснодар", "street": "ул. Центральная", "house": "33", "lat": 45.0498, "lng": 38.9768},
        
        {"city": "Сочи", "street": "ул. Морская", "house": "5", "lat": 43.5855, "lng": 39.7231},
        {"city": "Сочи", "street": "ул. Курортная", "house": "18", "lat": 43.5892, "lng": 39.7289},
        {"city": "Сочи", "street": "ул. Парковая", "house": "22", "lat": 43.5821, "lng": 39.7215},
        {"city": "Сочи", "street": "ул. Садовая", "house": "7", "lat": 43.5876, "lng": 39.7254},
        {"city": "Сочи", "street": "ул. Лесная", "house": "14", "lat": 43.5843, "lng": 39.7198},
        {"city": "Сочи", "street": "ул. Речная", "house": "9", "lat": 43.5867, "lng": 39.7223},
        
        {"city": "Анапа", "street": "ул. Набережная", "house": "3", "lat": 44.8947, "lng": 37.3166},
        {"city": "Анапа", "street": "ул. Пляжная", "house": "11", "lat": 44.8965, "lng": 37.3189},
        {"city": "Анапа", "street": "ул. Курортная", "house": "16", "lat": 44.8932, "lng": 37.3145},
        {"city": "Анапа", "street": "ул. Центральная", "house": "24", "lat": 44.8958, "lng": 37.3172},
        {"city": "Анапа", "street": "ул. Морская", "house": "8", "lat": 44.8971, "lng": 37.3198},
        {"city": "Анапа", "street": "ул. Солнечная", "house": "13", "lat": 44.8941, "lng": 37.3156},
        
        {"city": "Новороссийск", "street": "ул. Морская", "house": "6", "lat": 44.7239, "lng": 37.7683},
        {"city": "Новороссийск", "street": "ул. Центральная", "house": "19", "lat": 44.7256, "lng": 37.7712},
        {"city": "Новороссийск", "street": "ул. Портовая", "house": "4", "lat": 44.7218, "lng": 37.7654},
        {"city": "Новороссийск", "street": "ул. Набережная", "house": "27", "lat": 44.7245, "lng": 37.7698},
        {"city": "Новороссийск", "street": "ул. Горная", "house": "15", "lat": 44.7267, "lng": 37.7731},
        {"city": "Новороссийск", "street": "ул. Приморская", "house": "10", "lat": 44.7229, "lng": 37.7667},
        
        {"city": "Армавир", "street": "ул. Ленина", "house": "2", "lat": 45.0013, "lng": 41.1164},
        {"city": "Армавир", "street": "ул. Советская", "house": "17", "lat": 45.0031, "lng": 41.1189},
        {"city": "Армавир", "street": "ул. Мира", "house": "23", "lat": 44.9998, "lng": 41.1145},
        {"city": "Армавир", "street": "ул. Центральная", "house": "31", "lat": 45.0025, "lng": 41.1172},
        {"city": "Армавир", "street": "ул. Школьная", "house": "5", "lat": 45.0042, "lng": 41.1198},
        {"city": "Армавир", "street": "ул. Садовая", "house": "20", "lat": 45.0007, "lng": 41.1156}
    ]
    
    # Создаем адреса для каждого объекта недвижимости
    for i, property_obj in enumerate(properties):
        address_data = {
            "property_id": property_obj.id,
            **krasnodar_addresses[i % len(krasnodar_addresses)]
        }
        address = await crud_property_address.create(session, address_data)
        print(f"✅ Создан адрес для объекта {property_obj.id}")
    
    print("💰 Создание цен...")
    
    # Создаем цены для каждого объекта недвижимости
    for i, property_obj in enumerate(properties):
        base_price = 50000 + (i * 5000)  # 50k - 350k за м²
        current_price = base_price * (0.95 + (i % 10) * 0.01)  # ±5% от базовой цены
        
        price_data = {
            "property_id": property_obj.id,
            "base_price": base_price,
            "current_price": current_price,
            "price_per_sqm": current_price / property_obj.total_area,
            "currency": "RUB"
        }
        price = await crud_property_price.create(session, price_data)
        print(f"✅ Создана цена для объекта {property_obj.id}: {current_price} руб/м²")
    
    print("🏠 Создание характеристик жилых объектов...")
    
    # Создаем характеристики для жилых объектов
    for i, property_obj in enumerate(properties):
        residential_data = {
            "property_id": property_obj.id,
            "ceiling_height": 2.7 + (i % 3) * 0.1,  # 2.7-2.9 м
            "window_type": "пластиковые" if i % 2 == 0 else "деревянные",
            "balcony_area": 3.0 + (i % 3) if property_obj.balcony else 0,
            "loggia_area": 4.0 + (i % 2) if property_obj.loggia else 0,
            "storage_room": i % 3 == 0,  # каждый третий
            "pantry": i % 4 == 0,  # каждый четвертый
            "separate_bathroom": i % 2 == 0,  # чередуем
            "combined_bathroom": i % 2 == 1,  # чередуем
            "kitchen_area": 8.0 + (i % 5)  # 8-12 м²
        }
        residential = await crud_residential_property.create(session, residential_data)
        print(f"✅ Созданы характеристики для объекта {property_obj.id}")
    
    print("🔧 Создание особенностей объектов...")
    
    # Создаем особенности для каждого объекта
    for i, property_obj in enumerate(properties):
        features_data = {
            "property_id": property_obj.id,
            "elevator": True,
            "security": i % 2 == 0,  # чередуем
            "concierge": i % 3 == 0,  # каждый третий
            "parking": True,
            "playground": i % 2 == 0,  # чередуем
            "sports_ground": i % 4 == 0,  # каждый четвертый
            "green_area": True,
            "underground_parking": i % 2 == 0,  # чередуем
            "bicycle_parking": i % 3 == 0,  # каждый третий
            "electric_vehicle_charging": i % 5 == 0,  # каждый пятый
            "smart_home": i % 4 == 0,  # каждый четвертый
            "air_conditioning": i % 2 == 0,  # чередуем
            "furniture": i % 3 == 0,  # каждый третий
            "appliances": i % 4 == 0,  # каждый четвертый
            "renovation": "под ключ" if i % 2 == 0 else "черновая"
        }
        features = await crud_property_features.create(session, features_data)
        print(f"✅ Созданы особенности для объекта {property_obj.id}")
    
    print("📊 Создание аналитики...")
    
    # Создаем аналитику для каждого объекта
    for i, property_obj in enumerate(properties):
        analytics_data = {
            "property_id": property_obj.id,
            "views_count": 10 + (i % 50),  # 10-59 просмотров
            "favorites_count": 2 + (i % 10),  # 2-11 избранных
            "contact_requests": 1 + (i % 5),  # 1-5 запросов
            "avg_time_on_page": 120 + (i % 180),  # 2-5 минут
            "bounce_rate": 0.3 + (i % 40) * 0.01,  # 30-70%
            "conversion_rate": 0.05 + (i % 15) * 0.01,  # 5-20%
            "price_change_count": i % 3,  # 0-2 изменения цены
            "last_price_change": datetime.utcnow() - timedelta(days=i % 30),
            "market_value": property_obj.total_area * (45000 + (i % 10000)),  # рыночная стоимость
            "price_per_sqm_market": 45000 + (i % 10000),  # рыночная цена за м²
            "price_difference_percent": (i % 20) - 10,  # ±10% от рыночной
            "days_on_market": 15 + (i % 45),  # 15-60 дней на рынке
            "similar_properties_count": 5 + (i % 10),  # 5-14 похожих объектов
            "avg_similar_price": 50000 + (i % 15000),  # средняя цена похожих
            "price_competitiveness_score": 0.7 + (i % 30) * 0.01  # 70-100%
        }
        analytics = await crud_property_analytics.create(session, analytics_data)
        print(f"✅ Создана аналитика для объекта {property_obj.id}")
    
    print("📸 Создание медиа...")
    
    # Создаем медиа для каждого объекта
    for i, property_obj in enumerate(properties):
        for j in range(3):  # 3 медиа файла на объект
            media_data = {
                "property_id": property_obj.id,
                "media_type": "image" if j == 0 else "video" if j == 1 else "virtual_tour",
                "url": f"https://example.com/media/{property_obj.id}/{j}.jpg",
                "title": f"Фото {j+1} объекта {property_obj.id}",
                "description": f"Описание медиа файла {j+1}",
                "is_primary": j == 0,  # первое фото - основное
                "order_index": j
            }
            media = await crud_property_media.create(session, media_data)
            print(f"✅ Создано медиа {j+1} для объекта {property_obj.id}")
    
    print("🏷️ Создание промо-тегов...")
    
    # Создаем промо-теги для некоторых объектов
    promo_tags = ["Скидка 10%", "Ипотека 5%", "Скидка при покупке", "Акция", "Выгодное предложение"]
    for i, property_obj in enumerate(properties):
        if i % 3 == 0:  # каждый третий объект
            promo_data = {
                "property_id": property_obj.id,
                "tag_type": 'discount',
                "title": promo_tags[i % len(promo_tags)],
                "description": f"Специальное предложение для объекта {property_obj.id}",
                "discount_percent": 5 + (i % 15),  # 5-20% скидка
                "valid_until": datetime.utcnow() + timedelta(days=30 + (i % 60))
            }
            promo_tag = await crud_promo_tag.create(session, promo_data)
            print(f"✅ Создан промо-тег для объекта {property_obj.id}")
    
    print("🏦 Создание ипотечных программ...")
    
    # Создаем ипотечные программы
    mortgage_programs = [
        {"name": "Сбербанк Ипотека", "bank": "Сбербанк", "rate": 7.5, "min_down_payment": 15},
        {"name": "ВТБ Ипотека", "bank": "ВТБ", "rate": 8.2, "min_down_payment": 20},
        {"name": "Россельхозбанк Ипотека", "bank": "Россельхозбанк", "rate": 7.8, "min_down_payment": 10},
        {"name": "Газпромбанк Ипотека", "bank": "Газпромбанк", "rate": 8.5, "min_down_payment": 25},
        {"name": "Альфа-Банк Ипотека", "bank": "Альфа-Банк", "rate": 8.8, "min_down_payment": 30}
    ]
    
    for i, program_data in enumerate(mortgage_programs):
        for j in range(10):  # 10 объектов на программу
            property_index = (i * 10 + j) % len(properties)
            property_obj = properties[property_index]
            
            mortgage_data = {
                "property_id": property_obj.id,
                "program_type": 'standard',
                "bank_name": program_data["bank"],
                "program_name": program_data["name"],
                "interest_rate": program_data["rate"],
                "min_down_payment_percent": program_data["min_down_payment"],
                "max_loan_amount": 15000000,  # 15 млн
                "loan_term_years": 20,
                "monthly_payment": property_obj.total_area * 50000 * 0.8 / 240,  # примерный расчет
                "requirements": "Возраст от 21 года, стаж от 6 месяцев",
                "documents": "Паспорт, справка о доходах, документы на недвижимость"
            }
            mortgage = await crud_mortgage_program.create(session, mortgage_data)
            print(f"✅ Создана ипотечная программа {program_data['name']} для объекта {property_obj.id}")
    
    print("🎉 Создание акций...")
    
    # Создаем акции
    promotions_data = [
        {"name": "Весенняя распродажа", "type": 'discount', "discount_percent": 15},
        {"name": "Ипотека без первоначального взноса", "type": 'mortgage', "discount_percent": 0},
        {"name": "Скидка при покупке двух объектов", "type": 'bulk', "discount_percent": 20},
        {"name": "Акция для молодых семей", "type": 'special', "discount_percent": 10},
        {"name": "Скидка при оплате наличными", "type": 'cash', "discount_percent": 5}
    ]
    
    for i, promo_data in enumerate(promotions_data):
        promotion_data = {
            "name": promo_data["name"],
            "description": f"Описание акции: {promo_data['name']}",
            "promotion_type": promo_data["type"],
            "discount_percent": promo_data["discount_percent"],
            "start_date": datetime.utcnow(),
            "end_date": datetime.utcnow() + timedelta(days=90),
            "is_active": True,
            "max_uses": 100,
            "current_uses": 0
        }
        promotion = await crud_promotion.create(session, promotion_data)
        print(f"✅ Создана акция: {promo_data['name']}")
    
    print("👁️ Создание логов просмотров...")
    
    # Создаем логи просмотров
    for i, property_obj in enumerate(properties):
        for j in range(3):  # 3 просмотра на объект
            view_data = {
                "property_id": property_obj.id,
                "user_id": 1,  # анонимный пользователь
                "viewed_at": datetime.utcnow() - timedelta(hours=j),
                "session_duration": 60 + (j * 30),  # 1-2.5 минуты
                "source": "search" if j == 0 else "recommendations" if j == 1 else "direct"
            }
            view = await crud_views_log.create(session, view_data)
            print(f"✅ Создан лог просмотра {j+1} для объекта {property_obj.id}")
    
    print("📅 Создание бронирований...")
    
    # Создаем несколько бронирований
    for i in range(10):  # 10 бронирований
        property_obj = properties[i % len(properties)]
        booking_data = {
            "property_id": property_obj.id,
            "user_id": 1,  # тестовый пользователь
            "status": "active",
            "booked_at": datetime.utcnow() - timedelta(hours=i),
            "expires_at": datetime.utcnow() + timedelta(hours=24 - i)
        }
        booking = await crud_booking.create(session, booking_data)
        print(f"✅ Создано бронирование для объекта {property_obj.id}")
    
    print("✅ Все моковые данные созданы успешно!") 