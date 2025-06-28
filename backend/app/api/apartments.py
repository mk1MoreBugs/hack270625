from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Apartment, ViewsLog, ViewEvent, ApartmentStatus
from app.schemas import (
    ApartmentResponse, ApartmentCreate, ApartmentUpdate,
    ViewsLogCreate, ViewsLogResponse, ApartmentSearchParams,
    ApartmentStatsResponse
)
from app.services.stats_aggregator import StatsAggregatorService
from app.crud import CRUDApartment, CRUDStats, CRUDViewsLog
from app.database import get_async_session
from datetime import datetime

apartment = CRUDApartment(Apartment)
views_log = CRUDViewsLog(ViewsLog)

router = APIRouter(prefix="/apartments", tags=["apartments"])


@router.get("", response_model=List[ApartmentResponse])
async def get_apartments(
    status: Optional[ApartmentStatus] = None,
    rooms: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список квартир с фильтрацией"""
    if status:
        return await apartment.get_by_status(db, status)
    elif rooms:
        return await apartment.get_by_rooms(db, rooms)
    elif min_price and max_price:
        return await apartment.get_by_price_range(db, min_price, max_price)
    else:
        return await apartment.get_multi(db, skip=skip, limit=limit)


@router.get("/{apartment_id}", response_model=ApartmentResponse)
async def get_apartment(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить квартиру по ID"""
    db_apartment = await apartment.get(db, apartment_id)
    if not db_apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    
    # Записываем просмотр
    await views_log.create(db, {
        "apartment_id": apartment_id,
        "event_type": ViewEvent.VIEW,
        "timestamp": datetime.utcnow()
    })
    
    return db_apartment


@router.post("", response_model=ApartmentResponse)
async def create_apartment(
    apartment_data: ApartmentCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новую квартиру"""
    return await apartment.create(db, apartment_data.dict())


@router.put("/{apartment_id}", response_model=ApartmentResponse)
async def update_apartment(
    apartment_id: int,
    apartment_data: ApartmentUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить квартиру"""
    db_apartment = await apartment.get(db, apartment_id)
    if not db_apartment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return await apartment.update(db, db_apartment, apartment_data.dict(exclude_unset=True))


@router.delete("/{apartment_id}")
async def delete_apartment(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить квартиру"""
    if not await apartment.delete(db, apartment_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment not found"
        )
    return {"message": "Apartment deleted"}


@router.get("/{apartment_id}/stats", response_model=ApartmentStatsResponse)
async def get_apartment_stats(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить статистику по квартире"""
    stats = CRUDStats(db)
    apartment_stats = await stats.get_apartment_stats(apartment_id)
    
    if not apartment_stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apartment stats not found"
        )
    
    return apartment_stats


@router.get("/{apartment_id}/views", response_model=List[ViewsLogResponse])
async def get_apartment_views(
    apartment_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю просмотров квартиры"""
    views = await views_log.get_by_apartment(
        db,
        apartment_id,
        start_date,
        end_date,
        skip,
        limit
    )
    
    if not views:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Views not found"
        )
    
    return views 