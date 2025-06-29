from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database import get_async_session
from app.models import Property, UserRole
from app.schemas import PropertyCreate, PropertyUpdate, PropertyRead
from app.security import get_current_user_role
from typing import List, Optional

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=List[PropertyRead],
            summary="Получить список объектов недвижимости",
            description="Получение списка всех доступных объектов недвижимости с возможностью фильтрации")
async def get_properties(
    project_id: Optional[int] = None,
    building_id: Optional[int] = None,
    property_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    rooms: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session)
) -> List[PropertyRead]:
    query = select(Property)
    
    if project_id:
        query = query.where(Property.project_id == project_id)
    if building_id:
        query = query.where(Property.building_id == building_id)
    if property_type:
        query = query.where(Property.property_type == property_type)
    if min_price:
        query = query.join(Property.price).where(Property.price.current_price >= min_price)
    if max_price:
        query = query.join(Property.price).where(Property.price.current_price <= max_price)
    if min_area:
        query = query.join(Property.residential).where(Property.residential.total_area >= min_area)
    if max_area:
        query = query.join(Property.residential).where(Property.residential.total_area <= max_area)
    if rooms:
        query = query.join(Property.residential).where(Property.residential.rooms == rooms)
    
    properties = await session.execute(query)
    properties = properties.scalars().all()
    return [PropertyRead.from_orm(p) for p in properties]

@router.get("/{property_id}", response_model=PropertyRead,
            summary="Получить объект недвижимости",
            description="Получение информации о конкретном объекте недвижимости по его ID")
async def get_property(
    property_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> PropertyRead:
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект недвижимости не найден"
        )
    return PropertyRead.from_orm(property)

@router.post("/", response_model=PropertyRead,
             summary="Создать объект недвижимости",
             description="Создание нового объекта недвижимости (только для застройщиков)")
async def create_property(
    property_data: PropertyCreate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> PropertyRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут создавать объекты недвижимости"
        )
    
    property = Property(**property_data.dict())
    session.add(property)
    await session.commit()
    await session.refresh(property)
    return PropertyRead.from_orm(property)

@router.put("/{property_id}", response_model=PropertyRead,
            summary="Обновить объект недвижимости",
            description="Обновление информации об объекте недвижимости (только для застройщиков)")
async def update_property(
    property_id: int,
    property_data: PropertyUpdate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> PropertyRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут обновлять объекты недвижимости"
        )
    
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект недвижимости не найден"
        )
    
    for field, value in property_data.dict(exclude_unset=True).items():
        setattr(property, field, value)
    
    await session.commit()
    await session.refresh(property)
    return PropertyRead.from_orm(property)

@router.delete("/{property_id}",
               summary="Удалить объект недвижимости",
               description="Удаление объекта недвижимости (только для застройщиков)")
async def delete_property(
    property_id: int,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут удалять объекты недвижимости"
        )
    
    property = await session.get(Property, property_id)
    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Объект недвижимости не найден"
        )
    
    await session.delete(property)
    await session.commit()
    return {"message": "Объект недвижимости успешно удален"} 