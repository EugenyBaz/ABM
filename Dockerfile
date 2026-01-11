FROM python:3.12-slim-bullseye

WORKDIR /app

# Копируем только файлы зависимостей (Docker cache)
COPY pyproject.toml poetry.lock ./

# Установка Poetry БЕЗ wget/curl
RUN python - <<'EOF'
import urllib.request
urllib.request.urlretrieve(
    "https://install.python-poetry.org",
    "/tmp/install-poetry.py"
)
EOF

RUN PYTHONNOUSERSITE=1 python /tmp/install-poetry.py

ENV PATH="/root/.local/bin:$PATH"

# Ставим только prod-зависимости, без venv
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Копируем код
COPY . .