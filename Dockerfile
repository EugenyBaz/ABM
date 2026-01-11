FROM python:3.12-slim-bullseye

WORKDIR /app

# Обновляем pip
RUN pip install --no-cache-dir --upgrade pip

# Устанавливаем Poetry из PyPI (СТАБИЛЬНО)
RUN pip install --no-cache-dir poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Ставим зависимости без venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем код
COPY . .