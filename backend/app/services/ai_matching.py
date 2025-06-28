from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Property, PropertyType, PropertyCategory
from typing import List, Optional, Dict, Tuple
from app.crud import crud_property, crud_property_analytics
from datetime import datetime, timedelta


class PropertyMatchingService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def match_properties(
        self,
        budget: float,
        preferred_cities: List[str],
        preferred_districts: Optional[List[str]] = None,
        min_rooms: Optional[int] = None,
        max_rooms: Optional[int] = None,
        min_area: Optional[float] = None,
        max_area: Optional[float] = None,
        property_type: Optional[PropertyType] = None,
        category: Optional[PropertyCategory] = None,
        has_balcony: Optional[bool] = None,
        has_parking: Optional[bool] = None,
        max_floor: Optional[int] = None,
        limit: int = 10
    ) -> List[Property]:
        """
        ИИ-подбор объектов недвижимости по предпочтениям пользователя.
        Использует взвешенный скоринг для ранжирования результатов.
        """
        # Получаем базовый список объектов
        properties = await crud_property.get_available(self.session)
        
        # Фильтруем объекты по базовым критериям
        filtered_properties = []
        for prop in properties:
            # Проверяем цену
            if prop.price and prop.price.current_price > budget * 1.2:  # Допускаем превышение бюджета не более чем на 20%
                continue
            
            # Проверяем город
            if preferred_cities and prop.address and prop.address.city not in preferred_cities:
                continue
                
            # Проверяем район
            if preferred_districts and prop.address and prop.address.district not in preferred_districts:
                continue
                
            # Проверяем тип недвижимости
            if property_type and prop.property_type != property_type:
                continue
                
            # Проверяем категорию
            if category and prop.category != category:
                continue
                
            # Проверяем количество комнат (только для жилой недвижимости)
            if min_rooms and prop.residential and prop.residential.rooms and prop.residential.rooms < min_rooms:
                continue
                
            if max_rooms and prop.residential and prop.residential.rooms and prop.residential.rooms > max_rooms:
                continue
                
            # Проверяем площадь (только для жилой недвижимости)
            if min_area and prop.residential and prop.residential.total_area and prop.residential.total_area < min_area:
                continue
                
            if max_area and prop.residential and prop.residential.total_area and prop.residential.total_area > max_area:
                continue
                
            # Проверяем особенности
            if has_balcony is not None and prop.features and prop.features.balcony != has_balcony:
                continue
                
            if has_parking is not None and prop.features and prop.features.parking_type and not has_parking:
                continue
                
            # Проверяем этаж (только для жилой недвижимости)
            if max_floor and prop.residential and prop.residential.floor and prop.residential.floor > max_floor:
                continue
            
            filtered_properties.append(prop)
        
        if not filtered_properties:
            return []

        # Рассчитываем скоринг для каждого объекта
        scored_properties = []
        for property_obj in filtered_properties:
            score = await self._calculate_property_score(
                property_obj,
                budget=budget,
                preferred_districts=preferred_districts
            )
            scored_properties.append((property_obj, score))
        
        # Сортируем по скорингу и возвращаем топ limit объектов
        scored_properties.sort(key=lambda x: x[1], reverse=True)
        return [property_obj for property_obj, _ in scored_properties[:limit]]

    async def _calculate_property_score(
        self,
        property_obj: Property,
        budget: float,
        preferred_districts: Optional[List[str]]
    ) -> float:
        """
        Рассчитывает скоринг для объекта недвижимости на основе различных факторов.
        
        Факторы:
        1. Соответствие бюджету (вес: 0.3)
        2. Популярность района (вес: 0.2)
        3. Спрос на объект (вес: 0.2)
        4. Активность просмотров (вес: 0.15)
        5. Новизна объявления (вес: 0.15)
        """
        weights = {
            'budget_match': 0.3,
            'district_popularity': 0.2,
            'demand': 0.2,
            'views': 0.15,
            'freshness': 0.15
        }
        
        scores = {}
        
        # 1. Соответствие бюджету
        if property_obj.price:
            price_diff_percent = abs(property_obj.price.current_price - budget) / budget
            scores['budget_match'] = max(0, 1 - price_diff_percent)
        else:
            scores['budget_match'] = 0.5
        
        # 2. Популярность района
        if property_obj.address and property_obj.address.district:
            # Базовая популярность района (можно расширить логикой)
            scores['district_popularity'] = 0.7  # Заглушка
        else:
            scores['district_popularity'] = 0.5
        
        # 3. Спрос на объект
        if property_obj.analytics and property_obj.analytics.demand_score:
            scores['demand'] = min(1.0, property_obj.analytics.demand_score / 10.0)
        else:
            scores['demand'] = 0.5
        
        # 4. Активность просмотров
        if property_obj.analytics and property_obj.analytics.clicks_total:
            # Нормализуем количество просмотров
            scores['views'] = min(1.0, property_obj.analytics.clicks_total / 1000.0)
        else:
            scores['views'] = 0.5
        
        # 5. Новизна объявления
        days_active = (datetime.utcnow() - property_obj.created_at).days
        scores['freshness'] = max(0, 1 - (days_active / 30))  # Линейное убывание в течение 30 дней
        
        # Рассчитываем финальный скор
        final_score = sum(score * weights[factor] for factor, score in scores.items())
        
        # Применяем бонус если район в предпочитаемых
        if preferred_districts and property_obj.address and property_obj.address.district in preferred_districts:
            final_score *= 1.2
        
        return final_score 