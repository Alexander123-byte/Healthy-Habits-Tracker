# Используем базовый образ Python 3.12 slim
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt /

# Устанавливаем зависимости
RUN pip install -r /requirements.txt --no-cache-dir

# Копируем весь проект в рабочую директорию
COPY . .

# Создаем пользователя и группу для запуска Celery
RUN addgroup --system celery && adduser --system --ingroup celery celery

# Устанавливаем владельца каталога приложения
RUN chown -R celery:celery /app

# Переключаемся на созданного пользователя
USER celery
