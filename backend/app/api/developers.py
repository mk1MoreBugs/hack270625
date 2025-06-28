from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Developer, Project
from app.schemas import (
    DeveloperResponse, DeveloperCreate, DeveloperUpdate,
    ProjectResponse, ProjectCreate, ProjectUpdate
)
from app.crud import developer, project
from datetime import datetime

router = APIRouter(prefix="/developers", tags=["developers"])


@router.get("/", response_model=List[DeveloperResponse])
async def get_developers(
    verified: Optional[bool] = Query(None, description="Статус верификации"),
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список застройщиков"""
    if verified is not None:
        developers_list = await developer.get_verified(db) if verified else []
    else:
        developers_list = await developer.get_multi(db, skip=offset, limit=limit)
    
    return developers_list


@router.get("/{developer_id}", response_model=DeveloperResponse)
async def get_developer(developer_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получить информацию о застройщике"""
    developer_obj = await developer.get(db, developer_id)
    
    if not developer_obj:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    return developer_obj


@router.post("/", response_model=DeveloperResponse)
async def create_developer(
    developer_data: DeveloperCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать нового застройщика"""
    developer_dict = developer_data.dict()
    developer_obj = await developer.create(db, developer_dict)
    return developer_obj


@router.put("/{developer_id}", response_model=DeveloperResponse)
async def update_developer(
    developer_id: int,
    developer_data: DeveloperUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить информацию о застройщике"""
    developer_obj = await developer.get(db, developer_id)
    
    if not developer_obj:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    update_data = developer_data.dict(exclude_unset=True)
    developer_obj = await developer.update(db, developer_obj, update_data)
    return developer_obj


@router.delete("/{developer_id}")
async def delete_developer(developer_id: int, db: AsyncSession = Depends(get_async_session)):
    """Удалить застройщика"""
    success = await developer.delete(db, developer_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    return {"message": "Застройщик удален"}


@router.get("/{developer_id}/projects", response_model=List[ProjectResponse])
async def get_developer_projects(
    developer_id: int,
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить проекты застройщика"""
    projects_list = await project.get_by_developer(db, developer_id)
    
    # Применяем пагинацию
    start = offset
    end = start + limit
    return projects_list[start:end] 