from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update, delete
from typing import List, Optional, TypeVar, Generic, Type, Dict, Any
from app.models import (
    User, Developer, Project, Building, Property, PropertyAddress, PropertyPrice,
    ResidentialProperty, PropertyFeatures, PropertyAnalytics, CommercialProperty,
    HouseAndLand, PropertyMedia, PromoTag, MortgageProgram, PriceHistory, ViewsLog, Booking,
    Promotion, WebhookInbox, DynamicPricingConfig,
    UserRole, PropertyType, PropertyCategory, PropertyStatus, BookingStatus,
    ViewEvent, PriceChangeReason
)
from datetime import datetime, timedelta
import json
from sqlalchemy import and_, or_, func
from sqlalchemy.orm import joinedload
from uuid import UUID

# Generic type для CRUD операций
ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """Базовый класс для CRUD операций"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Получить объект по ID"""
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    

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
    

    async def delete(self, db: AsyncSession, id: Any) -> bool:
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
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Developer]:
        """Получить застройщика по названию"""
        result = await db.execute(select(Developer).where(Developer.name == name))
        return result.scalar_one_or_none()


class CRUDProject(CRUDBase[Project]):
    """CRUD операции для проектов"""
    
    async def get_by_developer(self, db: AsyncSession, developer_id: UUID) -> List[Project]:
        """Получить проекты по застройщику"""
        result = await db.execute(select(Project).where(Project.developer_id == developer_id))
        return result.scalars().all()
    
    async def get_by_name(self, db: AsyncSession, name: str) -> List[Project]:
        """Получить проекты по названию"""
        result = await db.execute(select(Project).where(Project.name == name))
        return result.scalars().all()


class CRUDBuilding(CRUDBase[Building]):
    """CRUD операции для зданий"""
    
    async def get_by_project(self, db: AsyncSession, project_id: UUID) -> List[Building]:
        """Получить здания по проекту"""
        result = await db.execute(select(Building).where(Building.project_id == project_id))
        return result.scalars().all()


