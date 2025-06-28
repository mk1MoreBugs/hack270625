from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Developer, Project, User
from app.schemas import (
    DeveloperResponse, DeveloperCreate, DeveloperUpdate,
    ProjectResponse
)
from app.crud import CRUDDeveloper, CRUDProject
from app.security import get_current_active_user, get_current_business

router = APIRouter(prefix="/developers", tags=["developers"])

developer_crud = CRUDDeveloper(Developer)
project_crud = CRUDProject(Project)


@router.post("", response_model=DeveloperResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    400: {
        "description": "Застройщик с таким ИНН уже существует",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Developer with this INN already exists"
                }
            }
        }
    }
})
async def create_developer(
    developer_data: DeveloperCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать нового застройщика
    
    Args:
        developer_data: Данные для создания застройщика
        
    Returns:
        DeveloperResponse: Созданный застройщик
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Застройщик с таким ИНН уже существует
    """
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


@router.put("/{developer_id}", response_model=DeveloperResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Застройщик не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Developer not found"
                }
            }
        }
    },
    400: {
        "description": "Застройщик с таким ИНН уже существует",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Developer with this INN already exists"
                }
            }
        }
    }
})
async def update_developer(
    developer_id: int,
    developer_data: DeveloperUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить застройщика
    
    Args:
        developer_id: ID застройщика
        developer_data: Данные для обновления
        
    Returns:
        DeveloperResponse: Обновленный застройщик
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Застройщик не найден
        400: Bad Request - Застройщик с таким ИНН уже существует
    """
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


@router.delete("/{developer_id}", responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Застройщик не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Developer not found"
                }
            }
        }
    },
    200: {
        "description": "Застройщик успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "Developer deleted"
                }
            }
        }
    }
})
async def delete_developer(
    developer_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить застройщика
    
    Args:
        developer_id: ID застройщика
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Застройщик не найден
    """
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