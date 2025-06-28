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
from sqlalchemy.orm import joinedload

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
    
    async def get_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        """Получить пользователя по email"""
        query = select(self.model).where(self.model.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_inn(
        self,
        db: AsyncSession,
        inn: str
    ) -> Optional[User]:
        """Получить застройщика по ИНН"""
        query = select(self.model).where(
            and_(
                self.model.inn == inn,
                self.model.role == UserRole.DEVELOPER
            )
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_role(self, db: AsyncSession, role: UserRole):
        """Получить пользователей по роли"""
        result = await db.execute(select(User).filter(User.role == role))
        return result.scalars().all()


    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100):
        """Получить список пользователей"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    async def get_active_developers(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Получить список активных застройщиков"""
        query = select(self.model).where(
            and_(
                self.model.is_active == True,
                self.model.role == UserRole.DEVELOPER
            )
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_active_admins(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Получить список активных администраторов"""
        query = select(self.model).where(
            and_(
                self.model.is_active == True,
                self.model.role == UserRole.ADMIN
            )
        ).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def deactivate(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        """Деактивировать пользователя"""
        user = await self.get(db, user_id)
        if user:
            user.is_active = False
            await db.commit()
            await db.refresh(user)
        return user
    
    async def activate(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        """Активировать пользователя"""
        user = await self.get(db, user_id)
        if user:
            user.is_active = True
            await db.commit()
            await db.refresh(user)
        return user


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
        return result.scalars().all()
    

    async def get_by_developer(self, db: AsyncSession, developer_id: int) -> List[Project]:
        """Получить проекты застройщика"""
        result = await db.execute(select(Project).where(Project.developer_id == developer_id))
        return result.scalars().all()
    

    async def get_by_class(self, db: AsyncSession, class_type: PropertyClass) -> List[Project]:
        """Получить проекты по классу недвижимости"""
        result = await db.execute(select(Project).where(Project.class_type == class_type))
        return result.scalars().all()


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


class CRUDStats(CRUDBase[ApartmentStats]):
    """CRUD операции для статистики"""
    
    def __init__(self, session: AsyncSession):
        super().__init__(ApartmentStats)
        self.session = session
        self.views_log_crud = CRUDViewsLog(ViewsLog)
        self.booking_crud = CRUDBooking(Booking)
    
    async def get_views_24h(self, apartment_id: int) -> int:
        """Получает количество просмотров за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.session.execute(
            select(func.count(ViewsLog.id))
            .where(
                ViewsLog.apartment_id == apartment_id,
                ViewsLog.event == "view",
                ViewsLog.occurred_at >= yesterday
            )
        )
        count = result.scalar_one()
        return count or 0
    
    async def get_leads_24h(self, apartment_id: int) -> int:
        """Получает количество лидов за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.session.execute(
            select(func.count(func.distinct(ViewsLog.user_id)))
            .where(
                ViewsLog.apartment_id == apartment_id,
                ViewsLog.user_id.is_not(None),
                ViewsLog.occurred_at >= yesterday
            )
        )
        count = result.scalar_one()
        return count or 0
    
    async def get_bookings_24h(self, apartment_id: int) -> int:
        """Получает количество бронирований за последние 24 часа"""
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        result = await self.session.execute(
            select(func.count(Booking.id))
            .where(
                Booking.apartment_id == apartment_id,
                Booking.booked_at >= yesterday
            )
        )
        count = result.scalar_one()
        return count or 0
    
    async def get_days_on_site(self, apartment: Apartment) -> int:
        """Получает количество дней на сайте"""
        return max(0, (datetime.utcnow() - apartment.created_at).days)
    
    async def get_apartment_stats(self, apartment_id: int) -> Optional[ApartmentStats]:
        """Получает статистику квартиры"""
        result = await self.session.execute(
            select(ApartmentStats).where(ApartmentStats.apartment_id == apartment_id)
        )
        return result.scalar_one_or_none()
    
    async def update_stats(
        self,
        apartment_id: int,
        views_24h: int,
        leads_24h: int,
        bookings_24h: int,
        days_on_site: int
    ) -> ApartmentStats:
        """Обновляет или создает статистику квартиры"""
        stats = await self.get_apartment_stats(apartment_id)
        
        if stats:
            stats.views_24h = views_24h
            stats.leads_24h = leads_24h
            stats.bookings_24h = bookings_24h
            stats.days_on_site = days_on_site
            stats.updated_at = datetime.utcnow()
        else:
            stats = ApartmentStats(
                apartment_id=apartment_id,
                views_24h=views_24h,
                leads_24h=leads_24h,
                bookings_24h=bookings_24h,
                days_on_site=days_on_site
            )
            self.session.add(stats)
        
        await self.session.commit()
        await self.session.refresh(stats)
        return stats
    
    async def get_district_stats(self, district: str) -> Dict[str, float]:
        """Получает статистику по району"""
        # Базовые метрики для расчета популярности района
        query = select(
            func.count(Apartment.id).label('total_apartments'),
            func.avg(ApartmentStats.views_24h).label('avg_views'),
            func.avg(ApartmentStats.leads_24h).label('avg_leads'),
            func.avg(ApartmentStats.bookings_24h).label('avg_bookings'),
            func.avg(ApartmentStats.days_on_site).label('avg_days_on_market')
        ).join(
            Building, Building.id == Apartment.building_id
        ).join(
            Project, Project.id == Building.project_id
        ).join(
            ApartmentStats, ApartmentStats.apartment_id == Apartment.id
        ).where(
            Project.district == district
        )
        
        result = await self.session.execute(query)
        stats = result.first()
        
        if not stats:
            return {'popularity_score': 0.5}  # Дефолтное значение если нет данных
        
        # Нормализуем и взвешиваем метрики для расчета популярности
        weights = {
            'views': 0.3,
            'leads': 0.3,
            'bookings': 0.3,
            'market_time': 0.1
        }
        
        # Получаем средние значения по всем районам для нормализации
        avg_query = select(
            func.avg(ApartmentStats.views_24h).label('avg_views'),
            func.avg(ApartmentStats.leads_24h).label('avg_leads'),
            func.avg(ApartmentStats.bookings_24h).label('avg_bookings'),
            func.avg(ApartmentStats.days_on_site).label('avg_days_on_market')
        ).join(
            ApartmentStats, ApartmentStats.apartment_id == Apartment.id
        )
        
        avg_result = await self.session.execute(avg_query)
        avg_stats = avg_result.first()
        
        if not avg_stats:
            return {'popularity_score': 0.5}
        
        # Нормализуем каждую метрику относительно средних значений
        normalized_stats = {
            'views': min(1.0, stats.avg_views / (avg_stats.avg_views * 2)) if avg_stats.avg_views > 0 else 0.5,
            'leads': min(1.0, stats.avg_leads / (avg_stats.avg_leads * 2)) if avg_stats.avg_leads > 0 else 0.5,
            'bookings': min(1.0, stats.avg_bookings / (avg_stats.avg_bookings * 2)) if avg_stats.avg_bookings > 0 else 0.5,
            'market_time': min(1.0, avg_stats.avg_days_on_market / (stats.avg_days_on_market + 1))  # Инвертируем т.к. меньше = лучше
        }
        
        # Рассчитываем финальный скор популярности
        popularity_score = sum(score * weights[metric] for metric, score in normalized_stats.items())
        
        return {'popularity_score': popularity_score}
    
    async def get_avg_views_24h(self) -> float:
        """Получает среднее количество просмотров по всем квартирам за 24 часа"""
        query = select(func.avg(ApartmentStats.views_24h))
        result = await self.session.execute(query)
        avg_views = result.scalar()
        return avg_views if avg_views is not None else 0.0


class CRUDWorker:
    """CRUD операции для задач воркера"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.apartment_crud = CRUDApartment(Apartment)
    
    async def get_apartment_for_task(self, apartment_id: int) -> Optional[Apartment]:
        """Получает квартиру для обработки в задаче"""
        return await self.apartment_crud.get(self.session, apartment_id)
    
    async def get_apartments_for_pricing(self) -> List[Apartment]:
        """Получает квартиры для обновления цен"""
        # Получаем квартиры, которые не обновлялись более часа
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        result = await self.session.execute(
            select(Apartment)
            .where(
                and_(
                    Apartment.status == ApartmentStatus.AVAILABLE,
                    or_(
                        Apartment.price_updated_at <= one_hour_ago,
                        Apartment.price_updated_at.is_(None)
                    )
                )
            )
            .order_by(Apartment.id)
        )
        return result.scalars().all()
    
    async def get_apartments_for_stats(self) -> List[Apartment]:
        """Получает квартиры для обновления статистики"""
        # Получаем квартиры, статистика которых не обновлялась более минуты
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        result = await self.session.execute(
            select(Apartment)
            .join(ApartmentStats, isouter=True)
            .where(
                and_(
                    Apartment.status == ApartmentStatus.AVAILABLE,
                    or_(
                        ApartmentStats.updated_at <= one_minute_ago,
                        ApartmentStats.updated_at.is_(None)
                    )
                )
            )
            .order_by(Apartment.id)
        )
        return result.scalars().all()
    
    async def update_apartment_price_timestamp(self, apartment_id: int) -> None:
        """Обновляет timestamp последнего обновления цены"""
        await self.session.execute(
            update(Apartment)
            .where(Apartment.id == apartment_id)
            .values(price_updated_at=datetime.utcnow())
        )
        await self.session.commit()


# Создаем экземпляры CRUD классов
user = CRUDUser(User)
developer = CRUDDeveloper(Developer)
project = CRUDProject(Project)
building = CRUDBuilding(Building)
apartment = CRUDApartment(Apartment)
views_log = CRUDViewsLog(ViewsLog)
booking = CRUDBooking(Booking)
price_history = CRUDPriceHistory(PriceHistory)
promotion = CRUDPromotion(Promotion)
webhook = CRUDWebhook(WebhookInbox)
dynamic_pricing_config = CRUDDynamicPricingConfig(DynamicPricingConfig)
