# Пустой файл для обозначения пакета api 

from app.api.apartments import router as apartments
from app.api.developers import router as developers
from app.api.projects import router as projects
from app.api.dynamic_pricing import router as dynamic_pricing
from app.api.users import router as users
from app.api.bookings import router as bookings
from app.api.promotions import router as promotions
from app.api.analytics import router as analytics
from app.api.map import router as map
from app.api.ai_matching import router as ai_matching
from app.api.webhooks import router as webhooks

__all__ = [
    "apartments",
    "developers",
    "projects",
    "dynamic_pricing",
    "users",
    "bookings",
    "promotions",
    "analytics",
    "map",
    "ai_matching",
    "webhooks"
] 