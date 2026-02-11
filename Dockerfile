# 1. Базовый образ Python
FROM python:3.11-slim

# 2. Рабочая директория в контейнере
WORKDIR /app

# 3. Копируем все файлы проекта
COPY . .

# 4. Обновляем pip и ставим зависимости
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 5. Экспорт переменных окружения (если хочешь, можно через .env)
ENV PYTHONUNBUFFERED=1

# 6. Команда по умолчанию — запуск FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
