from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import User, UserRole
from app.schemas import UserResponse, UserCreate, UserUpdate
from app.crud import CRUDUser

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


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать нового пользователя"""
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


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить пользователя"""
    db_user = await user_crud.get(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return await user_crud.update(db, db_user, user_data.dict(exclude_unset=True))


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить пользователя"""
    if not await user_crud.delete(db, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted"} 