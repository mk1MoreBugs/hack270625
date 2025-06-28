from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime
from app.models import Property, PropertyAnalytics
from app.crud import CRUDPropertyAnalytics


class StatsAggregatorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.analytics_crud = CRUDPropertyAnalytics(PropertyAnalytics)
    
    async def update_property_stats(self, property_id: str) -> PropertyAnalytics:
        """Обновляет статистику для конкретного объекта недвижимости"""
        # Получаем объект недвижимости
        result = await self.session.execute(
            select(Property).where(Property.id == property_id)
        )
        property_obj = result.scalar_one_or_none()
        
        if not property_obj:
            raise ValueError(f"Объект недвижимости с ID {property_id} не найден")
        
        # Собираем статистику через CRUD
        views_24h = await self.analytics_crud.get_views_count(self.session, property_id, hours=24)
        leads_24h = await self.analytics_crud.get_favourites_count(self.session, property_id, hours=24)
        bookings_24h = await self.analytics_crud.get_bookings_count(self.session, property_id, hours=24)
        days_on_site = await self.analytics_crud.get_days_on_market(self.session, property_obj)
        
        # Обновляем статистику
        return await self.analytics_crud.update_stats(
            self.session,
            property_id=property_id,
            days_on_market=days_on_site,
            clicks_total=views_24h,
            favourites_total=leads_24h,
            bookings_total=bookings_24h
        )
    
    async def update_all_property_stats(self) -> List[PropertyAnalytics]:
        """Обновляет статистику для всех объектов недвижимости"""
        result = await self.session.execute(select(Property))
        properties = result.scalars().all()
        
        updated_stats = []
        for property_obj in properties:
            try:
                stats = await self.update_property_stats(property_obj.id)
                updated_stats.append(stats)
            except Exception as e:
                print(f"Ошибка при обновлении статистики объекта {property_obj.id}: {e}")
                continue
        
        return updated_stats
    
    async def get_property_stats(self, property_id: str) -> Optional[PropertyAnalytics]:
        """Получает статистику объекта недвижимости"""
        stats = await self.analytics_crud.get(self.session, property_id)
        
        if not stats:
            # Если статистики нет, создаем ее
            stats = await self.update_property_stats(property_id)
        
        return stats 