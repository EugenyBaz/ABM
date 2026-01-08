from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.tasks import router as tasks_router
from app.database.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Жизненный цикл приложения FastAPI.

    Startup:
    - создаёт таблицы базы данных (используется для тестовой среды)

    Shutdown:
    - корректно закрывает соединение с базой данных
    """
    # Startup: создаём таблицы (для теста)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: закрываем соединение с базой
    await engine.dispose()


app = FastAPI(title="ABM-AsyncBridgeManager", lifespan=lifespan)

# Роуты
app.include_router(tasks_router)


# Health check
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Используется для проверки доступности приложения."""
    return {"status": "ok"}
