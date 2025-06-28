FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /backend

# Копируем код приложения
COPY . .
# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload