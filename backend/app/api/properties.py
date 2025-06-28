from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from app.database import get_async_session
from app.models import Property, Building, Project, Developer
from app.security import get_current_user, get_current_admin_user
from app.schemas import PropertyCreate, PropertyRead, PropertyUpdate, Message

router = APIRouter(
    prefix="/api/v1/project/properties",
    tags=["projects"]
)


@router.get(
    "",
    response_model=List[PropertyRead],
    summary="Получить список объектов недвижимости",
    description="Возвращает список всех объектов недвижимости с возможностью фильтрации и сортировки"
)
async def get_properties(
    *,
    session: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
    developer_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    building_id: Optional[UUID] = None,
    property_type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_area: Optional[float] = None,
    max_area: Optional[float] = None,
    min_rooms: Optional[int] = None,
    max_rooms: Optional[int] = None,
    floor_from: Optional[int] = None,
    floor_to: Optional[int] = None,
    has_balcony: Optional[bool] = None,
    has_loggia: Optional[bool] = None,
    has_parking: Optional[bool] = None,
    has_3d_tour: Optional[bool] = None,
    completion_date_before: Optional[datetime] = None,
    completion_date_after: Optional[datetime] = None,
    sort_by: Optional[str] = "created_at",
    sort_desc: bool = True
):
    """
    Получить список объектов недвижимости с опциональной фильтрацией и сортировкой.
    
    Параметры:
    - skip: Количество пропускаемых записей (пагинация)
    - limit: Максимальное количество возвращаемых записей
    - developer_id: Фильтр по ID застройщика
    - project_id: Фильтр по ID проекта
    - building_id: Фильтр по ID здания
    - property_type: Фильтр по типу недвижимости (residential, commercial)
    - category: Фильтр по категории недвижимости (flat_new, flat_secondary и т.д.)
    - status: Фильтр по статусу (available, reserved, sold)
    - min_price: Фильтр по минимальной цене
    - max_price: Фильтр по максимальной цене
    - min_area: Фильтр по минимальной общей площади
    - max_area: Фильтр по максимальной общей площади
    - min_rooms: Фильтр по минимальному количеству комнат
    - max_rooms: Фильтр по максимальному количеству комнат
    - floor_from: Фильтр по минимальному этажу
    - floor_to: Фильтр по максимальному этажу
    - has_balcony: Фильтр по наличию балкона
    - has_loggia: Фильтр по наличию лоджии
    - has_parking: Фильтр по наличию парковки
    - has_3d_tour: Фильтр по наличию 3D-тура
    - completion_date_before: Фильтр по дате завершения до
    - completion_date_after: Фильтр по дате завершения после
    - sort_by: Поле для сортировки (created_at, price, area, rooms, floor)
    - sort_desc: Сортировка по убыванию
    
    Возвращает:
    - Список объектов недвижимости, соответствующих критериям
    """
    query = select(Property)
    
    if developer_id:
        query = query.where(Property.developer_id == developer_id)
    if project_id:
        query = query.where(Property.project_id == project_id)
    if building_id:
        query = query.where(Property.building_id == building_id)
    if property_type:
        query = query.where(Property.property_type == property_type)
    if category:
        query = query.where(Property.category == category)
    if status:
        query = query.where(Property.status == status)
    if min_price is not None:
        query = query.join(Property.price).where(Property.price.current_price >= min_price)
    if max_price is not None:
        query = query.join(Property.price).where(Property.price.current_price <= max_price)
    if min_area is not None:
        query = query.join(Property.residential).where(Property.residential.total_area >= min_area)
    if max_area is not None:
        query = query.join(Property.residential).where(Property.residential.total_area <= max_area)
    if min_rooms is not None:
        query = query.join(Property.residential).where(Property.residential.rooms >= min_rooms)
    if max_rooms is not None:
        query = query.join(Property.residential).where(Property.residential.rooms <= max_rooms)
    if floor_from is not None:
        query = query.join(Property.residential).where(Property.residential.floor >= floor_from)
    if floor_to is not None:
        query = query.join(Property.residential).where(Property.residential.floor <= floor_to)
    if has_balcony is not None:
        query = query.join(Property.features).where(Property.features.balcony == has_balcony)
    if has_loggia is not None:
        query = query.join(Property.features).where(Property.features.loggia == has_loggia)
    if has_parking is not None:
        query = query.join(Property.features).where(Property.features.parking_type != None if has_parking else Property.features.parking_type == None)
    if has_3d_tour is not None:
        query = query.where(Property.has_3d_tour == has_3d_tour)
    if completion_date_before:
        query = query.join(Property.residential).where(Property.residential.completion_date <= completion_date_before)
    if completion_date_after:
        query = query.join(Property.residential).where(Property.residential.completion_date >= completion_date_after)
        
    if sort_by == "created_at":
        query = query.order_by(Property.created_at.desc() if sort_desc else Property.created_at)
    elif sort_by == "price":
        query = query.join(Property.price).order_by(Property.price.current_price.desc() if sort_desc else Property.price.current_price)
    elif sort_by == "area":
        query = query.join(Property.residential).order_by(Property.residential.total_area.desc() if sort_desc else Property.residential.total_area)
    elif sort_by == "rooms":
        query = query.join(Property.residential).order_by(Property.residential.rooms.desc() if sort_desc else Property.residential.rooms)
    elif sort_by == "floor":
        query = query.join(Property.residential).order_by(Property.residential.floor.desc() if sort_desc else Property.residential.floor)
        
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get(
    "/{property_id}",
    response_model=PropertyRead,
    summary="Получить объект недвижимости",
    description="Возвращает информацию о конкретном объекте недвижимости",
    responses={
        404: {"description": "Объект недвижимости не найден"}
    }
)
async def get_property(
    *,
    session: Session = Depends(get_async_session),
    property_id: UUID
):
    """
    Получить информацию об объекте недвижимости по ID.
    
    Параметры:
    - property_id: UUID объекта недвижимости
    
    Возвращает:
    - Детальная информация об объекте недвижимости со всеми связанными данными
    
    Ошибки:
    - 404: Объект недвижимости не найден
    """
    result = await session.execute(
        select(Property).where(Property.id == property_id)
    )
    property = result.scalar_one_or_none()
    if not property:
        raise HTTPException(status_code=404, detail="Объект недвижимости не найден")
    return property


