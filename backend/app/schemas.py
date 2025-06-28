from pydantic import BaseModel, Field, validator, EmailStr, constr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from uuid import UUID
from app.models import (
    UserRole, PropertyType, PropertyCategory, PropertyStatus, BookingStatus, 
    ViewEvent, PriceChangeReason
)


# User schemas
class UserBase(BaseModel):
    email: str
    display_name: str
    phone: Optional[str] = None
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    display_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Developer schemas
class DeveloperBase(BaseModel):
    name: str


class DeveloperCreate(DeveloperBase):
    pass


class DeveloperUpdate(BaseModel):
    name: Optional[str] = None


class DeveloperResponse(DeveloperBase):
    id: UUID

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    developer_id: Optional[UUID] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    developer_id: Optional[UUID] = None


class ProjectResponse(ProjectBase):
    id: UUID
    developer_id: Optional[UUID] = None

    class Config:
        from_attributes = True


# Building schemas
class BuildingBase(BaseModel):
    pass


class BuildingCreate(BuildingBase):
    project_id: Optional[UUID] = None


class BuildingUpdate(BaseModel):
    project_id: Optional[UUID] = None


class BuildingResponse(BuildingBase):
    id: UUID
    project_id: Optional[UUID] = None

    class Config:
        from_attributes = True


# Property schemas
class PropertyBase(BaseModel):
    external_id: Optional[str] = None
    property_type: PropertyType
    category: PropertyCategory
    developer_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    building_id: Optional[UUID] = None
    status: PropertyStatus = PropertyStatus.AVAILABLE
    has_3d_tour: bool = False


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    external_id: Optional[str] = None
    status: Optional[PropertyStatus] = None
    has_3d_tour: Optional[bool] = None


