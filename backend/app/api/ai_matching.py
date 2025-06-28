from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.schemas import ApartmentResponse, ApartmentMatchRequest
from app.services.ai_matching import match_apartments

router = APIRouter(prefix="/ai-matching", tags=["ai-matching"])


@router.post("/apartments", response_model=List[ApartmentResponse])
async def match_apartments_for_user(
    match_request: ApartmentMatchRequest,
    limit: int = Query(10, description="Количество рекомендаций"),
    db: AsyncSession = Depends(get_async_session)
):
    """ИИ-подбор квартир по предпочтениям пользователя"""
    matched_apartments = await match_apartments(
        db,
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