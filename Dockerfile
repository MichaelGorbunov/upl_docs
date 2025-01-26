# Используем базовый образ Python
FROM python:3.12-slim

# Копируем код приложения в контейнер
COPY . ./app

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости в контейнер
#COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt


# Команда для запуска приложения при старте контейнера
CMD ["bash"]
