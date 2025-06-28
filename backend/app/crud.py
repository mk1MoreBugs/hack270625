from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional, TypeVar, Generic, Type, Dict, Any, Sequence, Union
from app.models import (
    User, Developer, Project, Building, Apartment, 
    ApartmentStats, PriceHistory, ViewsLog, Booking,
    Promotion, WebhookInbox, DynamicPricingConfig,
    UserRole, PropertyClass, ApartmentStatus, BookingStatus,
    ViewEvent, PriceChangeReason
)
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, func, text
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from app.security import get_password_hash, verify_password
import json


ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс для CRUD операций"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """Получить объект по ID"""
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_multi(
        self, 
        db: AsyncSession, 
        *, 
        skip: int = 0, 
        limit: int = 100,
        order_by: Optional[Union[str, Sequence[str]]] = None
    ) -> List[ModelType]:
        """Получить список объектов с пагинацией и сортировкой"""
        query = select(self.model).offset(skip).limit(limit)
        
        if order_by:
            if isinstance(order_by, str):
                order_by = [order_by]
            for field in order_by:
                desc = field.startswith("-")
                field_name = field[1:] if desc else field
                if hasattr(self.model, field_name):
                    field_attr = getattr(self.model, field_name)
                    query = query.order_by(field_attr.desc() if desc else field_attr)
        
        result = await db.execute(query)
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """Создать новый объект"""
        try:
            obj_in_data = obj_in.dict() if hasattr(obj_in, "dict") else obj_in
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка создания объекта: {str(e)}"
            )
    
    async def update(
        self, 
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Обновить объект"""
        try:
            obj_data = db_obj.dict()
            update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in
            
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            
            if hasattr(db_obj, "updated_at"):
                setattr(db_obj, "updated_at", datetime.utcnow())
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка обновления объекта: {str(e)}"
            )
    
    async def delete(self, db: AsyncSession, *, id: int) -> bool:
        """Удалить объект по ID"""
        try:
            obj = await self.get(db, id)
            if not obj:
                return False
            await db.delete(obj)
            await db.commit()
            return True
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка удаления объекта: {str(e)}"
            )


