from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Developer, Project
from app.schemas import (
    DeveloperResponse, DeveloperCreate, DeveloperUpdate,
    ProjectResponse
)
from app.crud import CRUDDeveloper, CRUDProject

router = APIRouter(prefix="/developers", tags=["developers"])

developer_crud = CRUDDeveloper(Developer)
project_crud = CRUDProject(Project)


@router.post("", response_model=DeveloperResponse)
async def create_developer(
    developer_data: DeveloperCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать нового застройщика"""
    # Проверяем, не существует ли уже застройщик с таким ИНН
    existing_developer = await developer_crud.get_by_inn(db, developer_data.inn)
    if existing_developer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Developer with this INN already exists"
        )
    
    return await developer_crud.create(db, developer_data.dict())


@router.get("", response_model=List[DeveloperResponse])
async def get_developers(
    verified_only: bool = False,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список застройщиков"""
    if verified_only:
        return await developer_crud.get_verified(db)
    return await developer_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{developer_id}", response_model=DeveloperResponse)
async def get_developer(
    developer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить застройщика по ID"""
    db_developer = await developer_crud.get(db, developer_id)
    if not db_developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found"
        )
    return db_developer


@router.put("/{developer_id}", response_model=DeveloperResponse)
async def update_developer(
    developer_id: int,
    developer_data: DeveloperUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить застройщика"""
    db_developer = await developer_crud.get(db, developer_id)
    if not db_developer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found"
        )
    
    # Если обновляется ИНН, проверяем что он уникальный
    if developer_data.inn:
        existing_developer = await developer_crud.get_by_inn(db, developer_data.inn)
        if existing_developer and existing_developer.id != developer_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Developer with this INN already exists"
            )
    
    return await developer_crud.update(db, db_developer, developer_data.dict(exclude_unset=True))


@router.delete("/{developer_id}")
async def delete_developer(
    developer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить застройщика"""
    if not await developer_crud.delete(db, developer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found"
        )
    return {"message": "Developer deleted"}


@router.get("/{developer_id}/projects", response_model=List[ProjectResponse])
async def get_developer_projects(
    developer_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить проекты застройщика"""
    if not await developer_crud.get(db, developer_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found"
        )
    return await project_crud.get_by_developer(db, developer_id) 