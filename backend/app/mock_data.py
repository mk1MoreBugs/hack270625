import json
import random
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import (
    User, Developer, Project, Building, Property,
    PropertyAddress, PropertyPrice, ResidentialProperty,
    PropertyFeatures, PropertyAnalytics, PropertyMedia,
    PromoTag, MortgageProgram, PriceHistory, ViewsLog,
    Booking, Promotion, UserRole, PropertyType, PropertyCategory,
    PropertyStatus, BookingStatus, ViewEvent, PriceChangeReason,
    ViewType, FinishingType, ParkingType
)
from app.security import get_password_hash

# Загрузка датасета
with open("krasnodar_real_estate_dataset.json", "r", encoding="utf-8") as f:
    DATASET = json.load(f)

# Константы для генерации данных
DEVELOPER_COMPANIES = list(set(item["developer_name"] for item in DATASET))
CITIES = list(set(item["city"] for item in DATASET))
PROJECTS = list(set((item["project_id"], item["project_name"]) for item in DATASET))
BUILDINGS = list(set(item["building_id"] for item in DATASET))

# Списки для хранения сгенерированных ID
user_ids = []
developer_ids = []
project_ids = []
building_ids = []
property_ids = []

# Константы для генерации данных
DISTRICTS = ["Центральный", "Западный", "Карасунский", "Прикубанский", "Фестивальный"]
STREETS = ["Красная", "Северная", "Кубанская", "Ставропольская", "Российская"]

async def create_mock_users(session: AsyncSession) -> List[int]:
    """Создание тестовых пользователей"""
    users = []
    
    # Создаем админа
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        display_name="Администратор",
        role=UserRole.ADMIN,
        phone="+7900000000"
    )
    users.append(admin)
    
    # Создаем покупателей (25)
    for i in range(25):
        user = User(
            email=f"buyer{i+1}@example.com",
            hashed_password=get_password_hash(f"buyer{i+1}"),
            display_name=f"Покупатель {i+1}",
            role=UserRole.BUYER,
            phone=f"+7911{i:07d}"
        )
        users.append(user)
    
    # Создаем застройщиков (25)
    for i in range(25):
        user = User(
            email=f"developer{i+1}@example.com",
            hashed_password=get_password_hash(f"developer{i+1}"),
            display_name=f"Застройщик {i+1}",
            role=UserRole.DEVELOPER,
            phone=f"+7922{i:07d}",
            company_name=f"Строительная компания {i+1}"
        )
        users.append(user)
    
    # Сохраняем пользователей
    for user in users:
        session.add(user)
    
    await session.commit()
    user_ids.extend([user.id for user in users])
    return user_ids

async def create_mock_developers(session: AsyncSession) -> List[int]:
    """Создание тестовых застройщиков"""
    developers = []
    
    for i in range(25):
        developer = Developer(
            name=f"Строительная компания {i+1}",
            description=f"Крупный застройщик в Краснодарском крае. Компания специализируется на строительстве современных жилых комплексов.",
            founding_year=random.randint(1990, 2020),
            website=f"https://developer{i+1}.ru",
            rating=round(random.uniform(4.0, 5.0), 1),
            projects_count=random.randint(1, 5),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
        )
        developers.append(developer)
    
    # Сохраняем застройщиков
    for developer in developers:
        session.add(developer)
    
    await session.commit()
    developer_ids.extend([d.id for d in developers])
    return developer_ids

async def create_mock_projects(session: AsyncSession) -> List[int]:
    """Создание тестовых проектов"""
    projects = []
    
    for i in range(20):
        project = Project(
            name=f"ЖК Южный {i+1}",
            developer_id=random.choice(developer_ids),
            description=f"Современный жилой комплекс в {random.choice(CITIES)}",
            start_date=date.today() - timedelta(days=random.randint(100, 500)),
            completion_date=date.today() + timedelta(days=random.randint(100, 500)),
            status=random.choice(["active", "completed"]),
            total_area=random.randint(5000, 50000),
            total_units=random.randint(100, 1000),
            query=f"жк южный {i+1} краснодар новостройка"
        )
        projects.append(project)
    
    # Сохраняем проекты
    for project in projects:
        session.add(project)
    
    await session.commit()
    project_ids.extend([p.id for p in projects])
    return project_ids

async def create_mock_buildings(session: AsyncSession) -> List[int]:
    """Создание тестовых зданий"""
    buildings = []
    
    for i in range(50):
        project_id = random.choice(project_ids)
        building_number = str(random.randint(1, 10))
        building = Building(
            project_id=project_id,
            number=building_number,
            floors_total=random.randint(5, 25),
            completion_date=date.today() + timedelta(days=random.randint(100, 500)),
            status=random.choice(["under_construction", "completed"]),
            total_units=random.randint(50, 200),
            available_units=random.randint(10, 50),
            qury=f"корпус {building_number} литер {building_number}"
        )
        buildings.append(building)
    
    # Сохраняем здания
    for building in buildings:
        session.add(building)
    
    await session.commit()
    building_ids.extend([b.id for b in buildings])
    return building_ids

