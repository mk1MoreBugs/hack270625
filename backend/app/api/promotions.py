from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Promotion
from app.schemas import PromotionResponse, PromotionCreate, PromotionUpdate
from app.crud import promotion
from datetime import datetime

router = APIRouter(prefix="/promotions", tags=["promotions"])


@router.get("/", response_model=List[PromotionResponse])
async def get_promotions(
    active_only: bool = Query(False, description="Только активные акции"),
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список акций"""
    if active_only:
        now = datetime.utcnow()
        promotions_list = await promotion.get_active(db, now)
    else:
        promotions_list = await promotion.get_multi(db, skip=offset, limit=limit)
    
    # Применяем пагинацию
    start = offset
    end = start + limit
    return promotions_list[start:end]


@router.post("/", response_model=PromotionResponse)
async def create_promotion(
    promotion_data: PromotionCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новую акцию"""
    # Проверяем даты
    if promotion_data.ends_at <= promotion_data.starts_at:
        raise HTTPException(
            status_code=400,
            detail="Дата окончания акции должна быть позже даты начала"
        )
    
    promotion_dict = promotion_data.dict()
    promotion_obj = await promotion.create(db, promotion_dict)
    return promotion_obj


@router.get("/{promotion_id}", response_model=PromotionResponse)
async def get_promotion(
    promotion_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить информацию об акции"""
    promotion_obj = await promotion.get(db, promotion_id)
    if not promotion_obj:
        raise HTTPException(status_code=404, detail="Акция не найдена")
    return promotion_obj


@router.put("/{promotion_id}", response_model=PromotionResponse)
async def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить информацию об акции"""
    promotion_obj = await promotion.get(db, promotion_id)
    if not promotion_obj:
        raise HTTPException(status_code=404, detail="Акция не найдена")
    
    update_data = promotion_data.dict(exclude_unset=True)
    
    # Если обновляются даты, проверяем их корректность
    starts_at = update_data.get("starts_at", promotion_obj.starts_at)
    ends_at = update_data.get("ends_at", promotion_obj.ends_at)
    if ends_at <= starts_at:
        raise HTTPException(
            status_code=400,
            detail="Дата окончания акции должна быть позже даты начала"
        )
    
    promotion_obj = await promotion.update(db, promotion_obj, update_data)
    return promotion_obj


@router.delete("/{promotion_id}")
async def delete_promotion(
    promotion_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить акцию"""
    success = await promotion.delete(db, promotion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Акция не найдена")
    return {"message": "Акция удалена"} 