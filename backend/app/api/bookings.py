from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Booking, Apartment, BookingStatus
from app.schemas import BookingResponse, BookingCreate, BookingUpdate
from app.crud import CRUDBooking, CRUDApartment

router = APIRouter(prefix="/bookings", tags=["bookings"])

booking_crud = CRUDBooking(Booking)
apartment_crud = CRUDApartment(Apartment)


@router.post("", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новое бронирование"""
    # Проверяем существование квартиры
    apartment = await apartment_crud.get(db, booking_data.apartment_id)
    if not apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    
    # Проверяем, не забронирована ли уже квартира
    existing_bookings = await booking_crud.get_by_apartment(db, booking_data.apartment_id)
    active_bookings = [b for b in existing_bookings if b.status == BookingStatus.ACTIVE]
    if active_bookings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Apartment is already booked"
        )
    
    return await booking_crud.create(db, booking_data.dict())


@router.get("", response_model=List[BookingResponse])
async def get_bookings(
    status: BookingStatus = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список бронирований"""
    if status:
        return await booking_crud.get_by_status(db, status)
    return await booking_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирование по ID"""
    db_booking = await booking_crud.get(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return db_booking


@router.put("/{booking_id}", response_model=BookingResponse)
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить бронирование"""
    db_booking = await booking_crud.get(db, booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return await booking_crud.update(db, db_booking, booking_data.dict(exclude_unset=True))


@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить бронирование"""
    if not await booking_crud.delete(db, booking_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return {"message": "Booking deleted"}


@router.get("/user/{user_id}", response_model=List[BookingResponse])
async def get_user_bookings(
    user_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирования пользователя"""
    return await booking_crud.get_by_user(db, user_id)


@router.get("/apartment/{apartment_id}", response_model=List[BookingResponse])
async def get_apartment_bookings(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить бронирования квартиры"""
    # Проверяем существование квартиры
    if not await apartment_crud.get(db, apartment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return await booking_crud.get_by_apartment(db, apartment_id)


@router.get("/apartment/{apartment_id}/recent", response_model=List[BookingResponse])
async def get_recent_apartment_bookings(
    apartment_id: int,
    hours: int = 24,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить недавние бронирования квартиры"""
    # Проверяем существование квартиры
    if not await apartment_crud.get(db, apartment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return await booking_crud.get_recent_bookings(db, apartment_id, hours=hours) 