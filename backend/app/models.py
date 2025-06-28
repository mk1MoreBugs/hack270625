from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import json
from sqlalchemy import JSON


class UserRole(str, Enum):
    BUYER = "buyer"
    DEVELOPER = "developer"
    ADMIN = "admin"


class PropertyType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"


class PropertyCategory(str, Enum):
    FLAT_NEW = "flat_new"
    FLAT_SECONDARY = "flat_secondary"
    ROOM = "room"
    HOUSE = "house"
    TOWNHOUSE = "townhouse"
    PART_OF_HOUSE = "part_of_house"
    LAND_PLOT = "land_plot"
    GARAGE = "garage"
    OFFICE = "office"
    RETAIL = "retail"
    WAREHOUSE = "warehouse"


class PropertyStatus(str, Enum):
    AVAILABLE = "available"
    BOOKED = "booked"
    SOLD = "sold"
    ARCHIVED = "archived"


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


class FinishingType(str, Enum):
    NO_FINISHING = "без_отделки"
    PRE_FINISHING = "предчистовая"
    FINISHING = "чистовая"
    DESIGNER = "дизайнерская"
    WHITE_BOX = "white_box"
    TURNKEY = "под_ключ"


class ParkingType(str, Enum):
    NONE = "отсутствует"
    GROUND = "наземная"
    MULTILEVEL = "многоуровневая"
    UNDERGROUND = "подземный_паркинг"
    YARD = "во_дворе"


class ViewType(str, Enum):
    CITY = "город"
    PARK = "парк"
    RIVER = "река"
    YARD = "двор"
    MIXED = "смешанный"
    SEA = "море"
    MOUNTAINS = "горы"
    FOREST = "лес"


class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    display_name: str
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
    name: str = Field(index=True)
    description: Optional[str] = None
    founding_year: Optional[int] = None
    website: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    projects_count: Optional[int] = Field(default=0)
    
    # Relationships
    projects: List["Project"] = Relationship(back_populates="developer")
    properties: List["Property"] = Relationship(back_populates="developer")


class Project(SQLModel, table=True):
    __tablename__ = "projects"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    developer_id: Optional[int] = Field(default=None, foreign_key="developers.id")
    description: Optional[str] = None
    start_date: Optional[date] = None
    completion_date: Optional[date] = None
    status: str = Field(default="active")  # active, completed, frozen
    total_area: Optional[float] = None
    total_units: Optional[int] = None
    
    # Relationships
    developer: Optional[Developer] = Relationship(back_populates="projects")
    buildings: List["Building"] = Relationship(back_populates="project")
    properties: List["Property"] = Relationship(back_populates="project")


class Building(SQLModel, table=True):
    __tablename__ = "buildings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    number: Optional[str] = None
    floors_total: Optional[int] = Field(default=None, ge=1, le=100)
    completion_date: Optional[date] = None
    status: str = Field(default="under_construction")  # under_construction, completed
    total_units: Optional[int] = None
    available_units: Optional[int] = None
    
    # Relationships
    project: Optional[Project] = Relationship(back_populates="buildings")
    properties: List["Property"] = Relationship(back_populates="building")


