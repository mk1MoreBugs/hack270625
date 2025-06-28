from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Booking, BookingStatus
from app.schemas import BookingResponse, BookingCreate, BookingUpdate
from app.crud import booking, apartment
from datetime import datetime, timedelta

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("/", response_model=List[BookingResponse])
async def get_bookings(
    status: Optional[BookingStatus] = Query(None, description="Статус бронирования"),
    user_id: Optional[int] = Query(None, description="ID пользователя"),
    limit: int = Query(20, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список бронирований"""
    if status:
        bookings_list = await booking.get_by_status(db, status)
    elif user_id:
        bookings_list = await booking.get_by_user(db, user_id)
    else:
        bookings_list = await booking.get_multi(db, skip=offset, limit=limit)
    
    # Применяем пагинацию
    start = offset
    end = start + limit
    return bookings_list[start:end]


@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новое бронирование"""
    # Проверяем, что квартира существует и доступна
    apt = await apartment.get(db, booking_data.apartment_id)
    if not apt:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    if apt.status != "available":
        raise HTTPException(status_code=400, detail="Квартира недоступна для бронирования")
    
    # Создаем бронирование
    booking_dict = booking_data.dict()
    booking_dict["status"] = BookingStatus.PENDING
    booking_dict["booked_at"] = datetime.utcnow()
    booking_dict["expires_at"] = datetime.utcnow() + timedelta(hours=24)  # Бронь на 24 часа
    
    booking_obj = await booking.create(db, booking_dict)
    
    # Обновляем статус квартиры
    await apartment.update(db, apt, {"status": "reserved"})
    
    return booking_obj


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить информацию о бронировании"""
    booking_obj = await booking.get(db, booking_id)
    if not booking_obj:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    return booking_obj


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить информацию о бронировании"""
    booking_obj = await booking.get(db, booking_id)
    if not booking_obj:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    
    update_data = booking_data.dict(exclude_unset=True)
    
    # Если меняется статус на CANCELLED, освобождаем квартиру
    if update_data.get("status") == BookingStatus.CANCELLED:
        apt = await apartment.get(db, booking_obj.apartment_id)
        if apt:
            await apartment.update(db, apt, {"status": "available"})
    
    booking_obj = await booking.update(db, booking_obj, update_data)
    return booking_obj


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить бронирование"""
    booking_obj = await booking.get(db, booking_id)
    if not booking_obj:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    
    # Освобождаем квартиру
    apt = await apartment.get(db, booking_obj.apartment_id)
    if apt and apt.status == "reserved":
        await apartment.update(db, apt, {"status": "available"})
    
    success = await booking.delete(db, booking_id)
    return {"message": "Бронирование удалено"} 