from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_building
from app.schemas import BuildingCreate, BuildingUpdate, BuildingResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[BuildingResponse])
async def get_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    project_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список зданий с фильтрацией
    """
    try:
        buildings = await crud_building.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if project_id:
            buildings = [b for b in buildings if b.project_id == project_id]
        
        return buildings
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении зданий: {str(e)}"
        )


@router.get("/{building_id}", response_model=BuildingResponse)
async def get_building(
    building_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию о здании
    """
    try:
        building = await crud_building.get(db, building_id)
        if not building:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Здание не найдено"
            )
        return building
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении здания: {str(e)}"
        )


@router.post("/", response_model=BuildingResponse, status_code=status.HTTP_201_CREATED)
async def create_building(
    building_data: BuildingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать новое здание
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания здания"
            )
        
        building = await crud_building.create(db, building_data.dict())
        return building
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании здания: {str(e)}"
        )


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: UUID,
    building_data: BuildingUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить здание
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления здания"
            )
        
        building = await crud_building.get(db, building_id)
        if not building:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Здание не найдено"
            )
        
        updated_building = await crud_building.update(db, building, building_data.dict(exclude_unset=True))
        return updated_building
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении здания: {str(e)}"
        )


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_building(
    building_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить здание
    """
    try:
        # Проверяем права доступа
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления здания"
            )
        
        building = await crud_building.get(db, building_id)
        if not building:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Здание не найдено"
            )
        
        await crud_building.delete(db, building_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении здания: {str(e)}"
        ) 