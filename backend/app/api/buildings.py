from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import Session, select
from typing import List, Optional

from app.database import get_async_session
from app.models import Building, Project, Developer, UserRole
from app.security import get_current_user, get_current_admin_user, get_current_user_role
from app.schemas import BuildingCreate, BuildingRead, BuildingUpdate, Message, BuildingRead

router = APIRouter(
    prefix="/buildings",
    tags=["buildings"]
)


@router.get(
    "",
    response_model=List[BuildingRead],
    summary="Получить список зданий",
    description="Получение списка всех доступных зданий"
)
async def get_buildings(
    project_id: int = None,
    session: AsyncSession = Depends(get_async_session)
) -> List[BuildingRead]:
    query = select(Building)
    if project_id:
        query = query.where(Building.project_id == project_id)
    result = await session.execute(query)
    buildings = result.scalars().all()
    return [BuildingRead.from_orm(b) for b in buildings]


@router.get(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Получить здание",
    description="Получение информации о конкретном здании по его ID"
)
async def get_building(
    building_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> BuildingRead:
    building = await session.get(Building, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    return BuildingRead.from_orm(building)


@router.post(
    "",
    response_model=BuildingRead,
    summary="Создать здание",
    description="Создание нового здания в проекте (только для застройщиков)"
)
async def create_building(
    building_data: BuildingCreate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> BuildingRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут создавать здания"
        )
    
    building = Building(**building_data.dict())
    session.add(building)
    await session.commit()
    await session.refresh(building)
    return BuildingRead.from_orm(building)


@router.put(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Обновить здание",
    description="Обновление информации о здании (только для застройщиков)"
)
async def update_building(
    building_id: int,
    building_data: BuildingUpdate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> BuildingRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут обновлять здания"
        )
    
    building = await session.get(Building, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    
    for field, value in building_data.dict(exclude_unset=True).items():
        setattr(building, field, value)
    
    await session.commit()
    await session.refresh(building)
    return BuildingRead.from_orm(building)


@router.delete(
    "/{building_id}",
    response_model=Message,
    summary="Удалить здание",
    description="Удаление здания (только для застройщиков)"
)
async def delete_building(
    building_id: int,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут удалять здания"
        )
    
    building = await session.get(Building, building_id)
    if not building:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Здание не найдено"
        )
    
    await session.delete(building)
    await session.commit()
    return {"message": "Здание успешно удалено"} 