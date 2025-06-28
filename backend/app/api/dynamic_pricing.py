from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.database import get_async_session
from app.models import Property, DynamicPricingConfig, PriceHistory, PriceChangeReason, User
from app.schemas import (
    DynamicPricingConfigResponse, DynamicPricingConfigCreate, DynamicPricingConfigUpdate,
    PriceHistoryResponse
)
from app.crud import crud_property, crud_dynamic_pricing_config, crud_price_history
from app.security import get_current_active_user, get_current_business
from datetime import datetime, timedelta

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic-pricing"])


@router.post("/config", response_model=DynamicPricingConfigResponse, responses={
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
        DynamicPricingConfigResponse: Созданная конфигурация
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await crud_dynamic_pricing_config.create(db, config_data.dict())


@router.get("/config", response_model=List[DynamicPricingConfigResponse])
async def get_pricing_configs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список конфигураций динамического ценообразования"""
    return await crud_dynamic_pricing_config.get_multi(db, skip=skip, limit=limit)


@router.get("/config/active", response_model=DynamicPricingConfigResponse)
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


@router.get("/config/{config_id}", response_model=DynamicPricingConfigResponse)
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


@router.put("/config/{config_id}", response_model=DynamicPricingConfigResponse, responses={
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
        DynamicPricingConfigResponse: Обновленная конфигурация
        
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


@router.delete("/config/{config_id}", responses={
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
    200: {
        "description": "Конфигурация успешно удалена",
        "content": {
            "application/json": {
                "example": {
                    "message": "Configuration deleted"
                }
            }
        }
    }
})
async def delete_pricing_config(
    config_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить конфигурацию
    
    Args:
        config_id: ID конфигурации
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Конфигурация не найдена
    """
    db_config = await crud_dynamic_pricing_config.get(db, config_id)
    if not db_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    await crud_dynamic_pricing_config.delete(db, config_id)
    return {"message": "Configuration deleted"}


@router.post("/properties/{property_id}/price", responses={
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
        "description": "Объект недвижимости не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property not found"
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
    },
    200: {
        "description": "Цена успешно обновлена",
        "content": {
            "application/json": {
                "example": {
                    "message": "Price updated successfully"
                }
            }
        }
    }
})
async def update_property_price(
    property_id: UUID,
    new_price: float,
    reason: PriceChangeReason,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить цену объекта недвижимости
    
    Args:
        property_id: ID объекта недвижимости
        new_price: Новая цена
        reason: Причина изменения цены
        
    Returns:
        dict: Сообщение об успешном обновлении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Объект недвижимости не найден
        400: Bad Request - Некорректные данные
    """
    # Проверяем существование объекта недвижимости
    property_obj = await crud_property.get(db, property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Обновляем цену
    updated_price = await crud_property_price.update_price(db, property_id, new_price)
    if not updated_price:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update price"
        )
    
    return {"message": "Price updated successfully"}


@router.get("/properties/{property_id}/price-history", response_model=List[PriceHistoryResponse])
async def get_property_price_history(
    property_id: UUID,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю цен объекта недвижимости"""
    return await crud_price_history.get_by_property(db, property_id, limit)


@router.get("/price-history/recent", response_model=List[PriceHistoryResponse])
async def get_recent_price_changes(
    hours: int = 24,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить недавние изменения цен"""
    return await crud_price_history.get_recent_changes(db, hours) 