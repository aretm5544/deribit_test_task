# Используем образ Python 3.12 
FROM python:3.12-slim

# Устанавливаем системные зависимости для работы с Postgres и сборки пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Сначала копируем только requirements.txt для кэширования слоев
COPY requirements.txt .

# Устанавливаем библиотеки напрямую в систему контейнера
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Выставляем переменную окружения, чтобы Python не буферизировал логи
ENV PYTHONUNBUFFERED=1