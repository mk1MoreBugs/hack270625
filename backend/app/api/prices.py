from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_property_price
from app.schemas import PropertyPriceCreate, PropertyPriceUpdate, PropertyPriceResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/", response_model=List[PropertyPriceResponse])
async def get_prices(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_id: Optional[UUID] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список цен с фильтрацией
    """
    try:
        prices = await crud_property_price.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if property_id:
            prices = [p for p in prices if p.property_id == property_id]
        if min_price:
            prices = [p for p in prices if p.current_price >= min_price]
        if max_price:
            prices = [p for p in prices if p.current_price <= max_price]
        
        return prices
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении цен: {str(e)}"
        )


@router.get("/{price_id}", response_model=PropertyPriceResponse)
async def get_price(
    price_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию о цене
    """
    try:
        price = await crud_property_price.get(db, price_id)
        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Цена не найдена"
            )
        return price
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении цены: {str(e)}"
        )


@router.post("/", response_model=PropertyPriceResponse, status_code=status.HTTP_201_CREATED)
async def create_price(
    price_data: PropertyPriceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать новую цену
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания цены"
            )
        
        price = await crud_property_price.create(db, price_data.dict())
        return price
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании цены: {str(e)}"
        )


@router.put("/{price_id}", response_model=PropertyPriceResponse)
async def update_price(
    price_id: UUID,
    price_data: PropertyPriceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить цену
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления цены"
            )
        
        price = await crud_property_price.get(db, price_id)
        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Цена не найдена"
            )
        
        updated_price = await crud_property_price.update(db, price, price_data.dict(exclude_unset=True))
        return updated_price
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении цены: {str(e)}"
        )


@router.delete("/{price_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_price(
    price_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить цену
    """
    try:
        # Проверяем права доступа
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления цены"
            )
        
        price = await crud_property_price.get(db, price_id)
        if not price:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Цена не найдена"
            )
        
        await crud_property_price.delete(db, price_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении цены: {str(e)}"
        ) 