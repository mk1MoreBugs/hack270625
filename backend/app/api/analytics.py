from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from app.database import get_async_session
from app.models import PropertyAnalytics, ViewsLog
from app.schemas import PropertyAnalyticsRead, MarketAnalyticsResponse, ViewsLogRead
from app.crud import crud_property_analytics, crud_views_log
from app.security import get_current_user
from app.models import User

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/market", response_model=MarketAnalyticsResponse)
async def get_market_analytics(
    days: int = 30,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить аналитику по рынку"""
    # Получаем статистику просмотров
    total_views = await crud_views_log.get_total_views(db, days)
    avg_views = await crud_views_log.get_avg_views(db, days)
    avg_bookings = await crud_views_log.get_avg_bookings(db, days)
    
    return MarketAnalyticsResponse(
        total_views=total_views,
        avg_views=avg_views,
        avg_bookings=avg_bookings,
        period_days=days
    )


@router.get("/properties/{property_id}", response_model=PropertyAnalyticsRead)
async def get_property_analytics(
    property_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить аналитику по объекту недвижимости"""
    analytics = await crud_property_analytics.get_by_field(db, "property_id", property_id)
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics not found"
        )
    return analytics[0]


@router.get("/views/{property_id}", response_model=List[ViewsLogRead])
async def get_property_views(
    property_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить историю просмотров объекта недвижимости"""
    views = await crud_views_log.get_by_property(
        db,
        property_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return views


@router.get("/district/{district}/stats", response_model=Dict[str, float])
async def get_district_stats(
    district: str,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить статистику по району"""
    # Здесь можно добавить логику для получения статистики по району
    # Пока возвращаем базовую структуру
    return {
        "popularity_score": 0.75,
        "avg_price": 15000000.0,
        "demand_level": 0.8
    }


@router.get("/demand-clusters", response_model=List[dict])
async def get_demand_clusters(
    project_id: Optional[int] = Query(None, description="ID проекта"),
    property_type: Optional[str] = Query(None, description="Тип недвижимости"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить кластеры спроса для расчета динамических цен"""
    # Здесь можно добавить логику для получения кластеров спроса
    # Пока возвращаем базовую структуру
    return [
        {
            "cluster_id": 1,
            "demand_score": 0.8,
            "price_range": "15-20M",
            "property_count": 25
        },
        {
            "cluster_id": 2,
            "demand_score": 0.6,
            "price_range": "20-25M",
            "property_count": 15
        }
    ]


@router.get("/high-demand", response_model=List[PropertyAnalyticsRead])
async def get_high_demand_properties(
    min_score: int = Query(7, ge=1, le=10, description="Минимальный скор спроса"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить объекты с высоким спросом"""
    return await crud_property_analytics.get_high_demand(db, min_score)


@router.get("/popular", response_model=List[PropertyAnalyticsRead])
async def get_popular_properties(
    min_views: int = Query(100, ge=1, description="Минимальное количество просмотров"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить популярные объекты"""
    return await crud_property_analytics.get_popular(db, min_views) 