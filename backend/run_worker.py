#!/usr/bin/env python3
"""
Скрипт для запуска Celery worker
"""
import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.worker import celery_app
    celery_app.start() 