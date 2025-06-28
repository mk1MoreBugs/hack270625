from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict
from app.database import get_async_session
from app.models import ApartmentStats, ViewsLog
from app.schemas import ApartmentStatsResponse, MarketAnalyticsResponse, ViewsLogResponse
from app.crud import CRUDStats, CRUDViewsLog
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["analytics"])

stats_crud = CRUDStats(ApartmentStats)
views_crud = CRUDViewsLog(ViewsLog)


@router.get("/market", response_model=MarketAnalyticsResponse)
async def get_market_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить аналитику по рынку"""
    # Получаем статистику просмотров
    total_views = await views_crud.get_total_views(db, days)
    avg_views = await views_crud.get_avg_views(db, days)
    avg_bookings = await views_crud.get_avg_bookings(db, days)
    
    return MarketAnalyticsResponse(
        total_views=total_views,
        avg_views=avg_views,
        avg_bookings=avg_bookings,
        period_days=days
    )


@router.get("/apartments/{apartment_id}", response_model=ApartmentStatsResponse)
async def get_apartment_analytics(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить аналитику по квартире"""
    stats = await stats_crud.get_apartment_stats(apartment_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Statistics not found"
        )
    return stats


@router.get("/views/{apartment_id}", response_model=List[ViewsLogResponse])
async def get_apartment_views(
    apartment_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю просмотров квартиры"""
    views = await views_crud.get_by_apartment(
        db,
        apartment_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return views


@router.get("/district/{district_id}/stats", response_model=MarketAnalyticsResponse)
async def get_district_stats(
    district_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить статистику по району"""
    stats = await stats_crud.get_district_stats(district_id)
    
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District stats not found"
        )
    
    return MarketAnalyticsResponse(**stats)


@router.get("/demand-clusters", response_model=List[dict])
async def get_demand_clusters(
    project_id: Optional[int] = Query(None, description="ID проекта"),
    rooms: Optional[int] = Query(None, description="Количество комнат"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить кластеры спроса для расчета динамических цен"""
    clusters = await stats_crud.get_demand_clusters(
        db,
        project_id=project_id,
        rooms=rooms
    )
    return clusters 