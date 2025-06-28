from pydantic import BaseModel, Field, validator, EmailStr, constr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models import (
    UserRole, PropertyClass, ApartmentStatus, BookingStatus, 
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
    inn: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None


class DeveloperCreate(DeveloperBase):
    pass


class DeveloperUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None


class DeveloperResponse(DeveloperBase):
    id: int
    verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    name: str
    city: str
    region_code: str
    address: str
    description: Optional[str] = None
    class_type: PropertyClass
    completion_date: Optional[datetime] = None


class ProjectCreate(ProjectBase):
    developer_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    completion_date: Optional[datetime] = None


class ProjectResponse(ProjectBase):
    id: int
    developer_id: int
    created_at: datetime
    total_apartments: Optional[int] = None
    available_apartments: Optional[int] = None

    class Config:
        from_attributes = True


class ProjectGeoResponse(BaseModel):
    id: int
    name: str
    city: str
    address: str
    class_type: PropertyClass
    lat: float
    lon: float
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    available_count: int

    class Config:
        from_attributes = True


class MapFiltersResponse(BaseModel):
    cities: List[str]
    regions: List[str]
    property_classes: List[PropertyClass]
    price_ranges: Dict[str, float]  # min_price, max_price
    completion_years: List[int]


# Building schemas
class BuildingBase(BaseModel):
    name: str
    floors: int
    sections: Optional[int] = None
    commissioning_quarter: Optional[int] = None
    commissioning_year: Optional[int] = None


class BuildingCreate(BuildingBase):
    project_id: Optional[int] = None


class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    floors: Optional[int] = None
    commissioning_quarter: Optional[int] = None
    commissioning_year: Optional[int] = None


class BuildingResponse(BuildingBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Apartment schemas
class ApartmentBase(BaseModel):
    number: str
    floor: int
    rooms: int
    area_total: float
    area_living: Optional[float] = None
    area_kitchen: Optional[float] = None
    base_price: float
    current_price: float
    balcony: bool = False
    loggia: bool = False
    parking: bool = False
    layout_image_url: Optional[str] = None


class ApartmentCreate(ApartmentBase):
    building_id: int


class ApartmentUpdate(BaseModel):
    current_price: Optional[float] = None
    status: Optional[ApartmentStatus] = None
    layout_image_url: Optional[str] = None


class ApartmentResponse(ApartmentBase):
    id: int
    building_id: int
    status: ApartmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ApartmentMatchRequest(BaseModel):
    budget: float
    preferred_cities: List[str]
    preferred_districts: Optional[List[str]] = None
    min_rooms: Optional[int] = None
    max_rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    property_class: Optional[PropertyClass] = None
    has_balcony: Optional[bool] = None
    has_parking: Optional[bool] = None
    max_floor: Optional[int] = None


# Price History schemas
class PriceHistoryBase(BaseModel):
    old_price: float
    new_price: float
    reason: PriceChangeReason
    description: Optional[str] = None


class PriceHistoryCreate(PriceHistoryBase):
    apartment_id: int


class PriceHistoryResponse(PriceHistoryBase):
    id: int
    apartment_id: int
    changed_at: datetime

    class Config:
        from_attributes = True


# Views Log schemas
class ViewsLogBase(BaseModel):
    event: ViewEvent
    user_id: Optional[int] = None


class ViewsLogCreate(ViewsLogBase):
    apartment_id: int


class ViewsLogResponse(ViewsLogBase):
    id: int
    apartment_id: int
    occurred_at: datetime

    class Config:
        from_attributes = True


# Apartment Stats schemas
class ApartmentStatsBase(BaseModel):
    views_24h: int = 0
    leads_24h: int = 0
    bookings_24h: int = 0
    days_on_site: int = 0


class ApartmentStatsCreate(ApartmentStatsBase):
    apartment_id: int


class ApartmentStatsResponse(ApartmentStatsBase):
    apartment_id: int
    updated_at: datetime

    class Config:
        from_attributes = True


class MarketAnalyticsResponse(BaseModel):
    total_views: int
    avg_views: float
    avg_bookings: float
    period_days: int = 30


# Booking schemas
class BookingBase(BaseModel):
    apartment_id: int
    user_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    status: BookingStatus


class BookingResponse(BookingBase):
    id: int
    status: BookingStatus
    booked_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True


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


class DynamicPricingConfigResponse(DynamicPricingConfigBase):
    id: int
    created_at: datetime


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


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


# Search schemas
class ApartmentSearchParams(BaseModel):
    city: Optional[str] = None
    region_code: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    rooms: Optional[int] = None
    min_area: Optional[float] = None
    max_area: Optional[float] = None
    property_class: Optional[PropertyClass] = None
    status: Optional[ApartmentStatus] = None
    limit: Optional[int] = 20
    offset: Optional[int] = 0


# Dynamic Pricing Result schema
class DynamicPricingResult(BaseModel):
    apartment_id: int
    old_price: float
    new_price: float
    price_change_percent: float
    demand_score: float
    demand_normalized: float
    reason: str
    description: str


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
    inn: str
    ogrn: str


class AdminRegister(UserRegisterBase):
    """Схема для регистрации администратора"""
    role: UserRole = UserRole.ADMIN


class RefreshToken(BaseModel):
    """Схема для обновления токена"""
    refresh_token: str 