class CRUDUser(CRUDBase[User, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для пользователей"""
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_by_role(
        self, 
        db: AsyncSession, 
        role: UserRole,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Получить пользователей по роли"""
        result = await db.execute(
            select(User)
            .where(User.role == role)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> User:
        """Создать нового пользователя"""
        try:
            obj_in_data = obj_in.dict() if hasattr(obj_in, "dict") else obj_in
            
            if "password" in obj_in_data:
                password = obj_in_data.pop("password")
                obj_in_data["hashed_password"] = get_password_hash(password)
            
            db_obj = User(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка создания пользователя: {str(e)}"
            )
    
    async def update(
        self, 
        db: AsyncSession,
        *,
        db_obj: User,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> User:
        """Обновить пользователя"""
        try:
            update_data = obj_in.dict(exclude_unset=True) if hasattr(obj_in, "dict") else obj_in
            
            if "password" in update_data:
                password = update_data.pop("password")
                update_data["hashed_password"] = get_password_hash(password)
            
            return await super().update(db, db_obj=db_obj, obj_in=update_data)
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка обновления пользователя: {str(e)}"
            )
    
    async def authenticate(self, db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Аутентифицировать пользователя"""
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


class CRUDDeveloper(CRUDBase[Developer, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для застройщиков"""
    
    async def get_by_inn(self, db: AsyncSession, inn: str) -> Optional[Developer]:
        """Получить застройщика по ИНН"""
        result = await db.execute(
            select(Developer).where(Developer.inn == inn)
        )
        return result.scalar_one_or_none()
    
    async def get_verified(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Developer]:
        """Получить верифицированных застройщиков"""
        result = await db.execute(
            select(Developer)
            .where(Developer.verified == True)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDProject(CRUDBase[Project, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для проектов"""
    
    async def get_by_city(
        self, 
        db: AsyncSession, 
        city: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Получить проекты по городу"""
        result = await db.execute(
            select(Project)
            .where(Project.city == city)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_developer(
        self, 
        db: AsyncSession, 
        developer_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Получить проекты застройщика"""
        result = await db.execute(
            select(Project)
            .where(Project.developer_id == developer_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_class(
        self, 
        db: AsyncSession, 
        class_type: PropertyClass,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """Получить проекты по классу недвижимости"""
        result = await db.execute(
            select(Project)
            .where(Project.class_type == class_type)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDBuilding(CRUDBase[Building, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для корпусов"""
    
    async def get_by_project(
        self, 
        db: AsyncSession, 
        project_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Building]:
        """Получить корпуса проекта"""
        result = await db.execute(
            select(Building)
            .where(Building.project_id == project_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDApartment(CRUDBase[Apartment, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для квартир"""
    
    async def get_by_building(
        self, 
        db: AsyncSession, 
        building_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Получить квартиры корпуса"""
        result = await db.execute(
            select(Apartment)
            .where(Apartment.building_id == building_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        status: ApartmentStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Получить квартиры по статусу"""
        result = await db.execute(
            select(Apartment)
            .where(Apartment.status == status)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_rooms(
        self, 
        db: AsyncSession, 
        rooms: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Получить квартиры по количеству комнат"""
        result = await db.execute(
            select(Apartment)
            .where(Apartment.rooms == rooms)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_price_range(
        self, 
        db: AsyncSession, 
        min_price: float, 
        max_price: float,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Получить квартиры в диапазоне цен"""
        result = await db.execute(
            select(Apartment)
            .where(
                and_(
                    Apartment.current_price >= min_price,
                    Apartment.current_price <= max_price
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_available(
        self, 
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Apartment]:
        """Получить доступные квартиры"""
        return await self.get_by_status(db, ApartmentStatus.AVAILABLE, skip, limit)
    
    async def update_price(
        self, 
        db: AsyncSession, 
        apartment_id: int, 
        new_price: float,
        reason: PriceChangeReason,
        description: Optional[str] = None
    ) -> Optional[Apartment]:
        """Обновить цену квартиры"""
        try:
            apartment = await self.get(db, apartment_id)
            if not apartment:
                return None
            
            # Создаем запись в истории цен
            price_history = PriceHistory(
                apartment_id=apartment_id,
                old_price=apartment.current_price,
                new_price=new_price,
                reason=reason,
                description=description
            )
            
            # Обновляем цену квартиры
            apartment.current_price = new_price
            apartment.updated_at = datetime.utcnow()
            
            db.add_all([apartment, price_history])
            await db.commit()
            await db.refresh(apartment)
            return apartment
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка обновления цены: {str(e)}"
            )


class CRUDApartmentStats(CRUDBase[ApartmentStats, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для статистики квартир"""
    
    async def get_by_apartment(
        self, 
        db: AsyncSession, 
        apartment_id: int
    ) -> Optional[ApartmentStats]:
        """Получить статистику квартиры"""
        result = await db.execute(
            select(ApartmentStats)
            .where(ApartmentStats.apartment_id == apartment_id)
        )
        return result.scalar_one_or_none()
    
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
        try:
            stats = await self.get_by_apartment(db, apartment_id)
            if not stats:
                stats = ApartmentStats(apartment_id=apartment_id)
                db.add(stats)
            
            stats.views_24h = views_24h
            stats.leads_24h = leads_24h
            stats.bookings_24h = bookings_24h
            stats.days_on_site = days_on_site
            stats.updated_at = datetime.utcnow()
            
            await db.commit()
            await db.refresh(stats)
            return stats
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка обновления статистики: {str(e)}"
            )

    async def get_market_stats(
        self,
        db: AsyncSession,
        start_date: datetime,
        city: Optional[str] = None,
        region_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """Получить статистику рынка"""
        query = select([
            func.count(ApartmentStats.apartment_id).label("total_apartments"),
            func.avg(ApartmentStats.views_24h).label("avg_views"),
            func.avg(ApartmentStats.bookings_24h).label("avg_bookings")
        ]).select_from(ApartmentStats)
        
        if city or region_code:
            query = query.join(
                Apartment, 
                ApartmentStats.apartment_id == Apartment.id
            ).join(
                Building, 
                Apartment.building_id == Building.id
            ).join(
                Project, 
                Building.project_id == Project.id
            )
            
            if city:
                query = query.where(Project.city == city)
            if region_code:
                query = query.where(Project.region_code == region_code)
        
        result = await db.execute(query)
        stats = result.mappings().first()
        return {
            "total_apartments": stats["total_apartments"] or 0,
            "avg_views": float(stats["avg_views"] or 0),
            "avg_bookings": float(stats["avg_bookings"] or 0)
        }


class CRUDPriceHistory(CRUDBase[PriceHistory, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для истории цен"""
    
    async def get_by_apartment(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        skip: int = 0,
        limit: int = 10
    ) -> List[PriceHistory]:
        """Получить историю цен квартиры"""
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.apartment_id == apartment_id)
            .order_by(PriceHistory.changed_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recent_changes(
        self, 
        db: AsyncSession, 
        hours: int = 24
    ) -> List[PriceHistory]:
        """Получить недавние изменения цен"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.changed_at >= cutoff)
            .order_by(PriceHistory.changed_at.desc())
        )
        return result.scalars().all()


class CRUDViewsLog(CRUDBase[ViewsLog, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для логов просмотров"""
    
    async def get_by_apartment(
        self,
        db: AsyncSession,
        apartment_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ViewsLog]:
        """Получить логи просмотров квартиры"""
        query = select(ViewsLog).where(ViewsLog.apartment_id == apartment_id)
        
        if start_date:
            query = query.where(ViewsLog.occurred_at >= start_date)
        if end_date:
            query = query.where(ViewsLog.occurred_at <= end_date)
        
        query = query.order_by(ViewsLog.occurred_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_views_count(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        hours: int = 24
    ) -> Dict[str, int]:
        """Получить количество просмотров квартиры"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select([
                ViewsLog.event,
                func.count(ViewsLog.id).label("count")
            ])
            .where(
                and_(
                    ViewsLog.apartment_id == apartment_id,
                    ViewsLog.occurred_at >= cutoff
                )
            )
            .group_by(ViewsLog.event)
        )
        
        counts = {event: 0 for event in ViewEvent}
        for row in result.mappings():
            counts[row["event"]] = row["count"]
        
        return counts


class CRUDBooking(CRUDBase[Booking, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для бронирований"""
    
    async def get_by_apartment(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        """Получить бронирования квартиры"""
        result = await db.execute(
            select(Booking)
            .where(Booking.apartment_id == apartment_id)
            .order_by(Booking.booked_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_user(
        self, 
        db: AsyncSession, 
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        """Получить бронирования пользователя"""
        result = await db.execute(
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.booked_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        status: BookingStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[Booking]:
        """Получить бронирования по статусу"""
        result = await db.execute(
            select(Booking)
            .where(Booking.status == status)
            .order_by(Booking.booked_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recent_bookings(
        self, 
        db: AsyncSession, 
        apartment_id: int,
        hours: int = 24
    ) -> List[Booking]:
        """Получить недавние бронирования квартиры"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(Booking)
            .where(
                and_(
                    Booking.apartment_id == apartment_id,
                    Booking.booked_at >= cutoff
                )
            )
            .order_by(Booking.booked_at.desc())
        )
        return result.scalars().all()


class CRUDPromotion(CRUDBase[Promotion, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для акций"""
    
    async def get_active(
        self, 
        db: AsyncSession, 
        current_time: datetime,
        skip: int = 0,
        limit: int = 100
    ) -> List[Promotion]:
        """Получить активные акции"""
        result = await db.execute(
            select(Promotion)
            .where(
                and_(
                    Promotion.starts_at <= current_time,
                    Promotion.ends_at > current_time
                )
            )
            .order_by(Promotion.ends_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


class CRUDWebhook(CRUDBase[WebhookInbox, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для вебхуков"""
    
    async def get_unprocessed(
        self, 
        db: AsyncSession, 
        source: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[WebhookInbox]:
        """Получить необработанные вебхуки"""
        query = select(WebhookInbox).where(WebhookInbox.processed == False)
        
        if source:
            query = query.where(WebhookInbox.source == source)
        
        query = query.order_by(WebhookInbox.received_at.asc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDDynamicPricingConfig(CRUDBase[DynamicPricingConfig, CreateSchemaType, UpdateSchemaType]):
    """CRUD операции для конфигурации динамического ценообразования"""
    
    async def get_active(self, db: AsyncSession) -> Optional[DynamicPricingConfig]:
        """Получить активную конфигурацию"""
        result = await db.execute(
            select(DynamicPricingConfig)
            .where(DynamicPricingConfig.enabled == True)
            .order_by(DynamicPricingConfig.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()


# Инициализация CRUD объектов
user = CRUDUser(User)
developer = CRUDDeveloper(Developer)
project = CRUDProject(Project)
building = CRUDBuilding(Building)
apartment = CRUDApartment(Apartment)
apartment_stats = CRUDApartmentStats(ApartmentStats)
price_history = CRUDPriceHistory(PriceHistory)
views_log = CRUDViewsLog(ViewsLog)
booking = CRUDBooking(Booking)
promotion = CRUDPromotion(Promotion)
webhook = CRUDWebhook(WebhookInbox)
dynamic_pricing_config = CRUDDynamicPricingConfig(DynamicPricingConfig) 