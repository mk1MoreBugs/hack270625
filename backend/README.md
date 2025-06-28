# 🏠 Недвижимость 4.0 - Backend

Платформа для динамического ценообразования недвижимости с использованием FastAPI, PostgreSQL и Celery.

## 🚀 Возможности

### Для покупателей:
- 📍 Цифровая карта России с новостройками
- 🏢 Каталог проектов с полной информацией
- 🤖 ИИ-подбор квартир
- 💰 **Динамическое ценообразование** (как в авиабилетах!)
- 🎁 Акции и скидки
- 📅 Онлайн-бронирование

### Для застройщиков:
- 🏢 Личный кабинет с CRM
- 🔗 Интеграция с внешними CRM (Битрикс24, AMO CRM)
- 📊 Аналитика спроса
- 🔄 Автоматическое обновление остатков

### Для ассоциации застройщиков:
- ✅ Модерация контента
- 🛡️ Контроль сделок
- 📈 Аналитика рынка

## 🧠 Алгоритм динамического ценообразования

Цены автоматически изменяются на основе:

1. **Спрос (demand_score):**
   ```
   demand = 0.5 × views_24h + 2 × leads_24h + 5 × bookings_24h
   demand_normalized = demand / median_demand_in_cluster
   ```

2. **Правила изменения цены:**
   - `demand_normalized > 1.3` → цена повышается на +Δ%
   - `demand_normalized < 0.7` и `days_on_site > 14` → цена снижается на -Δ%
   - Иначе → цена не меняется

3. **Ограничения:**
   - Максимальное изменение: ±7% от базовой цены
   - Не чаще 1 раза в 24 часа
   - Не изменяется при недавних бронированиях

## 🛠 Технологии

- **Backend:** FastAPI + Python 3.11
- **База данных:** PostgreSQL 15
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Миграции:** Alembic
- **Фоновые задачи:** Celery + Redis
- **Контейнеризация:** Docker + Docker Compose
- **Документация:** OpenAPI (Swagger/ReDoc)

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd backend
```

### 2. Настройка переменных окружения
```bash
# Скопируйте пример файла
cp env.example .env

# Создайте файл с паролем для базы данных
echo "your_secure_password_here" > db_password.txt

# Отредактируйте .env файл под ваши нужды
nano .env
```


### 3. Запуск через Docker Compose
```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

### 4. Проверка работы
- 🌐 **API:** http://localhost:8000
- 📚 **Swagger UI:** http://localhost:8000/docs
- 🔍 **ReDoc:** http://localhost:8000/redoc
- 🏥 **Health Check:** http://localhost:8000/health

## 📊 Структура базы данных

### Основные сущности:
- **Users** - пользователи (покупатели, застройщики, модераторы)
- **Developers** - застройщики
- **Projects** - жилые комплексы
- **Buildings** - корпуса/секции
- **Apartments** - квартиры
- **PriceHistory** - история изменений цен
- **ViewsLog** - логи просмотров
- **ApartmentStats** - агрегированная статистика
- **Bookings** - бронирования
- **DynamicPricingConfig** - конфигурация алгоритма

## 🔧 API Endpoints

### Квартиры
- `GET /api/v1/apartments/` - список квартир с фильтрацией
- `GET /api/v1/apartments/{id}` - информация о квартире
- `POST /api/v1/apartments/` - создание квартиры
- `PUT /api/v1/apartments/{id}` - обновление квартиры
- `POST /api/v1/apartments/{id}/view` - запись просмотра
- `GET /api/v1/apartments/{id}/stats` - статистика квартиры

### Динамическое ценообразование
- `GET /api/v1/dynamic-pricing/config` - конфигурация
- `POST /api/v1/dynamic-pricing/config` - создание конфигурации
- `POST /api/v1/dynamic-pricing/update-all` - обновление всех цен
- `POST /api/v1/dynamic-pricing/update/{id}` - обновление цены квартиры
- `GET /api/v1/dynamic-pricing/calculate/{id}` - расчет изменения цены
- `GET /api/v1/dynamic-pricing/stats` - статистика изменений

## 🔄 Фоновые задачи

Celery worker автоматически выполняет:
- **Каждую минуту:** Обновление статистики квартир
- **Каждый час:** Динамическое ценообразование

### Ручной запуск задач:
```bash
# Обновление статистики
curl -X POST http://localhost:8000/api/v1/apartments/1/stats/update

# Обновление цен
curl -X POST http://localhost:8000/api/v1/dynamic-pricing/update-all
```

## 🧪 Тестирование

```bash
# Запуск тестов
pytest

# С покрытием
pytest --cov=app
```

## 📈 Мониторинг

### Логи Docker:
```bash
# Все сервисы
docker-compose logs

# Конкретный сервис
docker-compose logs app
docker-compose logs celery_worker
docker-compose logs postgres
```

### Статус Celery:
```bash
# Проверка задач
docker-compose exec celery_worker celery -A app.worker.celery inspect active
```

## 🔒 Безопасность

- Пароли хранятся в Docker secrets
- CORS настроен для продакшена
- Валидация данных через Pydantic
- Подготовленные SQL-запросы через SQLModel

## 🚀 Продакшен

### Переменные окружения для продакшена:
```bash
# Обязательно измените в продакшене!
SECRET_KEY=your_super_secure_secret_key
DATABASE_URL=postgresql://user:pass@prod-db:5432/db
REDIS_URL=redis://prod-redis:6379
```

### Масштабирование:
```bash
# Увеличить количество worker'ов
docker-compose up --scale celery_worker=3 -d
```

## 🤝 Разработка

### Структура проекта:
```
backend/
├── app/
│   ├── api/           # API роутеры
│   ├── services/      # Бизнес-логика
│   ├── models.py      # Модели данных
│   ├── schemas.py     # Pydantic схемы
│   ├── config.py      # Конфигурация
│   ├── database.py    # Настройка БД
│   ├── worker.py      # Celery задачи
│   └── main.py        # FastAPI приложение
├── alembic/           # Миграции
├── docker-compose.yml # Docker конфигурация
├── requirements.txt   # Зависимости Python
└── README.md         # Документация
```

### Заполнение таблиц
```python
docker compose up --build -d && docker compose exec app python init_db.py
```

### Добавление новых эндпоинтов:
1. Создайте роутер в `app/api/`
2. Добавьте схемы в `app/schemas.py`
3. Подключите роутер в `app/main.py`

### Создание миграций:
```bash
# Автогенерация миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head
```

## 📞 Поддержка

- 📧 Email: support@realestate4.ru
- 📱 Telegram: @realestate4_support
- 🐛 Issues: GitHub Issues

---

**Недвижимость 4.0** - Инновационная платформа для рынка недвижимости! 🏠✨ 