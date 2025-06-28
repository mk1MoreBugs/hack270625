from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import Project, Building, Apartment, PropertyClass, User
from app.schemas import (
    ProjectResponse, ProjectCreate, ProjectUpdate,
    BuildingResponse, BuildingCreate, BuildingUpdate,
    ApartmentResponse
)
from app.crud import CRUDProject, CRUDBuilding, CRUDApartment
from app.security import get_current_active_user, get_current_business

router = APIRouter(prefix="/projects", tags=["projects"])

project_crud = CRUDProject(Project)
building_crud = CRUDBuilding(Building)
apartment_crud = CRUDApartment(Apartment)


@router.post("", response_model=ProjectResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать новый проект
    
    Args:
        project_data: Данные для создания проекта
        
    Returns:
        ProjectResponse: Созданный проект
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await project_crud.create(db, project_data.dict())


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    city: Optional[str] = None,
    property_class: Optional[PropertyClass] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список проектов"""
    if city:
        return await project_crud.get_by_city(db, city)
    elif property_class:
        return await project_crud.get_by_class(db, property_class)
    return await project_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить проект по ID"""
    db_project = await project_crud.get(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Проект не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Project not found"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить проект
    
    Args:
        project_id: ID проекта
        project_data: Данные для обновления
        
    Returns:
        ProjectResponse: Обновленный проект
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Проект не найден
        400: Bad Request - Некорректные данные
    """
    db_project = await project_crud.get(db, project_id)
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return await project_crud.update(db, db_project, project_data.dict(exclude_unset=True))


@router.delete("/{project_id}", responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Проект не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Project not found"
                }
            }
        }
    },
    200: {
        "description": "Проект успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "Project deleted"
                }
            }
        }
    }
})
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить проект
    
    Args:
        project_id: ID проекта
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Проект не найден
    """
    if not await project_crud.delete(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return {"message": "Project deleted"}


@router.post("/{project_id}/buildings", response_model=BuildingResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Проект не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Project not found"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
async def create_building(
    project_id: int,
    building_data: BuildingCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать новый корпус в проекте
    
    Args:
        project_id: ID проекта
        building_data: Данные для создания корпуса
        
    Returns:
        BuildingResponse: Созданный корпус
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Проект не найден
        400: Bad Request - Некорректные данные
    """
    # Проверяем существование проекта
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    building_dict = building_data.dict()
    building_dict["project_id"] = project_id
    return await building_crud.create(db, building_dict)


@router.get("/{project_id}/buildings", response_model=List[BuildingResponse])
async def get_project_buildings(
    project_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список корпусов проекта"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return await building_crud.get_by_project(db, project_id)


@router.get("/{project_id}/buildings/{building_id}", response_model=BuildingResponse)
async def get_building(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить корпус по ID"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return db_building


@router.put("/{project_id}/buildings/{building_id}", response_model=BuildingResponse, responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Проект или корпус не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Project not found"
                }
            }
        }
    },
    400: {
        "description": "Некорректные данные",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Validation error"
                }
            }
        }
    }
})
async def update_building(
    project_id: int,
    building_id: int,
    building_data: BuildingUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Обновить корпус
    
    Args:
        project_id: ID проекта
        building_id: ID корпуса
        building_data: Данные для обновления
        
    Returns:
        BuildingResponse: Обновленный корпус
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Проект или корпус не найден
        400: Bad Request - Некорректные данные
    """
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    return await building_crud.update(db, db_building, building_data.dict(exclude_unset=True))


@router.delete("/{project_id}/buildings/{building_id}", responses={
    401: {
        "description": "Не авторизован",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Could not validate credentials"
                }
            }
        }
    },
    403: {
        "description": "Недостаточно прав",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Operation not permitted"
                }
            }
        }
    },
    404: {
        "description": "Проект или корпус не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Project not found"
                }
            }
        }
    },
    200: {
        "description": "Корпус успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "Building deleted"
                }
            }
        }
    }
})
async def delete_building(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить корпус
    
    Args:
        project_id: ID проекта
        building_id: ID корпуса
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Проект или корпус не найден
    """
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db_building = await building_crud.get(db, building_id)
    if not db_building or db_building.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    await building_crud.delete(db, building_id)
    return {"message": "Building deleted"}


@router.get("/{project_id}/buildings/{building_id}/apartments", response_model=List[ApartmentResponse])
async def get_building_apartments(
    project_id: int,
    building_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список квартир в корпусе"""
    if not await project_crud.get(db, project_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if not await building_crud.get(db, building_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Building not found"
        )
    
    return await apartment_crud.get_by_building(db, building_id) 