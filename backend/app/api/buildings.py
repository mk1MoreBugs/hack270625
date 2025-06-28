from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.models import Building, Project, Developer
from app.security import get_current_user, get_current_admin_user
from app.schemas import BuildingCreate, BuildingRead, BuildingUpdate, Message

router = APIRouter(
    prefix="/api/v1/project/buildings",
    tags=["projects"]
)


@router.get(
    "",
    response_model=List[BuildingRead],
    summary="Получить список зданий",
    description="Получить список зданий с возможностью фильтрации и сортировки",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа"}
    }
)
async def get_buildings(
    *,
    session: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
    developer_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_desc: bool = True
):
    """
    Получить список зданий с опциональной фильтрацией и сортировкой.
    
    Параметры:
    - skip: Количество пропускаемых записей (пагинация)
    - limit: Максимальное количество возвращаемых записей
    - developer_id: Фильтр по ID застройщика
    - project_id: Фильтр по ID проекта
    - name: Фильтр по названию здания (частичное совпадение, без учета регистра)
    - status: Фильтр по статусу здания
    - sort_by: Поле для сортировки (created_at, name, status)
    - sort_desc: Сортировка по убыванию
    
    Возвращает:
    - Список зданий, соответствующих критериям
    """
    query = select(Building)
    
    if developer_id:
        query = query.where(Building.developer_id == developer_id)
    if project_id:
        query = query.where(Building.project_id == project_id)
    if name:
        query = query.where(Building.name.ilike(f"%{name}%"))
    if status:
        query = query.where(Building.status == status)
        
    if sort_by == "created_at":
        query = query.order_by(Building.created_at.desc() if sort_desc else Building.created_at)
    elif sort_by == "name":
        query = query.order_by(Building.name.desc() if sort_desc else Building.name)
    elif sort_by == "status":
        query = query.order_by(Building.status.desc() if sort_desc else Building.status)
        
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Получить здание",
    description="Получить информацию о конкретном здании по ID",
    responses={
        404: {"description": "Здание не найдено"}
    }
)
async def get_building(
    *,
    session: Session = Depends(get_async_session),
    building_id: UUID
):
    """
    Получить информацию о здании по ID.
    
    Параметры:
    - building_id: UUID здания
    
    Возвращает:
    - Детальная информация о здании
    
    Ошибки:
    - 404: Здание не найдено
    """
    result = await session.execute(
        select(Building).where(Building.id == building_id)
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="Здание не найдено")
    return building


@router.post(
    "",
    response_model=BuildingRead,
    status_code=201,
    summary="Создать новое здание",
    description="Создать новое здание в системе",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Застройщик/Проект не найден"},
        409: {"description": "Здание с таким external_id уже существует"},
        422: {"description": "Ошибка валидации"}
    }
)
async def create_building(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    building: BuildingCreate
):
    """
    Создать новое здание.
    
    Параметры:
    - building: Данные здания
    
    Возвращает:
    - Созданное здание
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Застройщик/Проект не найден
    - 409: Здание с таким external_id уже существует
    """
    # Check if developer exists
    result = await session.execute(
        select(Developer).where(Developer.id == building.developer_id)
    )
    developer = result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    # Check if project exists
    result = await session.execute(
        select(Project).where(Project.id == building.project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Check for external_id uniqueness
    if building.external_id:
        result = await session.execute(
            select(Building).where(Building.external_id == building.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Здание с таким external_id уже существует"
            )
        
    db_building = Building.from_orm(building)
    session.add(db_building)
    await session.commit()
    await session.refresh(db_building)
    return db_building


@router.put(
    "/{building_id}",
    response_model=BuildingRead,
    summary="Обновить здание",
    description="Обновить информацию о существующем здании",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Здание/Застройщик/Проект не найден"},
        409: {"description": "Конфликт external_id с существующим зданием"},
        422: {"description": "Ошибка валидации"}
    }
)
async def update_building(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    building_id: UUID,
    building: BuildingUpdate
):
    """
    Обновить здание.
    
    Параметры:
    - building_id: UUID здания для обновления
    - building: Обновленные данные здания
    
    Возвращает:
    - Обновленное здание
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Здание не найдено
    - 404: Застройщик/Проект не найден
    - 409: Конфликт external_id с существующим зданием
    """
    result = await session.execute(
        select(Building).where(Building.id == building_id)
    )
    db_building = result.scalar_one_or_none()
    if not db_building:
        raise HTTPException(status_code=404, detail="Здание не найдено")
    
    # Check if new developer exists
    if building.developer_id and building.developer_id != db_building.developer_id:
        result = await session.execute(
            select(Developer).where(Developer.id == building.developer_id)
        )
        developer = result.scalar_one_or_none()
        if not developer:
            raise HTTPException(status_code=404, detail="Застройщик не найден")
    
    # Check if new project exists
    if building.project_id and building.project_id != db_building.project_id:
        result = await session.execute(
            select(Project).where(Project.id == building.project_id)
        )
        project = result.scalar_one_or_none()
        if not project:
            raise HTTPException(status_code=404, detail="Проект не найден")
    
    # Check for external_id uniqueness
    if building.external_id and building.external_id != db_building.external_id:
        result = await session.execute(
            select(Building).where(Building.external_id == building.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Здание с таким external_id уже существует"
            )
    
    building_data = building.dict(exclude_unset=True)
    for key, value in building_data.items():
        setattr(db_building, key, value)
    
    session.add(db_building)
    await session.commit()
    await session.refresh(db_building)
    return db_building


@router.delete(
    "/{building_id}",
    response_model=Message,
    summary="Удалить здание",
    description="Удалить существующее здание",
    responses={
        401: {"description": "Не авторизован"},
        403: {"description": "Нет прав доступа (не администратор)"},
        404: {"description": "Здание не найдено"}
    }
)
async def delete_building(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    building_id: UUID
):
    """
    Удалить здание.
    
    Параметры:
    - building_id: UUID здания для удаления
    
    Возвращает:
    - Сообщение об успехе
    
    Безопасность:
    - Требуется роль администратора
    
    Ошибки:
    - 401: Не авторизован
    - 403: Запрещено (не администратор)
    - 404: Здание не найдено
    """
    result = await session.execute(
        select(Building).where(Building.id == building_id)
    )
    building = result.scalar_one_or_none()
    if not building:
        raise HTTPException(status_code=404, detail="Здание не найдено")
    
    await session.delete(building)
    await session.commit()
    
    return {"message": "Здание успешно удалено"} 