from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict
from app.database import get_async_session
from app.models import WebhookInbox
from app.crud import webhook
from datetime import datetime

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/amo")
async def amo_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """Обработка вебхуков от AmoCRM"""
    payload = await request.json()
    
    # Сохраняем входящий вебхук
    webhook_data = {
        "source": "amo",
        "payload": payload,
        "received_at": datetime.utcnow(),
        "processed": False
    }
    await webhook.create(db, webhook_data)
    
    # TODO: Добавить асинхронную обработку вебхука
    return {"status": "received"}


@router.post("/bitrix")
async def bitrix_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """Обработка вебхуков от Битрикс24"""
    payload = await request.json()
    
    # Сохраняем входящий вебхук
    webhook_data = {
        "source": "bitrix",
        "payload": payload,
        "received_at": datetime.utcnow(),
        "processed": False
    }
    await webhook.create(db, webhook_data)
    
    # TODO: Добавить асинхронную обработку вебхука
    return {"status": "received"} 