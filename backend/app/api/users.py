from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import User, UserRole
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.crud import CRUDUser
from app.security import get_current_active_user, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])
user_crud = CRUDUser(User)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список пользователей"""
    return await user_crud.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=UserResponse, responses={
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
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
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
        UserResponse: Созданный пользователь
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await user_crud.create(db, user_data.dict())


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить пользователя по ID"""
    db_user = await user_crud.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=UserResponse, responses={
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
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
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
        UserResponse: Обновленный пользователь
        
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
            detail="User not found"
        )
    return await user_crud.update(db, db_user, user_data.dict(exclude_unset=True))


@router.delete("/{user_id}", responses={
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
        "description": "Пользователь не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "User not found"
                }
            }
        }
    },
    200: {
        "description": "Пользователь успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "User deleted"
                }
            }
        }
    }
})
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin)
):
    """
    Удалить пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Пользователь не найден
    """
    if not await user_crud.delete(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted"} 