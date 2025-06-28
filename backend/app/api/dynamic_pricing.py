from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Apartment, DynamicPricingConfig, PriceHistory, PriceChangeReason, User
from app.schemas import (
    DynamicPricingConfigResponse, DynamicPricingConfigCreate, DynamicPricingConfigUpdate,
    PriceHistoryResponse
)
from app.crud import CRUDApartment, CRUDDynamicPricingConfig, CRUDPriceHistory
from app.security import get_current_active_user, get_current_business
from datetime import datetime, timedelta

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic-pricing"])

apartment_crud = CRUDApartment(Apartment)
pricing_config_crud = CRUDDynamicPricingConfig(DynamicPricingConfig)
price_history_crud = CRUDPriceHistory(PriceHistory)


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
    db_config = await pricing_config_crud.get(db, config_id)
    if not db_config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return await pricing_config_crud.update(db, db_config, config_data.dict(exclude_unset=True))


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
    if not await pricing_config_crud.delete(db, config_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    return {"message": "Configuration deleted"}


@router.post("/apartments/{apartment_id}/price", responses={
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
        "description": "Квартира не найдена",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Apartment not found"
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
async def update_apartment_price(
    apartment_id: int,
    new_price: float,
    reason: PriceChangeReason,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить цену квартиры
    
    Args:
        apartment_id: ID квартиры
        new_price: Новая цена
        reason: Причина изменения цены
        
    Returns:
        dict: Сообщение об успешном обновлении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Квартира не найдена
        400: Bad Request - Некорректные данные
    """
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