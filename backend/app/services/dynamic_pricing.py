from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import statistics
from app.models import (
    Property, PropertyAnalytics, PriceHistory, ViewsLog, Booking,
    PriceChangeReason, DynamicPricingConfig, PropertyStatus
)
from app.schemas import DynamicPricingResult
from app.config import settings
from app.crud import (
    crud_property, crud_property_analytics, crud_booking, crud_dynamic_pricing_config,
    CRUDDynamicPricing
)


class DynamicPricingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.config = None
        self.crud = CRUDDynamicPricing(session)
    
    async def _get_config(self) -> DynamicPricingConfig:
        """Получает актуальную конфигурацию динамического ценообразования"""
        if self.config is None:
            self.config = await crud_dynamic_pricing_config.get_active(self.session)
            
            if not self.config:
                # Создаем дефолтную конфигурацию
                config_data = {
                    "k1": 0.5,  # views coefficient
                    "k2": 2.0,  # leads coefficient  
                    "k3": 5.0,  # bookings coefficient
                    "enabled": True
                }
                self.config = await crud_dynamic_pricing_config.create(self.session, config_data)
        
        return self.config
    
    async def calculate_demand_score(self, property_id: int) -> float:
        """Рассчитывает оценку спроса на основе просмотров и бронирований"""
        # Получаем статистику за последние 30 дней
        start_date = datetime.utcnow() - timedelta(days=30)
        
        # Получаем количество просмотров
        views_result = await self.session.execute(
            select(func.count(ViewsLog.id))
            .where(
                and_(
                    ViewsLog.property_id == property_id,
                    ViewsLog.occurred_at >= start_date
                )
            )
        )
        views_count = views_result.scalar() or 0
        
        # Получаем количество бронирований
        bookings_result = await self.session.execute(
            select(func.count(Booking.id))
            .where(
                and_(
                    Booking.property_id == property_id,
                    Booking.booked_at >= start_date
                )
            )
        )
        bookings_count = bookings_result.scalar() or 0
        
        # Простая формула для оценки спроса
        # Можно настроить веса для просмотров и бронирований
        views_weight = 0.3
        bookings_weight = 0.7
        
        # Нормализуем значения (предполагаем, что хорошие показатели - это 100 просмотров и 5 бронирований в месяц)
        normalized_views = min(views_count / 100.0, 1.0)
        normalized_bookings = min(bookings_count / 5.0, 1.0)
        
        return (normalized_views * views_weight + normalized_bookings * bookings_weight) * 100
    
    async def get_cluster_median_demand(self, property_obj: Property) -> float:
        """Получает медианный спрос для кластера (проект + тип комнат)"""
        # Получаем все объекты того же проекта и типа комнат
        project_id = property_obj.project_id if property_obj.project else None
        rooms = property_obj.residential.rooms if property_obj.residential else None
        
        cluster_properties = await self.crud.get_cluster_properties(
            project_id,
            rooms,
            property_obj.id
        )
        
        if not cluster_properties:
            return 0.0
        
        # Вычисляем медианный спрос
        demands = [p.analytics.demand_score for p in cluster_properties if p.analytics]
        if not demands:
            return 0.0
        
        demands.sort()
        mid = len(demands) // 2
        if len(demands) % 2 == 0:
            return (demands[mid - 1] + demands[mid]) / 2
        return demands[mid]
    
    async def should_update_price(self, property_obj: Property) -> bool:
        """Проверяет, можно ли обновлять цену для объекта недвижимости"""
        # Проверяем ограничение "не чаще 1 раза в 24 ч"
        recent_changes = await self.crud.get_recent_price_changes(property_obj.id)
        
        if recent_changes:
            last_price_change = recent_changes[0]
            time_since_last_change = datetime.utcnow() - last_price_change.changed_at
            if time_since_last_change < timedelta(hours=24):
                return False
        
        # Проверяем, не было ли бронирования в последние 24 часа
        recent_bookings = await crud_booking.get_recent_bookings(self.session, property_obj.id, hours=24)
        
        if recent_bookings:
            return False
        
        return True
    
    async def calculate_price_adjustment(
        self,
        current_price: float,
        demand_score: float,
        median_demand: float
    ) -> float:
        """Рассчитывает корректировку цены на основе спроса"""
        # Настройки для корректировки цены
        max_adjustment = 0.10  # Максимальное изменение цены (10%)
        demand_threshold = 0.2  # Порог разницы в спросе для изменения цены
        
        # Нормализуем оценки спроса
        demand_normalized = demand_score / 100.0
        median_normalized = median_demand / 100.0
        
        # Вычисляем разницу в спросе
        demand_diff = demand_normalized - median_normalized
        
        if abs(demand_diff) < demand_threshold:
            return current_price
        
        # Рассчитываем процент изменения
        adjustment_percent = demand_diff * max_adjustment
        
        # Применяем изменение к текущей цене
        new_price = current_price * (1 + adjustment_percent)
        
        # Округляем до тысяч
        return round(new_price / 1000) * 1000
    
    def apply_price_limits(self, property_obj: Property, new_price: float) -> float:
        """Применяет ограничения на изменение цены"""
        if not property_obj.price:
            return new_price
            
        max_allowed_price = property_obj.price.base_price * (1 + settings.price_max_shift / 100)
        min_allowed_price = property_obj.price.base_price * (1 - settings.price_max_shift / 100)
        
        return max(min_allowed_price, min(max_allowed_price, new_price))
    
    async def generate_price_change_description(self, property_obj: Property, price_change: float) -> str:
        """Генерирует описание изменения цены"""
        analytics = await crud_property_analytics.get(self.session, property_obj.id)
        
        if price_change > 0:
            return f"Цена повышена на {price_change:.1f}% из-за высокого спроса ({analytics.clicks_total} просмотров за 24 ч)"
        elif price_change < 0:
            return f"Цена снижена на {abs(price_change):.1f}% из-за низкого спроса ({analytics.days_on_market} дней на сайте)"
        else:
            return "Цена осталась без изменений"
    
    async def update_property_price(self, property_obj: Property) -> Dict[str, Any]:
        """Обновляет цену объекта на основе динамического ценообразования"""
        if not property_obj.price:
            return {
                "success": False,
                "error": "Property has no price information"
            }
        
        # Получаем текущие показатели
        current_price = property_obj.price.current_price
        demand_score = await self.calculate_demand_score(property_obj.id)
        median_demand = await self.get_cluster_median_demand(property_obj)
        
        # Рассчитываем новую цену
        new_price = await self.calculate_price_adjustment(
            current_price,
            demand_score,
            median_demand
        )
        
        if new_price == current_price:
            return {
                "success": True,
                "message": "No price adjustment needed",
                "price_change": 0
            }
        
        # Определяем причину изменения
        price_change = new_price - current_price
        price_change_percent = (price_change / current_price) * 100
        
        if price_change > 0:
            reason = "high_demand"
            description = "Increased due to high demand"
        else:
            reason = "low_demand"
            description = "Decreased due to low demand"
        
        # Обновляем цену
        await self.crud.update_property_price(
            property_obj.id,
            new_price,
            reason,
            description
        )
        
        return {
            "success": True,
            "old_price": current_price,
            "new_price": new_price,
            "price_change": price_change,
            "price_change_percent": price_change_percent,
            "demand_score": demand_score,
            "median_demand": median_demand,
            "reason": reason,
            "description": description
        }
    
    async def update_all_property_prices(self) -> List[DynamicPricingResult]:
        """Обновляет цены всех доступных объектов недвижимости"""
        available_properties = await crud_property.get_by_status(self.session, PropertyStatus.AVAILABLE)
        
        results = []
        for property_obj in available_properties:
            try:
                result = await self.update_property_price(property_obj)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Ошибка при обновлении цены объекта {property_obj.id}: {e}")
                continue
        
        return results 