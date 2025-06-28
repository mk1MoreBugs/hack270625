from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
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
    
    async def calculate_demand_score(self, property_obj: Property) -> float:
        """Вычисляет demand_score для объекта недвижимости"""
        analytics = await crud_property_analytics.get(self.session, property_obj.id)
        
        if not analytics:
            return 0.0
        
        config = await self._get_config()
        
        # demand = 0.5·views_t24h + 2·leads_t24h + 5·bookings_t24h
        demand = (
            config.k1 * analytics.clicks_total +
            config.k2 * analytics.favourites_total +
            config.k3 * analytics.bookings_total
        )
        
        return demand
    
    async def get_cluster_median_demand(self, property_obj: Property) -> float:
        """Получает медианный спрос для кластера (проект + тип комнат)"""
        # Получаем все объекты того же проекта и типа комнат
        cluster_properties = await self.crud.get_cluster_properties(
            property_obj.project.id if property_obj.project else None,
            property_obj.residential.rooms if property_obj.residential else None,
            property_obj.id
        )
        
        if not cluster_properties:
            return 1.0  # Если нет других объектов в кластере
        
        # Вычисляем demand_score для каждого объекта в кластере
        demand_scores = []
        for prop in cluster_properties:
            demand = await self.calculate_demand_score(prop)
            if demand > 0:
                demand_scores.append(demand)
        
        if not demand_scores:
            return 1.0
        
        return statistics.median(demand_scores)
    
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
    
    async def calculate_price_change(self, property_obj: Property) -> Optional[float]:
        """Вычисляет изменение цены в процентах"""
        demand_score = await self.calculate_demand_score(property_obj)
        median_demand = await self.get_cluster_median_demand(property_obj)
        
        if median_demand == 0:
            return None
        
        demand_normalized = demand_score / median_demand
        analytics = await crud_property_analytics.get(self.session, property_obj.id)
        
        # Алгоритм изменения цены
        if demand_normalized > 1.3:
            # Высокий спрос - повышаем цену
            price_change = min(settings.elasticity_cap, 3.0)
            return price_change
        elif demand_normalized < 0.7 and analytics and analytics.days_on_market > 14:
            # Низкий спрос и объект давно на сайте - снижаем цену
            price_change = -min(settings.elasticity_cap, 3.0)
            return price_change
        else:
            # Оставляем цену без изменений
            return 0.0
    
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
    
    async def update_property_price(self, property_obj: Property) -> Optional[DynamicPricingResult]:
        """Обновляет цену объекта недвижимости согласно алгоритму динамического ценообразования"""
        if not await self.should_update_price(property_obj):
            return None
        
        price_change_percent = await self.calculate_price_change(property_obj)
        if price_change_percent is None or price_change_percent == 0:
            return None
        
        # Вычисляем новую цену
        price_change_multiplier = 1 + price_change_percent / 100
        new_price = property_obj.price.current_price * price_change_multiplier
        
        # Применяем ограничения
        new_price = self.apply_price_limits(property_obj, new_price)
        
        # Проверяем, действительно ли цена изменилась
        if abs(new_price - property_obj.price.current_price) < 0.01:
            return None
        
        old_price = property_obj.price.current_price
        
        # Обновляем цену объекта недвижимости
        await self.crud.update_property_price(property_obj.id, new_price)
        
        # Создаем запись в истории цен
        description = await self.generate_price_change_description(property_obj, price_change_percent)
        price_history_data = {
            "property_id": property_obj.id,
            "old_price": old_price,
            "new_price": new_price,
            "reason": PriceChangeReason.DYNAMIC,
            "description": description
        }
        
        await self.crud.create_price_history(price_history_data)
        
        # Вычисляем demand_score для результата
        demand_score = await self.calculate_demand_score(property_obj)
        median_demand = await self.get_cluster_median_demand(property_obj)
        demand_normalized = demand_score / median_demand if median_demand > 0 else 0
        
        return DynamicPricingResult(
            property_id=property_obj.id,
            old_price=old_price,
            new_price=new_price,
            price_change_percent=price_change_percent,
            demand_score=demand_score,
            demand_normalized=demand_normalized,
            reason="dynamic",
            description=description
        )
    
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