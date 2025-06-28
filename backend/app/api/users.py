from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import User, UserRole
from app.schemas import UserRead, UserCreate, UserUpdate, Message
from app.crud import CRUDUser
from app.security import get_current_active_user, get_current_admin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)
user_crud = CRUDUser(User)


@router.get(
    "/",
    response_model=List[UserRead],
    summary="Получить список пользователей",
    description="Возвращает список всех пользователей с пагинацией",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"}
    }
)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список пользователей"""
    return await user_crud.get_multi(db, skip=skip, limit=limit)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя",
    description="Создает нового пользователя (только для администраторов)",
    responses={
        201: {"description": "Пользователь создан"},
        400: {"description": "Некорректные данные"},
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"},
        422: {"description": "Ошибка валидации"}
    }
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin)
):
    """
    Создать нового пользователя
    
    Args:
        user_data: Данные для создания пользователя
        
    Returns:
        UserRead: Созданный пользователь
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await user_crud.create(db, user_data.dict())


@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Получить пользователя",
    description="Возвращает информацию о конкретном пользователе",
    responses={
        404: {"description": "Пользователь не найден"},
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"}
    }
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить пользователя по ID"""
    db_user = await user_crud.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return db_user


@router.put(
    "/{user_id}",
    response_model=UserRead,
    summary="Обновить пользователя",
    description="Обновляет информацию о существующем пользователе",
    responses={
        401: {
            "description": "Не авторизован",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Не удалось проверить учетные данные"
                    }
                }
            }
        },
        403: {
            "description": "Недостаточно прав",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Операция не разрешена"
                    }
                }
            }
        },
        404: {
            "description": "Пользователь не найден",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Пользователь не найден"
                    }
                }
            }
        },
        400: {
            "description": "Некорректные данные",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Ошибка валидации"
                    }
                }
            }
        },
        422: {"description": "Ошибка валидации"}
    }
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновить пользователя
    
    Args:
        user_id: ID пользователя
        user_data: Данные для обновления
        
    Returns:
        UserRead: Обновленный пользователь
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Пользователь не найден
        400: Bad Request - Некорректные данные
    """
    db_user = await user_crud.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return await user_crud.update(db, db_user, user_data.dict(exclude_unset=True))


@router.delete(
    "/{user_id}",
    response_model=Message,
    summary="Удалить пользователя",
    description="Удаляет существующего пользователя (только для администраторов)",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"},
        404: {"description": "Пользователь не найден"}
    }
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: dict = Depends(get_current_admin)
):
    """Удалить пользователя"""
    user = await user_crud.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )
    
    await user_crud.delete(db, user_id)
    return Message(message="Пользователь удален") 