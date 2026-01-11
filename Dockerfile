FROM python:3.12-slim-bullseye

WORKDIR /app

# pip и poetry (гарантированно в PATH)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

# зависимости
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --only main

# код
COPY . .