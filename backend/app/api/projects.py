from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.database import get_async_session
from app.models import Project, UserRole
from app.schemas import ProjectCreate, ProjectUpdate, ProjectRead
from app.security import get_current_user_role
from typing import List

router = APIRouter(prefix="/projects", tags=["projects"])

@router.get("/", response_model=List[ProjectRead],
            summary="Получить список проектов",
            description="Получение списка всех доступных проектов")
async def get_projects(
    session: AsyncSession = Depends(get_async_session)
) -> List[ProjectRead]:
    projects = await session.execute(select(Project))
    projects = projects.scalars().all()
    return [ProjectRead.from_orm(p) for p in projects]

@router.get("/{project_id}", response_model=ProjectRead,
            summary="Получить проект",
            description="Получение информации о конкретном проекте по его ID")
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    return ProjectRead.from_orm(project)

@router.post("/", response_model=ProjectRead,
             summary="Создать проект",
             description="Создание нового проекта (только для застройщиков)")
async def create_project(
    project_data: ProjectCreate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут создавать проекты"
        )
    
    project = Project(**project_data.dict())
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectRead.from_orm(project)

@router.put("/{project_id}", response_model=ProjectRead,
            summary="Обновить проект",
            description="Обновление информации о проекте (только для застройщиков)")
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
) -> ProjectRead:
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут обновлять проекты"
        )
    
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    
    for field, value in project_data.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    await session.commit()
    await session.refresh(project)
    return ProjectRead.from_orm(project)

@router.delete("/{project_id}",
               summary="Удалить проект",
               description="Удаление проекта (только для застройщиков)")
async def delete_project(
    project_id: int,
    current_user_role: UserRole = Depends(get_current_user_role),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user_role != UserRole.DEVELOPER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только застройщики могут удалять проекты"
        )
    
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )
    
    await session.delete(project)
    await session.commit()
    return {"message": "Проект успешно удален"} 