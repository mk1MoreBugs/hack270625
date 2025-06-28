from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.database import get_async_session
from app.models import WebhookInbox, User
from app.schemas import WebhookRead, WebhookCreate, Message
from app.crud import CRUDWebhook
from app.security import get_current_active_user, get_current_business, get_current_admin_user

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
webhook_crud = CRUDWebhook(WebhookInbox)


@router.post("", response_model=WebhookRead, responses={
    201: {"description": "Вебхук создан"},
    400: {"description": "Некорректные данные"},
    401: {"description": "Не авторизован"},
    403: {"description": "Нет прав доступа"}
})
async def create_webhook(
    webhook_data: WebhookCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Создать новый вебхук
    
    Args:
        webhook_data: Данные для создания вебхука
        
    Returns:
        WebhookRead: Созданный вебхук
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
    return await webhook_crud.create(db, webhook_data.dict())


@router.get("", response_model=List[WebhookRead])
async def get_webhooks(
    source: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить список вебхуков"""
    if source:
        return await webhook_crud.get_unprocessed(db, source)
    return await webhook_crud.get_multi(db, skip=skip, limit=limit)


@router.get("/{webhook_id}", response_model=WebhookRead)
async def get_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Получить вебхук по ID"""
    db_webhook = await webhook_crud.get(db, webhook_id)
    if not db_webhook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    return db_webhook


@router.delete("/{webhook_id}", response_model=Message)
async def delete_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_async_session),
    _: dict = Depends(get_current_admin_user)
):
    """Delete a webhook"""
    webhook = await webhook_crud.get(db, webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    await webhook_crud.delete(db, webhook_id)
    return Message(message="Webhook deleted") 