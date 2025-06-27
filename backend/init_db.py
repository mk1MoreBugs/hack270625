#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных
"""
import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.init_db import main
    import asyncio
    
    asyncio.run(main()) 