from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.schemas import ProjectGeoResponse, MapFiltersResponse
from app.crud import project
from datetime import datetime

router = APIRouter(prefix="/map", tags=["map"])


@router.get("/projects", response_model=List[ProjectGeoResponse])
async def get_projects_geo(
    city: Optional[str] = Query(None, description="Город"),
    region_code: Optional[str] = Query(None, description="Код региона"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    property_class: Optional[str] = Query(None, description="Класс жилья"),
    completion_year: Optional[int] = Query(None, description="Год сдачи"),
    db: AsyncSession = Depends(get_async_session)
):
    """Получить геоданные проектов для карты"""
    projects = await project.get_geo_data(
        db,
        city=city,
        region_code=region_code,
        min_price=min_price,
        max_price=max_price,
        property_class=property_class,
        completion_year=completion_year
    )
    return projects


@router.get("/filters", response_model=MapFiltersResponse)
async def get_map_filters(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить доступные фильтры для карты"""
    filters = await project.get_map_filters(db)
    return filters 