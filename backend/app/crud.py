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

# Generic type для CRUD операций
ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    """Базовый класс для CRUD операций"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
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
    

    async def get_by_field(
        self,
        db: AsyncSession,
        field_name: str,
        field_value: Any
    ) -> List[ModelType]:
        """Базовый метод для фильтрации по полю"""
        result = await db.execute(
            select(self.model).where(getattr(self.model, field_name) == field_value)
        )
        return result.scalars().all()
    
    async def get_by_time_window(
        self,
        db: AsyncSession,
        field_name: str,
        hours: int = 24,
        property_id: Optional[int] = None
    ) -> List[ModelType]:
        """Базовый метод для получения данных в временном окне"""
        since = datetime.utcnow() - timedelta(hours=hours)
        query = select(self.model).where(getattr(self.model, field_name) >= since)
        
        if property_id:
            query = query.where(self.model.property_id == property_id)
            
        result = await db.execute(query)
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
    
    async def get_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        return (await self.get_by_field(db, "email", email))[0]
    
    async def get_by_role(self, db: AsyncSession, role: UserRole) -> List[User]:
        """Получить пользователей по роли"""
        return await self.get_by_field(db, "role", role)


    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100):
        """Получить список пользователей"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


class CRUDDeveloper(CRUDBase[Developer]):
    """CRUD операции для застройщиков"""
    
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[Developer]:
        """Получить застройщика по названию"""
        result = await self.get_by_field(db, "name", name)
        return result[0] if result else None


class CRUDProject(CRUDBase[Project]):
    """CRUD операции для проектов"""
    
    async def get_by_developer(self, db: AsyncSession, developer_id: int) -> List[Project]:
        """Получить проекты по застройщику"""
        return await self.get_by_field(db, "developer_id", developer_id)
    
    async def get_by_name(self, db: AsyncSession, name: str) -> List[Project]:
        """Получить проекты по названию"""
        return await self.get_by_field(db, "name", name)


class CRUDBuilding(CRUDBase[Building]):
    """CRUD операции для зданий"""
    
    async def get_by_project(self, db: AsyncSession, project_id: int) -> List[Building]:
        """Получить здания по проекту"""
        return await self.get_by_field(db, "project_id", project_id)


class CRUDProperty(CRUDBase[Property]):
    """CRUD операции для объектов недвижимости"""
    
    async def get_by_building(self, db: AsyncSession, building_id: int) -> List[Property]:
        """Получить объекты по зданию"""
        return await self.get_by_field(db, "building_id", building_id)

    async def get_by_project(self, db: AsyncSession, project_id: int) -> List[Property]:
        """Получить объекты по проекту"""
        return await self.get_by_field(db, "project_id", project_id)
    
    async def get_by_developer(self, db: AsyncSession, developer_id: int) -> List[Property]:
        """Получить объекты по застройщику"""
        return await self.get_by_field(db, "developer_id", developer_id)
    
    async def get_by_status(self, db: AsyncSession, status: PropertyStatus) -> List[Property]:
        """Получить объекты по статусу"""
        return await self.get_by_field(db, "status", status)

    async def get_by_type(self, db: AsyncSession, property_type: PropertyType) -> List[Property]:
        """Получить объекты по типу"""
        return await self.get_by_field(db, "property_type", property_type)
    
    async def get_by_category(self, db: AsyncSession, category: PropertyCategory) -> List[Property]:
        """Получить объекты по категории"""
        return await self.get_by_field(db, "category", category)
    
    async def get_available(self, db: AsyncSession) -> List[Property]:
        """Получить доступные объекты"""
        return await self.get_by_field(db, "status", PropertyStatus.AVAILABLE)
    
    async def get_with_relations(self, db: AsyncSession, property_id: int) -> Optional[Property]:
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
        return await self.get_by_field(db, "city", city)
    
    async def get_by_region(self, db: AsyncSession, region: str) -> List[PropertyAddress]:
        """Получить адреса по региону"""
        return await self.get_by_field(db, "region", region)
    
    async def get_by_district(self, db: AsyncSession, district: str) -> List[PropertyAddress]:
        """Получить адреса по району"""
        return await self.get_by_field(db, "district", district)
    

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
        property_id: int, 
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
        return await self.get_by_field(db, "rooms", rooms)
    
    async def get_by_area_range(
        self, 
        db: AsyncSession, 
        min_area: float, 
        max_area: float
    ) -> List[ResidentialProperty]:
        """Получить объекты по диапазону площади"""
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
        return await self.get_by_field(db, "rooms", 0)