class CRUDProperty(CRUDBase[Property]):
    """CRUD операции для объектов недвижимости"""
    
    async def get_by_building(self, db: AsyncSession, building_id: UUID) -> List[Property]:
        """Получить объекты по зданию"""
        result = await db.execute(select(Property).where(Property.building_id == building_id))
        return result.scalars().all()
    
    async def get_by_project(self, db: AsyncSession, project_id: UUID) -> List[Property]:
        """Получить объекты по проекту"""
        result = await db.execute(select(Property).where(Property.project_id == project_id))
        return result.scalars().all()
    
    async def get_by_developer(self, db: AsyncSession, developer_id: UUID) -> List[Property]:
        """Получить объекты по застройщику"""
        result = await db.execute(select(Property).where(Property.developer_id == developer_id))
        return result.scalars().all()
    
    async def get_by_status(self, db: AsyncSession, status: PropertyStatus) -> List[Property]:
        """Получить объекты по статусу"""
        result = await db.execute(select(Property).where(Property.status == status))
        return result.scalars().all()
    
    async def get_by_type(self, db: AsyncSession, property_type: PropertyType) -> List[Property]:
        """Получить объекты по типу"""
        result = await db.execute(select(Property).where(Property.property_type == property_type))
        return result.scalars().all()
    
    async def get_by_category(self, db: AsyncSession, category: PropertyCategory) -> List[Property]:
        """Получить объекты по категории"""
        result = await db.execute(select(Property).where(Property.category == category))
        return result.scalars().all()
    
    async def get_available(self, db: AsyncSession) -> List[Property]:
        """Получить доступные объекты"""
        result = await db.execute(select(Property).where(Property.status == PropertyStatus.AVAILABLE))
        return result.scalars().all()
    
    async def get_with_relations(self, db: AsyncSession, property_id: UUID) -> Optional[Property]:
        """Получить объект со всеми связанными данными"""
        query = select(Property).where(Property.id == property_id).options(
            joinedload(Property.developer),
            joinedload(Property.project),
            joinedload(Property.building),
            joinedload(Property.address),
            joinedload(Property.price),
            joinedload(Property.residential),
            joinedload(Property.features),
            joinedload(Property.analytics),
            joinedload(Property.commercial),
            joinedload(Property.house_land),
            joinedload(Property.media),
            joinedload(Property.promo_tags),
            joinedload(Property.mortgage_programs)
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()


class CRUDPropertyAddress(CRUDBase[PropertyAddress]):
    """CRUD операции для адресов объектов"""
    
    async def get_by_city(self, db: AsyncSession, city: str) -> List[PropertyAddress]:
        """Получить адреса по городу"""
        result = await db.execute(select(PropertyAddress).where(PropertyAddress.city == city))
        return result.scalars().all()
    
    async def get_by_region(self, db: AsyncSession, region: str) -> List[PropertyAddress]:
        """Получить адреса по региону"""
        result = await db.execute(select(PropertyAddress).where(PropertyAddress.region == region))
        return result.scalars().all()
    
    async def get_by_district(self, db: AsyncSession, district: str) -> List[PropertyAddress]:
        """Получить адреса по району"""
        result = await db.execute(select(PropertyAddress).where(PropertyAddress.district == district))
        return result.scalars().all()


class CRUDPropertyPrice(CRUDBase[PropertyPrice]):
    """CRUD операции для цен объектов"""
    
    async def get_by_price_range(
        self, 
        db: AsyncSession, 
        min_price: float, 
        max_price: float
    ) -> List[PropertyPrice]:
        """Получить цены в диапазоне"""
        result = await db.execute(
            select(PropertyPrice).where(
                and_(
                    PropertyPrice.current_price >= min_price,
                    PropertyPrice.current_price <= max_price
                )
            )
        )
        return result.scalars().all()
    
    async def update_price(
        self, 
        db: AsyncSession, 
        property_id: UUID, 
        new_price: float
    ) -> Optional[PropertyPrice]:
        """Обновить цену объекта"""
        price_obj = await self.get(db, property_id)
        if price_obj:
            old_price = price_obj.current_price
            price_obj.current_price = new_price
            await db.commit()
            await db.refresh(price_obj)
            
            # Создать запись в истории цен
            price_history = PriceHistory(
                property_id=property_id,
                old_price=old_price,
                new_price=new_price,
                reason=PriceChangeReason.MANUAL
            )
            db.add(price_history)
            await db.commit()
            
        return price_obj


class CRUDResidentialProperty(CRUDBase[ResidentialProperty]):
    """CRUD операции для жилой недвижимости"""
    
    async def get_by_rooms(self, db: AsyncSession, rooms: int) -> List[ResidentialProperty]:
        """Получить объекты по количеству комнат"""
        result = await db.execute(select(ResidentialProperty).where(ResidentialProperty.rooms == rooms))
        return result.scalars().all()
    
    async def get_by_area_range(
        self, 
        db: AsyncSession, 
        min_area: float, 
        max_area: float
    ) -> List[ResidentialProperty]:
        """Получить объекты по площади"""
        result = await db.execute(
            select(ResidentialProperty).where(
                and_(
                    ResidentialProperty.total_area >= min_area,
                    ResidentialProperty.total_area <= max_area
                )
            )
        )
        return result.scalars().all()
    
    async def get_studios(self, db: AsyncSession) -> List[ResidentialProperty]:
        """Получить студии"""
        result = await db.execute(select(ResidentialProperty).where(ResidentialProperty.is_studio == True))
        return result.scalars().all()


class CRUDPropertyFeatures(CRUDBase[PropertyFeatures]):
    """CRUD операции для особенностей объектов"""
    
    async def get_with_balcony(self, db: AsyncSession) -> List[PropertyFeatures]:
        """Получить объекты с балконом"""
        result = await db.execute(select(PropertyFeatures).where(PropertyFeatures.balcony == True))
        return result.scalars().all()
    
    async def get_with_parking(self, db: AsyncSession) -> List[PropertyFeatures]:
        """Получить объекты с парковкой"""
        result = await db.execute(select(PropertyFeatures).where(PropertyFeatures.parking_type.isnot(None)))
        return result.scalars().all()


class CRUDPropertyAnalytics(CRUDBase[PropertyAnalytics]):
    """CRUD операции для аналитики объектов"""
    
    async def get_high_demand(self, db: AsyncSession, min_score: int = 7) -> List[PropertyAnalytics]:
        """Получить объекты с высоким спросом"""
        result = await db.execute(
            select(PropertyAnalytics).where(PropertyAnalytics.demand_score >= min_score)
        )
        return result.scalars().all()
    
    async def get_popular(self, db: AsyncSession, min_views: int = 100) -> List[PropertyAnalytics]:
        """Получить популярные объекты"""
        result = await db.execute(
            select(PropertyAnalytics).where(PropertyAnalytics.clicks_total >= min_views)
        )
        return result.scalars().all()


class CRUDCommercialProperty(CRUDBase[CommercialProperty]):
    """CRUD операции для коммерческой недвижимости"""
    
    async def get_by_subtype(self, db: AsyncSession, subtype: PropertyCategory) -> List[CommercialProperty]:
        """Получить объекты по подтипу"""
        result = await db.execute(select(CommercialProperty).where(CommercialProperty.commercial_subtype == subtype))
        return result.scalars().all()
    
    async def get_open_space(self, db: AsyncSession) -> List[CommercialProperty]:
        """Получить объекты с открытой планировкой"""
        result = await db.execute(select(CommercialProperty).where(CommercialProperty.open_space == True))
        return result.scalars().all()


class CRUDHouseAndLand(CRUDBase[HouseAndLand]):
    """CRUD операции для домов и участков"""
    
    async def get_by_land_area(
        self, 
        db: AsyncSession, 
        min_area: float, 
        max_area: float
    ) -> List[HouseAndLand]:
        """Получить объекты по площади участка"""
        result = await db.execute(
            select(HouseAndLand).where(
                and_(
                    HouseAndLand.land_area >= min_area,
                    HouseAndLand.land_area <= max_area
                )
            )
        )
        return result.scalars().all()
    
    async def get_by_year_built(self, db: AsyncSession, year: int) -> List[HouseAndLand]:
        """Получить объекты по году постройки"""
        result = await db.execute(select(HouseAndLand).where(HouseAndLand.year_built == year))
        return result.scalars().all()


class CRUDPropertyMedia(CRUDBase[PropertyMedia]):
    """CRUD операции для медиа объектов"""
    
    async def get_by_property(self, db: AsyncSession, property_id: UUID) -> List[PropertyMedia]:
        """Получить медиа по объекту"""
        result = await db.execute(select(PropertyMedia).where(PropertyMedia.property_id == property_id))
        return result.scalars().all()


class CRUDPromoTag(CRUDBase[PromoTag]):
    """CRUD операции для промо-тегов"""
    
    async def get_by_property(self, db: AsyncSession, property_id: UUID) -> List[PromoTag]:
        """Получить теги по объекту"""
        result = await db.execute(select(PromoTag).where(PromoTag.property_id == property_id))
        return result.scalars().all()
    
    async def get_by_tag(self, db: AsyncSession, tag: str) -> List[PromoTag]:
        """Получить объекты по тегу"""
        result = await db.execute(select(PromoTag).where(PromoTag.tag == tag))
        return result.scalars().all()


class CRUDMortgageProgram(CRUDBase[MortgageProgram]):
    """CRUD операции для ипотечных программ"""
    
    async def get_by_property(self, db: AsyncSession, property_id: UUID) -> List[MortgageProgram]:
        """Получить программы по объекту"""
        result = await db.execute(select(MortgageProgram).where(MortgageProgram.property_id == property_id))
        return result.scalars().all()


class CRUDPriceHistory(CRUDBase[PriceHistory]):
    """CRUD операции для истории цен"""
    
    async def get_by_property(
        self, 
        db: AsyncSession, 
        property_id: UUID,
        limit: int = 10
    ) -> List[PriceHistory]:
        """Получить историю цен по объекту"""
        result = await db.execute(
            select(PriceHistory)
            .where(PriceHistory.property_id == property_id)
            .order_by(PriceHistory.changed_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
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
        return result.scalars().all()


class CRUDViewsLog(CRUDBase[ViewsLog]):
    """CRUD операции для логов просмотров"""
    
    async def get_by_property(
        self,
        db: AsyncSession,
        property_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ):
        """Получить логи просмотров по объекту"""
        query = select(ViewsLog).where(ViewsLog.property_id == property_id)
        
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
        property_id: UUID,
        hours: int = 24
    ) -> int:
        """Получить количество просмотров за период"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(func.count(ViewsLog.id))
            .where(
                and_(
                    ViewsLog.property_id == property_id,
                    ViewsLog.event == ViewEvent.VIEW,
                    ViewsLog.occurred_at >= since
                )
            )
        )
        return result.scalar() or 0
    
    async def get_favourites_count(
        self, 
        db: AsyncSession, 
        property_id: UUID,
        hours: int = 24
    ) -> int:
        """Получить количество добавлений в избранное за период"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(func.count(ViewsLog.id))
            .where(
                and_(
                    ViewsLog.property_id == property_id,
                    ViewsLog.event == ViewEvent.FAVOURITE,
                    ViewsLog.occurred_at >= since
                )
            )
        )
        return result.scalar() or 0


class CRUDBooking(CRUDBase[Booking]):
    """CRUD операции для бронирований"""
    
    async def get_by_property(
        self, 
        db: AsyncSession, 
        property_id: UUID
    ) -> List[Booking]:
        """Получить бронирования по объекту"""
        result = await db.execute(select(Booking).where(Booking.property_id == property_id))
        return result.scalars().all()
    
    async def get_by_user(
        self, 
        db: AsyncSession, 
        user_id: int
    ) -> List[Booking]:
        """Получить бронирования пользователя"""
        result = await db.execute(select(Booking).where(Booking.user_id == user_id))
        return result.scalars().all()
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        status: BookingStatus
    ) -> List[Booking]:
        """Получить бронирования по статусу"""
        result = await db.execute(select(Booking).where(Booking.status == status))
        return result.scalars().all()
    
    async def get_recent_bookings(
        self, 
        db: AsyncSession, 
        property_id: UUID,
        hours: int = 24
    ) -> List[Booking]:
        """Получить недавние бронирования"""
        since = datetime.utcnow() - timedelta(hours=hours)
        result = await db.execute(
            select(Booking)
            .where(
                and_(
                    Booking.property_id == property_id,
                    Booking.booked_at >= since
                )
            )
            .order_by(Booking.booked_at.desc())
        )
        return result.scalars().all()


