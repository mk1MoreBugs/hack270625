from pydantic import BaseModel, Field, validator, EmailStr, constr, confloat
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from app.models import (
    UserRole, PropertyClass, ApartmentStatus, BookingStatus, 
    ViewEvent, PriceChangeReason
)


# Base schema for common fields
class TimestampedSchema(BaseModel):
    """Базовая схема для объектов с временными метками"""
    created_at: datetime
    updated_at: Optional[datetime] = None


# User schemas
class UserBase(BaseModel):
    """Базовая схема пользователя"""
    email: EmailStr
    display_name: constr(min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    role: UserRole


class UserCreate(UserBase):
    """Схема создания пользователя"""
    password: constr(min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Схема обновления пользователя"""
    email: Optional[EmailStr] = None
    display_name: Optional[constr(min_length=2, max_length=100)] = None
    phone: Optional[str] = Field(default=None, max_length=20)
    password: Optional[constr(min_length=8, max_length=100)] = None


class UserResponse(UserBase, TimestampedSchema):
    """Схема ответа с данными пользователя"""
    id: int

    class Config:
        from_attributes = True


# Developer schemas
class DeveloperBase(BaseModel):
    """Базовая схема застройщика"""
    name: constr(min_length=2, max_length=100)
    inn: constr(min_length=10, max_length=12)
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None


class DeveloperCreate(DeveloperBase):
    """Схема создания застройщика"""
    pass


class DeveloperUpdate(BaseModel):
    """Схема обновления застройщика"""
    name: Optional[constr(min_length=2, max_length=100)] = None
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None


class DeveloperResponse(DeveloperBase, TimestampedSchema):
    """Схема ответа с данными застройщика"""
    id: int
    verified: bool

    class Config:
        from_attributes = True


# Project schemas
class ProjectBase(BaseModel):
    """Базовая схема проекта"""
    name: constr(min_length=2, max_length=100)
    city: str
    region_code: constr(min_length=2, max_length=2)
    address: str
    description: Optional[str] = None
    class_type: PropertyClass
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = Field(default=None, ge=0)
    available_apartments: Optional[int] = Field(default=None, ge=0)

    @validator("available_apartments")
    def validate_available_apartments(cls, v, values):
        if v is not None and values.get("total_apartments") is not None:
            if v > values["total_apartments"]:
                raise ValueError("Available apartments cannot exceed total apartments")
        return v


class ProjectCreate(ProjectBase):
    """Схема создания проекта"""
    developer_id: int


class ProjectUpdate(BaseModel):
    """Схема обновления проекта"""
    name: Optional[constr(min_length=2, max_length=100)] = None
    description: Optional[str] = None
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = Field(default=None, ge=0)
    available_apartments: Optional[int] = Field(default=None, ge=0)


class ProjectResponse(ProjectBase, TimestampedSchema):
    """Схема ответа с данными проекта"""
    id: int
    developer_id: int

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
    """Базовая схема корпуса"""
    name: constr(min_length=1, max_length=50)
    floors: int = Field(gt=0)
    completion_date: Optional[datetime] = None


class BuildingCreate(BuildingBase):
    """Схема создания корпуса"""
    project_id: int


class BuildingUpdate(BaseModel):
    """Схема обновления корпуса"""
    name: Optional[constr(min_length=1, max_length=50)] = None
    floors: Optional[int] = Field(default=None, gt=0)
    completion_date: Optional[datetime] = None


class BuildingResponse(BuildingBase, TimestampedSchema):
    """Схема ответа с данными корпуса"""
    id: int
    project_id: int

    class Config:
        from_attributes = True


# Apartment schemas
class ApartmentBase(BaseModel):
    """Базовая схема квартиры"""
    number: constr(max_length=20)
    floor: int = Field(gt=0)
    rooms: int = Field(gt=0, le=10)
    area_total: float = Field(gt=0)
    area_living: Optional[float] = Field(default=None, gt=0)
    area_kitchen: Optional[float] = Field(default=None, gt=0)
    base_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    balcony: bool = False
    loggia: bool = False
    parking: bool = False

    @validator("area_living")
    def validate_living_area(cls, v, values):
        if v is not None and values.get("area_total") is not None:
            if v >= values["area_total"]:
                raise ValueError("Living area must be less than total area")
        return v


class ApartmentCreate(ApartmentBase):
    """Схема создания квартиры"""
    building_id: int


class ApartmentUpdate(BaseModel):
    """Схема обновления квартиры"""
    current_price: Optional[float] = Field(default=None, gt=0)
    status: Optional[ApartmentStatus] = None


class ApartmentResponse(ApartmentBase, TimestampedSchema):
    """Схема ответа с данными квартиры"""
    id: int
    building_id: int
    status: ApartmentStatus

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
    """Базовая схема истории цен"""
    old_price: float = Field(gt=0)
    new_price: float = Field(gt=0)
    reason: PriceChangeReason
    description: Optional[str] = None


class PriceHistoryCreate(PriceHistoryBase):
    """Схема создания записи истории цен"""
    apartment_id: int


class PriceHistoryResponse(PriceHistoryBase, TimestampedSchema):
    """Схема ответа с данными истории цен"""
    id: int
    apartment_id: int
    changed_at: datetime

    class Config:
        from_attributes = True


# Views Log schemas
class ViewsLogBase(BaseModel):
    """Базовая схема лога просмотров"""
    event: ViewEvent
    user_id: Optional[int] = None


class ViewsLogCreate(ViewsLogBase):
    """Схема создания записи лога просмотров"""
    apartment_id: int


class ViewsLogResponse(ViewsLogBase, TimestampedSchema):
    """Схема ответа с данными лога просмотров"""
    id: int
    apartment_id: int
    occurred_at: datetime

    class Config:
        from_attributes = True


# Apartment Stats schemas
class ApartmentStatsBase(BaseModel):
    """Базовая схема статистики квартиры"""
    views_24h: int = Field(default=0, ge=0)
    leads_24h: int = Field(default=0, ge=0)
    bookings_24h: int = Field(default=0, ge=0)
    days_on_site: int = Field(default=0, ge=0)


class ApartmentStatsCreate(ApartmentStatsBase):
    """Схема создания статистики квартиры"""
    apartment_id: int


class ApartmentStatsResponse(ApartmentStatsBase):
    """Схема ответа с данными статистики квартиры"""
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
    """Базовая схема бронирования"""
    apartment_id: int
    user_id: int


class BookingCreate(BookingBase):
    """Схема создания бронирования"""
    pass


class BookingUpdate(BaseModel):
    """Схема обновления бронирования"""
    status: BookingStatus


class BookingResponse(BookingBase, TimestampedSchema):
    """Схема ответа с данными бронирования"""
    id: int
    status: BookingStatus
    booked_at: datetime

    class Config:
        from_attributes = True


# Promotion schemas
class PromotionBase(BaseModel):
    """Базовая схема акции"""
    name: constr(min_length=2, max_length=100)
    discount_percent: confloat(gt=0, le=100)
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[Dict[str, Any]] = None

    @validator("ends_at")
    def validate_dates(cls, v, values):
        if "starts_at" in values and v <= values["starts_at"]:
            raise ValueError("End date must be after start date")
        return v


class PromotionCreate(PromotionBase):
    """Схема создания акции"""
    pass


class PromotionUpdate(BaseModel):
    """Схема обновления акции"""
    name: Optional[constr(min_length=2, max_length=100)] = None
    discount_percent: Optional[confloat(gt=0, le=100)] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    conditions: Optional[Dict[str, Any]] = None


class PromotionResponse(PromotionBase, TimestampedSchema):
    """Схема ответа с данными акции"""
    id: int

    class Config:
        from_attributes = True


# Dynamic Pricing Config schemas
class DynamicPricingConfigBase(BaseModel):
    """Базовая схема конфигурации динамического ценообразования"""
    k1: float = Field(default=0.5, gt=0)
    k2: float = Field(default=2.0, gt=0)
    k3: float = Field(default=5.0, gt=0)
    enabled: bool = True


class DynamicPricingConfigCreate(DynamicPricingConfigBase):
    """Схема создания конфигурации динамического ценообразования"""
    pass


class DynamicPricingConfigUpdate(BaseModel):
    """Схема обновления конфигурации динамического ценообразования"""
    k1: Optional[float] = Field(default=None, gt=0)
    k2: Optional[float] = Field(default=None, gt=0)
    k3: Optional[float] = Field(default=None, gt=0)
    enabled: Optional[bool] = None


class DynamicPricingConfigResponse(DynamicPricingConfigBase, TimestampedSchema):
    """Схема ответа с данными конфигурации динамического ценообразования"""
    id: int

    class Config:
        from_attributes = True


# Authentication schemas
class Token(BaseModel):
    """Схема токена авторизации"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные токена"""
    email: Optional[str] = None


# Webhook schemas
class WebhookBase(BaseModel):
    """Базовая схема вебхука"""
    source: str
    payload: Dict[str, Any]


class WebhookCreate(WebhookBase):
    """Схема создания вебхука"""
    pass


class WebhookResponse(WebhookBase, TimestampedSchema):
    """Схема ответа с данными вебхука"""
    id: int
    received_at: datetime
    processed: bool

    class Config:
        from_attributes = True


# Search and Filter schemas
class ApartmentSearchParams(BaseModel):
    """Параметры поиска квартир"""
    city: Optional[str] = None
    region_code: Optional[str] = None
    min_price: Optional[float] = Field(default=None, gt=0)
    max_price: Optional[float] = Field(default=None, gt=0)
    rooms: Optional[int] = Field(default=None, gt=0, le=10)
    min_area: Optional[float] = Field(default=None, gt=0)
    max_area: Optional[float] = Field(default=None, gt=0)
    property_class: Optional[PropertyClass] = None
    status: Optional[ApartmentStatus] = None
    limit: Optional[int] = Field(default=20, gt=0, le=100)
    offset: Optional[int] = Field(default=0, ge=0)

    @validator("max_price")
    def validate_price_range(cls, v, values):
        if v is not None and values.get("min_price") is not None:
            if v <= values["min_price"]:
                raise ValueError("Maximum price must be greater than minimum price")
        return v

    @validator("max_area")
    def validate_area_range(cls, v, values):
        if v is not None and values.get("min_area") is not None:
            if v <= values["min_area"]:
                raise ValueError("Maximum area must be greater than minimum area")
        return v


class DynamicPricingResult(BaseModel):
    """Результат расчета динамической цены"""
    apartment_id: int
    old_price: float = Field(gt=0)
    new_price: float = Field(gt=0)
    price_change_percent: float
    demand_score: float = Field(ge=0)
    demand_normalized: float = Field(ge=0, le=1)
    reason: str
    description: str 