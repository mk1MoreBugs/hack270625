from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Promotion
from app.schemas import PromotionResponse, PromotionCreate, PromotionUpdate
from app.crud import CRUDPromotion
from datetime import datetime

router = APIRouter(prefix="/promotions", tags=["promotions"])
promotion_crud = CRUDPromotion(Promotion)


@router.post("", response_model=PromotionResponse)
async def create_promotion(
    promotion_data: PromotionCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новую акцию"""
    return await promotion_crud.create(db, promotion_data.dict())


@router.get("", response_model=List[PromotionResponse])
async def get_promotions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список акций"""
    return await promotion_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/active", response_model=List[PromotionResponse])
async def get_active_promotions(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список активных акций"""
    return await promotion_crud.get_active(db, datetime.utcnow())


@router.get("/{promotion_id}", response_model=PromotionResponse)
async def get_promotion(
    promotion_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить акцию по ID"""
    db_promotion = await promotion_crud.get(db, promotion_id)
    if not db_promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found"
        )
    return db_promotion


@router.put("/{promotion_id}", response_model=PromotionResponse)
async def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить акцию"""
    db_promotion = await promotion_crud.get(db, promotion_id)
    if not db_promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found"
        )
    return await promotion_crud.update(db, db_promotion, promotion_data.dict(exclude_unset=True))


@router.delete("/{promotion_id}")
async def delete_promotion(
    promotion_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить акцию"""
    if not await promotion_crud.delete(db, promotion_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found"
        )
    return {"message": "Promotion deleted"} 