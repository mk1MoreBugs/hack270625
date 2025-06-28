from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Apartment, PropertyClass
from typing import List, Optional, Dict, Tuple
from app.crud import CRUDStats, CRUDApartment
from datetime import datetime, timedelta


class ApartmentMatchingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.stats = CRUDStats(session)
        self.apartments = CRUDApartment(Apartment)
    
    async def match_apartments(
        self,
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
        # Получаем базовый список квартир
        apartments = await self.apartments.get_available(self.session)
        
        # Фильтруем квартиры по базовым критериям
        filtered_apartments = []
        for apt in apartments:
            if apt.price > budget * 1.2:  # Допускаем превышение бюджета не более чем на 20%
                continue
            
            if preferred_cities and apt.building.project.city not in preferred_cities:
                continue
                
            if preferred_districts and apt.building.project.district not in preferred_districts:
                continue
                
            if min_rooms and apt.rooms < min_rooms:
                continue
                
            if max_rooms and apt.rooms > max_rooms:
                continue
                
            if min_area and apt.area_total < min_area:
                continue
                
            if max_area and apt.area_total > max_area:
                continue
                
            if property_class and apt.building.project.class_type != property_class:
                continue
                
            if has_balcony is not None and apt.has_balcony != has_balcony:
                continue
                
            if has_parking is not None and apt.has_parking != has_parking:
                continue
                
            if max_floor and apt.floor > max_floor:
                continue
            
            filtered_apartments.append(apt)
        
        if not filtered_apartments:
            return []

        # Рассчитываем скоринг для каждой квартиры
        scored_apartments = []
        for apartment in filtered_apartments:
            score = await self._calculate_apartment_score(
                apartment,
                budget=budget,
                preferred_districts=preferred_districts
            )
            scored_apartments.append((apartment, score))
        
        # Сортируем по скорингу и возвращаем топ limit квартир
        scored_apartments.sort(key=lambda x: x[1], reverse=True)
        return [apartment for apartment, _ in scored_apartments[:limit]]

    async def _calculate_apartment_score(
        self,
        apartment: Apartment,
        budget: float,
        preferred_districts: Optional[List[str]]
    ) -> float:
        """
        Рассчитывает скоринг для квартиры на основе различных факторов.
        
        Факторы:
        1. Соответствие бюджету (вес: 0.3)
        2. Популярность района (вес: 0.2)
        3. Качество инфраструктуры (вес: 0.15)
        4. Транспортная доступность (вес: 0.15)
        5. Активность просмотров (вес: 0.1)
        6. Новизна объявления (вес: 0.1)
        """
        weights = {
            'budget_match': 0.3,
            'district_popularity': 0.2,
            'infrastructure': 0.15,
            'transport': 0.15,
            'views': 0.1,
            'freshness': 0.1
        }
        
        scores = {}
        
        # 1. Соответствие бюджету
        price_diff_percent = abs(apartment.current_price - budget) / budget
        scores['budget_match'] = max(0, 1 - price_diff_percent)
        
        # 2. Популярность района
        district_stats = await self.stats.get_district_stats(apartment.building.project.district)
        scores['district_popularity'] = min(1.0, district_stats.get('popularity_score', 0.5))
        
        # 3. Качество инфраструктуры (нормализованный скор из базы)
        scores['infrastructure'] = min(1.0, apartment.infrastructure_score or 0.5)
        
        # 4. Транспортная доступность (нормализованный скор из базы)
        scores['transport'] = min(1.0, apartment.transport_score or 0.5)
        
        # 5. Активность просмотров за последние 24 часа
        views_24h = await self.stats.get_views_24h(apartment.id)
        avg_views = await self.stats.get_avg_views_24h()
        scores['views'] = min(1.0, views_24h / (avg_views * 2)) if avg_views > 0 else 0.5
        
        # 6. Новизна объявления
        days_active = (datetime.utcnow() - apartment.created_at).days
        scores['freshness'] = max(0, 1 - (days_active / 30))  # Линейное убывание в течение 30 дней
        
        # Рассчитываем финальный скор
        final_score = sum(score * weights[factor] for factor, score in scores.items())
        
        # Применяем бонус если район в предпочитаемых
        if preferred_districts and apartment.building.project.district in preferred_districts:
            final_score *= 1.2
        
        return final_score 