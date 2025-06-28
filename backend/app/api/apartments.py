from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Apartment, ViewsLog, ViewEvent
from app.schemas import (
    ApartmentResponse, ApartmentCreate, ApartmentUpdate,
    ViewsLogCreate, ViewsLogResponse, ApartmentSearchParams,
    ApartmentStatsResponse
)
from app.services.stats_aggregator import StatsAggregatorService
from app.crud import apartment, apartment_stats, views_log
from datetime import datetime

router = APIRouter(prefix="/apartments", tags=["apartments"])


@router.get("/", response_model=List[ApartmentResponse])
async def get_apartments(
    city: Optional[str] = Query(None, description="Город"),
    region_code: Optional[str] = Query(None, description="Код региона"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    rooms: Optional[int] = Query(None, description="Количество комнат"),
    min_area: Optional[float] = Query(None, description="Минимальная площадь"),
    max_area: Optional[float] = Query(None, description="Максимальная площадь"),
    status: Optional[str] = Query(None, description="Статус квартиры"),
    limit: Optional[int] = Query(20, description="Количество записей"),
    offset: Optional[int] = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список квартир с фильтрацией"""
    apartments_list = await apartment.get_multi(db, skip=offset, limit=limit)
    
    # Применяем фильтры
    filtered_apartments = []
    for apt in apartments_list:
        # Фильтр по цене
        if min_price is not None and apt.current_price < min_price:
            continue
        if max_price is not None and apt.current_price > max_price:
            continue
        
        # Фильтр по комнатам
        if rooms is not None and apt.rooms != rooms:
            continue
        
        # Фильтр по площади
        if min_area is not None and apt.area_total < min_area:
            continue
        if max_area is not None and apt.area_total > max_area:
            continue
        
        # Фильтр по статусу
        if status and apt.status != status:
            continue
        
        # Преобразуем модель в схему Pydantic
        filtered_apartments.append(
            ApartmentResponse(
                id=apt.id,
                number=apt.number,
                floor=apt.floor,
                rooms=apt.rooms,
                area_total=apt.area_total,
                area_living=apt.area_living,
                area_kitchen=apt.area_kitchen,
                base_price=apt.base_price,
                current_price=apt.current_price,
                balcony=apt.balcony,
                loggia=apt.loggia,
                parking=apt.parking,
                building_id=apt.building_id,
                status=apt.status,
                created_at=apt.created_at,
                updated_at=apt.updated_at
            )
        )
    
    return filtered_apartments


@router.get("/{apartment_id}", response_model=ApartmentResponse)
async def get_apartment(apartment_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получить информацию о конкретной квартире"""
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    return apartment_obj


@router.post("/", response_model=ApartmentResponse)
async def create_apartment(
    apartment_data: ApartmentCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новую квартиру"""
    apartment_dict = apartment_data.dict()
    apartment_obj = await apartment.create(db, apartment_dict)
    return apartment_obj


@router.put("/{apartment_id}", response_model=ApartmentResponse)
async def update_apartment(
    apartment_id: int,
    apartment_data: ApartmentUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить информацию о квартире"""
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    update_data = apartment_data.dict(exclude_unset=True)
    apartment_obj = await apartment.update(db, apartment_obj, update_data)
    return apartment_obj


@router.delete("/{apartment_id}")
async def delete_apartment(apartment_id: int, db: AsyncSession = Depends(get_async_session)):
    """Удалить квартиру"""
    success = await apartment.delete(db, apartment_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    return {"message": "Квартира удалена"}


@router.post("/{apartment_id}/view", response_model=ViewsLogResponse)
async def log_apartment_view(
    apartment_id: int,
    view_data: ViewsLogCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Записать просмотр квартиры"""
    # Проверяем, что квартира существует
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    # Создаем запись о просмотре
    view_log_data = {
        "apartment_id": apartment_id,
        "user_id": view_data.user_id,
        "event": view_data.event,
        "occurred_at": datetime.utcnow()
    }
    
    view_log_obj = await views_log.create(db, view_log_data)
    return view_log_obj


@router.get("/{apartment_id}/stats", response_model=ApartmentStatsResponse)
async def get_apartment_stats(apartment_id: int, db: AsyncSession = Depends(get_async_session)):
    """Получить статистику квартиры"""
    # Проверяем, что квартира существует
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    # Получаем или создаем статистику
    stats = await apartment_stats.get_by_apartment(db, apartment_id)
    
    if not stats:
        # Если статистики нет, создаем пустую
        stats = await apartment_stats.update_stats(db, apartment_id, 0, 0, 0, 0)
    
    return stats


@router.post("/{apartment_id}/stats/update")
async def update_apartment_stats(apartment_id: int, db: AsyncSession = Depends(get_async_session)):
    """Обновить статистику квартиры"""
    # Проверяем, что квартира существует
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    # Обновляем статистику
    aggregator = StatsAggregatorService(db)
    stats = await aggregator.update_apartment_stats(apartment_id)
    
    return {
        "message": "Статистика обновлена",
        "apartment_id": apartment_id,
        "stats": {
            "views_24h": stats.views_24h,
            "leads_24h": stats.leads_24h,
            "bookings_24h": stats.bookings_24h,
            "days_on_site": stats.days_on_site
        }
    } 