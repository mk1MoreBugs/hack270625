from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    # Database Configuration
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "real_estate_db"
    postgres_user: str = "real_estate_user"
    postgres_password_file: str = "./db_password.txt"
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Dynamic Pricing
    elasticity_cap: float = 3.0
    price_max_shift: float = 7.0
    price_update_interval: int = 3600
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Недвижимость 4.0"
    version: str = "1.0.0"
    
    @property
    def database_url(self) -> str:
        """Формирует URL для подключения к базе данных"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        """Формирует URL для подключения к Redis"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def postgres_password(self):
        """Загружает пароль от базы данных из файла"""
        with open(self.postgres_password_file, encoding="utf-8") as f:
            return f.readline().strip()
    
settings = Settings()
