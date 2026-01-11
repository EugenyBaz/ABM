FROM python:3.12-slim-bullseye

WORKDIR /app

# Увеличиваем таймауты и ретраи
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_RETRIES=10
ENV POETRY_HTTP_TIMEOUT=120

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .