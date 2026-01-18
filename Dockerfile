FROM python:3.12-slim-bullseye

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем только зависимости (для Docker cache)
COPY pyproject.toml poetry.lock ./

# Ставим зависимости без venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root
# Копируем код
COPY . .