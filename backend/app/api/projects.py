from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Project, Building, Apartment
from app.schemas import (
    ProjectResponse, ProjectCreate, ProjectUpdate,
    BuildingResponse, BuildingCreate, BuildingUpdate,
    ApartmentResponse
)
from app.crud import project, building, apartment
from datetime import datetime

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    city: Optional[str] = Query(None, description="Город"),
    region_code: Optional[str] = Query(None, description="Код региона"),
    property_class: Optional[str] = Query(None, description="Класс недвижимости"),
    developer_id: Optional[int] = Query(None, description="ID застройщика"),
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список проектов"""
    projects_list = await project.get_multi(db, skip=offset, limit=limit)
    
    # Применяем фильтры
    filtered_projects = []
    for proj in projects_list:
        # Фильтр по городу
        if city and proj.city != city:
            continue
        
        # Фильтр по региону
        if region_code and proj.region_code != region_code:
            continue
        
        # Фильтр по классу недвижимости
        if property_class and proj.class_type != property_class:
            continue
        
        # Фильтр по застройщику
        if developer_id and proj.developer_id != developer_id:
            continue
        
        filtered_projects.append(proj)
    
    return filtered_projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получить информацию о проекте"""
    project_obj = await project.get(db, project_id)
    
    if not project_obj:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return project_obj


@router.post("/", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новый проект"""
    project_dict = project_data.dict()
    project_obj = await project.create(db, project_dict)
    return project_obj


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить информацию о проекте"""
    project_obj = await project.get(db, project_id)
    
    if not project_obj:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    update_data = project_data.dict(exclude_unset=True)
    project_obj = await project.update(db, project_obj, update_data)
    return project_obj


@router.delete("/{project_id}")
async def delete_project(project_id: int, db: AsyncSession = Depends(get_async_session)):
    """Удалить проект"""
    success = await project.delete(db, project_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    return {"message": "Проект удален"}


@router.get("/{project_id}/buildings", response_model=List[BuildingResponse])
async def get_project_buildings(
    project_id: int,
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить корпуса проекта"""
    buildings_list = await building.get_by_project(db, project_id)
    
    # Применяем пагинацию
    start = offset
    end = start + limit
    return buildings_list[start:end]


@router.post("/{project_id}/buildings", response_model=BuildingResponse)
async def create_project_building(
    project_id: int,
    building_data: BuildingCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новый корпус в проекте"""
    # Проверяем, что проект существует
    project_obj = await project.get(db, project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Создаем корпус
    building_dict = building_data.dict()
    building_dict["project_id"] = project_id
    building_obj = await building.create(db, building_dict)
    return building_obj


@router.get("/{project_id}/apartments", response_model=List[ApartmentResponse])
async def get_project_apartments(
    project_id: int,
    rooms: Optional[int] = Query(None, description="Количество комнат"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    status: Optional[str] = Query(None, description="Статус квартиры"),
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить квартиры проекта"""
    # Получаем все квартиры
    apartments_list = await apartment.get_multi(db, skip=0, limit=1000)  # Большой лимит для фильтрации
    
    # Фильтруем по проекту и другим параметрам
    filtered_apartments = []
    for apt in apartments_list:
        # Проверяем, что квартира принадлежит проекту
        if apt.building.project.id != project_id:
            continue
        
        # Фильтр по комнатам
        if rooms is not None and apt.rooms != rooms:
            continue
        
        # Фильтр по цене
        if min_price is not None and apt.current_price < min_price:
            continue
        if max_price is not None and apt.current_price > max_price:
            continue
        
        # Фильтр по статусу
        if status and apt.status != status:
            continue
        
        filtered_apartments.append(apt)
    
    # Применяем пагинацию
    start = offset
    end = start + limit
    return filtered_apartments[start:end] 