from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_async_session
from app.models import Apartment, DynamicPricingConfig
from app.schemas import (
    DynamicPricingConfigResponse, DynamicPricingConfigCreate,
    DynamicPricingConfigUpdate, DynamicPricingResult
)
from app.services.dynamic_pricing import DynamicPricingService
from app.crud import apartment, dynamic_pricing_config
from datetime import datetime, timedelta

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic-pricing"])


@router.get("/config", response_model=DynamicPricingConfigResponse)
async def get_dynamic_pricing_config(db: AsyncSession = Depends(get_async_session)):
    """Получить текущую конфигурацию динамического ценообразования"""
    config = await dynamic_pricing_config.get_active(db)
    
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    return config


@router.post("/config", response_model=DynamicPricingConfigResponse)
async def create_dynamic_pricing_config(
    config_data: DynamicPricingConfigCreate,
    db: AsyncSession = Depends(get_async_session)
):
    """Создать новую конфигурацию динамического ценообразования"""
    # Отключаем все существующие конфигурации
    existing_configs = await dynamic_pricing_config.get_multi(db, skip=0, limit=100)
    for config in existing_configs:
        await dynamic_pricing_config.update(db, config, {"enabled": False})
    
    # Создаем новую конфигурацию
    config_dict = config_data.dict()
    config = await dynamic_pricing_config.create(db, config_dict)
    
    return config


@router.put("/config/{config_id}", response_model=DynamicPricingConfigResponse)
async def update_dynamic_pricing_config(
    config_id: int,
    config_data: DynamicPricingConfigUpdate,
    db: AsyncSession = Depends(get_async_session)
):
    """Обновить конфигурацию динамического ценообразования"""
    config = await dynamic_pricing_config.get(db, config_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Конфигурация не найдена")
    
    update_data = config_data.dict(exclude_unset=True)
    config = await dynamic_pricing_config.update(db, config, update_data)
    
    return config


@router.post("/update-all")
async def update_all_prices(db: AsyncSession = Depends(get_async_session)):
    """Запустить обновление цен для всех квартир"""
    # Запускаем обновление цен напрямую
    pricing_service = DynamicPricingService(db)
    results = await pricing_service.update_all_apartment_prices()
    
    return {
        "message": "Обновление цен завершено",
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
        ]
    }


@router.post("/update/{apartment_id}")
async def update_apartment_price(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Запустить обновление цены для конкретной квартиры"""
    # Проверяем, что квартира существует
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    # Запускаем обновление цены напрямую
    pricing_service = DynamicPricingService(db)
    result = await pricing_service.update_apartment_price(apartment_obj)
    
    if result:
        return {
            "message": f"Цена обновлена для квартиры {apartment_id}",
            "apartment_id": apartment_id,
            "old_price": result.old_price,
            "new_price": result.new_price,
            "price_change_percent": result.price_change_percent,
            "demand_score": result.demand_score
        }
    else:
        return {
            "message": f"Цена для квартиры {apartment_id} не требует изменений",
            "apartment_id": apartment_id
        }


@router.get("/calculate/{apartment_id}", response_model=DynamicPricingResult)
async def calculate_apartment_price_change(
    apartment_id: int,
    db: AsyncSession = Depends(get_async_session)
):
    """Рассчитать изменение цены для квартиры без применения"""
    apartment_obj = await apartment.get(db, apartment_id)
    
    if not apartment_obj:
        raise HTTPException(status_code=404, detail="Квартира не найдена")
    
    pricing_service = DynamicPricingService(db)
    
    # Проверяем, можно ли обновлять цену
    if not await pricing_service.should_update_price(apartment_obj):
        raise HTTPException(
            status_code=400,
            detail="Цена не может быть обновлена (ограничения по времени или недавнее бронирование)"
        )
    
    # Вычисляем изменение цены
    price_change_percent = await pricing_service.calculate_price_change(apartment_obj)
    if price_change_percent is None or price_change_percent == 0:
        raise HTTPException(
            status_code=400,
            detail="Цена не требует изменений"
        )
    
    # Вычисляем новую цену
    price_change_multiplier = 1 + price_change_percent / 100
    new_price = apartment_obj.current_price * price_change_multiplier
    new_price = pricing_service.apply_price_limits(apartment_obj, new_price)
    
    # Вычисляем demand_score
    demand_score = await pricing_service.calculate_demand_score(apartment_obj)
    median_demand = await pricing_service.get_cluster_median_demand(apartment_obj)
    demand_normalized = demand_score / median_demand if median_demand > 0 else 0
    
    # Генерируем описание
    description = await pricing_service.generate_price_change_description(apartment_obj, price_change_percent)
    
    return DynamicPricingResult(
        apartment_id=apartment_obj.id,
        old_price=apartment_obj.current_price,
        new_price=new_price,
        price_change_percent=price_change_percent,
        demand_score=demand_score,
        demand_normalized=demand_normalized,
        reason="calculated",
        description=description
    )


@router.get("/stats")
async def get_dynamic_pricing_stats(db: AsyncSession = Depends(get_async_session)):
    """Получить статистику динамического ценообразования"""
    # Количество квартир с измененными ценами за последние 24 часа
    from app.models import PriceHistory, PriceChangeReason
    from app.crud import price_history
    
    yesterday = datetime.utcnow() - timedelta(hours=24)
    
    recent_price_changes = await price_history.get_recent_changes(db, hours=24)
    
    # Статистика по изменениям цен
    price_increases = len([pc for pc in recent_price_changes if pc.new_price > pc.old_price])
    price_decreases = len([pc for pc in recent_price_changes if pc.new_price < pc.old_price])
    
    # Среднее изменение цены
    if recent_price_changes:
        avg_change_percent = sum(
            ((pc.new_price - pc.old_price) / pc.old_price) * 100
            for pc in recent_price_changes
        ) / len(recent_price_changes)
    else:
        avg_change_percent = 0
    
    return {
        "total_price_changes_24h": len(recent_price_changes),
        "price_increases_24h": price_increases,
        "price_decreases_24h": price_decreases,
        "average_change_percent_24h": round(avg_change_percent, 2),
        "last_update": datetime.utcnow().isoformat()
    } 