from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.schemas import ApartmentResponse, ApartmentMatchRequest
from app.services.ai_matching import ApartmentMatchingService
from app.models import User
from app.security import get_current_active_user

router = APIRouter(prefix="/ai-matching", tags=["ai-matching"])


async def get_matching_service(db: AsyncSession = Depends(get_async_session)) -> ApartmentMatchingService:
    """Фабрика для создания сервиса подбора квартир"""
    return ApartmentMatchingService(db)


@router.post("/apartments", response_model=List[ApartmentResponse], responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
async def match_apartments_for_user(
    match_request: ApartmentMatchRequest,
    limit: int = Query(10, description="Количество рекомендаций"),
    matching_service: ApartmentMatchingService = Depends(get_matching_service),
    current_user: User = Depends(get_current_active_user)
):
    """
    ИИ-подбор квартир по предпочтениям пользователя
    
    Args:
        match_request: Параметры для подбора квартир
        limit: Количество рекомендаций
        
    Returns:
        List[ApartmentResponse]: Список подобранных квартир
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    matched_apartments = await matching_service.match_apartments(
        budget=match_request.budget,
        preferred_cities=match_request.preferred_cities,
        preferred_districts=match_request.preferred_districts,
        min_rooms=match_request.min_rooms,
        max_rooms=match_request.max_rooms,
        min_area=match_request.min_area,
        max_area=match_request.max_area,
        property_class=match_request.property_class,
        has_balcony=match_request.has_balcony,
        has_parking=match_request.has_parking,
        max_floor=match_request.max_floor,
        limit=limit
    )
    return matched_apartments 