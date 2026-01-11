FROM python:3.12-slim-bullseye

# Рабочая директория
WORKDIR /app

# --- FIX: HTTPS + IPv4 для apt (критично для Docker/VPS) ---
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list && \
    echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4

# Системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        wget \
        gnupg \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Копируем только файлы зависимостей (кэш Docker)
COPY pyproject.toml poetry.lock ./

# Установка Poetry
RUN wget -qO- https://install.python-poetry.org | \
    PYTHONNOUSERSITE=1 python -

# Добавляем Poetry в PATH
ENV PATH="/root/.local/bin:$PATH"

# Отключаем venv и ставим зависимости
RUN poetry config virtualenvs.create false && \
    poetry install

# Копируем остальной код
COPY . .