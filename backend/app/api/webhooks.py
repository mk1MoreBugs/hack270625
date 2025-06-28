from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import WebhookInbox
from app.schemas import WebhookResponse, WebhookCreate
from app.crud import CRUDWebhook

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
webhook_crud = CRUDWebhook(WebhookInbox)


@router.post("", response_model=WebhookResponse)
async def create_webhook(
    webhook_data: WebhookCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новый вебхук"""
    return await webhook_crud.create(db, webhook_data.dict())


@router.get("", response_model=List[WebhookResponse])
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


@router.get("/{webhook_id}", response_model=WebhookResponse)
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


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Удалить вебхук"""
    if not await webhook_crud.delete(db, webhook_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    return {"message": "Webhook deleted"} 