from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from app.models import Property, PropertyAnalytics, ViewsLog, Booking
from app.crud import CRUDPropertyAnalytics


class StatsAggregatorService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.analytics_crud = CRUDPropertyAnalytics(session)
    
    async def update_property_stats(self, property_id: int) -> PropertyAnalytics:
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
        
        # Получаем или создаем объект аналитики
        result = await self.session.execute(
            select(PropertyAnalytics).where(PropertyAnalytics.property_id == property_id)
        )
        analytics = result.scalar_one_or_none()
        
        if not analytics:
            analytics = PropertyAnalytics(property_id=property_id)
        
        # Получаем даты для расчетов
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        
        # Получаем количество просмотров за последнюю неделю
        views_week_result = await self.session.execute(
            select(func.count(ViewsLog.id))
            .where(
                and_(
                    ViewsLog.property_id == property_id,
                    ViewsLog.occurred_at >= week_ago
                )
            )
        )
        analytics.views_last_week = views_week_result.scalar() or 0
        
        # Получаем количество просмотров за последний месяц
        views_month_result = await self.session.execute(
            select(func.count(ViewsLog.id))
            .where(
                and_(
                    ViewsLog.property_id == property_id,
                    ViewsLog.occurred_at >= month_ago
                )
            )
        )
        analytics.views_last_month = views_month_result.scalar() or 0
        
        # Получаем общее количество просмотров
        views_total_result = await self.session.execute(
            select(func.count(ViewsLog.id))
            .where(ViewsLog.property_id == property_id)
        )
        analytics.clicks_total = views_total_result.scalar() or 0
        
        # Получаем количество бронирований
        bookings_result = await self.session.execute(
            select(func.count(Booking.id))
            .where(Booking.property_id == property_id)
        )
        analytics.bookings_total = bookings_result.scalar() or 0
        
        # Получаем дату создания объекта
        property_result = await self.session.execute(
            select(Property.created_at)
            .where(Property.id == property_id)
        )
        created_at = property_result.scalar_one_or_none()
        
        if created_at:
            # Вычисляем количество дней на рынке
            days_on_market = (now - created_at).days
            analytics.days_on_market = max(0, days_on_market)
        
        # Рассчитываем RLI индекс (отношение просмотров к среднему)
        if analytics.views_last_month > 0:
            avg_views_result = await self.session.execute(
                select(func.avg(PropertyAnalytics.views_last_month))
            )
            avg_views = avg_views_result.scalar() or 1
            analytics.rli_index = min(analytics.views_last_month / avg_views, 1.0)
        
        # Рассчитываем оценку спроса
        if analytics.clicks_total > 0:
            views_weight = 0.4
            bookings_weight = 0.6
            max_views = 1000  # Предполагаемое максимальное количество просмотров
            max_bookings = 50  # Предполагаемое максимальное количество бронирований
            
            views_score = min(analytics.clicks_total / max_views, 1.0) * views_weight * 100
            bookings_score = min(analytics.bookings_total / max_bookings, 1.0) * bookings_weight * 100
            analytics.demand_score = int(views_score + bookings_score)
        
        # Сохраняем изменения
        self.session.add(analytics)
        await self.session.commit()
        await self.session.refresh(analytics)
        
        return analytics
    
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
    
    async def get_property_stats(self, property_id: int) -> Optional[PropertyAnalytics]:
        """Получает статистику объекта недвижимости"""
        stats = await self.analytics_crud.get(self.session, property_id)
        
        if not stats:
            # Если статистики нет, создаем ее
            stats = await self.update_property_stats(property_id)
        
        return stats

    async def get_market_stats(
        self,
        days: int = 30,
        property_type: Optional[str] = None,
        city: Optional[str] = None
    ) -> Dict[str, Any]:
        """Получает статистику по рынку"""
        now = datetime.utcnow()
        start_date = now - timedelta(days=days)
        
        # Базовый запрос для фильтрации по времени
        query = select(Property).where(Property.created_at >= start_date)
        
        # Добавляем дополнительные фильтры
        if property_type:
            query = query.where(Property.property_type == property_type)
        
        # Получаем объекты
        result = await self.session.execute(query)
        properties = result.scalars().all()
        
        if not properties:
            return {
                "total_properties": 0,
                "avg_views": 0,
                "avg_bookings": 0,
                "avg_days_on_market": 0
            }
        
        # Собираем статистику
        total_views = 0
        total_bookings = 0
        total_days = 0
        
        for prop in properties:
            if prop.analytics:
                total_views += prop.analytics.views_last_month or 0
                total_bookings += prop.analytics.bookings_total or 0
                total_days += prop.analytics.days_on_market or 0
        
        count = len(properties)
        
        return {
            "total_properties": count,
            "avg_views": round(total_views / count, 2),
            "avg_bookings": round(total_bookings / count, 2),
            "avg_days_on_market": round(total_days / count, 2)
        } 