@router.post(
    "",
    response_model=PropertyRead,
    status_code=201,
    summary="Создать новый объект недвижимости",
    description="Создает новый объект недвижимости с указанными параметрами",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Застройщик/Проект/Здание не найдены"},
        409: {"description": "Объект недвижимости с таким external_id уже существует"},
        422: {"description": "Ошибка валидации"}
    }
)
async def create_property(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    property: PropertyCreate
):
    """
    Создать новый объект недвижимости.
    
    Параметры:
    - property: Данные объекта недвижимости
    
    Возвращает:
    - Созданный объект недвижимости
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Застройщик/Проект/Здание не найдены
    - 409: Объект недвижимости с таким external_id уже существует
    """
    # Check if developer exists
    if property.developer_id:
        result = await session.execute(
            select(Developer).where(Developer.id == property.developer_id)
        )
        developer = result.scalar_one_or_none()
        if not developer:
            raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    # Check if project exists
    if property.project_id:
        result = await session.execute(
            select(Project).where(Project.id == property.project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Check if building exists
    if property.building_id:
        result = await session.execute(
            select(Building).where(Building.id == property.building_id)
        )
        building = result.scalar_one_or_none()
        if not building:
            raise HTTPException(status_code=404, detail="Здание не найдено")
    
    # Check for external_id uniqueness
    if property.external_id:
        result = await session.execute(
            select(Property).where(Property.external_id == property.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Объект недвижимости с таким external_id уже существует"
            )
    
    db_property = Property.from_orm(property)
    session.add(db_property)
    await session.commit()
    await session.refresh(db_property)
    return db_property


@router.put(
    "/{property_id}",
    response_model=PropertyRead,
    summary="Обновить объект недвижимости",
    description="Обновляет информацию о существующем объекте недвижимости",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Объект недвижимости/Застройщик/Проект/Здание не найдены"},
        409: {"description": "Конфликт external_id с существующим объектом"},
        422: {"description": "Ошибка валидации"}
    }
)
async def update_property(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    property_id: UUID,
    property: PropertyUpdate
):
    """
    Обновить объект недвижимости.
    
    Параметры:
    - property_id: UUID объекта недвижимости для обновления
    - property: Обновленные данные объекта недвижимости
    
    Возвращает:
    - Обновленный объект недвижимости
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Объект недвижимости не найден
    - 404: Застройщик/Проект/Здание не найдены
    - 409: Конфликт external_id с существующим объектом
    """
    result = await session.execute(
        select(Property).where(Property.id == property_id)
    )
    db_property = result.scalar_one_or_none()
    if not db_property:
        raise HTTPException(status_code=404, detail="Объект недвижимости не найден")
    
    # Check if new developer exists
    if property.developer_id and property.developer_id != db_property.developer_id:
        result = await session.execute(
            select(Developer).where(Developer.id == property.developer_id)
        )
        developer = result.scalar_one_or_none()
        if not developer:
            raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    # Check if new project exists
    if property.project_id and property.project_id != db_property.project_id:
        result = await session.execute(
            select(Project).where(Project.id == property.project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Check if new building exists
    if property.building_id and property.building_id != db_property.building_id:
        result = await session.execute(
            select(Building).where(Building.id == property.building_id)
        )
        building = result.scalar_one_or_none()
        if not building:
            raise HTTPException(status_code=404, detail="Здание не найдено")
    
    # Check for external_id uniqueness
    if property.external_id and property.external_id != db_property.external_id:
        result = await session.execute(
            select(Property).where(Property.external_id == property.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Объект недвижимости с таким external_id уже существует"
            )
    
    property_data = property.dict(exclude_unset=True)
    for key, value in property_data.items():
        setattr(db_property, key, value)
    
    session.add(db_property)
    await session.commit()
    await session.refresh(db_property)
    return db_property


@router.delete(
    "/{property_id}",
    response_model=Message,
    summary="Удалить объект недвижимости",
    description="Удаляет существующий объект недвижимости",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Объект недвижимости не найден"}
    }
)
async def delete_property(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    property_id: UUID
):
    """
    Удалить объект недвижимости.
    
    Параметры:
    - property_id: UUID объекта недвижимости для удаления
    
    Возвращает:
    - Сообщение об успехе
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Объект недвижимости не найден
    """
    result = await session.execute(
        select(Property).where(Property.id == property_id)
    )
    property = result.scalar_one_or_none()
    if not property:
        raise HTTPException(status_code=404, detail="Объект недвижимости не найден")
    
    await session.delete(property)
    await session.commit()
    
    return {"message": "Объект недвижимости успешно удален"} 