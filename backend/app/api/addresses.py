from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_property_address
from app.schemas import PropertyAddressCreate, PropertyAddressUpdate, PropertyAddressResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("/", response_model=List[PropertyAddressResponse])
async def get_addresses(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_id: Optional[UUID] = None,
    city: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список адресов с фильтрацией
    """
    try:
        addresses = await crud_property_address.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if property_id:
            addresses = [a for a in addresses if a.property_id == property_id]
        if city:
            addresses = [a for a in addresses if city.lower() in a.city.lower()]
        
        return addresses
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении адресов: {str(e)}"
        )


@router.get("/{address_id}", response_model=PropertyAddressResponse)
async def get_address(
    address_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию об адресе
    """
    try:
        address = await crud_property_address.get(db, address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден"
            )
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении адреса: {str(e)}"
        )


@router.post("/", response_model=PropertyAddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(
    address_data: PropertyAddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать новый адрес
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания адреса"
            )
        
        address = await crud_property_address.create(db, address_data.dict())
        return address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании адреса: {str(e)}"
        )


@router.put("/{address_id}", response_model=PropertyAddressResponse)
async def update_address(
    address_id: UUID,
    address_data: PropertyAddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить адрес
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления адреса"
            )
        
        address = await crud_property_address.get(db, address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден"
            )
        
        updated_address = await crud_property_address.update(db, address, address_data.dict(exclude_unset=True))
        return updated_address
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении адреса: {str(e)}"
        )


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(
    address_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить адрес
    """
    try:
        # Проверяем права доступа
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления адреса"
            )
        
        address = await crud_property_address.get(db, address_id)
        if not address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Адрес не найден"
            )
        
        await crud_property_address.delete(db, address_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении адреса: {str(e)}"
        ) 