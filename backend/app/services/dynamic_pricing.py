from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import statistics
from app.models import (
    Apartment, ApartmentStats, PriceHistory, ViewsLog, Booking,
    PriceChangeReason, DynamicPricingConfig
)
from app.schemas import DynamicPricingResult
from app.config import settings
from app.crud import apartment, apartment_stats, price_history, booking, dynamic_pricing_config


class DynamicPricingService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.config = None
    
    async def _get_config(self) -> DynamicPricingConfig:
        """Получает актуальную конфигурацию динамического ценообразования"""
        if self.config is None:
            self.config = await dynamic_pricing_config.get_active(self.session)
            
            if not self.config:
                # Создаем дефолтную конфигурацию
                config_data = {
                    "k1": 0.5,  # views coefficient
                    "k2": 2.0,  # leads coefficient  
                    "k3": 5.0,  # bookings coefficient
                    "enabled": True
                }
                self.config = await dynamic_pricing_config.create(self.session, config_data)
        
        return self.config
    
    async def calculate_demand_score(self, apartment: Apartment) -> float:
        """Вычисляет demand_score для квартиры"""
        stats = await apartment_stats.get_by_apartment(self.session, apartment.id)
        
        if not stats:
            return 0.0
        
        config = await self._get_config()
        
        # demand = 0.5·views_t24h + 2·leads_t24h + 5·bookings_t24h
        demand = (
            config.k1 * stats.views_24h +
            config.k2 * stats.leads_24h +
            config.k3 * stats.bookings_24h
        )
        
        return demand
    
    async def get_cluster_median_demand(self, apartment: Apartment) -> float:
        """Получает медианный спрос для кластера (проект + тип комнат)"""
        # Получаем все квартиры того же проекта и типа комнат
        result = await self.session.exec(
            select(Apartment)
            .join(Apartment.building)
            .join(Apartment.building.project)
            .where(
                Apartment.building.project.id == apartment.building.project.id,
                Apartment.rooms == apartment.rooms,
                Apartment.id != apartment.id
            )
        )
        cluster_apartments = result.all()
        
        if not cluster_apartments:
            return 1.0  # Если нет других квартир в кластере
        
        # Вычисляем demand_score для каждой квартиры в кластере
        demand_scores = []
        for apt in cluster_apartments:
            demand = await self.calculate_demand_score(apt)
            if demand > 0:
                demand_scores.append(demand)
        
        if not demand_scores:
            return 1.0
        
        return statistics.median(demand_scores)
    
    async def should_update_price(self, apartment: Apartment) -> bool:
        """Проверяет, можно ли обновлять цену для квартиры"""
        # Проверяем ограничение "не чаще 1 раза в 24 ч"
        recent_changes = await price_history.get_by_apartment(self.session, apartment.id, limit=1)
        
        if recent_changes:
            last_price_change = recent_changes[0]
            time_since_last_change = datetime.utcnow() - last_price_change.changed_at
            if time_since_last_change < timedelta(hours=24):
                return False
        
        # Проверяем, не было ли бронирования в последние 24 часа
        recent_bookings = await booking.get_recent_bookings(self.session, apartment.id, hours=24)
        
        if recent_bookings:
            return False
        
        return True
    
    async def calculate_price_change(self, apartment: Apartment) -> Optional[float]:
        """Вычисляет изменение цены в процентах"""
        demand_score = await self.calculate_demand_score(apartment)
        median_demand = await self.get_cluster_median_demand(apartment)
        
        if median_demand == 0:
            return None
        
        demand_normalized = demand_score / median_demand
        stats = await apartment_stats.get_by_apartment(self.session, apartment.id)
        
        # Алгоритм изменения цены
        if demand_normalized > 1.3:
            # Высокий спрос - повышаем цену
            price_change = min(settings.elasticity_cap, 3.0)
            return price_change
        elif demand_normalized < 0.7 and stats and stats.days_on_site > 14:
            # Низкий спрос и квартира давно на сайте - снижаем цену
            price_change = -min(settings.elasticity_cap, 3.0)
            return price_change
        else:
            # Оставляем цену без изменений
            return 0.0
    
    def apply_price_limits(self, apartment: Apartment, new_price: float) -> float:
        """Применяет ограничения на изменение цены"""
        max_allowed_price = apartment.base_price * (1 + settings.price_max_shift / 100)
        min_allowed_price = apartment.base_price * (1 - settings.price_max_shift / 100)
        
        return max(min_allowed_price, min(max_allowed_price, new_price))
    
    async def generate_price_change_description(self, apartment: Apartment, price_change: float) -> str:
        """Генерирует описание изменения цены"""
        stats = await apartment_stats.get_by_apartment(self.session, apartment.id)
        
        if price_change > 0:
            return f"Цена повышена на {price_change:.1f}% из-за высокого спроса ({stats.views_24h} просмотров за 24 ч)"
        elif price_change < 0:
            return f"Цена снижена на {abs(price_change):.1f}% из-за низкого спроса ({stats.days_on_site} дней на сайте)"
        else:
            return "Цена осталась без изменений"
    
    async def update_apartment_price(self, apartment: Apartment) -> Optional[DynamicPricingResult]:
        """Обновляет цену квартиры согласно алгоритму динамического ценообразования"""
        if not await self.should_update_price(apartment):
            return None
        
        price_change_percent = await self.calculate_price_change(apartment)
        if price_change_percent is None or price_change_percent == 0:
            return None
        
        # Вычисляем новую цену
        price_change_multiplier = 1 + price_change_percent / 100
        new_price = apartment.current_price * price_change_multiplier
        
        # Применяем ограничения
        new_price = self.apply_price_limits(apartment, new_price)
        
        # Проверяем, действительно ли цена изменилась
        if abs(new_price - apartment.current_price) < 0.01:
            return None
        
        old_price = apartment.current_price
        
        # Обновляем цену квартиры
        await apartment.update_price(self.session, apartment.id, new_price)
        
        # Создаем запись в истории цен
        description = await self.generate_price_change_description(apartment, price_change_percent)
        price_history_data = {
            "apartment_id": apartment.id,
            "old_price": old_price,
            "new_price": new_price,
            "reason": PriceChangeReason.DYNAMIC,
            "description": description
        }
        
        await price_history.create(self.session, price_history_data)
        
        # Вычисляем demand_score для результата
        demand_score = await self.calculate_demand_score(apartment)
        median_demand = await self.get_cluster_median_demand(apartment)
        demand_normalized = demand_score / median_demand if median_demand > 0 else 0
        
        return DynamicPricingResult(
            apartment_id=apartment.id,
            old_price=old_price,
            new_price=new_price,
            price_change_percent=price_change_percent,
            demand_score=demand_score,
            demand_normalized=demand_normalized,
            reason="dynamic",
            description=description
        )
    
    async def update_all_apartment_prices(self) -> List[DynamicPricingResult]:
        """Обновляет цены всех доступных квартир"""
        available_apartments = await apartment.get_by_status(self.session, ApartmentStatus.AVAILABLE)
        
        results = []
        for apartment_obj in available_apartments:
            try:
                result = await self.update_apartment_price(apartment_obj)
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Ошибка при обновлении цены квартиры {apartment_obj.id}: {e}")
                continue
        
        return results 