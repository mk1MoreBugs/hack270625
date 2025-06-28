from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Apartment, DynamicPricingConfig, PriceHistory, PriceChangeReason
from app.schemas import (
    DynamicPricingConfigResponse, DynamicPricingConfigCreate, DynamicPricingConfigUpdate,
    PriceHistoryResponse
)
from app.crud import CRUDApartment, CRUDDynamicPricingConfig, CRUDPriceHistory
from datetime import datetime, timedelta

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic-pricing"])

apartment_crud = CRUDApartment(Apartment)
pricing_config_crud = CRUDDynamicPricingConfig(DynamicPricingConfig)
price_history_crud = CRUDPriceHistory(PriceHistory)


@router.post("/config", response_model=DynamicPricingConfigResponse)
async def create_pricing_config(
    config_data: DynamicPricingConfigCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать конфигурацию динамического ценообразования"""
    return await pricing_config_crud.create(db, config_data.dict())


@router.get("/config", response_model=List[DynamicPricingConfigResponse])
async def get_pricing_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список конфигураций динамического ценообразования"""
    return await pricing_config_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/config/active", response_model=DynamicPricingConfigResponse)
async def get_active_config(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить активную конфигурацию"""
    config = await pricing_config_crud.get_active(db)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active configuration found"
        )
    return config


@router.get("/config/{config_id}", response_model=DynamicPricingConfigResponse)
async def get_pricing_config(
    config_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить конфигурацию по ID"""
    config = await pricing_config_crud.get(db, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return config


@router.put("/config/{config_id}", response_model=DynamicPricingConfigResponse)
async def update_pricing_config(
    config_id: int,
    config_data: DynamicPricingConfigUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить конфигурацию"""
    db_config = await pricing_config_crud.get(db, config_id)
    if not db_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return await pricing_config_crud.update(db, db_config, config_data.dict(exclude_unset=True))


@router.delete("/config/{config_id}")
async def delete_pricing_config(
    config_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить конфигурацию"""
    if not await pricing_config_crud.delete(db, config_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return {"message": "Configuration deleted"}


@router.post("/apartments/{apartment_id}/price")
async def update_apartment_price(
    apartment_id: int,
    new_price: float,
    reason: PriceChangeReason,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить цену квартиры"""
    # Проверяем существование квартиры
    apartment = await apartment_crud.get(db, apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    
    # Обновляем цену
    updated_apartment = await apartment_crud.update_price(db, apartment_id, new_price)
    
    # Сохраняем историю изменения цены
    price_history_data = {
        "apartment_id": apartment_id,
        "old_price": apartment.current_price,
        "new_price": new_price,
        "change_reason": reason,
        "changed_at": datetime.utcnow()
    }
    await price_history_crud.create(db, price_history_data)
    
    return {"message": "Price updated successfully"}


@router.get("/apartments/{apartment_id}/price-history", response_model=List[PriceHistoryResponse])
async def get_apartment_price_history(
    apartment_id: int,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю изменения цен квартиры"""
    # Проверяем существование квартиры
    if not await apartment_crud.get(db, apartment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    
    return await price_history_crud.get_by_apartment(db, apartment_id, limit=limit)


@router.get("/price-history/recent", response_model=List[PriceHistoryResponse])
async def get_recent_price_changes(
    hours: int = 24,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить недавние изменения цен"""
    return await price_history_crud.get_recent_changes(db, hours=hours) 