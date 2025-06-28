from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Promotion, User
from app.schemas import PromotionResponse, PromotionCreate, PromotionUpdate
from app.crud import CRUDPromotion
from app.security import get_current_active_user, get_current_business
from datetime import datetime

router = APIRouter(prefix="/promotions", tags=["promotions"])
promotion_crud = CRUDPromotion(Promotion)


@router.post("", response_model=PromotionResponse, responses={
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
async def create_promotion(
    promotion_data: PromotionCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать новую акцию
    
    Args:
        promotion_data: Данные для создания акции
        
    Returns:
        PromotionResponse: Созданная акция
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
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


@router.put("/{promotion_id}", response_model=PromotionResponse, responses={
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
        "description": "Акция не найдена",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Promotion not found"
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
async def update_promotion(
    promotion_id: int,
    promotion_data: PromotionUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить акцию
    
    Args:
        promotion_id: ID акции
        promotion_data: Данные для обновления
        
    Returns:
        PromotionResponse: Обновленная акция
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Акция не найдена
        400: Bad Request - Некорректные данные
    """
    db_promotion = await promotion_crud.get(db, promotion_id)
    if not db_promotion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found"
        )
    return await promotion_crud.update(db, db_promotion, promotion_data.dict(exclude_unset=True))


@router.delete("/{promotion_id}", responses={
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
        "description": "Акция не найдена",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Promotion not found"
                }
            }
        }
    },
    200: {
        "description": "Акция успешно удалена",
        "content": {
            "application/json": {
                "example": {
                    "message": "Promotion deleted"
                }
            }
        }
    }
})
async def delete_promotion(
    promotion_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить акцию
    
    Args:
        promotion_id: ID акции
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Акция не найдена
    """
    if not await promotion_crud.delete(db, promotion_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promotion not found"
        )
    return {"message": "Promotion deleted"} 