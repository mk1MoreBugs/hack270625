from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import json


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


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: str
    role: UserRole
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    views_logs: List["ViewsLog"] = Relationship(back_populates="user")
    bookings: List["Booking"] = Relationship(back_populates="user")


class Developer(SQLModel, table=True):
    __tablename__ = "developers"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    inn: str = Field(unique=True, index=True)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="developer")


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    developer_id: int = Field(foreign_key="developers.id")
    name: str
    city: str
    region_code: str
    address: str
    description: Optional[str] = None
    class_type: PropertyClass
    completion_date: Optional[datetime] = None
    total_apartments: Optional[int] = None
    available_apartments: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    developer: Developer = Relationship(back_populates="projects")
    buildings: List["Building"] = Relationship(back_populates="project")


class Building(SQLModel, table=True):
    __tablename__ = "buildings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    name: str
    floors: int
    completion_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    project: Project = Relationship(back_populates="buildings")
    apartments: List["Apartment"] = Relationship(back_populates="building")


class Apartment(SQLModel, table=True):
    __tablename__ = "apartments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="buildings.id")
    number: str
    floor: int
    rooms: int
    area_total: float
    area_living: Optional[float] = None
    area_kitchen: Optional[float] = None
    base_price: float
    current_price: float
    status: ApartmentStatus = Field(default=ApartmentStatus.AVAILABLE)
    balcony: bool = Field(default=False)
    loggia: bool = Field(default=False)
    parking: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    building: Building = Relationship(back_populates="apartments")
    price_history: List["PriceHistory"] = Relationship(back_populates="apartment")
    views_logs: List["ViewsLog"] = Relationship(back_populates="apartment")
    bookings: List["Booking"] = Relationship(back_populates="apartment")
    stats: Optional["ApartmentStats"] = Relationship(back_populates="apartment")


class PriceHistory(SQLModel, table=True):
    __tablename__ = "price_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int = Field(foreign_key="apartments.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    old_price: float
    new_price: float
    reason: PriceChangeReason
    description: Optional[str] = None
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="price_history")


class ViewsLog(SQLModel, table=True):
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
    views_24h: int = Field(default=0)
    leads_24h: int = Field(default=0)
    bookings_24h: int = Field(default=0)
    days_on_site: int = Field(default=0)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="stats")


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int = Field(foreign_key="apartments.id")
    user_id: int = Field(foreign_key="users.id")
    status: BookingStatus = Field(default=BookingStatus.ACTIVE)
    booked_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    apartment: Apartment = Relationship(back_populates="bookings")
    user: User = Relationship(back_populates="bookings")


class Promotion(SQLModel, table=True):
    __tablename__ = "promotions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    discount_percent: float
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[str] = None  # JSONB as string
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WebhookInbox(SQLModel, table=True):
    __tablename__ = "webhook_inbox"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    payload: str  # JSONB as string
    received_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)


class DynamicPricingConfig(SQLModel, table=True):
    __tablename__ = "dynamic_pricing_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    k1: float = Field(default=0.5)  # views coefficient
    k2: float = Field(default=2.0)  # leads coefficient
    k3: float = Field(default=5.0)  # bookings coefficient
    enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow) 