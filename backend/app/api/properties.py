from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_property
from app.schemas import PropertyCreate, PropertyUpdate, PropertyResponse, PropertyFullResponse, PropertySearchParams
from app.security import get_current_user
from app.models import User, PropertyType, PropertyCategory, PropertyStatus

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/", response_model=List[PropertyResponse])
async def get_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_type: Optional[PropertyType] = None,
    category: Optional[PropertyCategory] = None,
    status: Optional[PropertyStatus] = None,
    building_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    developer_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список объектов недвижимости с фильтрацией
    """
    try:
        properties = await crud_property.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if property_type:
            properties = [p for p in properties if p.property_type == property_type]
        if category:
            properties = [p for p in properties if p.category == category]
        if status:
            properties = [p for p in properties if p.status == status]
        if building_id:
            properties = [p for p in properties if p.building_id == building_id]
        if project_id:
            properties = [p for p in properties if p.project_id == project_id]
        if developer_id:
            properties = [p for p in properties if p.developer_id == developer_id]
        
        return properties
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении объектов недвижимости: {str(e)}"
        )


@router.get("/search", response_model=List[PropertyResponse])
async def search_properties(
    params: PropertySearchParams = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Поиск объектов недвижимости по параметрам
    """
    try:
        # Базовый запрос
        properties = await crud_property.get_multi(db, skip=params.offset, limit=params.limit)
        
        # Применяем фильтры
        if params.property_type:
            properties = [p for p in properties if p.property_type == params.property_type]
        if params.category:
            properties = [p for p in properties if p.category == params.category]
        if params.status:
            properties = [p for p in properties if p.status == params.status]
        if params.developer_id:
            properties = [p for p in properties if p.developer_id == params.developer_id]
        if params.project_id:
            properties = [p for p in properties if p.project_id == params.project_id]
        
        return properties
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при поиске объектов: {str(e)}"
        )


@router.get("/{property_id}", response_model=PropertyFullResponse)
async def get_property(
    property_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить полную информацию об объекте недвижимости
    """
    try:
        property_obj = await crud_property.get_with_relations(db, property_id)
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Объект недвижимости не найден"
            )
        return property_obj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении объекта: {str(e)}"
        )


@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
async def create_property(
    property_data: PropertyCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать новый объект недвижимости
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания объекта недвижимости"
            )
        
        property_obj = await crud_property.create(db, property_data.dict())
        return property_obj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании объекта: {str(e)}"
        )


@router.put("/{property_id}", response_model=PropertyResponse)
async def update_property(
    property_id: UUID,
    property_data: PropertyUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить объект недвижимости
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления объекта недвижимости"
            )
        
        property_obj = await crud_property.get(db, property_id)
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Объект недвижимости не найден"
            )
        
        updated_property = await crud_property.update(db, property_obj, property_data.dict(exclude_unset=True))
        return updated_property
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении объекта: {str(e)}"
        )


@router.delete("/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_property(
    property_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить объект недвижимости
    """
    try:
        # Проверяем права доступа
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления объекта недвижимости"
            )
        
        property_obj = await crud_property.get(db, property_id)
        if not property_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Объект недвижимости не найден"
            )
        
        await crud_property.delete(db, property_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении объекта: {str(e)}"
        ) 