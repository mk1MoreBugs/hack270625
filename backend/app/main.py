from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings
from app.database import create_db_and_tables
from app.api import apartments, dynamic_pricing, developers, projects
import secrets


security = HTTPBasic()


def verify_docs_access(credentials: HTTPBasicCredentials = Depends(security)):
    """Проверяет доступ к документации"""
    is_username_correct = secrets.compare_digest(
        credentials.username.encode("utf8"),
        settings.docs_username.encode("utf8")
    )
    is_password_correct = secrets.compare_digest(
        credentials.password.encode("utf8"),
        settings.docs_password.encode("utf8")
    )
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan контекст для инициализации и очистки"""
    # Startup
    await create_db_and_tables()
    print("🚀 Приложение Недвижимость 4.0 запущено!")
    print(f"📚 Документация API: http://localhost:8000/docs")
    print(f"🔍 ReDoc: http://localhost:8000/redoc")
    
    yield
    
    # Shutdown
    print("🛑 Приложение Недвижимость 4.0 остановлено!")


# Создаем FastAPI приложение
app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    lifespan=lifespan,
    description="""
    🏠 **Недвижимость 4.0** - Платформа для динамического ценообразования недвижимости
    
    ## Возможности
    
    ### Для покупателей:
    - 📍 Цифровая карта России с новостройками
    - 🏢 Каталог проектов с полной информацией
    - 🤖 ИИ-подбор квартир
    - 💰 Динамическое ценообразование
    - 🎁 Акции и скидки
    - 📅 Онлайн-бронирование
    
    ### Для застройщиков:
    - 🏢 Личный кабинет с CRM
    - 🔗 Интеграция с внешними CRM
    - 📊 Аналитика спроса
    - 🔄 Автоматическое обновление остатков
    
    ### Для ассоциации застройщиков:
    - ✅ Модерация контента
    - 🛡️ Контроль сделок
    - 📈 Аналитика рынка
    
    ## Динамическое ценообразование
    
    Алгоритм автоматически изменяет цены квартир на основе:
    - 👀 Просмотров за 24 часа
    - 👤 Лидов за 24 часа  
    - 📅 Бронирований за 24 часа
    - 📊 Дней на сайте
    
    Цены изменяются в пределах ±7% от базовой стоимости.
    """,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    #docs_url=None,  # Отключаем стандартные эндпоинты
    #redoc_url=None  # Отключаем стандартные эндпоинты
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(apartments.router, prefix=settings.api_v1_str)
app.include_router(dynamic_pricing.router, prefix=settings.api_v1_str)
app.include_router(developers.router, prefix=settings.api_v1_str)
app.include_router(projects.router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "🏠 Добро пожаловать в Недвижимость 4.0!",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": f"{settings.api_v1_str}/"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {
        "status": "healthy",
        "service": "Недвижимость 4.0",
        "version": settings.version,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Создаем защищенные эндпоинты для документации
@app.get("/docs", include_in_schema=False)
async def get_swagger_ui_html(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт для Swagger UI"""
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        title=f"{settings.project_name} - Swagger UI"
    )

@app.get("/redoc", include_in_schema=False)
async def get_redoc_html(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт для ReDoc"""
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        title=f"{settings.project_name} - ReDoc"
    )

@app.get(f"{settings.api_v1_str}/openapi.json", include_in_schema=False)
async def get_openapi_json(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт для OpenAPI JSON"""
    return app.openapi()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 