from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import AsyncSessionLocal
from app.services.stats_aggregator import StatsAggregatorService
from app.services.dynamic_pricing import DynamicPricingService
from app.crud import apartment
import asyncio

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
    async with AsyncSessionLocal() as session:
        return session


@celery_app.task
def update_stats_task():
    """Задача для обновления статистики всех квартир"""
    async def _update_stats():
        session = await get_async_session()
        try:
            aggregator = StatsAggregatorService(session)
            updated_stats = await aggregator.update_all_apartment_stats()
            return {
                "status": "success",
                "updated_apartments": len(updated_stats),
                "message": f"Статистика обновлена для {len(updated_stats)} квартир"
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
def update_single_apartment_stats_task(apartment_id: int):
    """Задача для обновления статистики конкретной квартиры"""
    async def _update_single_stats():
        session = await get_async_session()
        try:
            aggregator = StatsAggregatorService(session)
            stats = await aggregator.update_apartment_stats(apartment_id)
            return {
                "status": "success",
                "apartment_id": apartment_id,
                "stats": {
                    "views_24h": stats.views_24h,
                    "leads_24h": stats.leads_24h,
                    "bookings_24h": stats.bookings_24h,
                    "days_on_site": stats.days_on_site
                },
                "message": f"Статистика обновлена для квартиры {apartment_id}"
            }
        except Exception as e:
            return {
                "status": "error",
                "apartment_id": apartment_id,
                "error": str(e),
                "message": f"Ошибка при обновлении статистики квартиры {apartment_id}"
            }
        finally:
            await session.close()
    
    return asyncio.run(_update_single_stats())


@celery_app.task
def update_dynamic_pricing_task():
    """Задача для обновления цен всех квартир"""
    async def _update_pricing():
        session = await get_async_session()
        try:
            pricing_service = DynamicPricingService(session)
            results = await pricing_service.update_all_apartment_prices()
            
            return {
                "status": "success",
                "updated_apartments": len(results),
                "results": [
                    {
                        "apartment_id": result.apartment_id,
                        "old_price": result.old_price,
                        "new_price": result.new_price,
                        "price_change_percent": result.price_change_percent,
                        "demand_score": result.demand_score
                    }
                    for result in results
                ],
                "message": f"Цены обновлены для {len(results)} квартир"
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
def update_single_apartment_price_task(apartment_id: int):
    """Задача для обновления цены конкретной квартиры"""
    async def _update_single_price():
        session = await get_async_session()
        try:
            apartment_obj = await apartment.get(session, apartment_id)
            if not apartment_obj:
                return {
                    "status": "error",
                    "apartment_id": apartment_id,
                    "error": "Квартира не найдена",
                    "message": f"Квартира {apartment_id} не найдена"
                }
            
            pricing_service = DynamicPricingService(session)
            result = await pricing_service.update_apartment_price(apartment_obj)
            
            if result:
                return {
                    "status": "success",
                    "apartment_id": apartment_id,
                    "old_price": result.old_price,
                    "new_price": result.new_price,
                    "price_change_percent": result.price_change_percent,
                    "demand_score": result.demand_score,
                    "message": f"Цена обновлена для квартиры {apartment_id}"
                }
            else:
                return {
                    "status": "no_change",
                    "apartment_id": apartment_id,
                    "message": f"Цена для квартиры {apartment_id} не требует изменений"
                }
        except Exception as e:
            return {
                "status": "error",
                "apartment_id": apartment_id,
                "error": str(e),
                "message": f"Ошибка при обновлении цены квартиры {apartment_id}"
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