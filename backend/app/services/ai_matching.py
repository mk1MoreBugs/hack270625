from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Apartment, Building, Project
from typing import List, Optional
from app.models import PropertyClass


async def match_apartments(
    db: AsyncSession,
    budget: float,
    preferred_cities: List[str],
    preferred_districts: Optional[List[str]] = None,
    min_rooms: Optional[int] = None,
    max_rooms: Optional[int] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    property_class: Optional[PropertyClass] = None,
    has_balcony: Optional[bool] = None,
    has_parking: Optional[bool] = None,
    max_floor: Optional[int] = None,
    limit: int = 10
) -> List[Apartment]:
    """
    ИИ-подбор квартир по предпочтениям пользователя.
    Использует взвешенный скоринг для ранжирования результатов.
    """
    # Базовый запрос
    query = (
        select(Apartment)
        .join(Building)
        .join(Project)
        .filter(
            and_(
                Apartment.current_price <= budget,
                Project.city.in_(preferred_cities)
            )
        )
    )
    
    # Добавляем фильтры по опциональным параметрам
    if min_rooms:
        query = query.filter(Apartment.rooms >= min_rooms)
    if max_rooms:
        query = query.filter(Apartment.rooms <= max_rooms)
    if min_area:
        query = query.filter(Apartment.area_total >= min_area)
    if max_area:
        query = query.filter(Apartment.area_total <= max_area)
    if property_class:
        query = query.filter(Project.class_type == property_class)
    if has_balcony is not None:
        query = query.filter(Apartment.balcony == has_balcony)
    if has_parking is not None:
        query = query.filter(Apartment.parking == has_parking)
    if max_floor:
        query = query.filter(Apartment.floor <= max_floor)
    if preferred_districts:
        # Предполагаем, что район можно извлечь из адреса
        district_conditions = [
            Project.address.ilike(f"%{district}%")
            for district in preferred_districts
        ]
        query = query.filter(or_(*district_conditions))
    
    # Добавляем скоринг для ранжирования
    # TODO: Добавить ML-модель для более точного ранжирования
    query = query.order_by(
        # Приоритет отдаем квартирам, которые ближе к желаемому бюджету
        (Apartment.current_price / budget).desc()
    )
    
    # Получаем результаты
    result = await db.execute(query.limit(limit))
    return result.scalars().all() 