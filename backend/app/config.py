from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os
import secrets
from functools import cached_property


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Project info
    project_name: str = "Real Estate 4.0"
    version: str = "1.0.0"
    api_v1_str: str = "/api/v1"
    
    # Security
    secret_key: str = secrets.token_urlsafe(32)
    docs_username: str = "admin"  # Change in production!
    docs_password: str = "admin"  # Change in production!
    
    # Database
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "real_estate"
    
    # Debug mode
    debug: bool = True
    
    # CORS
    allowed_origins: list = ["*"]  # Change in production!

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
    
    # Documentation access
    docs_username: str = "admin"
    docs_password: str = "admin"
    
    @cached_property
    def database_url(self) -> str:
        """Get database URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        """Формирует URL для подключения к Redis"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    
settings = Settings()
 