class CRUDPropertyFeatures(CRUDBase[PropertyFeatures]):
    """CRUD операции для характеристик объектов"""
    
    async def get_with_balcony(self, db: AsyncSession) -> List[PropertyFeatures]:
        """Получить объекты с балконом"""
        return await self.get_by_field(db, "balcony", True)
    
    async def get_with_parking(self, db: AsyncSession) -> List[PropertyFeatures]:
        """Получить объекты с парковкой"""
        return await self.get_by_field(db, "parking_type", True)


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
    
    async def get_by_property(self, db: AsyncSession, property_id: int) -> List[PropertyMedia]:
        """Получить медиа по объекту"""
        result = await db.execute(select(PropertyMedia).where(PropertyMedia.property_id == property_id))
        return result.scalars().all()


class CRUDPromoTag(CRUDBase[PromoTag]):
    """CRUD операции для промо-тегов"""
    
    async def get_by_property(self, db: AsyncSession, property_id: int) -> List[PromoTag]:
        """Получить теги по объекту"""
        result = await db.execute(select(PromoTag).where(PromoTag.property_id == property_id))
        return result.scalars().all()
    
    async def get_by_tag(self, db: AsyncSession, tag: str) -> List[PromoTag]:
        """Получить объекты по тегу"""
        result = await db.execute(select(PromoTag).where(PromoTag.tag == tag))
        return result.scalars().all()


class CRUDMortgageProgram(CRUDBase[MortgageProgram]):
    """CRUD операции для ипотечных программ"""
    
    async def get_by_property(self, db: AsyncSession, property_id: int) -> List[MortgageProgram]:
        """Получить программы по объекту"""
        result = await db.execute(select(MortgageProgram).where(MortgageProgram.property_id == property_id))
        return result.scalars().all()


