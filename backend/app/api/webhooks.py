from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_async_session
from app.models import WebhookInbox, User
from app.schemas import WebhookResponse, WebhookCreate
from app.crud import CRUDWebhook
from app.security import get_current_active_user, get_current_business

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
webhook_crud = CRUDWebhook(WebhookInbox)


@router.post("", response_model=WebhookResponse, responses={
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
        WebhookResponse: Созданный вебхук
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        400: Bad Request - Некорректные данные
    """
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


@router.delete("/{webhook_id}", responses={
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
        "description": "Вебхук не найден",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Webhook not found"
                }
            }
        }
    },
    200: {
        "description": "Вебхук успешно удален",
        "content": {
            "application/json": {
                "example": {
                    "message": "Webhook deleted"
                }
            }
        }
    }
})
async def delete_webhook(
    webhook_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_business)
):
    """
    Удалить вебхук
    
    Args:
        webhook_id: ID вебхука
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        401: Unauthorized - Не авторизован
        403: Forbidden - Недостаточно прав
        404: Not Found - Вебхук не найден
    """
    if not await webhook_crud.delete(db, webhook_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Webhook not found"
        )
    return {"message": "Webhook deleted"} 