from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.schemas import ProjectGeoResponse, MapFiltersResponse
from app.crud import CRUDProject
from datetime import datetime
from app.models import Project

router = APIRouter(prefix="/map", tags=["map"])
project_crud = CRUDProject(Project)


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
    # Временно возвращаем пустой список, пока не реализована логика get_geo_data
    return []


@router.get("/filters", response_model=MapFiltersResponse)
async def get_map_filters(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить доступные фильтры для карты"""
    # Временно возвращаем пустые фильтры, пока не реализована логика get_map_filters
    return MapFiltersResponse()


@router.get("", response_model=List[ProjectGeoResponse])
async def get_map_data(
    db: AsyncSession = Depends(get_async_session)
):
    """Получить данные для карты"""
    return await project_crud.get_multi(db) 