class CRUDPriceHistory(CRUDBase[PriceHistory]):
    """CRUD операции для истории цен"""
    
    async def get_by_property(
        self, 
        db: AsyncSession, 
        property_id: int,
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
        property_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[ViewsLog]:
        """Получить логи просмотров объекта"""
        query = select(ViewsLog).where(ViewsLog.property_id == property_id)
        
        if start_date:
            query = query.where(ViewsLog.viewed_at >= start_date)
        if end_date:
            query = query.where(ViewsLog.viewed_at <= end_date)
            
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()
    
    async def get_views_count(
        self, 
        db: AsyncSession, 
        property_id: int,
        hours: int = 24
    ) -> int:
        """Получить количество просмотров за период"""
        logs = await self.get_by_time_window(db, "viewed_at", hours, property_id)
        return len([log for log in logs if log.event_type == ViewEvent.VIEW])
    
    async def get_favourites_count(
        self, 
        db: AsyncSession, 
        property_id: int,
        hours: int = 24
    ) -> int:
        """Получить количество добавлений в избранное за период"""
        logs = await self.get_by_time_window(db, "viewed_at", hours, property_id)
        return len([log for log in logs if log.event_type == ViewEvent.FAVOURITE])


class CRUDBooking(CRUDBase[Booking]):
    """CRUD операции для бронирований"""
    
    async def get_by_property(
        self, 
        db: AsyncSession, 
        property_id: int
    ) -> List[Booking]:
        """Получить бронирования объекта"""
        return await self.get_by_field(db, "property_id", property_id)
    
    async def get_by_user(
        self, 
        db: AsyncSession, 
        user_id: int  # Возвращаем int, так как это соответствует модели
    ) -> List[Booking]:
        """Получить бронирования пользователя"""
        return await self.get_by_field(db, "user_id", user_id)
    
    async def get_by_status(
        self, 
        db: AsyncSession, 
        status: BookingStatus
    ) -> List[Booking]:
        """Получить бронирования по статусу"""
        return await self.get_by_field(db, "status", status)
    
    async def get_recent_bookings(
        self, 
        db: AsyncSession, 
        property_id: int,
        hours: int = 24
    ) -> List[Booking]:
        """Получить недавние бронирования"""
        return await self.get_by_time_window(db, "created_at", hours, property_id)


class CRUDDynamicPricingConfig(CRUDBase[DynamicPricingConfig]):
    """CRUD операции для конфигурации динамического ценообразования"""
    
    async def get_active(self, db: AsyncSession) -> Optional[DynamicPricingConfig]:
        """Получить активную конфигурацию"""
        result = await db.execute(
            select(DynamicPricingConfig)
            .where(DynamicPricingConfig.enabled == True)
            .order_by(DynamicPricingConfig.created_at.desc())
        )
        return result.scalar_one_or_none()


class CRUDDynamicPricing:
    """CRUD операции для динамического ценообразования"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_cluster_properties(
        self,
        project_id: Optional[int],
        rooms: Optional[int],
        exclude_property_id: int
    ) -> List[Property]:
        """Получить объекты из того же кластера (проект + тип комнат)"""
        query = select(Property).where(
            and_(
                Property.id != exclude_property_id,
                Property.status == PropertyStatus.AVAILABLE
            )
        )
        
        if project_id:
            query = query.where(Property.project_id == project_id)
        
        if rooms is not None:
            query = query.join(ResidentialProperty).where(ResidentialProperty.rooms == rooms)
            
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_recent_price_changes(
        self,
        property_id: int,
        hours: int = 24
    ) -> List[PriceHistory]:
        """Получить недавние изменения цены"""
        since = datetime.utcnow() - timedelta(hours=hours)
        query = select(PriceHistory).where(
            and_(
                PriceHistory.property_id == property_id,
                PriceHistory.changed_at >= since
            )
        ).order_by(PriceHistory.changed_at.desc())
        
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def update_property_price(
        self,
        property_id: int,
        new_price: float
    ) -> Optional[PropertyPrice]:
        """Обновить цену объекта недвижимости"""
        query = update(PropertyPrice).where(
            PropertyPrice.property_id == property_id
        ).values(
            current_price=new_price,
            updated_at=datetime.utcnow()
        )
        await self.session.execute(query)
        await self.session.commit()
        
        # Получаем обновленный объект
        result = await self.session.execute(
            select(PropertyPrice).where(PropertyPrice.property_id == property_id)
        )
        return result.scalar_one_or_none()
    
    async def create_price_history(self, data: dict) -> PriceHistory:
        """Создать запись в истории цен"""
        price_history = PriceHistory(
            property_id=data["property_id"],
            old_price=data["old_price"],
            new_price=data["new_price"],
            reason=data["reason"],
            description=data["description"],
            changed_at=datetime.utcnow()
        )
        self.session.add(price_history)
        await self.session.commit()
        await self.session.refresh(price_history)
        return price_history


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
    
    async def get_property_for_task(self, property_id: int) -> Optional[Property]:
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
    
    async def update_property_price_timestamp(self, property_id: int) -> None:
        """Обновить временную метку цены объекта"""
        await self.session.execute(
            update(Property)
            .where(Property.id == property_id)
            .values(updated_at=datetime.utcnow())
        )
        await self.session.commit()


# Создаем глобальные экземпляры CRUD классов
# Для классов, не требующих сессию
crud_user = CRUDUser(User)
crud_developer = CRUDDeveloper(Developer)
crud_project = CRUDProject(Project)
crud_building = CRUDBuilding(Building)
crud_property = CRUDProperty(Property)
crud_property_address = CRUDPropertyAddress(PropertyAddress)
crud_property_price = CRUDPropertyPrice(PropertyPrice)
crud_residential = CRUDResidentialProperty(ResidentialProperty)
crud_property_features = CRUDPropertyFeatures(PropertyFeatures)
crud_property_analytics = CRUDPropertyAnalytics(PropertyAnalytics)
crud_commercial = CRUDCommercialProperty(CommercialProperty)
crud_house_land = CRUDHouseAndLand(HouseAndLand)
crud_property_media = CRUDPropertyMedia(PropertyMedia)
crud_promo_tag = CRUDPromoTag(PromoTag)
crud_mortgage = CRUDMortgageProgram(MortgageProgram)
crud_price_history = CRUDPriceHistory(PriceHistory)
crud_views_log = CRUDViewsLog(ViewsLog)
crud_booking = CRUDBooking(Booking)
crud_dynamic_pricing_config = CRUDDynamicPricingConfig(DynamicPricingConfig)
crud_promotion = CRUDPromotion(Promotion)
crud_webhook = CRUDWebhook(WebhookInbox)

# Примечание: Следующие классы требуют активную сессию и должны создаваться в runtime:
# - CRUDDynamicPricing
# - CRUDWorker
