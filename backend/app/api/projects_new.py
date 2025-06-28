from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID

from app.database import get_async_session
from app.models import Project, Developer
from app.security import get_current_user, get_current_admin_user
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate, Message

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=List[ProjectRead])
async def get_projects(
    *,
    session: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
    developer_id: Optional[UUID] = None,
    name: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_desc: bool = True
):
    """
    Get list of projects with optional filtering and sorting.
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - developer_id: Filter by developer ID
    - name: Filter by project name (case-insensitive partial match)
    - status: Filter by project status
    - sort_by: Sort field (created_at, name, status)
    - sort_desc: Sort in descending order
        
    Returns:
    - List of projects matching the criteria
    """
    query = select(Project)
    
    if developer_id:
        query = query.where(Project.developer_id == developer_id)
    if name:
        query = query.where(Project.name.ilike(f"%{name}%"))
    if status:
        query = query.where(Project.status == status)
        
    if sort_by == "created_at":
        query = query.order_by(Project.created_at.desc() if sort_desc else Project.created_at)
    elif sort_by == "name":
        query = query.order_by(Project.name.desc() if sort_desc else Project.name)
    elif sort_by == "status":
        query = query.order_by(Project.status.desc() if sort_desc else Project.status)
        
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    *,
    session: Session = Depends(get_async_session),
    project_id: UUID
):
    """
    Get a specific project by ID.
    
    Parameters:
    - project_id: UUID of the project
        
    Returns:
    - Project details
        
    Raises:
    - 404: Project not found
    """
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("", response_model=ProjectRead, status_code=201)
async def create_project(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    project: ProjectCreate
):
    """
    Create a new project.
    
    Parameters:
    - project: Project data
        
    Returns:
    - Created project
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 404: Developer not found
    - 409: Project with same external_id already exists
    """
    # Check if developer exists
    result = await session.execute(
        select(Developer).where(Developer.id == project.developer_id)
    )
    developer = result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    
    # Check for external_id uniqueness
    if project.external_id:
        result = await session.execute(
            select(Project).where(Project.external_id == project.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Project with this external_id already exists"
            )
    
    db_project = Project.from_orm(project)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    project_id: UUID,
    project: ProjectUpdate
):
    """
    Update a project.
    
    Parameters:
    - project_id: UUID of the project to update
    - project: Updated project data
        
    Returns:
    - Updated project
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 404: Project not found
    - 404: Developer not found
    - 409: External ID conflict with existing project
    """
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    db_project = result.scalar_one_or_none()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if new developer exists
    if project.developer_id and project.developer_id != db_project.developer_id:
        result = await session.execute(
            select(Developer).where(Developer.id == project.developer_id)
        )
        developer = result.scalar_one_or_none()
        if not developer:
            raise HTTPException(status_code=404, detail="Developer not found")
    
    # Check for external_id uniqueness
    if project.external_id and project.external_id != db_project.external_id:
        result = await session.execute(
            select(Project).where(Project.external_id == project.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Project with this external_id already exists"
            )
    
    project_data = project.dict(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    
    await session.commit()
    await session.refresh(db_project)
    return db_project


@router.delete("/{project_id}", response_model=Message)
async def delete_project(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    project_id: UUID
):
    """
    Delete a project.
    
    Parameters:
    - project_id: UUID of the project to delete
        
    Returns:
    - Success message
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 404: Project not found
    """
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await session.delete(project)
    await session.commit()
    
    return Message(message="Project successfully deleted") 