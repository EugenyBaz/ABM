import httpx
from app.core.config import settings

API_URL = f"{settings.API_URL}/tasks/"

async def create_task_api(title: str, description: str, user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            json={
                "title": title,
                "description": description,
                "status": "pending",
            },
            headers={
                "X-Telegram-User-Id": str(user_id),
            },
        )
        response.raise_for_status()
        return response.json()


async def get_tasks_api(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            API_URL,
            headers={
                "X-Telegram-User-Id": str(user_id),
            },
        )
        response.raise_for_status()
        return response.json()

from sqlalchemy.ext.asyncio import AsyncSession
from app.models.tasks import Task

async def create_task_test(session: AsyncSession, user_id: int, title: str, description: str):
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task