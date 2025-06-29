from pydantic import BaseModel, Field, validator, EmailStr, constr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models import (
    UserRole, PropertyType, PropertyCategory, PropertyStatus, BookingStatus, 
    ViewEvent, PriceChangeReason, ViewType, FinishingType, ParkingType
)


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    display_name: str
    phone: Optional[str] = None
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None


class UserRead(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Developer schemas
class DeveloperBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    founding_year: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    website: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)


class DeveloperCreate(DeveloperBase):
    pass


class DeveloperUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    founding_year: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    website: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5)


class DeveloperRead(DeveloperBase):
    id: int
    projects_count: int = 0

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: Optional[str] = None
    start_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: str = "active"
    total_area: Optional[float] = Field(None, gt=0)
    total_units: Optional[int] = Field(None, gt=0)


class ProjectCreate(ProjectBase):
    developer_id: int


class ProjectUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: Optional[str] = None
    total_area: Optional[float] = Field(None, gt=0)
    total_units: Optional[int] = Field(None, gt=0)
    developer_id: Optional[int] = None


class ProjectRead(ProjectBase):
    id: int
    developer_id: int

    class Config:
        from_attributes = True


# Building schemas
class BuildingBase(BaseModel):
    number: Optional[str] = None
    floors_total: Optional[int] = Field(None, ge=1, le=100)
    completion_date: Optional[datetime] = None
    status: str = "under_construction"
    total_units: Optional[int] = Field(None, gt=0)
    available_units: Optional[int] = Field(None, ge=0)


class BuildingCreate(BuildingBase):
    project_id: int


class BuildingUpdate(BaseModel):
    number: Optional[str] = None
    floors_total: Optional[int] = Field(None, ge=1, le=100)
    completion_date: Optional[datetime] = None
    status: Optional[str] = None
    total_units: Optional[int] = Field(None, gt=0)
    available_units: Optional[int] = Field(None, ge=0)
    project_id: Optional[int] = None


