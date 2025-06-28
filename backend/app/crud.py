from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional, TypeVar, Generic, Type, Dict, Any
from app.models import (
    User, Developer, Project, Building, Apartment, 
    ApartmentStats, PriceHistory, ViewsLog, Booking,
    Promotion, WebhookInbox, DynamicPricingConfig,
    UserRole, PropertyClass, ApartmentStatus, BookingStatus,
    ViewEvent, PriceChangeReason
)
from datetime import datetime, timedelta
import json
from sqlalchemy import and_, or_, func

# Generic type для CRUD операций
ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """Базовый класс для CRUD операций"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.first()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """Получить список объектов с пагинацией"""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: dict) -> ModelType:
        """Создать новый объект"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(
        self, 
        db: AsyncSession, 
        db_obj: ModelType, 
        obj_in: dict
    ) -> ModelType:
        """Обновить объект"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, id: int) -> bool:
        """Удалить объект по ID"""
        obj = await self.get(db, id)
        if obj:
            await db.delete(obj)
            await db.commit()
            return True
        return False


class CRUDUser(CRUDBase[User]):
    """CRUD операции для пользователей"""
    
    async def get_by_email(self, db: AsyncSession, email: str):
        """Получить пользователя по email"""
        result = await db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_by_role(self, db: AsyncSession, role: UserRole):
        """Получить пользователей по роли"""
        result = await db.execute(select(User).filter(User.role == role))
        return result.scalars().all()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100):
        """Получить список пользователей"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


class CRUDDeveloper(CRUDBase[Developer]):
    """CRUD операции для застройщиков"""
    
    async def get_by_inn(self, db: AsyncSession, inn: str) -> Optional[Developer]:
        """Получить застройщика по ИНН"""
        result = await db.execute(select(Developer).where(Developer.inn == inn))
        return result.first()
    
    async def get_verified(self, db: AsyncSession) -> List[Developer]:
        """Получить верифицированных застройщиков"""
        result = await db.execute(select(Developer).where(Developer.verified == True))
        return result.all()


class CRUDProject(CRUDBase[Project]):
    """CRUD операции для проектов"""
    
    async def get_by_city(self, db: AsyncSession, city: str) -> List[Project]:
        """Получить проекты по городу"""
        result = await db.execute(select(Project).where(Project.city == city))
        return result.all()
    
    async def get_by_developer(self, db: AsyncSession, developer_id: int) -> List[Project]:
        """Получить проекты застройщика"""
        result = await db.execute(select(Project).where(Project.developer_id == developer_id))
        return result.all()
    
    async def get_by_class(self, db: AsyncSession, class_type: PropertyClass) -> List[Project]:
        """Получить проекты по классу недвижимости"""
        result = await db.execute(select(Project).where(Project.class_type == class_type))
        return result.all()


class CRUDBuilding(CRUDBase[Building]):
    """CRUD операции для корпусов"""
    
    async def get_by_project(self, db: AsyncSession, project_id: int) -> List[Building]:
        """Получить корпуса проекта"""
        result = await db.execute(select(Building).where(Building.project_id == project_id))
        return result.all()


