# Frontend Project

## Требования

- Node.js 20.x
- Docker (опционально)
- Docker Compose (опционально)

## Локальный запуск

1. Установите зависимости:
```bash
npm install --legacy-peer-deps
```

2. Создайте файл .env с настройками:
```bash
NEXT_PUBLIC_API_HOST=46.173.24.165
NEXT_PUBLIC_API_PORT=8000
HOST=46.173.24.165  # хост для запуска приложения
PORT=3000           # порт для запуска приложения
```

3. Запустите проект:
```bash
npm run dev
```

## Запуск через Docker

### Разработка

```bash
# Использование значений по умолчанию
docker-compose -f docker-compose.dev.yml up

# Или с указанием переменных окружения
HOST=46.173.24.165 PORT=3000 docker-compose -f docker-compose.dev.yml up
```

### Продакшн

```bash
# Использование значений по умолчанию
docker-compose up

# Или с указанием переменных окружения
HOST=46.173.24.165 PORT=3000 docker-compose up
```

## Переменные окружения

- `NEXT_PUBLIC_API_HOST` - хост API (по умолчанию: 46.173.24.165)
- `NEXT_PUBLIC_API_PORT` - порт API (по умолчанию: 8000)
- `HOST` - хост для запуска приложения (по умолчанию: 46.173.24.165)
- `PORT` - порт для запуска приложения (по умолчанию: 3000)

## Обработка ошибок

Проект включает обработку следующих ошибок API:
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 500 Internal Server Error

## Примечания

- Некоторые эндпоинты API могут быть недоступны (auth, post, put, delete)
- Для локальной разработки можно использовать localhost в качестве HOST и NEXT_PUBLIC_API_HOST 