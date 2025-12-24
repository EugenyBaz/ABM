import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models.tasks import Task

# Фикстура для чистой сессии
@pytest.fixture
async def async_session_fixture(async_session: AsyncSession):
    # очищаем таблицу tasks перед тестом
    await async_session.execute("DELETE FROM tasks;")
    await async_session.commit()
    yield async_session
    await async_session.execute("DELETE FROM tasks;")
    await async_session.commit()

# Фикстура для заполнения тестовыми задачами
@pytest.fixture
async def sample_tasks(async_session_fixture: AsyncSession):
    tasks = [
        Task(user_id=111111, title="Task A", description="Desc A"),
        Task(user_id=222222, title="Task B", description="Desc B"),
        Task(user_id=333333, title="Task C", description="Desc C"),
    ]
    async_session_fixture.add_all(tasks)
    await async_session_fixture.commit()
    # обновляем объекты, чтобы был доступ к id
    await async_session_fixture.refresh(tasks[0])
    await async_session_fixture.refresh(tasks[1])
    await async_session_fixture.refresh(tasks[2])
    return tasks

# Фикстура для клиента FastAPI
@pytest.fixture
async def client(sample_tasks):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac