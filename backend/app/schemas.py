from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.models import (
    UserRole, PropertyClass, ApartmentStatus, BookingStatus, 
    ViewEvent, PriceChangeReason
)


# User schemas
class UserBase(BaseModel):
    email: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


# Developer schemas
class DeveloperBase(BaseModel):
    name: str
    inn: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None


class DeveloperCreate(DeveloperBase):
    pass


class DeveloperUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    verified: Optional[bool] = None


class DeveloperResponse(DeveloperBase):
    id: int
    verified: bool
    created_at: datetime


# Project schemas
class ProjectBase(BaseModel):
    name: str
    city: str
    region_code: str
    address: str
    description: Optional[str] = None
    class_type: PropertyClass
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = None
    available_apartments: Optional[int] = None


class ProjectCreate(ProjectBase):
    developer_id: int


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = None
    available_apartments: Optional[int] = None


class ProjectResponse(ProjectBase):
    id: int
    developer_id: int
    created_at: datetime


# Building schemas
class BuildingBase(BaseModel):
    name: str
    floors: int
    completion_date: Optional[datetime] = None


class BuildingCreate(BuildingBase):
    project_id: int


class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    floors: Optional[int] = None
    completion_date: Optional[datetime] = None


class BuildingResponse(BuildingBase):
    id: int
    project_id: int
    created_at: datetime


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


class ApartmentCreate(ApartmentBase):
    building_id: int


class ApartmentUpdate(BaseModel):
    current_price: Optional[float] = None
    status: Optional[ApartmentStatus] = None
    balcony: Optional[bool] = None
    loggia: Optional[bool] = None
    parking: Optional[bool] = None


class ApartmentResponse(ApartmentBase):
    id: int
    building_id: int
    status: ApartmentStatus
    created_at: datetime
    updated_at: datetime


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


# Views Log schemas
class ViewsLogBase(BaseModel):
    event: ViewEvent


class ViewsLogCreate(ViewsLogBase):
    apartment_id: int
    user_id: Optional[int] = None


class ViewsLogResponse(ViewsLogBase):
    id: int
    apartment_id: int
    user_id: Optional[int]
    occurred_at: datetime


# Apartment Stats schemas
class ApartmentStatsBase(BaseModel):
    views_24h: int
    leads_24h: int
    bookings_24h: int
    days_on_site: int


class ApartmentStatsCreate(ApartmentStatsBase):
    apartment_id: int


class ApartmentStatsUpdate(ApartmentStatsBase):
    pass


class ApartmentStatsResponse(ApartmentStatsBase):
    apartment_id: int
    updated_at: datetime


# Booking schemas
class BookingBase(BaseModel):
    apartment_id: int
    user_id: int


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    status: Optional[BookingStatus] = None


class BookingResponse(BookingBase):
    id: int
    status: BookingStatus
    booked_at: datetime


# Promotion schemas
class PromotionBase(BaseModel):
    name: str
    discount_percent: float
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[dict] = None


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    name: Optional[str] = None
    discount_percent: Optional[float] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    conditions: Optional[dict] = None


class PromotionResponse(PromotionBase):
    id: int
    created_at: datetime


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
class WebhookInboxBase(BaseModel):
    source: str
    payload: dict


class WebhookInboxCreate(WebhookInboxBase):
    pass


class WebhookInboxResponse(WebhookInboxBase):
    id: int
    received_at: datetime
    processed: bool


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
    limit: int = 20
    offset: int = 0


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