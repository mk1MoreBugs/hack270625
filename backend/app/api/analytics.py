from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import ApartmentStats, ViewsLog
from app.schemas import ApartmentStatsResponse, MarketAnalyticsResponse, ViewsLogResponse
from app.crud import apartment_stats, views_log
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/market", response_model=MarketAnalyticsResponse)
async def get_market_analytics(
    city: Optional[str] = Query(None, description="Город"),
    region_code: Optional[str] = Query(None, description="Код региона"),
    period_days: int = Query(30, description="Период анализа в днях"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить аналитику рынка"""
    start_date = datetime.utcnow() - timedelta(days=period_days)
    
    # Получаем статистику по просмотрам и бронированиям
    stats = await apartment_stats.get_market_stats(
        db,
        start_date=start_date,
        city=city,
        region_code=region_code
    )
    
    return stats


@router.get("/apartments/{apartment_id}/stats", response_model=ApartmentStatsResponse)
async def get_apartment_stats(
    apartment_id: int,
    period_days: int = Query(30, description="Период анализа в днях"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить статистику по квартире"""
    stats = await apartment_stats.get(db, apartment_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Статистика не найдена")
    return stats


@router.get("/apartments/{apartment_id}/views", response_model=List[ViewsLogResponse])
async def get_apartment_views(
    apartment_id: int,
    start_date: Optional[datetime] = Query(None, description="Начальная дата"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата"),
    limit: int = Query(100, description="Количество записей"),
    offset: int = Query(0, description="Смещение"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю просмотров квартиры"""
    views = await views_log.get_by_apartment(
        db,
        apartment_id,
        start_date=start_date,
        end_date=end_date,
        skip=offset,
        limit=limit
    )
    return views


@router.get("/demand-clusters", response_model=List[dict])
async def get_demand_clusters(
    project_id: Optional[int] = Query(None, description="ID проекта"),
    rooms: Optional[int] = Query(None, description="Количество комнат"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить кластеры спроса для расчета динамических цен"""
    clusters = await apartment_stats.get_demand_clusters(
        db,
        project_id=project_id,
        rooms=rooms
    )
    return clusters 