import json
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Any
import random

from app.models import (
    Developer, Project, Building, Property,
    PropertyAddress, PropertyPrice, ResidentialProperty,
    PropertyFeatures, PropertyAnalytics, PropertyMedia,
    PromoTag, MortgageProgram, PriceHistory, ViewsLog,
    Booking, User, UserRole, PropertyType, PropertyCategory, PropertyStatus,
    BookingStatus, ViewEvent, PriceChangeReason, ViewType, FinishingType, ParkingType
)


def load_krasnodar_dataset() -> List[Dict[str, Any]]:
    """Загружает 20 случайных объектов из датасета Краснодарского края"""
    with open("krasnodar_real_estate_dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # Фильтруем только объекты из Краснодарского края и с полными данными
        krasnodar_data = [
            item for item in data 
            if item.get("region") == "Краснодарский край" 
            and item.get("developer_name") 
            and item.get("project_name")
            and item.get("building_id")
            and item.get("address_full")
            and item.get("city")
        ]
        # Выбираем случайные 20 объектов
        return random.sample(krasnodar_data, min(20, len(krasnodar_data)))


async def create_mock_data(session: AsyncSession):
    """Создает тестовые данные в базе данных используя датасет Краснодарского края"""
    properties_data = load_krasnodar_dataset()
    
    # Словари для хранения уникальных объектов
    developers: Dict[str, Developer] = {}
    projects: Dict[str, Project] = {}
    buildings: Dict[str, Building] = {}
    
    # Маппинг русских названий видов на английские
    view_type_mapping = {
        'ДВОР': 'YARD',
        'ЛЕС': 'FOREST',
        'ГОРОД': 'CITY',
        'ГОРЫ': 'MOUNTAINS',
        'МОРЕ': 'SEA',
        'ПАРК': 'PARK',
        'СМЕШАННЫЙ': 'MIXED',
        'РЕКА': 'RIVER'
    }
    
    # Маппинг русских названий типов парковки на английские
    parking_type_mapping = {
        'НАЗЕМНАЯ': 'GROUND',
        'ПОДЗЕМНАЯ': 'UNDERGROUND',
        'МНОГОУРОВНЕВАЯ': 'MULTILEVEL',
        'ДВОР': 'YARD',
        'НЕТ': 'NONE'
    }
    
    # Создаем уникальных застройщиков
    for prop in properties_data:
        dev_id = prop.get("developer_id")
        if dev_id and dev_id not in developers:
            dev_name = prop.get("developer_name", "").strip()
            if not dev_name:
                continue
                
            website = f"https://{dev_name.lower().replace(' ', '-').replace('«', '').replace('»', '')}.ru"
            developer = Developer(
                id=len(developers) + 1,  # Используем инкрементальные ID
                name=dev_name,
                description=f"Надежный застройщик в {prop.get('city', 'Краснодарском крае')}",
                founding_year=random.randint(1990, 2020),
                website=website,
                rating=round(random.uniform(3.5, 5.0), 1),
                projects_count=random.randint(1, 10)
            )
            developers[dev_id] = developer
            session.add(developer)
    
    # Создаем уникальные проекты
    for prop in properties_data:
        proj_id = prop.get("project_id")
        if proj_id and proj_id not in projects:
            proj_name = prop.get("project_name", "").strip()
            if not proj_name:
                continue
                
            dev_id = prop.get("developer_id")
            if not dev_id or dev_id not in developers:
                continue
                
            completion_date = prop.get("completion_date")
            if not completion_date:
                continue
                
            try:
                completion_dt = datetime.fromisoformat(completion_date)
                project = Project(
                    id=len(projects) + 1,  # Используем инкрементальные ID
                    name=proj_name,
                    description=f"Современный жилой комплекс в {prop.get('city', 'Краснодарском крае')}",
                    developer_id=developers[dev_id].id,
                    start_date=(completion_dt - timedelta(days=365*3)).date(),
                    completion_date=completion_dt.date(),
                    status="active",
                    total_area=random.randint(10000, 50000),
                    total_units=random.randint(100, 1000)
                )
                projects[proj_id] = project
                session.add(project)
            except (ValueError, TypeError):
                continue
    
    # Создаем уникальные здания
    for prop in properties_data:
        building_id = prop.get("building_id")
        if building_id and building_id not in buildings:
            proj_id = prop.get("project_id")
            if not proj_id or proj_id not in projects:
                continue
                
            completion_date = prop.get("completion_date")
            if not completion_date:
                continue
                
            try:
                completion_dt = datetime.fromisoformat(completion_date)
                building = Building(
                    id=len(buildings) + 1,  # Используем инкрементальные ID
                    project_id=projects[proj_id].id,
                    number=str(random.randint(1, 10)),
                    floors_total=prop.get("floors_total") or random.randint(5, 25),
                    completion_date=completion_dt.date(),
                    status="under_construction",
                    total_units=random.randint(50, 200),
                    available_units=random.randint(10, 50)
                )
                buildings[building_id] = building
                session.add(building)
            except (ValueError, TypeError):
                continue
    
    # Создаем объекты недвижимости
    for i, prop in enumerate(properties_data, 1):
        try:
            # Проверяем наличие всех необходимых связей
            dev_id = prop.get("developer_id")
            proj_id = prop.get("project_id")
            building_id = prop.get("building_id")
            
            if not (dev_id in developers and proj_id in projects and building_id in buildings):
                continue
            
            # Создаем основную запись о недвижимости
            property = Property(
                id=i,
                external_id=prop.get("external_id"),
                created_at=datetime.fromisoformat(prop["created_at"]),
                updated_at=datetime.fromisoformat(prop["updated_at"]),
                property_type=PropertyType.RESIDENTIAL,
                category=PropertyCategory.FLAT_NEW,
                developer_id=developers[dev_id].id,
                project_id=projects[proj_id].id,
                building_id=buildings[building_id].id,
                status=PropertyStatus.AVAILABLE,
                has_3d_tour=prop.get("has_3d_tour", False)
            )
            session.add(property)
            
            # Создаем адрес
            if all(prop.get(k) for k in ["address_full", "city", "region", "lat", "lng"]):
                address = PropertyAddress(
                    property_id=property.id,
                    address_full=prop["address_full"],
                    city=prop["city"],
                    region=prop["region"],
                    district=prop.get("district"),
                    lat=float(prop["lat"]),
                    lng=float(prop["lng"])
                )
                session.add(address)
            
            # Создаем цену
            if all(prop.get(k) for k in ["base_price", "current_price"]):
                base_price = float(prop["base_price"])
                current_price = float(prop["current_price"])
                price = PropertyPrice(
                    property_id=property.id,
                    base_price=base_price,
                    current_price=current_price,
                    currency="RUB",
                    price_per_m2=float(prop["price_per_m2"]) if prop.get("price_per_m2") else None,
                    original_price=base_price,
                    discount_amount=base_price - current_price if current_price < base_price else None,
                    discount_percent=round((1 - current_price / base_price) * 100, 2) if current_price < base_price else None
                )
                session.add(price)
            
            # Создаем детали жилой недвижимости
            if prop.get("completion_date"):
                residential = ResidentialProperty(
                    property_id=property.id,
                    unit_number=prop.get("unit_number"),
                    floor=prop.get("floor"),
                    floors_total=prop.get("floors_total"),
                    rooms=prop.get("rooms"),
                    is_studio=prop.get("is_studio", False),
                    is_free_plan=prop.get("is_free_plan", False),
                    total_area=float(prop["total_area"]) if prop.get("total_area") else None,
                    living_area=float(prop["living_area"]) if prop.get("living_area") else None,
                    kitchen_area=float(prop["kitchen_area"]) if prop.get("kitchen_area") else None,
                    ceiling_height=float(prop["ceiling_height"]) if prop.get("ceiling_height") else None,
                    completion_date=datetime.fromisoformat(prop["completion_date"])
                )
                session.add(residential)
            
            # Создаем характеристики
            view_type = None
            if prop.get('view'):
                view_type = view_type_mapping.get(prop['view'].upper())
            
            parking_type = None
            if prop.get('parking_type'):
                parking_type = parking_type_mapping.get(prop['parking_type'].upper())
            
            features = PropertyFeatures(
                property_id=property.id,
                balcony=prop.get("balcony", False),
                loggia=prop.get("loggia", False),
                terrace=prop.get("terrace", False),
                view=view_type,
                finishing=prop.get("finishing"),
                parking_type=parking_type,
                parking_price=prop.get("parking_price"),
                has_furniture=prop.get("has_furniture"),
                has_appliances=prop.get("has_appliances")
            )
            session.add(features)
            
            # Создаем аналитику
            analytics = PropertyAnalytics(
                property_id=property.id,
                days_on_market=int(prop.get("days_on_market", 0)),
                rli_index=float(prop["rli_index"]) if prop.get("rli_index") else None,
                demand_score=int(prop["demand_score"]) if prop.get("demand_score") else None,
                clicks_total=int(prop.get("clicks_total", 0)),
                favourites_total=int(prop.get("favourites_total", 0)),
                bookings_total=int(prop.get("bookings_total", 0)),
                views_last_week=random.randint(10, 100),
                views_last_month=random.randint(50, 500),
                price_trend=random.uniform(-5.0, 5.0)
            )
            session.add(analytics)
            
            # Создаем медиа
            media_data = prop.get("media", {})
            if isinstance(media_data, dict):
                media = PropertyMedia(
                    property_id=property.id,
                    layout_image_url=media_data.get("layout_image_url"),
                    vr_tour_url=media_data.get("vr_tour_url"),
                    video_url=media_data.get("video_url"),
                    main_photo_url=f"https://krasnodar-realty.ru/photos/{property.id}/main.jpg",
                    photo_urls=[f"https://krasnodar-realty.ru/photos/{property.id}/{j}.jpg" for j in range(1, 6)]
                )
                session.add(media)
            
            # Создаем промо-теги
            for tag in prop.get("promo_tags", []):
                if tag and isinstance(tag, str):
                    promo_tag = PromoTag(
                        property_id=property.id,
                        tag=tag,
                        active=True,
                        expires_at=datetime.now() + timedelta(days=random.randint(30, 90))
                    )
                    session.add(promo_tag)
            
            # Создаем ипотечные программы
            if prop.get("mortgage_program_ids"):
                program = MortgageProgram(
                    property_id=property.id,
                    name="Семейная ипотека",
                    bank_name="СберБанк",
                    interest_rate=random.uniform(3.0, 7.0),
                    down_payment_percent=random.uniform(10.0, 20.0),
                    term_years=random.randint(10, 30),
                    monthly_payment=float(prop["current_price"]) * 0.004 if prop.get("current_price") else None,
                    requirements="Требуется подтверждение дохода"
                )
                session.add(program)
        except (ValueError, TypeError, KeyError) as e:
            print(f"Ошибка при создании объекта недвижимости: {e}")
            continue
    
    # Сохраняем все изменения
    await session.commit()
    
    # Выводим информацию о завершении
    print("\n✨ Готово! Тестовые данные успешно созданы.")
    print("📊 Создано:")
    print(f"   - {len(properties_data)} объектов недвижимости")
    print(f"   - {len(developers)} застройщиков")
    print(f"   - {len(projects)} проектов")
    print(f"   - {len(buildings)} зданий")
    print("   - Тестовые пользователи и дополнительные данные")

# Тестовые пользователи
test_users = [
    User(
        id=1,
        email="buyer@krasnodar-realty.ru",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGpJ4vZKkyu",  # test_password
        display_name="Иван Покупатель",
        role=UserRole.BUYER,
        phone="+7 (918) 123-45-67"
    ),
    User(
        id=2,
        email="developer@krasnodar-realty.ru",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGpJ4vZKkyu",  # test_password
        display_name="ООО Застройщик",
        role=UserRole.DEVELOPER,
        phone="+7 (918) 765-43-21"
    ),
    User(
        id=3,
        email="admin@krasnodar-realty.ru",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyNiGpJ4vZKkyu",  # test_password
        display_name="Администратор",
        role=UserRole.ADMIN,
        phone="+7 (918) 999-99-99"
    )
]

# Тестовый застройщик
test_developer = Developer(
    id=999,
    name="Краснодар Девелопмент",
    description="Ведущий застройщик жилой и коммерческой недвижимости в Краснодарском крае",
    founding_year=2010,
    website="https://krasnodar-development.ru",
    rating=4.8,
    projects_count=12
)

# Тестовый проект
test_project = Project(
    id=999,
    name="ЖК Южный Парк",
    developer_id=999,
    description="Современный жилой комплекс бизнес-класса в центре Краснодара",
    start_date=datetime.now().date(),
    completion_date=(datetime.now() + timedelta(days=365*2)).date(),
    status="active",
    total_area=75000.0,
    total_units=800
)

# Тестовое здание
test_building = Building(
    id=999,
    project_id=999,
    number="3А",
    floors_total=24,
    completion_date=(datetime.now() + timedelta(days=365)).date(),
    status="under_construction",
    total_units=240,
    available_units=180
)

# Создаем тестовый объект недвижимости
test_property = Property(
    id=1,
    external_id="TEST-001",
    property_type=PropertyType.RESIDENTIAL,
    category=PropertyCategory.FLAT_NEW,
    developer_id=1,
    project_id=1,
    building_id=1,
    status=PropertyStatus.AVAILABLE,
    has_3d_tour=True
)

# Создаем тестовый адрес
test_address = PropertyAddress(
    property_id=1,
    address_full="ул. Красная, д. 1",
    city="Краснодар",
    region="Краснодарский край",
    district="Центральный",
    lat=45.0355,
    lng=38.9750,
    postal_code="350000"
)

# Создаем тестовую цену
test_price = PropertyPrice(
    property_id=1,
    base_price=5000000.0,
    current_price=4800000.0,
    currency="RUB",
    price_per_m2=100000.0,
    original_price=5000000.0,
    discount_amount=200000.0,
    discount_percent=4.0
)

# Создаем тестовые характеристики жилой недвижимости
test_residential = ResidentialProperty(
    property_id=1,
    unit_number="123",
    floor=10,
    floors_total=20,
    rooms=2,
    is_studio=False,
    is_free_plan=False,
    total_area=60.5,
    living_area=40.0,
    kitchen_area=12.0,
    ceiling_height=2.8,
    completion_date=datetime.now() + timedelta(days=180)
)

# Создаем тестовые особенности
test_features = PropertyFeatures(
    property_id=1,
    balcony=True,
    loggia=False,
    terrace=False,
    view="город",
    finishing="чистовая",
    parking_type="подземный_паркинг",
    parking_price=500000.0,
    has_furniture=False,
    has_appliances=False
)

# Создаем тестовую аналитику
test_analytics = PropertyAnalytics(
    property_id=1,
    days_on_market=30,
    rli_index=0.8,
    demand_score=75,
    clicks_total=150,
    favourites_total=20,
    bookings_total=2,
    views_last_week=50,
    views_last_month=200,
    price_trend=1.5
)

# Создаем тестовые медиа
test_media = PropertyMedia(
    property_id=1,
    layout_image_url="https://example.com/layout.jpg",
    vr_tour_url="https://example.com/vr_tour",
    video_url="https://example.com/video.mp4",
    main_photo_url="https://example.com/main.jpg",
    photo_urls=["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"]
)

# Создаем тестовые промо-теги
test_promo_tag = PromoTag(
    property_id=1,
    tag="Акция",
    active=True,
    expires_at=datetime.now() + timedelta(days=30)
)

# Создаем тестовую ипотечную программу
test_mortgage = MortgageProgram(
    id=1,
    property_id=1,
    name="Семейная ипотека",
    bank_name="СберБанк",
    interest_rate=5.5,
    down_payment_percent=15.0,
    term_years=20,
    monthly_payment=35000.0,
    requirements='{"age": "21-65", "employment": "official"}'
)

# Создаем тестовую историю цен
test_price_history = PriceHistory(
    id=1,
    property_id=1,
    changed_at=datetime.now() - timedelta(days=7),
    old_price=5000000.0,
    new_price=4800000.0,
    reason=PriceChangeReason.PROMO,
    description="Сезонная акция"
)

# Создаем тестовый лог просмотров
test_views_log = ViewsLog(
    id=1,
    property_id=1,
    user_id=1,
    event=ViewEvent.VIEW,
    occurred_at=datetime.now() - timedelta(hours=2),
    source="web",
    session_id="test_session"
)

# Создаем тестовое бронирование
test_booking = Booking(
    id=1,
    property_id=1,
    user_id=1,
    status=BookingStatus.ACTIVE,
    booked_at=datetime.now() - timedelta(days=1),
    expires_at=datetime.now() + timedelta(days=2),
    payment_status="pending",
    booking_fee=10000.0
)

# Список всех тестовых данных
test_data = {
    "users": test_users,
    "developer": test_developer,
    "project": test_project,
    "building": test_building,
    "property": test_property,
    "address": test_address,
    "price": test_price,
    "residential": test_residential,
    "features": test_features,
    "analytics": test_analytics,
    "media": test_media,
    "promo_tag": test_promo_tag,
    "mortgage": test_mortgage,
    "price_history": test_price_history,
    "views_log": test_views_log,
    "booking": test_booking
}