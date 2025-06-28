from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from pydantic import validator, constr
import json
from sqlalchemy import String, TypeDecorator, JSON


class EmailType(TypeDecorator):
    """Custom type for email addresses"""
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value


class JsonType(TypeDecorator):
    """Custom type for JSON fields"""
    impl = JSON
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return None


class UserRole(str, Enum):
    BUYER = "buyer"
    DEVELOPER = "developer"
    ADMIN = "admin"


class PropertyClass(str, Enum):
    ECONOM = "econom"
    COMFORT = "comfort"
    BUSINESS = "business"
    PREMIUM = "premium"


class ApartmentStatus(str, Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"


class BookingStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class ViewEvent(str, Enum):
    VIEW = "view"
    FAVOURITE = "favourite"


class PriceChangeReason(str, Enum):
    DYNAMIC = "dynamic"
    MANUAL = "manual"
    PROMO = "promo"


class TimestampedModel(SQLModel):
    """Базовый класс для моделей с временными метками"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class User(TimestampedModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_type=EmailType, unique=True)
    hashed_password: str
    display_name: constr(min_length=2, max_length=100)
    role: UserRole
    phone: Optional[str] = Field(default=None, max_length=20)
    
    # Relationships
    views_logs: List["ViewsLog"] = Relationship(back_populates="user")
    bookings: List["Booking"] = Relationship(back_populates="user")


class Developer(TimestampedModel, table=True):
    __tablename__ = "developers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: constr(min_length=2, max_length=100)
    inn: str = Field(unique=True, min_length=10, max_length=12)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    verified: bool = Field(default=False)
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="developer")


class Project(TimestampedModel, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    developer_id: int = Field(foreign_key="developers.id")
    name: constr(min_length=2, max_length=100)
    city: str
    region_code: str = Field(max_length=2)
    address: str
    description: Optional[str] = None
    class_type: PropertyClass
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = Field(default=None, ge=0)
    available_apartments: Optional[int] = Field(default=None, ge=0)
    
    # Relationships
    developer: Developer = Relationship(back_populates="projects")
    buildings: List["Building"] = Relationship(back_populates="project")

    @validator("available_apartments")
    def validate_available_apartments(cls, v, values):
        if v is not None and values.get("total_apartments") is not None:
            if v > values["total_apartments"]:
                raise ValueError("Available apartments cannot exceed total apartments")
        return v


class Building(TimestampedModel, table=True):
    __tablename__ = "buildings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    name: constr(min_length=1, max_length=50)
    floors: int = Field(gt=0)
    completion_date: Optional[datetime] = None
    
    # Relationships
    project: Project = Relationship(back_populates="buildings")
    apartments: List["Apartment"] = Relationship(back_populates="building")


class Apartment(TimestampedModel, table=True):
    __tablename__ = "apartments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="buildings.id")
    number: str = Field(max_length=20)
    floor: int = Field(gt=0)
    rooms: int = Field(gt=0, le=10)
    area_total: float = Field(gt=0)
    area_living: Optional[float] = Field(default=None, gt=0)
    area_kitchen: Optional[float] = Field(default=None, gt=0)
    base_price: float = Field(gt=0)
    current_price: float = Field(gt=0)
    status: ApartmentStatus = Field(default=ApartmentStatus.AVAILABLE)
    balcony: bool = Field(default=False)
    loggia: bool = Field(default=False)
    parking: bool = Field(default=False)
    
    # Relationships
    building: Building = Relationship(back_populates="apartments")
    price_history: List["PriceHistory"] = Relationship(back_populates="apartment")
    views_logs: List["ViewsLog"] = Relationship(back_populates="apartment")
    bookings: List["Booking"] = Relationship(back_populates="apartment")
    stats: Optional["ApartmentStats"] = Relationship(back_populates="apartment")

    @validator("area_living")
    def validate_living_area(cls, v, values):
        if v is not None and values.get("area_total") is not None:
            if v >= values["area_total"]:
                raise ValueError("Living area must be less than total area")
        return v

    @validator("floor")
    def validate_floor(cls, v, values):
        if "building_id" in values:
            # TODO: Add validation against building.floors
            pass
        return v


class PriceHistory(TimestampedModel, table=True):
    __tablename__ = "price_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int = Field(foreign_key="apartments.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    old_price: float = Field(gt=0)
    new_price: float = Field(gt=0)
    reason: PriceChangeReason
    description: Optional[str] = None
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="price_history")


class ViewsLog(TimestampedModel, table=True):
    __tablename__ = "views_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int = Field(foreign_key="apartments.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    event: ViewEvent
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="views_logs")
    user: Optional[User] = Relationship(back_populates="views_logs")


class ApartmentStats(SQLModel, table=True):
    __tablename__ = "apartment_stats"
    
    apartment_id: int = Field(primary_key=True, foreign_key="apartments.id")
    views_24h: int = Field(default=0, ge=0)
    leads_24h: int = Field(default=0, ge=0)
    bookings_24h: int = Field(default=0, ge=0)
    days_on_site: int = Field(default=0, ge=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="stats")


class Booking(TimestampedModel, table=True):
    __tablename__ = "bookings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int = Field(foreign_key="apartments.id")
    user_id: int = Field(foreign_key="users.id")
    status: BookingStatus = Field(default=BookingStatus.ACTIVE)
    booked_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="bookings")
    user: User = Relationship(back_populates="bookings")


class Promotion(TimestampedModel, table=True):
    __tablename__ = "promotions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: constr(min_length=2, max_length=100)
    discount_percent: float = Field(gt=0, le=100)
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[Dict[str, Any]] = Field(default=None, sa_type=JsonType)

    @validator("ends_at")
    def validate_dates(cls, v, values):
        if "starts_at" in values and v <= values["starts_at"]:
            raise ValueError("End date must be after start date")
        return v


class WebhookInbox(TimestampedModel, table=True):
    __tablename__ = "webhook_inbox"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    payload: Dict[str, Any] = Field(sa_type=JsonType)
    received_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)


class DynamicPricingConfig(TimestampedModel, table=True):
    __tablename__ = "dynamic_pricing_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    k1: float = Field(default=0.5, gt=0)  # views coefficient
    k2: float = Field(default=2.0, gt=0)  # leads coefficient
    k3: float = Field(default=5.0, gt=0)  # bookings coefficient
    enabled: bool = Field(default=True) 