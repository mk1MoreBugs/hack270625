from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Project
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from app.crud import crud_project
from app.security import get_current_user
from app.models import User

router = APIRouter(
    prefix="/api/v1/project",
    tags=["projects"]
)


@router.get(
    "/",
    response_model=List[ProjectRead],
    summary="Получить список проектов",
    description="Возвращает список всех проектов с возможностью фильтрации по застройщику"
)
async def get_projects(
    developer_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
) -> List[ProjectRead]:
    """
    Получить список проектов
    
    Args:
        developer_id: ID застройщика для фильтрации
        skip: Количество пропускаемых записей
        limit: Максимальное количество возвращаемых записей
        db: Сессия базы данных
    
    Returns:
        List[ProjectRead]: Список проектов
    """
    if developer_id:
        return await crud_project.get_by_developer(db, developer_id)
    return await crud_project.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый проект",
    description="Создает новый проект с указанными параметрами",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"},
        422: {"description": "Ошибка валидации"}
    }
)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> ProjectRead:
    """
    Создать новый проект
    
    Args:
        project_in: Данные нового проекта
        db: Сессия базы данных
        current_user: Текущий пользователь
    
    Returns:
        ProjectRead: Созданный проект
    """
    return await crud_project.create(db, obj_in=project_in)


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Получить проект",
    description="Возвращает информацию о конкретном проекте",
    responses={
        404: {"description": "Проект не найден"}
    }
)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    """
    Получить проект
    
    Args:
        project_id: ID проекта
        db: Сессия базы данных
    
    Returns:
        ProjectRead: Информация о проекте
    """
    project = await crud_project.get(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
    summary="Обновить проект",
    description="Обновляет информацию о существующем проекте",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"},
        404: {"description": "Проект не найден"},
        422: {"description": "Ошибка валидации"}
    }
)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> ProjectRead:
    """
    Обновить проект
    
    Args:
        project_id: ID проекта
        project_in: Обновленные данные проекта
        db: Сессия базы данных
        current_user: Текущий пользователь
    
    Returns:
        ProjectRead: Обновленный проект
    """
    project = await crud_project.get(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    return await crud_project.update(db, db_obj=project, obj_in=project_in)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить проект",
    description="Удаляет существующий проект",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"},
        404: {"description": "Проект не найден"}
    }
)
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Удалить проект
    
    Args:
        project_id: ID проекта
        db: Сессия базы данных
        current_user: Текущий пользователь
    """
    project = await crud_project.get(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    await crud_project.remove(db, id=project_id) 