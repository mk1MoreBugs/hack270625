from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.database import get_async_session
from app.models import Booking, Property, BookingStatus, User
from app.schemas import BookingResponse, BookingCreate, BookingUpdate
from app.crud import crud_booking, crud_property
from app.security import get_current_active_user

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse, responses={
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
        "description": "Объект недвижимости не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property not found"
                }
            }
        }
    },
    400: {
        "description": "Объект уже забронирован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Property is already booked"
                }
            }
        }
    }
})
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Создать новое бронирование
    
    Args:
        booking_data: Данные для создания бронирования
        
    Returns:
        BookingResponse: Созданное бронирование
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Объект недвижимости не найден
        400: Bad Request - Объект уже забронирован
    """
    # Проверяем существование объекта недвижимости
    property_obj = await crud_property.get(db, booking_data.property_id)
    if not property_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )
    
    # Проверяем, не забронирован ли уже объект
    existing_bookings = await crud_booking.get_by_property(db, booking_data.property_id)
    active_bookings = [b for b in existing_bookings if b.status == BookingStatus.ACTIVE]
    if active_bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property is already booked"
        )
    
    return await crud_booking.create(db, booking_data.dict())


@router.get("", response_model=List[BookingResponse])
async def get_bookings(
    status: BookingStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список бронирований"""
    if status:
        return await crud_booking.get_by_status(db, status)
    return await crud_booking.get_multi(db, skip=skip, limit=limit)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирование по ID"""
    db_booking = await crud_booking.get(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return db_booking


@router.put("/{booking_id}", response_model=BookingResponse, responses={
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
        "description": "Бронирование не найдено",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Booking not found"
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
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Обновить бронирование
    
    Args:
        booking_id: ID бронирования
        booking_data: Данные для обновления
        
    Returns:
        BookingResponse: Обновленное бронирование
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Бронирование не найдено
        400: Bad Request - Некорректные данные
    """
    db_booking = await crud_booking.get(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return await crud_booking.update(db, db_booking, booking_data.dict(exclude_unset=True))


@router.delete("/{booking_id}", responses={
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
        "description": "Бронирование не найдено",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Booking not found"
                }
            }
        }
    },
    200: {
        "description": "Бронирование успешно удалено",
        "content": {
            "application/json": {
                "example": {
                    "message": "Booking deleted"
                }
            }
        }
    }
})
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_active_user)
):
    """
    Удалить бронирование
    
    Args:
        booking_id: ID бронирования
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Бронирование не найдено
    """
    db_booking = await crud_booking.get(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    await crud_booking.delete(db, booking_id)
    return {"message": "Booking deleted"}


@router.get("/user/{user_id}", response_model=List[BookingResponse])
async def get_user_bookings(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирования пользователя"""
    return await crud_booking.get_by_user(db, user_id)


@router.get("/property/{property_id}", response_model=List[BookingResponse])
async def get_property_bookings(
    property_id: UUID,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирования объекта недвижимости"""
    return await crud_booking.get_by_property(db, property_id)


@router.get("/property/{property_id}/recent", response_model=List[BookingResponse])
async def get_recent_property_bookings(
    property_id: UUID,
    hours: int = 24,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить недавние бронирования объекта недвижимости"""
    return await crud_booking.get_recent_bookings(db, property_id, hours) 