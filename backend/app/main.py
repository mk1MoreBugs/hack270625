from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings
from app.database import create_db_and_tables
from app.api import (
    auth, buildings, properties, users,
    addresses, analytics, bookings, developers,
    dynamic_pricing, map, media, prices, promotions,
    webhooks, projects
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
    title="Real Estate API",
    description="API для работы с недвижимостью",
    version="1.0.0",
    lifespan=lifespan,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
    #docs_url=None,  # Disable default endpoints
    #redoc_url=None  # Disable default endpoints
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(developers.router, prefix="/api/v1")
app.include_router(buildings.router, prefix="/api/v1")
app.include_router(properties.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(addresses.router, prefix="/api/v1")
app.include_router(prices.router, prefix="/api/v1")
app.include_router(media.router, prefix="/api/v1")
app.include_router(bookings.router, prefix="/api/v1")
app.include_router(promotions.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(dynamic_pricing.router, prefix="/api/v1")
app.include_router(map.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в API для работы с недвижимостью",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


@app.get("/tbexport")
async def tbexport():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <div>
                <iframe src="tbexport/tbexport.html" allowfullscreen="true"></iframe>
                <iframe src="tbexport/tbexport.mview" allowfullscreen="true"></iframe>
            </div>
        </body>
    </html>
    """


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
 