from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings
from app.database import create_db_and_tables
from app.api import (
    properties, developers, projects, buildings, 
    addresses, prices, media, dynamic_pricing, users, bookings, 
    promotions, analytics, map, ai_matching, webhooks, auth
)
import secrets


security = HTTPBasic()


def verify_docs_access(credentials: HTTPBasicCredentials = Depends(security)):
    """Проверка доступа к документации API"""
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
    """Жизненный цикл приложения для инициализации и очистки"""
    # Startup
    await create_db_and_tables()
    print("🚀 Real Estate 4.0 API запущен!")
    print(f"📚 Документация API: http://localhost:8000/docs")
    print(f"🔍 ReDoc: http://localhost:8000/redoc")
    
    yield
    
    # Shutdown
    print("🛑 Real Estate 4.0 API остановлен!")


# Create FastAPI application
app = FastAPI(
    title="Real Estate 4.0 API",
    description="API для платформы динамического ценообразования в сфере недвижимости",
    version=settings.version,
    lifespan=lifespan,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    #docs_url=None,  # Disable default endpoints
    #redoc_url=None  # Disable default endpoints
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router, prefix=settings.api_v1_str)
app.include_router(users.router, prefix=settings.api_v1_str)
app.include_router(developers.router, prefix=settings.api_v1_str)
app.include_router(projects.router, prefix=settings.api_v1_str)
app.include_router(buildings.router, prefix=settings.api_v1_str)
app.include_router(properties.router, prefix=settings.api_v1_str)
app.include_router(addresses.router, prefix=settings.api_v1_str)
app.include_router(prices.router, prefix=settings.api_v1_str)
app.include_router(media.router, prefix=settings.api_v1_str)
app.include_router(bookings.router, prefix=settings.api_v1_str)
app.include_router(promotions.router, prefix=settings.api_v1_str)
app.include_router(analytics.router, prefix=settings.api_v1_str)
app.include_router(dynamic_pricing.router, prefix=settings.api_v1_str)
app.include_router(ai_matching.router, prefix=settings.api_v1_str)
app.include_router(map.router, prefix=settings.api_v1_str)
app.include_router(webhooks.router, prefix=settings.api_v1_str)


@app.get(
    "/",
    tags=["default"],
    summary="Корневой эндпоинт",
    description="Возвращает основную информацию о сервисе"
)
async def root():
    """Корневой эндпоинт"""
    return {
        "name": settings.project_name,
        "version": settings.version,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get(
    "/health",
    tags=["default"],
    summary="Проверка здоровья",
    description="Проверка работоспособности приложения"
)
async def health_check():
    """Проверка работоспособности приложения"""
    return {
        "status": "healthy",
        "service": settings.project_name,
        "version": settings.version,
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Create protected documentation endpoints
@app.get("/docs", include_in_schema=False)
async def get_swagger_ui_html(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт Swagger UI"""
    from fastapi.openapi.docs import get_swagger_ui_html
    return get_swagger_ui_html(
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        title=f"{settings.project_name} - Swagger UI"
    )


@app.get("/redoc", include_in_schema=False)
async def get_redoc_html(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт ReDoc"""
    from fastapi.openapi.docs import get_redoc_html
    return get_redoc_html(
        openapi_url=f"{settings.api_v1_str}/openapi.json",
        title=f"{settings.project_name} - ReDoc"
    )


@app.get(f"{settings.api_v1_str}/openapi.json", include_in_schema=False)
async def get_openapi_json(credentials: HTTPBasicCredentials = Depends(verify_docs_access)):
    """Защищенный эндпоинт OpenAPI JSON"""
    return app.openapi()
 