from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.v1.tasks import router as tasks_router
from app.database.database import engine, Base
from app.api.test_task import router as test_task_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: создаём таблицы (для теста)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: закрываем соединение с базой
    await engine.dispose()

app = FastAPI(title="ABM-AsyncBridgeManager", lifespan=lifespan)

# Роуты
app.include_router(tasks_router)
app.include_router(test_task_router)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}