from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func
from typing import List
from datetime import datetime, timedelta
from app.models import Apartment, ApartmentStats, ViewsLog, Booking
from app.crud import apartment_stats, views_log, booking


class StatsAggregatorService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def calculate_views_24h(self, apartment_id: int) -> int:
        """Вычисляет количество просмотров за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.session.exec(
            select(func.count(ViewsLog.id))
            .where(
                ViewsLog.apartment_id == apartment_id,
                ViewsLog.event == "view",
                ViewsLog.occurred_at >= yesterday
            )
        )
        count = result.first()
        return count or 0
    
    async def calculate_leads_24h(self, apartment_id: int) -> int:
        """Вычисляет количество лидов за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        # Лиды - это уникальные пользователи, которые просмотрели квартиру
        result = await self.session.exec(
            select(func.count(func.distinct(ViewsLog.user_id)))
            .where(
                ViewsLog.apartment_id == apartment_id,
                ViewsLog.user_id.is_not(None),
                ViewsLog.occurred_at >= yesterday
            )
        )
        count = result.first()
        return count or 0
    
    async def calculate_bookings_24h(self, apartment_id: int) -> int:
        """Вычисляет количество бронирований за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.session.exec(
            select(func.count(Booking.id))
            .where(
                Booking.apartment_id == apartment_id,
                Booking.booked_at >= yesterday
            )
        )
        count = result.first()
        return count or 0
    
    async def calculate_days_on_site(self, apartment: Apartment) -> int:
        """Вычисляет количество дней, которые квартира находится на сайте"""
        days_on_site = (datetime.utcnow() - apartment.created_at).days
        return max(0, days_on_site)
    
    async def update_apartment_stats(self, apartment_id: int) -> ApartmentStats:
        """Обновляет статистику для конкретной квартиры"""
        apartment = await self.session.exec(
            select(Apartment).where(Apartment.id == apartment_id)
        ).first()
        
        if not apartment:
            raise ValueError(f"Квартира с ID {apartment_id} не найдена")
        
        views_24h = await self.calculate_views_24h(apartment_id)
        leads_24h = await self.calculate_leads_24h(apartment_id)
        bookings_24h = await self.calculate_bookings_24h(apartment_id)
        days_on_site = await self.calculate_days_on_site(apartment)
        
        # Обновляем статистику через CRUD
        stats = await apartment_stats.update_stats(
            self.session, 
            apartment_id, 
            views_24h, 
            leads_24h, 
            bookings_24h, 
            days_on_site
        )
        
        return stats
    
    async def update_all_apartment_stats(self) -> List[ApartmentStats]:
        """Обновляет статистику для всех квартир"""
        apartments = await self.session.exec(select(Apartment)).all()
        
        updated_stats = []
        for apartment in apartments:
            try:
                stats = await self.update_apartment_stats(apartment.id)
                updated_stats.append(stats)
            except Exception as e:
                print(f"Ошибка при обновлении статистики квартиры {apartment.id}: {e}")
                continue
        
        return updated_stats
    
    async def get_apartment_stats(self, apartment_id: int) -> ApartmentStats:
        """Получает статистику квартиры"""
        stats = await apartment_stats.get_by_apartment(self.session, apartment_id)
        
        if not stats:
            # Если статистики нет, создаем ее
            stats = await self.update_apartment_stats(apartment_id)
        
        return stats 