class CRUDDynamicPricingConfig(CRUDBase[DynamicPricingConfig]):
    """CRUD операции для конфигурации динамического ценообразования"""
    
    async def get_active(self, db: AsyncSession) -> Optional[DynamicPricingConfig]:
        """Получить активную конфигурацию"""
        result = await db.execute(
            select(DynamicPricingConfig).where(DynamicPricingConfig.enabled == True)
        )
        return result.scalar_one_or_none()


class CRUDPromotion(CRUDBase[Promotion]):
    """CRUD операции для акций"""
    
    async def get_active(self, db: AsyncSession, current_time: datetime):
        """Получить активные акции"""
        result = await db.execute(
            select(Promotion).where(
                and_(
                    Promotion.starts_at <= current_time,
                    Promotion.ends_at >= current_time
                )
            )
        )
        return result.scalars().all()


class CRUDWebhook(CRUDBase[WebhookInbox]):
    """CRUD операции для вебхуков"""
    
    async def get_unprocessed(self, db: AsyncSession, source: Optional[str] = None):
        """Получить необработанные вебхуки"""
        query = select(WebhookInbox).where(WebhookInbox.processed == False)
        if source:
            query = query.where(WebhookInbox.source == source)
        result = await db.execute(query)
        return result.scalars().all()


