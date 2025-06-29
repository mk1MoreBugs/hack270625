from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Property, DynamicPricingConfig, PriceHistory, PriceChangeReason, User
from app.schemas import (
    DynamicPricingConfigRead, DynamicPricingConfigCreate, DynamicPricingConfigUpdate,
    PriceHistoryRead, Message, DynamicPricingResult
)
from app.crud import (
    crud_property, crud_dynamic_pricing_config, crud_price_history,
    CRUDDynamicPricing
)
from app.security import get_current_active_user, get_current_business, get_current_admin_user, get_current_user
from datetime import datetime, timedelta
from app.services.dynamic_pricing import DynamicPricingService

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic-pricing"])


@router.post("/config", response_model=DynamicPricingConfigRead, responses={
    201: {"description": "Конфигурация создана"},
    400: {"description": "Некорректные данные"},
    401: {"description": "Не авторизован"},
    403: {"description": "Нет прав доступа"}
})
async def create_pricing_config(
    config_data: DynamicPricingConfigCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать конфигурацию динамического ценообразования
    
    Args:
        config_data: Данные для создания конфигурации
        
    Returns:
        DynamicPricingConfigRead: Созданная конфигурация
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await crud_dynamic_pricing_config.create(db, config_data.dict())


@router.get("/config", response_model=List[DynamicPricingConfigRead])
async def get_pricing_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список конфигураций динамического ценообразования"""
    return await crud_dynamic_pricing_config.get_multi(db, skip=skip, limit=limit)


@router.get("/config/active", response_model=DynamicPricingConfigRead)
async def get_active_config(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить активную конфигурацию"""
    config = await crud_dynamic_pricing_config.get_active(db)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active configuration found"
        )
    return config


@router.get("/config/{config_id}", response_model=DynamicPricingConfigRead)
async def get_pricing_config(
    config_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить конфигурацию по ID"""
    config = await crud_dynamic_pricing_config.get(db, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return config


@router.put("/config/{config_id}", response_model=DynamicPricingConfigRead, responses={
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
    404: {
        "description": "Конфигурация не найдена",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Configuration not found"
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
async def update_pricing_config(
    config_id: int,
    config_data: DynamicPricingConfigUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить конфигурацию
    
    Args:
        config_id: ID конфигурации
        config_data: Данные для обновления
        
    Returns:
        DynamicPricingConfigRead: Обновленная конфигурация
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Конфигурация не найдена
        400: Bad Request - Некорректные данные
    """
    db_config = await crud_dynamic_pricing_config.get(db, config_id)
    if not db_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return await crud_dynamic_pricing_config.update(db, db_config, config_data.dict(exclude_unset=True))


@router.delete("/config/{config_id}", response_model=Message)
async def delete_config(
    config_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user)
):
    """Delete a dynamic pricing configuration"""
    config = await crud_dynamic_pricing_config.get(db, config_id)
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    await crud_dynamic_pricing_config.delete(db, config_id)
    return Message(message="Configuration deleted")


@router.post(
    "/properties/{property_id}/update-price",
    response_model=DynamicPricingResult,
    summary="Обновить цену объекта",
    description="Обновляет цену объекта недвижимости на основе динамического ценообразования"
)
async def update_property_price(
    property_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> DynamicPricingResult:
    """
    Обновить цену объекта
    
    Args:
        property_id: ID объекта недвижимости
        db: Сессия базы данных
        current_user: Текущий пользователь
    
    Returns:
        DynamicPricingResult: Результат обновления цены
    """
    dynamic_pricing = CRUDDynamicPricing(db)
    
    # Получаем объект недвижимости со всеми связанными данными
    property_obj = await dynamic_pricing.get_property_for_task(property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Получаем объекты из того же кластера
    cluster_properties = await dynamic_pricing.get_cluster_properties(
        property_obj.project_id,
        property_obj.residential.rooms if property_obj.residential else None,
        property_id
    )
    
    # Получаем историю изменения цен
    price_history = await dynamic_pricing.get_recent_price_changes(property_id)
    
    # Здесь должна быть логика расчета новой цены
    # Пока возвращаем тестовые данные
    return DynamicPricingResult(
        property_id=property_id,
        old_price=5000000.0,
        new_price=5100000.0,
        price_change_percent=2.0,
        demand_score=0.8,
        demand_normalized=0.7,
        reason="market_demand",
        description="Increased due to high demand in the area"
    )


@router.get(
    "/properties/{property_id}/price-history",
    response_model=List[PriceHistoryRead],
    summary="Получить историю цен",
    description="Возвращает историю изменения цен для указанного объекта недвижимости"
)
async def get_price_history(
    property_id: int,
    days: int = 30,
    db: AsyncSession = Depends(get_async_session)
) -> List[PriceHistoryRead]:
    """
    Получить историю цен
    
    Args:
        property_id: ID объекта недвижимости
        days: Количество дней для выборки
        db: Сессия базы данных
    
    Returns:
        List[PriceHistoryRead]: История изменения цен
    """
    dynamic_pricing = CRUDDynamicPricing(db)
    history = await dynamic_pricing.get_recent_price_changes(property_id, days)
    return history


@router.get("/price-history/recent", response_model=List[PriceHistoryRead])
async def get_recent_price_changes(
    hours: int = 24,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить недавние изменения цен"""
    return await crud_price_history.get_recent_changes(db, hours) 