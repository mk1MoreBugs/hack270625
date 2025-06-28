from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.crud import crud_property_media
from app.schemas import PropertyMediaCreate, PropertyMediaUpdate, PropertyMediaResponse
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/media", tags=["media"])


@router.get("/", response_model=List[PropertyMediaResponse])
async def get_media(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    property_id: Optional[UUID] = None,
    media_type: Optional[str] = None,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить список медиа с фильтрацией
    """
    try:
        media_list = await crud_property_media.get_multi(db, skip=skip, limit=limit)
        
        # Применяем фильтры
        if property_id:
            media_list = [m for m in media_list if m.property_id == property_id]
        if media_type:
            media_list = [m for m in media_list if m.media_type == media_type]
        
        return media_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении медиа: {str(e)}"
        )


@router.get("/{media_id}", response_model=PropertyMediaResponse)
async def get_media_item(
    media_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получить информацию о медиа
    """
    try:
        media = await crud_property_media.get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Медиа не найдено"
            )
        return media
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении медиа: {str(e)}"
        )


@router.post("/", response_model=PropertyMediaResponse, status_code=status.HTTP_201_CREATED)
async def create_media(
    media_data: PropertyMediaCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создать новое медиа
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для создания медиа"
            )
        
        media = await crud_property_media.create(db, media_data.dict())
        return media
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании медиа: {str(e)}"
        )


@router.put("/{media_id}", response_model=PropertyMediaResponse)
async def update_media(
    media_id: UUID,
    media_data: PropertyMediaUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Обновить медиа
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для обновления медиа"
            )
        
        media = await crud_property_media.get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Медиа не найдено"
            )
        
        updated_media = await crud_property_media.update(db, media, media_data.dict(exclude_unset=True))
        return updated_media
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении медиа: {str(e)}"
        )


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Удалить медиа
    """
    try:
        # Проверяем права доступа
        if current_user.role not in ["admin", "developer"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для удаления медиа"
            )
        
        media = await crud_property_media.get(db, media_id)
        if not media:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Медиа не найдено"
            )
        
        await crud_property_media.delete(db, media_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении медиа: {str(e)}"
        ) 