class PropertyResponse(PropertyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Property Address schemas
class PropertyAddressBase(BaseModel):
    address_full: str
    city: str
    region: str
    district: Optional[str] = None
    lat: float
    lng: float


class PropertyAddressCreate(PropertyAddressBase):
    property_id: UUID


class PropertyAddressUpdate(BaseModel):
    address_full: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class PropertyAddressResponse(PropertyAddressBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Property Price schemas
class PropertyPriceBase(BaseModel):
    base_price: float
    current_price: float
    currency: str = "RUB"
    price_per_m2: Optional[float] = None


class PropertyPriceCreate(PropertyPriceBase):
    property_id: UUID


class PropertyPriceUpdate(BaseModel):
    base_price: Optional[float] = None
    current_price: Optional[float] = None
    currency: Optional[str] = None
    price_per_m2: Optional[float] = None


class PropertyPriceResponse(PropertyPriceBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Residential Property schemas
class ResidentialPropertyBase(BaseModel):
    unit_number: Optional[str] = None
    floor: Optional[int] = None
    floors_total: Optional[int] = None
    rooms: Optional[int] = None
    is_studio: bool = False
    is_free_plan: bool = False
    total_area: Optional[float] = None
    living_area: Optional[float] = None
    kitchen_area: Optional[float] = None
    ceiling_height: Optional[float] = None
    completion_date: Optional[datetime] = None


class ResidentialPropertyCreate(ResidentialPropertyBase):
    property_id: UUID


class ResidentialPropertyUpdate(BaseModel):
    unit_number: Optional[str] = None
    floor: Optional[int] = None
    floors_total: Optional[int] = None
    rooms: Optional[int] = None
    is_studio: Optional[bool] = None
    is_free_plan: Optional[bool] = None
    total_area: Optional[float] = None
    living_area: Optional[float] = None
    kitchen_area: Optional[float] = None
    ceiling_height: Optional[float] = None
    completion_date: Optional[datetime] = None


class ResidentialPropertyResponse(ResidentialPropertyBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Property Features schemas
class PropertyFeaturesBase(BaseModel):
    balcony: bool = False
    loggia: bool = False
    terrace: bool = False
    view: Optional[str] = None
    finishing: Optional[str] = None
    parking_type: Optional[str] = None
    parking_price: Optional[float] = None


class PropertyFeaturesCreate(PropertyFeaturesBase):
    property_id: UUID


class PropertyFeaturesUpdate(BaseModel):
    balcony: Optional[bool] = None
    loggia: Optional[bool] = None
    terrace: Optional[bool] = None
    view: Optional[str] = None
    finishing: Optional[str] = None
    parking_type: Optional[str] = None
    parking_price: Optional[float] = None


class PropertyFeaturesResponse(PropertyFeaturesBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Property Analytics schemas
class PropertyAnalyticsBase(BaseModel):
    days_on_market: Optional[int] = None
    rli_index: Optional[float] = None
    demand_score: Optional[int] = None
    clicks_total: Optional[int] = None
    favourites_total: Optional[int] = None
    bookings_total: Optional[int] = None


class PropertyAnalyticsCreate(PropertyAnalyticsBase):
    property_id: UUID


class PropertyAnalyticsUpdate(BaseModel):
    days_on_market: Optional[int] = None
    rli_index: Optional[float] = None
    demand_score: Optional[int] = None
    clicks_total: Optional[int] = None
    favourites_total: Optional[int] = None
    bookings_total: Optional[int] = None


class PropertyAnalyticsResponse(PropertyAnalyticsBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Commercial Property schemas
class CommercialPropertyBase(BaseModel):
    commercial_subtype: Optional[PropertyCategory] = None
    open_space: Optional[bool] = None
    has_showcase_windows: Optional[bool] = None
    allowed_activity: Optional[str] = None
    tax_rate: Optional[float] = None
    maintenance_fee: Optional[float] = None


class CommercialPropertyCreate(CommercialPropertyBase):
    property_id: UUID


class CommercialPropertyUpdate(BaseModel):
    commercial_subtype: Optional[PropertyCategory] = None
    open_space: Optional[bool] = None
    has_showcase_windows: Optional[bool] = None
    allowed_activity: Optional[str] = None
    tax_rate: Optional[float] = None
    maintenance_fee: Optional[float] = None


class CommercialPropertyResponse(CommercialPropertyBase):
    property_id: UUID

    class Config:
        from_attributes = True


# House and Land schemas
class HouseAndLandBase(BaseModel):
    land_area: Optional[float] = None
    floors_in_house: Optional[int] = None
    house_material: Optional[str] = None
    year_built: Optional[int] = None
    has_fence: Optional[bool] = None
    garage_on_plot: Optional[bool] = None
    bathhouse_on_plot: Optional[bool] = None


class HouseAndLandCreate(HouseAndLandBase):
    property_id: UUID


class HouseAndLandUpdate(BaseModel):
    land_area: Optional[float] = None
    floors_in_house: Optional[int] = None
    house_material: Optional[str] = None
    year_built: Optional[int] = None
    has_fence: Optional[bool] = None
    garage_on_plot: Optional[bool] = None
    bathhouse_on_plot: Optional[bool] = None


class HouseAndLandResponse(HouseAndLandBase):
    property_id: UUID

    class Config:
        from_attributes = True


# Property Media schemas
class PropertyMediaBase(BaseModel):
    layout_image_url: Optional[str] = None
    vr_tour_url: Optional[str] = None
    video_url: Optional[str] = None


class PropertyMediaCreate(PropertyMediaBase):
    property_id: UUID


class PropertyMediaUpdate(BaseModel):
    layout_image_url: Optional[str] = None
    vr_tour_url: Optional[str] = None
    video_url: Optional[str] = None


class PropertyMediaResponse(PropertyMediaBase):
    id: int
    property_id: UUID

    class Config:
        from_attributes = True


# Promo Tag schemas
class PromoTagBase(BaseModel):
    tag: str


class PromoTagCreate(PromoTagBase):
    property_id: UUID


class PromoTagUpdate(BaseModel):
    tag: Optional[str] = None


class PromoTagResponse(PromoTagBase):
    id: int
    property_id: UUID

    class Config:
        from_attributes = True


# Mortgage Program schemas
class MortgageProgramBase(BaseModel):
    pass


class MortgageProgramCreate(MortgageProgramBase):
    property_id: UUID


class MortgageProgramResponse(MortgageProgramBase):
    id: UUID
    property_id: UUID

    class Config:
        from_attributes = True


# Price History schemas
class PriceHistoryBase(BaseModel):
    old_price: float
    new_price: float
    reason: PriceChangeReason
    description: Optional[str] = None


class PriceHistoryCreate(PriceHistoryBase):
    property_id: UUID


class PriceHistoryResponse(PriceHistoryBase):
    id: int
    property_id: UUID
    changed_at: datetime

    class Config:
        from_attributes = True


# Views Log schemas
class ViewsLogBase(BaseModel):
    event: ViewEvent
    user_id: Optional[int] = None


class ViewsLogCreate(ViewsLogBase):
    property_id: UUID


class ViewsLogResponse(ViewsLogBase):
    id: int
    property_id: UUID
    occurred_at: datetime

    class Config:
        from_attributes = True


# Booking schemas
class BookingBase(BaseModel):
    property_id: UUID
    user_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    status: BookingStatus


class BookingResponse(BookingBase):
    id: int
    status: BookingStatus
    booked_at: datetime

    class Config:
        from_attributes = True


# Property Search schemas
class PropertySearchParams(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    property_type: Optional[PropertyType] = None
    category: Optional[PropertyCategory] = None
    rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    status: Optional[PropertyStatus] = None
    developer_id: Optional[UUID] = None
    project_id: Optional[UUID] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0


# Property Match schemas
class PropertyMatchRequest(BaseModel):
    budget: float
    preferred_cities: List[str]
    preferred_districts: Optional[List[str]] = None
    min_rooms: Optional[int] = None
    max_rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    property_type: Optional[PropertyType] = None
    category: Optional[PropertyCategory] = None
    has_balcony: Optional[bool] = None
    has_parking: Optional[bool] = None
    max_floor: Optional[int] = None


# Market Analytics schemas
class MarketAnalyticsResponse(BaseModel):
    total_views: int
    avg_views: float
    avg_bookings: float
    period_days: int = 30


# Promotion schemas
class PromotionBase(BaseModel):
    name: str
    discount_percent: float
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[Dict[str, Any]] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    discount_percent: Optional[float] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    conditions: Optional[Dict[str, Any]] = None


class PromotionResponse(PromotionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Dynamic Pricing schemas
class DynamicPricingConfigBase(BaseModel):
    k1: float = 0.5
    k2: float = 2.0
    k3: float = 5.0
    enabled: bool = True


class DynamicPricingConfigCreate(DynamicPricingConfigBase):
    pass


class DynamicPricingConfigUpdate(BaseModel):
    k1: Optional[float] = None
    k2: Optional[float] = None
    k3: Optional[float] = None
    enabled: Optional[bool] = None


class DynamicPricingConfigResponse(DynamicPricingConfigBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DynamicPricingResult(BaseModel):
    property_id: UUID
    old_price: float
    new_price: float
    price_change_percent: float
    demand_score: float
    demand_normalized: float
    reason: str
    description: str


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TokenResponse(BaseModel):
    """Схема ответа с токенами"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Схема данных токена"""
    sub: Optional[int] = None
    exp: Optional[datetime] = None


class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    email: EmailStr
    password: str


class UserRegisterBase(BaseModel):
    """Базовая схема для регистрации пользователя"""
    email: EmailStr
    password: constr(min_length=8)
    full_name: str
    phone: str


class BuyerRegister(UserRegisterBase):
    """Схема для регистрации покупателя"""
    role: UserRole = UserRole.BUYER


class DeveloperRegister(UserRegisterBase):
    """Схема для регистрации застройщика"""
    role: UserRole = UserRole.DEVELOPER
    company_name: str


class AdminRegister(UserRegisterBase):
    """Схема для регистрации администратора"""
    role: UserRole = UserRole.ADMIN


class RefreshToken(BaseModel):
    """Схема для обновления токена"""
    refresh_token: str


# Webhook schemas
class WebhookBase(BaseModel):
    source: str
    payload: Dict[str, Any]


class WebhookCreate(WebhookBase):
    pass


class WebhookResponse(WebhookBase):
    id: int
    received_at: datetime
    processed: bool

    class Config:
        from_attributes = True


# Comprehensive Property Response
class PropertyFullResponse(BaseModel):
    """Полная информация об объекте недвижимости со всеми связанными данными"""
    id: UUID
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    property_type: PropertyType
    category: PropertyCategory
    status: PropertyStatus
    has_3d_tour: bool
    
    # Related data
    developer: Optional[DeveloperResponse] = None
    project: Optional[ProjectResponse] = None
    building: Optional[BuildingResponse] = None
    address: Optional[PropertyAddressResponse] = None
    price: Optional[PropertyPriceResponse] = None
    residential: Optional[ResidentialPropertyResponse] = None
    features: Optional[PropertyFeaturesResponse] = None
    analytics: Optional[PropertyAnalyticsResponse] = None
    commercial: Optional[CommercialPropertyResponse] = None
    house_land: Optional[HouseAndLandResponse] = None
    media: List[PropertyMediaResponse] = []
    promo_tags: List[PromoTagResponse] = []
    mortgage_programs: List[MortgageProgramResponse] = []

    class Config:
        from_attributes = True


class ProjectGeoResponse(BaseModel):
    id: UUID
    name: str
    lat: float
    lng: float
    # Добавьте другие поля по необходимости


class MapFiltersResponse(BaseModel):
    cities: List[str] = []
    region_codes: List[str] = []
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    property_classes: List[str] = []
    completion_years: List[int] = []
    # Добавьте другие поля по необходимости 