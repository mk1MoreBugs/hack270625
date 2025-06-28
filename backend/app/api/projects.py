from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Project, Building, Apartment, PropertyClass
from app.schemas import (
    ProjectResponse, ProjectCreate, ProjectUpdate,
    BuildingResponse, BuildingCreate, BuildingUpdate,
    ApartmentResponse
)
from app.crud import CRUDProject, CRUDBuilding, CRUDApartment

router = APIRouter(prefix="/projects", tags=["projects"])

project_crud = CRUDProject(Project)
building_crud = CRUDBuilding(Building)
apartment_crud = CRUDApartment(Apartment)


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новый проект"""
    return await project_crud.create(db, project_data.dict())


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    city: Optional[str] = None,
    property_class: Optional[PropertyClass] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список проектов"""
    if city:
        return await project_crud.get_by_city(db, city)
    elif property_class:
        return await project_crud.get_by_class(db, property_class)
    return await project_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить проект по ID"""
    db_project = await project_crud.get(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить проект"""
    db_project = await project_crud.get(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return await project_crud.update(db, db_project, project_data.dict(exclude_unset=True))


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить проект"""
    if not await project_crud.delete(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"message": "Project deleted"}


@router.post("/{project_id}/buildings", response_model=BuildingResponse)
async def create_building(
    project_id: int,
    building_data: BuildingCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новый корпус в проекте"""
    # Проверяем существование проекта
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    building_dict = building_data.dict()
    building_dict["project_id"] = project_id
    return await building_crud.create(db, building_dict)


@router.get("/{project_id}/buildings", response_model=List[BuildingResponse])
async def get_project_buildings(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список корпусов проекта"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return await building_crud.get_by_project(db, project_id)


@router.get("/{project_id}/buildings/{building_id}", response_model=BuildingResponse)
async def get_building(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить корпус по ID"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return db_building


@router.put("/{project_id}/buildings/{building_id}", response_model=BuildingResponse)
async def update_building(
    project_id: int,
    building_id: int,
    building_data: BuildingUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить корпус"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return await building_crud.update(db, db_building, building_data.dict(exclude_unset=True))


@router.delete("/{project_id}/buildings/{building_id}")
async def delete_building(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить корпус"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    await building_crud.delete(db, building_id)
    return {"message": "Building deleted"}


@router.get("/{project_id}/buildings/{building_id}/apartments", response_model=List[ApartmentResponse])
async def get_building_apartments(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список квартир в корпусе"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    return await apartment_crud.get_by_building(db, building_id) 