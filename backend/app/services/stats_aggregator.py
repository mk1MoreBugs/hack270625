from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Optional
from datetime import datetime
from app.models import Apartment, ApartmentStats
from app.crud import CRUDStats


class StatsAggregatorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.stats_crud = CRUDStats(session)
    
    async def update_apartment_stats(self, apartment_id: int) -> ApartmentStats:
        """Обновляет статистику для конкретной квартиры"""
        # Получаем квартиру
        result = await self.session.execute(
            select(Apartment).where(Apartment.id == apartment_id)
        )
        apartment = result.scalar_one_or_none()
        
        if not apartment:
            raise ValueError(f"Квартира с ID {apartment_id} не найдена")
        
        # Собираем статистику через CRUD
        views_24h = await self.stats_crud.get_views_24h(apartment_id)
        leads_24h = await self.stats_crud.get_leads_24h(apartment_id)
        bookings_24h = await self.stats_crud.get_bookings_24h(apartment_id)
        days_on_site = await self.stats_crud.get_days_on_site(apartment)
        
        # Обновляем статистику
        return await self.stats_crud.update_stats(
            apartment_id=apartment_id,
            views_24h=views_24h,
            leads_24h=leads_24h,
            bookings_24h=bookings_24h,
            days_on_site=days_on_site
        )
    
    async def update_all_apartment_stats(self) -> List[ApartmentStats]:
        """Обновляет статистику для всех квартир"""
        result = await self.session.execute(select(Apartment))
        apartments = result.scalars().all()
        
        updated_stats = []
        for apartment in apartments:
            try:
                stats = await self.update_apartment_stats(apartment.id)
                updated_stats.append(stats)
            except Exception as e:
                print(f"Ошибка при обновлении статистики квартиры {apartment.id}: {e}")
                continue
        
        return updated_stats
    
    async def get_apartment_stats(self, apartment_id: int) -> Optional[ApartmentStats]:
        """Получает статистику квартиры"""
        stats = await self.stats_crud.get_apartment_stats(apartment_id)
        
        if not stats:
            # Если статистики нет, создаем ее
            stats = await self.update_apartment_stats(apartment_id)
        
        return stats 