async def create_mock_properties(session: AsyncSession) -> List[int]:
    """Создание тестовых объектов недвижимости"""
    properties = []
    
    for i in range(100):
        property_type = PropertyType.RESIDENTIAL
        category = random.choice([
            PropertyCategory.FLAT_NEW,
            PropertyCategory.FLAT_SECONDARY,
            PropertyCategory.TOWNHOUSE
        ])
        rooms = random.randint(1, 4)
        area = random.randint(30, 150)
        
        property = Property(
            external_id=f"PROP{i+1}",
            property_type=property_type,
            category=category,
            developer_id=random.choice(developer_ids),
            project_id=random.choice(project_ids),
            building_id=random.choice(building_ids),
            status=random.choice(list(PropertyStatus)),
            has_3d_tour=random.choice([True, False]),
            qury=f"{category.value} {rooms}к квартира {area}м2"
        )
        properties.append(property)
    
    # Сохраняем объекты недвижимости
    for property in properties:
        session.add(property)
    
    await session.commit()
    property_ids.extend([p.id for p in properties])
    return property_ids

async def create_mock_addresses(session: AsyncSession) -> None:
    """Создание тестовых адресов"""
    addresses = []
    
    for i, property_id in enumerate(property_ids):
        city = random.choice(CITIES)
        district = random.choice(DISTRICTS)
        street = random.choice(STREETS)
        building_num = random.randint(1, 100)
        
        address = PropertyAddress(
            property_id=property_id,
            address_full=f"г. {city}, ул. {street}, д. {building_num}",
            city=city,
            region="Краснодарский край",
            district=district,
            lat=random.uniform(43.5, 45.5),
            lng=random.uniform(38.5, 40.5),
            postal_code=f"35{random.randint(1000, 9999)}"
        )
        addresses.append(address)
    
    # Сохраняем адреса
    for address in addresses:
        session.add(address)
    
    await session.commit()

async def create_mock_prices(session: AsyncSession) -> None:
    """Создание тестовых цен"""
    prices = []
    
    for property_id in property_ids:
        base_price = random.randint(3000000, 15000000)
        current_price = base_price * random.uniform(0.9, 1.1)
        area = random.uniform(30, 120)
        
        price = PropertyPrice(
            property_id=property_id,
            base_price=base_price,
            current_price=current_price,
            currency="RUB",
            price_per_m2=round(current_price / area, 2),
            original_price=base_price,
            discount_amount=base_price - current_price if current_price < base_price else None,
            discount_percent=round((1 - current_price / base_price) * 100, 2) if current_price < base_price else None
        )
        prices.append(price)
    
    # Сохраняем цены
    for price in prices:
        session.add(price)
    
    await session.commit()

async def create_mock_residential_properties(session: AsyncSession) -> None:
    """Создание тестовых характеристик жилой недвижимости"""
    residential_properties = []
    
    for i, item in enumerate(DATASET[:200]):
        residential = ResidentialProperty(
            property_id=property_ids[i],
            unit_number=item["unit_number"],
            floor=item["floor"],
            floors_total=item["floors_total"],
            rooms=item["rooms"],
            is_studio=item["is_studio"],
            is_free_plan=item["is_free_plan"],
            total_area=item["total_area"],
            living_area=item["living_area"],
            kitchen_area=item["kitchen_area"],
            ceiling_height=item["ceiling_height"],
            completion_date=datetime.strptime(
                item["completion_date"][:10],
                "%Y-%m-%d"
            ) if item["completion_date"] else None
        )
        residential_properties.append(residential)
    
    # Сохраняем характеристики
    for residential in residential_properties:
        session.add(residential)
    
    await session.commit()

async def create_mock_features(session: AsyncSession) -> None:
    """Создание тестовых особенностей недвижимости"""
    features = []
    
    for i, item in enumerate(DATASET[:200]):
        if company is None:
            continue
        feature = PropertyFeatures(
            property_id=property_ids[i],
            balcony=item["balcony"],
            loggia=item["loggia"],
            terrace=item["terrace"],
            view=item["view"].lower() if item.get("view") else None,
            finishing=item["finishing"],
            parking_type=item["parking_type"],
            parking_price=item.get("parking_price"),
            has_furniture=random.choice([True, False]),
            has_appliances=random.choice([True, False])
        )
        features.append(feature)
    
    # Сохраняем особенности
    for feature in features:
        session.add(feature)
    
    await session.commit()