class CRUDWorker:
    """CRUD операции для воркера"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_property_for_task(self, property_id: UUID) -> Optional[Property]:
        """Получить объект для задачи"""
        result = await self.session.execute(select(Property).where(Property.id == property_id))
        return result.scalar_one_or_none()
    
    async def get_properties_for_pricing(self) -> List[Property]:
        """Получить объекты для динамического ценообразования"""
        result = await self.session.execute(
            select(Property)
            .where(Property.status == PropertyStatus.AVAILABLE)
            .options(
                joinedload(Property.price),
                joinedload(Property.analytics)
            )
        )
        return result.scalars().all()
    
    async def get_properties_for_stats(self) -> List[Property]:
        """Получить объекты для обновления статистики"""
        result = await self.session.execute(
            select(Property)
            .where(Property.status == PropertyStatus.AVAILABLE)
            .options(
                joinedload(Property.analytics),
                joinedload(Property.views_logs),
                joinedload(Property.bookings)
            )
        )
        return result.scalars().all()
    
    async def update_property_price_timestamp(self, property_id: UUID) -> None:
        """Обновить временную метку цены объекта"""
        await self.session.execute(
            update(Property)
            .where(Property.id == property_id)
            .values(updated_at=datetime.utcnow())
        )
        await self.session.commit()


# Создание экземпляров CRUD классов
crud_user = CRUDUser(User)
crud_developer = CRUDDeveloper(Developer)
crud_project = CRUDProject(Project)
crud_building = CRUDBuilding(Building)
crud_property = CRUDProperty(Property)
crud_property_address = CRUDPropertyAddress(PropertyAddress)
crud_property_price = CRUDPropertyPrice(PropertyPrice)
crud_residential_property = CRUDResidentialProperty(ResidentialProperty)
crud_property_features = CRUDPropertyFeatures(PropertyFeatures)
crud_property_analytics = CRUDPropertyAnalytics(PropertyAnalytics)
crud_commercial_property = CRUDCommercialProperty(CommercialProperty)
crud_house_land = CRUDHouseAndLand(HouseAndLand)
crud_property_media = CRUDPropertyMedia(PropertyMedia)
crud_promo_tag = CRUDPromoTag(PromoTag)
crud_mortgage_program = CRUDMortgageProgram(MortgageProgram)
crud_price_history = CRUDPriceHistory(PriceHistory)
crud_views_log = CRUDViewsLog(ViewsLog)
crud_booking = CRUDBooking(Booking)
crud_dynamic_pricing_config = CRUDDynamicPricingConfig(DynamicPricingConfig)
crud_promotion = CRUDPromotion(Promotion)
crud_webhook = CRUDWebhook(WebhookInbox)
