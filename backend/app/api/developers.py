from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_developer
from app.schemas import DeveloperCreate, DeveloperUpdate, DeveloperResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/developers", tags=["developers"])


@router.get("/", response_model=List[DeveloperResponse])
async def get_developers(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    name: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список застройщиков с фильтрацией
    """
    try:
        developers = await crud_developer.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if name:
            developers = [d for d in developers if name.lower() in d.name.lower()]
        
        return developers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении застройщиков: {str(e)}"
        )


@router.get("/{developer_id}", response_model=DeveloperResponse)
async def get_developer(
    developer_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию о застройщике
    """
    try:
        developer = await crud_developer.get(db, developer_id)
        if not developer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Застройщик не найден"
            )
        return developer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении застройщика: {str(e)}"
        )


@router.post("/", response_model=DeveloperResponse, status_code=status.HTTP_201_CREATED)
async def create_developer(
    developer_data: DeveloperCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать нового застройщика
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания застройщика"
            )
        
        developer = await crud_developer.create(db, developer_data.dict())
        return developer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании застройщика: {str(e)}"
        )


@router.put("/{developer_id}", response_model=DeveloperResponse)
async def update_developer(
    developer_id: UUID,
    developer_data: DeveloperUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить застройщика
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления застройщика"
            )
        
        developer = await crud_developer.get(db, developer_id)
        if not developer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Застройщик не найден"
            )
        
        updated_developer = await crud_developer.update(db, developer, developer_data.dict(exclude_unset=True))
        return updated_developer
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении застройщика: {str(e)}"
        )


@router.delete("/{developer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_developer(
    developer_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить застройщика
    """
    try:
        # Проверяем права доступа
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления застройщика"
            )
        
        developer = await crud_developer.get(db, developer_id)
        if not developer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Застройщик не найден"
            )
        
        await crud_developer.delete(db, developer_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении застройщика: {str(e)}"
        ) 