class CRUDApartment(CRUDBase[Apartment]):
    """CRUD операции для квартир"""
    
    async def get_by_building(self, db: AsyncSession, building_id: int) -> List[Apartment]:
        """Получить квартиры корпуса"""
        result = await db.execute(select(Apartment).where(Apartment.building_id == building_id))
        return result.all()
    
    async def get_by_status(self, db: AsyncSession, status: ApartmentStatus) -> List[Apartment]:
        """Получить квартиры по статусу"""
        result = await db.execute(select(Apartment).where(Apartment.status == status))
        return result.all()
    
    async def get_by_rooms(self, db: AsyncSession, rooms: int) -> List[Apartment]:
        """Получить квартиры по количеству комнат"""
        result = await db.execute(select(Apartment).where(Apartment.rooms == rooms))
        return result.all()
    
    async def get_by_price_range(
        self, 
        db: AsyncSession, 
        min_price: float, 
        max_price: float
    ) -> List[Apartment]:
        """Получить квартиры в диапазоне цен"""
        result = await db.execute(
            select(Apartment).where(
                Apartment.current_price >= min_price,
                Apartment.current_price <= max_price
            )
        )
        return result.all()
    
    async def get_available(self, db: AsyncSession) -> List[Apartment]:
        """Получить доступные квартиры"""
        return await self.get_by_status(db, ApartmentStatus.AVAILABLE)
    
    async def update_price(
        self, 
        db: AsyncSession, 
        apartment_id: int, 
        new_price: float
    ) -> Optional[Apartment]:
        """Обновить цену квартиры"""
        apartment = await self.get(db, apartment_id)
        if apartment:
            apartment.current_price = new_price
            apartment.updated_at = datetime.utcnow()
            db.add(apartment)
            await db.commit()
            await db.refresh(apartment)
        return apartment


class CRUDApartmentStats(CRUDBase[ApartmentStats]):
    """CRUD операции для статистики квартир"""
    
    async def get_by_apartment(self, db: AsyncSession, apartment_id: int) -> Optional[ApartmentStats]:
        """Получить статистику квартиры"""
        result = await db.execute(select(ApartmentStats).where(ApartmentStats.apartment_id == apartment_id))
        return result.first()
    
    async def update_stats(
        self, 
        db: AsyncSession, 
        apartment_id: int, 
        views_24h: int,
        leads_24h: int,
        bookings_24h: int,
        days_on_site: int
    ) -> ApartmentStats:
        """Обновить статистику квартиры"""
        stats = await self.get_by_apartment(db, apartment_id)
        if not stats:
            stats = ApartmentStats(apartment_id=apartment_id)
            db.add(stats)
        
        stats.views_24h = views_24h
        stats.leads_24h = leads_24h
        stats.bookings_24h = bookings_24h
        stats.days_on_site = days_on_site
        stats.updated_at = datetime.utcnow()
        
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
        return stats

    async def get_market_stats(
        self,
        db: AsyncSession,
        start_date: datetime,
        city: Optional[str] = None,
        region_code: Optional[str] = None
    ):
        """Получить статистику рынка"""
        query = select(
            func.count(ApartmentStats.id).label("total_views"),
            func.avg(ApartmentStats.views_24h).label("avg_views"),
            func.avg(ApartmentStats.bookings_24h).label("avg_bookings")
        )
        
        if city or region_code:
            query = query.join(Apartment).join(Building).join(Project)
            if city:
                query = query.filter(Project.city == city)
            if region_code:
                query = query.filter(Project.region_code == region_code)
        
        result = await db.execute(query)
        return result.mappings().one()

    async def get_demand_clusters(
        self,
        db: AsyncSession,
        project_id: Optional[int] = None,
        rooms: Optional[int] = None
    ):
        """Получить кластеры спроса"""
        query = select(
            Apartment.rooms,
            func.count(ApartmentStats.id).label("total_apartments"),
            func.avg(ApartmentStats.views_24h).label("avg_views"),
            func.avg(ApartmentStats.bookings_24h).label("avg_bookings")
        ).join(ApartmentStats)
        
        if project_id:
            query = query.join(Building).filter(Building.project_id == project_id)
        if rooms:
            query = query.filter(Apartment.rooms == rooms)
        
        query = query.group_by(Apartment.rooms)
        result = await db.execute(query)
        return result.mappings().all()


