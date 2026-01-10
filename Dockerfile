FROM python:3.12-slim

# --- system deps (ВАЖНО) ---
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# --- poetry ---
RUN pip install --no-cache-dir poetry

# --- workdir ---
WORKDIR /app

# --- deps ---
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# --- source ---
COPY . .

# --- run api ---
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]