from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
import secrets


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Database Configuration
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "app"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    
    # Redis Configuration
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Security
    secret_key: str = secrets.token_urlsafe(32)
    
    # JWT settings
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30
    
    # Bcrypt settings
    bcrypt_rounds: int = 12  # Количество раундов хеширования
    
    # Dynamic Pricing
    elasticity_cap: float = 3.0
    price_max_shift: float = 7.0
    price_update_interval: int = 3600
    
    # Celery
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Недвижимость 4.0"
    version: str = "1.0.0"
    
    # Documentation access
    docs_username: str = "admin"
    docs_password: str = "change_this"
    
    @property
    def database_url(self) -> str:
        """Формирует URL для подключения к базе данных"""
        url = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        print(url)
        return url
    
    @property
    def redis_url(self) -> str:
        """Формирует URL для подключения к Redis"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    
settings = Settings()
 