class CRUDPriceHistory(CRUDBase[PriceHistory]):
    """CRUD операции для истории цен"""
    
    async def get_by_apartment(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        limit: int = 10
    ) -> List[PriceHistory]:
        """Получить историю цен квартиры"""
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.apartment_id == apartment_id)
            .order_by(PriceHistory.changed_at.desc())
            .limit(limit)
        )
        return result.all()
    
    async def get_recent_changes(
        self, 
        db: AsyncSession, 
        hours: int = 24
    ) -> List[PriceHistory]:
        """Получить недавние изменения цен"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.changed_at >= since)
            .order_by(PriceHistory.changed_at.desc())
        )
        return result.all()


class CRUDViewsLog(CRUDBase[ViewsLog]):
    """CRUD операции для логов просмотров"""
    
    async def get_by_apartment(
        self,
        db: AsyncSession,
        apartment_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Получить историю просмотров квартиры"""
        query = select(ViewsLog).filter(ViewsLog.apartment_id == apartment_id)
        
        if start_date:
            query = query.filter(ViewsLog.occurred_at >= start_date)
        if end_date:
            query = query.filter(ViewsLog.occurred_at <= end_date)
        
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_views_count(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        hours: int = 24
    ) -> int:
        """Получить количество просмотров квартиры за период"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(ViewsLog)
            .where(
                ViewsLog.apartment_id == apartment_id,
                ViewsLog.event == ViewEvent.VIEW,
                ViewsLog.occurred_at >= since
            )
        )
        return len(result.all())


class CRUDBooking(CRUDBase[Booking]):
    """CRUD операции для бронирований"""
    
    async def get_by_apartment(
        self, 
        db: AsyncSession, 
        apartment_id: int
    ) -> List[Booking]:
        """Получить бронирования квартиры"""
        result = await db.execute(select(Booking).where(Booking.apartment_id == apartment_id))
        return result.all()
    
    async def get_by_user(
        self, 
        db: AsyncSession, 
        user_id: int
    ) -> List[Booking]:
        """Получить бронирования пользователя"""
        result = await db.execute(select(Booking).where(Booking.user_id == user_id))
        return result.all()
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        status: BookingStatus
    ) -> List[Booking]:
        """Получить бронирования по статусу"""
        result = await db.execute(select(Booking).where(Booking.status == status))
        return result.all()
    
    async def get_recent_bookings(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        hours: int = 24
    ) -> List[Booking]:
        """Получить недавние бронирования квартиры"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(Booking)
            .where(
                Booking.apartment_id == apartment_id,
                Booking.booked_at >= since
            )
        )
        return result.all()


class CRUDDynamicPricingConfig(CRUDBase[DynamicPricingConfig]):
    """CRUD операции для конфигурации динамического ценообразования"""
    
    async def get_active(self, db: AsyncSession) -> Optional[DynamicPricingConfig]:
        """Получить активную конфигурацию"""
        result = await db.execute(
            select(DynamicPricingConfig).where(DynamicPricingConfig.enabled == True)
        )
        return result.first()


class CRUDPromotion(CRUDBase[Promotion]):
    async def get_active(self, db: AsyncSession, current_time: datetime):
        """Получить активные акции"""
        result = await db.execute(
            select(Promotion).filter(
                and_(
                    Promotion.starts_at <= current_time,
                    Promotion.ends_at > current_time
                )
            )
        )
        return result.scalars().all()


class CRUDWebhook(CRUDBase[WebhookInbox]):
    async def get_unprocessed(self, db: AsyncSession, source: Optional[str] = None):
        """Получить необработанные вебхуки"""
        query = select(WebhookInbox).filter(WebhookInbox.processed == False)
        if source:
            query = query.filter(WebhookInbox.source == source)
        result = await db.execute(query)
        return result.scalars().all()


# Создаем экземпляры CRUD классов
user = CRUDUser(User)
developer = CRUDDeveloper(Developer)
project = CRUDProject(Project)
building = CRUDBuilding(Building)
apartment = CRUDApartment(Apartment)
apartment_stats = CRUDApartmentStats(ApartmentStats)
price_history = CRUDPriceHistory(PriceHistory)
views_log = CRUDViewsLog(ViewsLog)
booking = CRUDBooking(Booking)
dynamic_pricing_config = CRUDDynamicPricingConfig(DynamicPricingConfig)
promotion = CRUDPromotion(Promotion)
webhook = CRUDWebhook(WebhookInbox) 