class BuildingRead(BuildingBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True


# Property schemas
class PropertyBase(BaseModel):
    external_id: Optional[str] = None
    property_type: PropertyType
    category: PropertyCategory
    developer_id: Optional[int] = None
    project_id: Optional[int] = None
    building_id: Optional[int] = None
    status: PropertyStatus = PropertyStatus.AVAILABLE
    has_3d_tour: bool = False


class PropertyCreate(PropertyBase):
    pass


class PropertyUpdate(BaseModel):
    external_id: Optional[str] = None
    property_type: Optional[PropertyType] = None
    category: Optional[PropertyCategory] = None
    status: Optional[PropertyStatus] = None
    has_3d_tour: Optional[bool] = None
    developer_id: Optional[int] = None
    project_id: Optional[int] = None
    building_id: Optional[int] = None


class PropertyRead(PropertyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    developer_id: Optional[int] = None
    project_id: Optional[int] = None
    building_id: Optional[int] = None

    class Config:
        from_attributes = True


# Property Address schemas
class PropertyAddressBase(BaseModel):
    address_full: str
    city: str
    region: str
    district: Optional[str] = None
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    postal_code: Optional[str] = None


class PropertyAddressCreate(PropertyAddressBase):
    property_id: int


class PropertyAddressUpdate(BaseModel):
    address_full: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    postal_code: Optional[str] = None


class PropertyAddressRead(PropertyAddressBase):
    property_id: int

    class Config:
        from_attributes = True


# Property Price schemas
class PropertyPriceBase(BaseModel):
    base_price: float = Field(..., ge=0)
    current_price: float = Field(..., ge=0)
    currency: str = "RUB"
    price_per_m2: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    discount_amount: Optional[float] = Field(None, ge=0)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)


class PropertyPriceCreate(PropertyPriceBase):
    property_id: int


class PropertyPriceUpdate(BaseModel):
    base_price: Optional[float] = Field(None, ge=0)
    current_price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    price_per_m2: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    discount_amount: Optional[float] = Field(None, ge=0)
    discount_percent: Optional[float] = Field(None, ge=0, le=100)


class PropertyPriceRead(PropertyPriceBase):
    property_id: int

    class Config:
        from_attributes = True


# Residential Property schemas
class ResidentialPropertyBase(BaseModel):
    unit_number: Optional[str] = None
    floor: Optional[int] = Field(None, ge=1, le=100)
    floors_total: Optional[int] = Field(None, ge=1, le=100)
    rooms: Optional[int] = Field(None, ge=0, le=10)
    is_studio: bool = False
    is_free_plan: bool = False
    total_area: Optional[float] = Field(None, ge=0)
    living_area: Optional[float] = Field(None, ge=0)
    kitchen_area: Optional[float] = Field(None, ge=0)
    ceiling_height: Optional[float] = Field(None, ge=0)
    completion_date: Optional[datetime] = None


class ResidentialPropertyCreate(ResidentialPropertyBase):
    property_id: int


class ResidentialPropertyUpdate(BaseModel):
    unit_number: Optional[str] = None
    floor: Optional[int] = Field(None, ge=1, le=100)
    floors_total: Optional[int] = Field(None, ge=1, le=100)
    rooms: Optional[int] = Field(None, ge=0, le=10)
    is_studio: Optional[bool] = None
    is_free_plan: Optional[bool] = None
    total_area: Optional[float] = Field(None, ge=0)
    living_area: Optional[float] = Field(None, ge=0)
    kitchen_area: Optional[float] = Field(None, ge=0)
    ceiling_height: Optional[float] = Field(None, ge=0)
    completion_date: Optional[datetime] = None


class ResidentialPropertyRead(ResidentialPropertyBase):
    property_id: int

    class Config:
        from_attributes = True


# Property Features schemas
class PropertyFeaturesBase(BaseModel):
    balcony: bool = False
    loggia: bool = False
    terrace: bool = False
    view: Optional[ViewType] = None
    finishing: Optional[FinishingType] = None
    parking_type: Optional[ParkingType] = None
    parking_price: Optional[float] = Field(None, ge=0)
    has_furniture: bool = False
    has_appliances: bool = False


class PropertyFeaturesCreate(PropertyFeaturesBase):
    property_id: int


class PropertyFeaturesUpdate(BaseModel):
    balcony: Optional[bool] = None
    loggia: Optional[bool] = None
    terrace: Optional[bool] = None
    view: Optional[ViewType] = None
    finishing: Optional[FinishingType] = None
    parking_type: Optional[ParkingType] = None
    parking_price: Optional[float] = Field(None, ge=0)
    has_furniture: Optional[bool] = None
    has_appliances: Optional[bool] = None


class PropertyFeaturesRead(PropertyFeaturesBase):
    property_id: int

    class Config:
        from_attributes = True


# Property Analytics schemas
class PropertyAnalyticsBase(BaseModel):
    days_on_market: Optional[int] = Field(None, ge=0)
    rli_index: Optional[float] = Field(None, ge=0, le=1)
    demand_score: Optional[int] = Field(None, ge=0, le=100)
    clicks_total: Optional[int] = Field(None, ge=0)
    favourites_total: Optional[int] = Field(None, ge=0)
    bookings_total: Optional[int] = Field(None, ge=0)
    views_last_week: Optional[int] = Field(None, ge=0)
    views_last_month: Optional[int] = Field(None, ge=0)
    price_trend: Optional[float] = None


class PropertyAnalyticsCreate(PropertyAnalyticsBase):
    property_id: int


class PropertyAnalyticsUpdate(BaseModel):
    days_on_market: Optional[int] = Field(None, ge=0)
    rli_index: Optional[float] = Field(None, ge=0, le=1)
    demand_score: Optional[int] = Field(None, ge=0, le=100)
    clicks_total: Optional[int] = Field(None, ge=0)
    favourites_total: Optional[int] = Field(None, ge=0)
    bookings_total: Optional[int] = Field(None, ge=0)
    views_last_week: Optional[int] = Field(None, ge=0)
    views_last_month: Optional[int] = Field(None, ge=0)
    price_trend: Optional[float] = None


class PropertyAnalyticsRead(PropertyAnalyticsBase):
    property_id: int

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
    property_id: int


class CommercialPropertyUpdate(BaseModel):
    commercial_subtype: Optional[PropertyCategory] = None
    open_space: Optional[bool] = None
    has_showcase_windows: Optional[bool] = None
    allowed_activity: Optional[str] = None
    tax_rate: Optional[float] = None
    maintenance_fee: Optional[float] = None


class CommercialPropertyRead(CommercialPropertyBase):
    property_id: int

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
    property_id: int


class HouseAndLandUpdate(BaseModel):
    land_area: Optional[float] = None
    floors_in_house: Optional[int] = None
    house_material: Optional[str] = None
    year_built: Optional[int] = None
    has_fence: Optional[bool] = None
    garage_on_plot: Optional[bool] = None
    bathhouse_on_plot: Optional[bool] = None


class HouseAndLandRead(HouseAndLandBase):
    property_id: int

    class Config:
        from_attributes = True


# Property Media schemas
class PropertyMediaBase(BaseModel):
    layout_image_url: Optional[str] = None
    vr_tour_url: Optional[str] = None
    video_url: Optional[str] = None
    main_photo_url: Optional[str] = None
    photo_urls: Optional[List[str]] = None


class PropertyMediaCreate(PropertyMediaBase):
    property_id: int


class PropertyMediaUpdate(BaseModel):
    layout_image_url: Optional[str] = None
    vr_tour_url: Optional[str] = None
    video_url: Optional[str] = None
    main_photo_url: Optional[str] = None
    photo_urls: Optional[List[str]] = None


class PropertyMediaRead(PropertyMediaBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# Promo Tag schemas
class PromoTagBase(BaseModel):
    tag: str
    active: bool = True
    expires_at: Optional[datetime] = None


class PromoTagCreate(PromoTagBase):
    property_id: int


class PromoTagUpdate(BaseModel):
    tag: Optional[str] = None
    active: Optional[bool] = None
    expires_at: Optional[datetime] = None


class PromoTagRead(PromoTagBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# Mortgage Program schemas
class MortgageProgramBase(BaseModel):
    name: str
    bank_name: str
    interest_rate: float = Field(..., ge=0, le=30)
    down_payment_percent: float = Field(..., ge=0, le=100)
    term_years: int = Field(..., ge=1, le=30)
    monthly_payment: Optional[float] = None
    requirements: Optional[str] = None


class MortgageProgramCreate(MortgageProgramBase):
    property_id: int


class MortgageProgramUpdate(BaseModel):
    name: Optional[str] = None
    bank_name: Optional[str] = None
    interest_rate: Optional[float] = Field(None, ge=0, le=30)
    down_payment_percent: Optional[float] = Field(None, ge=0, le=100)
    term_years: Optional[int] = Field(None, ge=1, le=30)
    monthly_payment: Optional[float] = None
    requirements: Optional[str] = None


class MortgageProgramRead(MortgageProgramBase):
    id: int
    property_id: int

    class Config:
        from_attributes = True


# Price History schemas
class PriceHistoryBase(BaseModel):
    old_price: float
    new_price: float
    reason: PriceChangeReason
    description: Optional[str] = None


class PriceHistoryCreate(PriceHistoryBase):
    property_id: int


class PriceHistoryRead(PriceHistoryBase):
    id: int
    property_id: int
    changed_at: datetime

    class Config:
        from_attributes = True


# Views Log schemas
class ViewsLogBase(BaseModel):
    event: ViewEvent
    user_id: Optional[int] = None


class ViewsLogCreate(ViewsLogBase):
    property_id: int


class ViewsLogRead(ViewsLogBase):
    id: int
    property_id: int
    occurred_at: datetime

    class Config:
        from_attributes = True


# Booking schemas
class BookingBase(BaseModel):
    property_id: int
    user_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    status: BookingStatus


class BookingRead(BookingBase):
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
    developer_id: Optional[int] = None
    project_id: Optional[int] = None
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


class PromotionRead(PromotionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Dynamic Pricing Config schemas
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


class DynamicPricingConfigRead(DynamicPricingConfigBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DynamicPricingResult(BaseModel):
    property_id: int
    old_price: float
    new_price: float
    price_change_percent: float
    demand_score: float
    demand_normalized: float
    reason: str
    description: str


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


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


class WebhookBase(BaseModel):
    source: str
    payload: Dict[str, Any]


class WebhookCreate(WebhookBase):
    pass


class WebhookRead(WebhookBase):
    id: int
    received_at: datetime
    processed: bool

    class Config:
        from_attributes = True


class PropertyFullResponse(BaseModel):
    """Полная информация об объекте недвижимости со всеми связанными данными"""
    id: int
    external_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    property_type: PropertyType
    category: PropertyCategory
    status: PropertyStatus
    has_3d_tour: bool
    
    # Related data
    developer: Optional[DeveloperRead] = None
    project: Optional[ProjectRead] = None
    building: Optional[BuildingRead] = None
    address: Optional[PropertyAddressRead] = None
    price: Optional[PropertyPriceRead] = None
    residential: Optional[ResidentialPropertyRead] = None
    features: Optional[PropertyFeaturesRead] = None
    analytics: Optional[PropertyAnalyticsRead] = None
    commercial: Optional[CommercialPropertyRead] = None
    house_land: Optional[HouseAndLandRead] = None
    media: List[PropertyMediaRead] = []
    promo_tags: List[PromoTagRead] = []
    mortgage_programs: List[MortgageProgramRead] = []

    class Config:
        from_attributes = True


class ProjectGeoResponse(BaseModel):
    id: int
    name: str
    lat: float
    lng: float


class MapFiltersResponse(BaseModel):
    cities: List[str] = []
    region_codes: List[str] = []
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    property_classes: List[str] = []
    completion_years: List[int] = []


class Message(BaseModel):
    """Схема для сообщений об успешном выполнении операции"""
    message: str 