class Property(SQLModel, table=True):
    __tablename__ = "properties"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    external_id: Optional[str] = Field(default=None, max_length=50, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    property_type: PropertyType
    category: PropertyCategory
    developer_id: Optional[int] = Field(default=None, foreign_key="developers.id")
    project_id: Optional[int] = Field(default=None, foreign_key="projects.id")
    building_id: Optional[int] = Field(default=None, foreign_key="buildings.id")
    status: PropertyStatus = Field(default=PropertyStatus.AVAILABLE)
    has_3d_tour: bool = Field(default=False)
    
    # Relationships
    developer: Optional[Developer] = Relationship(back_populates="properties")
    project: Optional[Project] = Relationship(back_populates="properties")
    building: Optional[Building] = Relationship(back_populates="properties")
    address: Optional["PropertyAddress"] = Relationship(back_populates="property")
    price: Optional["PropertyPrice"] = Relationship(back_populates="property")
    residential: Optional["ResidentialProperty"] = Relationship(back_populates="property")
    features: Optional["PropertyFeatures"] = Relationship(back_populates="property")
    analytics: Optional["PropertyAnalytics"] = Relationship(back_populates="property")
    commercial: Optional["CommercialProperty"] = Relationship(back_populates="property")
    house_land: Optional["HouseAndLand"] = Relationship(back_populates="property")
    media: List["PropertyMedia"] = Relationship(back_populates="property")
    promo_tags: List["PromoTag"] = Relationship(back_populates="property")
    mortgage_programs: List["MortgageProgram"] = Relationship(back_populates="property")
    price_history: List["PriceHistory"] = Relationship(back_populates="property")
    views_logs: List["ViewsLog"] = Relationship(back_populates="property")
    bookings: List["Booking"] = Relationship(back_populates="property")


class PropertyAddress(SQLModel, table=True):
    __tablename__ = "property_addresses"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    address_full: str
    city: str = Field(max_length=50, index=True)
    region: str = Field(max_length=50, index=True)
    district: Optional[str] = Field(default=None, max_length=50, index=True)
    lat: float = Field(ge=-90, le=90)
    lng: float = Field(ge=-180, le=180)
    postal_code: Optional[str] = None
    
    # Relationships
    property: Property = Relationship(back_populates="address")


class PropertyPrice(SQLModel, table=True):
    __tablename__ = "property_prices"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    base_price: float = Field(ge=0)
    current_price: float = Field(ge=0)
    currency: str = Field(default="RUB", max_length=3)
    price_per_m2: Optional[float] = Field(default=None, ge=0)
    original_price: Optional[float] = Field(default=None, ge=0)  # Price before any discounts
    discount_amount: Optional[float] = Field(default=None, ge=0)
    discount_percent: Optional[float] = Field(default=None, ge=0, le=100)
    
    # Relationships
    property: Property = Relationship(back_populates="price")


class ResidentialProperty(SQLModel, table=True):
    __tablename__ = "residential_properties"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    unit_number: Optional[str] = Field(default=None, max_length=20)
    floor: Optional[int] = Field(default=None, ge=1, le=100)
    floors_total: Optional[int] = Field(default=None, ge=1, le=100)
    rooms: Optional[int] = Field(default=None, ge=0, le=10)
    is_studio: bool = Field(default=False)
    is_free_plan: bool = Field(default=False)
    total_area: Optional[float] = Field(default=None, ge=0)
    living_area: Optional[float] = Field(default=None, ge=0)
    kitchen_area: Optional[float] = Field(default=None, ge=0)
    ceiling_height: Optional[float] = Field(default=None, ge=0)
    completion_date: Optional[datetime] = Field(default=None)
    
    # Relationships
    property: Property = Relationship(back_populates="residential")


class PropertyFeatures(SQLModel, table=True):
    __tablename__ = "property_features"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    balcony: bool = Field(default=False)
    loggia: bool = Field(default=False)
    terrace: bool = Field(default=False)
    view: Optional[ViewType] = None
    finishing: Optional[FinishingType] = None
    parking_type: Optional[ParkingType] = None
    parking_price: Optional[float] = Field(default=None, ge=0)
    has_furniture: Optional[bool] = Field(default=False)
    has_appliances: Optional[bool] = Field(default=False)
    
    # Relationships
    property: Property = Relationship(back_populates="features")


class PropertyAnalytics(SQLModel, table=True):
    __tablename__ = "property_analytics"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    days_on_market: Optional[int] = Field(default=None, ge=0)
    rli_index: Optional[float] = Field(default=None, ge=0, le=1)
    demand_score: Optional[int] = Field(default=None, ge=0, le=100)
    clicks_total: Optional[int] = Field(default=None, ge=0)
    favourites_total: Optional[int] = Field(default=None, ge=0)
    bookings_total: Optional[int] = Field(default=None, ge=0)
    views_last_week: Optional[int] = Field(default=None, ge=0)
    views_last_month: Optional[int] = Field(default=None, ge=0)
    price_trend: Optional[float] = Field(default=None)  # Percentage change
    
    # Relationships
    property: Property = Relationship(back_populates="analytics")


class CommercialProperty(SQLModel, table=True):
    __tablename__ = "commercial_properties"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    commercial_subtype: Optional[PropertyCategory] = Field(default=None)
    open_space: Optional[bool] = Field(default=None)
    has_showcase_windows: Optional[bool] = Field(default=None)
    allowed_activity: Optional[str] = Field(default=None, max_length=50)
    tax_rate: Optional[float] = Field(default=None, ge=0, le=100)
    maintenance_fee: Optional[float] = Field(default=None, ge=0)
    tenant_business_type: Optional[str] = None
    separate_entrance: Optional[bool] = Field(default=None)
    
    # Relationships
    property: Property = Relationship(back_populates="commercial")


class HouseAndLand(SQLModel, table=True):
    __tablename__ = "houses_and_lands"
    
    property_id: int = Field(primary_key=True, foreign_key="properties.id")
    land_area: Optional[float] = Field(default=None, ge=0)
    floors_in_house: Optional[int] = Field(default=None, ge=1, le=10)
    house_material: Optional[str] = Field(default=None, max_length=20)
    year_built: Optional[int] = Field(default=None)
    has_fence: Optional[bool] = Field(default=None)
    garage_on_plot: Optional[bool] = Field(default=None)
    bathhouse_on_plot: Optional[bool] = Field(default=None)
    electricity: Optional[bool] = Field(default=None)
    water_supply: Optional[bool] = Field(default=None)
    gas_supply: Optional[bool] = Field(default=None)
    sewage: Optional[bool] = Field(default=None)
    
    # Relationships
    property: Property = Relationship(back_populates="house_land")


class PropertyMedia(SQLModel, table=True):
    __tablename__ = "property_media"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    layout_image_url: Optional[str] = Field(default=None)
    vr_tour_url: Optional[str] = Field(default=None)
    video_url: Optional[str] = Field(default=None)
    main_photo_url: Optional[str] = Field(default=None)
    photo_urls: Optional[List[str]] = Field(default=None, sa_type=JSON)  # Store as JSON array
    
    # Relationships
    property: Property = Relationship(back_populates="media")


class PromoTag(SQLModel, table=True):
    __tablename__ = "promo_tags"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    tag: str = Field(max_length=50)
    active: bool = Field(default=True)
    expires_at: Optional[datetime] = None
    
    # Relationships
    property: Property = Relationship(back_populates="promo_tags")


class MortgageProgram(SQLModel, table=True):
    __tablename__ = "mortgage_programs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    name: str
    bank_name: str
    interest_rate: float = Field(ge=0, le=30)
    down_payment_percent: float = Field(ge=0, le=100)
    term_years: int = Field(ge=1, le=30)
    monthly_payment: Optional[float] = None
    requirements: Optional[str] = None  # JSON string
    
    # Relationships
    property: Property = Relationship(back_populates="mortgage_programs")


class PriceHistory(SQLModel, table=True):
    __tablename__ = "price_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    changed_at: datetime = Field(default_factory=datetime.utcnow)
    old_price: float = Field(ge=0)
    new_price: float = Field(ge=0)
    reason: PriceChangeReason
    description: Optional[str] = Field(default=None)
    
    # Relationships
    property: Property = Relationship(back_populates="price_history")


class ViewsLog(SQLModel, table=True):
    __tablename__ = "views_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    event: ViewEvent
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    source: Optional[str] = None  # web, mobile_app, etc.
    session_id: Optional[str] = None
    
    # Relationships
    property: Property = Relationship(back_populates="views_logs")
    user: Optional[User] = Relationship(back_populates="views_logs")


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    property_id: int = Field(foreign_key="properties.id")
    user_id: int = Field(foreign_key="users.id")
    status: BookingStatus = Field(default=BookingStatus.ACTIVE)
    booked_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    payment_status: Optional[str] = None
    booking_fee: Optional[float] = None
    
    # Relationships
    property: Property = Relationship(back_populates="bookings")
    user: User = Relationship(back_populates="bookings")


class Promotion(SQLModel, table=True):
    __tablename__ = "promotions"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    discount_percent: float = Field(ge=0, le=100)
    starts_at: datetime
    ends_at: datetime
    conditions: Optional[str] = Field(default=None)  # JSONB as string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    max_uses: Optional[int] = None
    current_uses: Optional[int] = Field(default=0)


class WebhookInbox(SQLModel, table=True):
    __tablename__ = "webhook_inbox"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    payload: str  # JSONB as string
    received_at: datetime = Field(default_factory=datetime.utcnow)
    processed: bool = Field(default=False)
    error_message: Optional[str] = None
    retry_count: int = Field(default=0)


class DynamicPricingConfig(SQLModel, table=True):
    __tablename__ = "dynamic_pricing_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    k1: float = Field(default=0.5)  # views coefficient
    k2: float = Field(default=2.0)  # leads coefficient
    k3: float = Field(default=5.0)  # bookings coefficient
    enabled: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    min_price_change: float = Field(default=-5.0)  # Maximum price decrease in percent
    max_price_change: float = Field(default=5.0)  # Maximum price increase in percent
    update_interval_hours: int = Field(default=24) 