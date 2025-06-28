from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import AsyncSessionLocal
from app.services.stats_aggregator import StatsAggregatorService
from app.services.dynamic_pricing import DynamicPricingService
from app.crud import CRUDWorker
import asyncio
from typing import Dict, Any, List

# Создаем Celery приложение
celery_app = Celery(
    "real_estate_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.worker"]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
)


async def get_async_session() -> AsyncSession:
    """Получает асинхронную сессию для работы с базой данных"""


    celery_engine = create_async_engine(
        str(settings.database_url).replace("postgresql://", "postgresql+asyncpg://"),
        pool_size=5,
        max_overflow=10,
        )

    CelerySessionLocal = sessionmaker(
        bind=celery_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        )

    async with CelerySessionLocal() as session:
        return session


def format_stats_response(stats: Any) -> Dict[str, Any]:
    """Форматирует ответ для задачи обновления статистики"""
    return {
        "views_24h": stats.views_24h,
        "leads_24h": stats.leads_24h,
        "bookings_24h": stats.bookings_24h,
        "days_on_site": stats.days_on_site
    }


def format_pricing_response(result: Any) -> Dict[str, Any]:
    """Форматирует ответ для задачи обновления цен"""
    return {
        "property_id": result.property_id,
        "old_price": result.old_price,
        "new_price": result.new_price,
        "price_change_percent": result.price_change_percent,
        "demand_score": result.demand_score
    }


@celery_app.task
def update_stats_task():
    """Задача для обновления статистики всех объектов недвижимости"""
    async def _update_stats():
        session = await get_async_session()
        try:
            worker_crud = CRUDWorker(session)
            properties = await worker_crud.get_properties_for_stats()
            
            if not properties:
                return {
                    "status": "success",
                    "message": "Нет объектов недвижимости для обновления статистики"
                }
            
            aggregator = StatsAggregatorService(session)
            updated_stats = []
            
            for property_obj in properties:
                try:
                    stats = await aggregator.update_property_stats(property_obj.id)
                    updated_stats.append(format_stats_response(stats))
                except Exception as e:
                    print(f"Ошибка при обновлении статистики объекта {property_obj.id}: {e}")
                    continue
            
            return {
                "status": "success",
                "updated_properties": len(updated_stats),
                "stats": updated_stats,
                "message": f"Статистика обновлена для {len(updated_stats)} объектов недвижимости"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Ошибка при обновлении статистики"
            }
        finally:
            await session.close()
    
    return asyncio.run(_update_stats())


@celery_app.task
def update_single_property_stats_task(property_id: str):
    """Задача для обновления статистики конкретного объекта недвижимости"""
    async def _update_single_stats():
        session = await get_async_session()
        try:
            worker_crud = CRUDWorker(session)
            property_obj = await worker_crud.get_property_for_task(property_id)
            
            if not property_obj:
                return {
                    "status": "error",
                    "property_id": property_id,
                    "message": f"Объект недвижимости {property_id} не найден"
                }
            
            aggregator = StatsAggregatorService(session)
            stats = await aggregator.update_property_stats(property_id)
            
            return {
                "status": "success",
                "property_id": property_id,
                "stats": format_stats_response(stats),
                "message": f"Статистика обновлена для объекта недвижимости {property_id}"
            }
        except Exception as e:
            return {
                "status": "error",
                "property_id": property_id,
                "error": str(e),
                "message": f"Ошибка при обновлении статистики объекта недвижимости {property_id}"
            }
        finally:
            await session.close()
    
    return asyncio.run(_update_single_stats())


@celery_app.task
def update_dynamic_pricing_task():
    """Задача для обновления цен всех объектов недвижимости"""
    async def _update_pricing():
        session = await get_async_session()
        try:
            worker_crud = CRUDWorker(session)
            properties = await worker_crud.get_properties_for_pricing()
            
            if not properties:
                return {
                    "status": "success",
                    "message": "Нет объектов недвижимости для обновления цен"
                }
            
            pricing_service = DynamicPricingService(session)
            results = []
            
            for property_obj in properties:
                try:
                    result = await pricing_service.update_property_price(property_obj)
                    if result:
                        results.append(format_pricing_response(result))
                        await worker_crud.update_property_price_timestamp(property_obj.id)
                except Exception as e:
                    print(f"Ошибка при обновлении цены объекта {property_obj.id}: {e}")
                    continue
            
            return {
                "status": "success",
                "updated_properties": len(results),
                "results": results,
                "message": f"Цены обновлены для {len(results)} объектов недвижимости"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": "Ошибка при обновлении цен"
            }
        finally:
            await session.close()
    
    return asyncio.run(_update_pricing())


@celery_app.task
def update_single_property_price_task(property_id: str):
    """Задача для обновления цены конкретного объекта недвижимости"""
    async def _update_single_price():
        session = await get_async_session()
        try:
            worker_crud = CRUDWorker(session)
            property_obj = await worker_crud.get_property_for_task(property_id)
            
            if not property_obj:
                return {
                    "status": "error",
                    "property_id": property_id,
                    "message": f"Объект недвижимости {property_id} не найден"
                }
            
            pricing_service = DynamicPricingService(session)
            result = await pricing_service.update_property_price(property_obj)
            
            if result:
                await worker_crud.update_property_price_timestamp(property_obj.id)
                return {
                    "status": "success",
                    "property_id": property_id,
                    **format_pricing_response(result),
                    "message": f"Цена обновлена для объекта недвижимости {property_id}"
                }
            else:
                return {
                    "status": "no_change",
                    "property_id": property_id,
                    "message": f"Цена для объекта недвижимости {property_id} не требует изменений"
                }
        except Exception as e:
            return {
                "status": "error",
                "property_id": property_id,
                "error": str(e),
                "message": f"Ошибка при обновлении цены объекта недвижимости {property_id}"
            }
        finally:
            await session.close()
    
    return asyncio.run(_update_single_price())


# Периодические задачи
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Настройка периодических задач"""
    # Обновление статистики каждую минуту
    sender.add_periodic_task(
        60.0,  # каждые 60 секунд
        update_stats_task.s(),
        name="update-stats-every-minute"
    )
    
    # Обновление цен каждый час
    sender.add_periodic_task(
        3600.0,  # каждые 3600 секунд (1 час)
        update_dynamic_pricing_task.s(),
        name="update-pricing-every-hour"
    )


if __name__ == "__main__":
    celery_app.start() 