async def create_mock_analytics(session: AsyncSession) -> None:
    """Создание тестовой аналитики"""
    analytics = []
    
    for i, item in enumerate(DATASET[:200]):
        analytic = PropertyAnalytics(
            property_id=property_ids[i],
            days_on_market=item["days_on_market"],
            rli_index=item["rli_index"],
            demand_score=item["demand_score"],
            clicks_total=item["clicks_total"],
            favourites_total=item["favourites_total"],
            bookings_total=item["bookings_total"],
            views_last_week=random.randint(10, 100),
            views_last_month=random.randint(50, 500),
            price_trend=random.uniform(-5.0, 5.0)
        )
        analytics.append(analytic)
    
    # Сохраняем аналитику
    for analytic in analytics:
        session.add(analytic)
    
    await session.commit()

async def create_mock_media(session: AsyncSession) -> None:
    """Создание тестовых медиа"""
    media_items = []
    
    for property_id in property_ids:
        # Создаем 1-2 медиа для каждого объекта (всего примерно 150)
        for _ in range(random.randint(1, 2)):
            media = PropertyMedia(
                property_id=property_id,
                layout_image_url=f"https://example.com/layouts/{property_id}.jpg",
                vr_tour_url=f"https://example.com/vr/{property_id}" if random.random() > 0.5 else None,
                video_url=f"https://example.com/videos/{property_id}.mp4" if random.random() > 0.7 else None,
                main_photo_url=f"https://example.com/photos/{property_id}/main.jpg",
                photo_urls=[f"https://example.com/photos/{property_id}/{j}.jpg" for j in range(1, 6)]
            )
            media_items.append(media)
    
    # Сохраняем медиа
    for media in media_items:
        session.add(media)
    
    await session.commit()

async def create_mock_promotions(session: AsyncSession) -> None:
    """Создание тестовых промоакций с валидацией"""
    promotions = []
    
    for i in range(10):
        # Генерируем даты с учетом валидации
        starts_at = datetime.utcnow() + timedelta(days=random.randint(1, 30))
        ends_at = starts_at + timedelta(days=random.randint(30, 90))
        
        # Генерируем скидку с учетом валидации
        discount_percent = round(random.uniform(5, 15), 2)  # Ограничиваем скидку разумным диапазоном
        
        # Генерируем количество использований с учетом валидации
        max_uses = random.randint(50, 200)
        current_uses = random.randint(0, max_uses - 1)  # Гарантируем, что current_uses < max_uses
        
        promotion = Promotion(
            name=f"Акция {i+1}",
            description=f"Специальное предложение на квартиры. Скидка {discount_percent}%",
            discount_percent=discount_percent,
            starts_at=starts_at,
            ends_at=ends_at,
            conditions=json.dumps({
                "min_price": 1000000,
                "max_price": 10000000,
                "property_types": ["flat_new", "townhouse"],
                "min_area": 40,
                "max_area": 150
            }),
            is_active=True,
            max_uses=max_uses,
            current_uses=current_uses
        )
        promotions.append(promotion)
    
    # Сохраняем промоакции
    for promotion in promotions:
        session.add(promotion)
    
    await session.commit()

async def create_mock_bookings(session: AsyncSession) -> None:
    """Создание тестовых броней"""
    bookings = []
    
    for _ in range(50):
        booking = Booking(
            property_id=random.choice(property_ids),
            user_id=random.choice(user_ids[:26]),  # Только покупатели (25 + админ)
            status=random.choice(list(BookingStatus)),
            booked_at=datetime.now() - timedelta(days=random.randint(1, 30)),
            expires_at=datetime.now() + timedelta(days=random.randint(1, 14)),
            payment_status=random.choice(["pending", "paid", "cancelled"]),
            booking_fee=random.randint(10000, 50000)
        )
        bookings.append(booking)
    
    # Сохраняем брони
    for booking in bookings:
        session.add(booking)
    
    await session.commit()

async def create_all_mock_data(session: AsyncSession) -> None:
    """Создание всех моковых данных"""
    print("Создание пользователей...")
    await create_mock_users(session)
    
    print("Создание застройщиков...")
    await create_mock_developers(session)
    
    print("Создание проектов...")
    await create_mock_projects(session)
    
    print("Создание зданий...")
    await create_mock_buildings(session)
    
    print("Создание объектов недвижимости...")
    await create_mock_properties(session)
    
    print("Создание адресов...")
    await create_mock_addresses(session)
    
    print("Создание цен...")
    await create_mock_prices(session)
    
    print("Создание медиа...")
    await create_mock_media(session)
    
    print("Создание акций...")
    await create_mock_promotions(session)
    
    print("Создание броней...")
    await create_mock_bookings(session)
    
    print("Моковые данные успешно созданы!")