FROM python:3.12-slim-bullseye

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Установка Poetry
RUN wget -O- https://install.python-poetry.org | PYTHONNOUSERSITE=1 python -

# ДОБАВЛЯЕМ Poetry в PATH (КЛЮЧЕВО!)
ENV PATH="/root/.local/bin:$PATH"

# Ставим зависимости без venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем код
COPY . .