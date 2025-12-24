from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.bot.services import create_task_test
from fastapi import APIRouter

from app.models.tasks import Task

router = APIRouter()

@router.post("/test_task")
async def test_task(user_id: int, db: AsyncSession = Depends(get_db)):
    # Создаем задачу прямо в базе
    new_task = Task(
        user_id=user_id,
        title="Test task",
        description="This is a test",
        status="pending"
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return {"task_id": new_task.id, "user_id": new_task.user_id}