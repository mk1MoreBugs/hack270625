from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional

from app.database import get_async_session
from app.models import Developer
from app.security import get_current_user, get_current_admin_user
from app.schemas import DeveloperCreate, DeveloperRead, DeveloperUpdate, Message

router = APIRouter(prefix="/developers", tags=["developers"])


@router.get("", response_model=List[DeveloperRead])
async def get_developers(
    *,
    session: Session = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    sort_by: Optional[str] = "created_at",
    sort_desc: bool = True
):
    """
    Get list of developers with optional filtering and sorting.
    
    Parameters:
    - skip: Number of records to skip (pagination)
    - limit: Maximum number of records to return
    - name: Filter by developer name (case-insensitive partial match)
    - sort_by: Sort field (created_at, name)
    - sort_desc: Sort in descending order
    
    Returns:
    - List of developers matching the criteria
    """
    query = select(Developer)
    
    if name:
        query = query.where(Developer.name.ilike(f"%{name}%"))
        
    if sort_by == "created_at":
        query = query.order_by(Developer.created_at.desc() if sort_desc else Developer.created_at)
    elif sort_by == "name":
        query = query.order_by(Developer.name.desc() if sort_desc else Developer.name)
        
    query = query.offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/{developer_id}", response_model=DeveloperRead)
async def get_developer(
    *,
    session: Session = Depends(get_async_session),
    developer_id: int
):
    """
    Get a specific developer by ID.
    
    Parameters:
    - developer_id: id of the developer
    
    Returns:
    - Developer details
    
    Raises:
    - 404: Developer not found
    """
    result = await session.execute(
        select(Developer).where(Developer.id == developer_id)
    )
    developer = result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    return developer


@router.post("", response_model=DeveloperRead, status_code=201)
async def create_developer(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    developer: DeveloperCreate
):
    """
    Create a new developer.
    
    Parameters:
    - developer: Developer data
        
    Returns:
    - Created developer
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 409: Developer with same external_id already exists
    """
    # Check for external_id uniqueness
    if developer.external_id:
        result = await session.execute(
            select(Developer).where(Developer.external_id == developer.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Developer with this external_id already exists"
            )
    
    db_developer = Developer.from_orm(developer)
    session.add(db_developer)
    await session.commit()
    await session.refresh(db_developer)
    return db_developer


@router.put("/{developer_id}", response_model=DeveloperRead)
async def update_developer(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    developer_id: int,
    developer: DeveloperUpdate
):
    """
    Update a developer.
    
    Parameters:
    - developer_id: id of the developer to update
    - developer: Updated developer data
        
    Returns:
    - Updated developer
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 404: Developer not found
    - 409: External ID conflict with existing developer
    """
    result = await session.execute(
        select(Developer).where(Developer.id == developer_id)
    )
    db_developer = result.scalar_one_or_none()
    if not db_developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    
    # Check for external_id uniqueness
    if developer.external_id and developer.external_id != db_developer.external_id:
        result = await session.execute(
            select(Developer).where(Developer.external_id == developer.external_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="Developer with this external_id already exists"
            )
    
    developer_data = developer.dict(exclude_unset=True)
    for key, value in developer_data.items():
        setattr(db_developer, key, value)
    
    session.add(db_developer)
    await session.commit()
    await session.refresh(db_developer)
    return db_developer


@router.delete("/{developer_id}", response_model=Message)
async def delete_developer(
    *,
    session: Session = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user),
    developer_id: int
):
    """
    Delete a developer.
    
    Parameters:
    - developer_id: id of the developer to delete
        
    Returns:
    - Success message
    
    Security:
    - Requires admin role
        
    Raises:
    - 401: Unauthorized
    - 403: Forbidden (not admin)
    - 404: Developer not found
    """
    result = await session.execute(
        select(Developer).where(Developer.id == developer_id)
    )
    developer = result.scalar_one_or_none()
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")
    
    await session.delete(developer)
    await session.commit()
    
    return Message(message="Developer successfully deleted") 