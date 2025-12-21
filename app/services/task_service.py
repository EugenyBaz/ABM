from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.tasks import Task
from app.schemas.task import TaskCreate, TaskUpdate

async def get_tasks(session: AsyncSession, user_id: int):
    result = await session.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()

async def get_task(session: AsyncSession, task_id: int, user_id: int):
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def create_task(session: AsyncSession, task: TaskCreate, user_id: int):
    db_task = Task(**task.dict(), user_id=user_id)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def update_task(session: AsyncSession, task_id: int, user_id: int, task: TaskUpdate):
    db_task = await get_task(session, task_id, user_id)
    if not db_task:
        return None
    for field, value in task.dict(exclude_unset=True).items():
        setattr(db_task, field, value)
    await session.commit()
    await session.refresh(db_task)
    return db_task

async def delete_task(session: AsyncSession, task_id: int, user_id: int):
    db_task = await get_task(session, task_id, user_id)
    if not db_task:
        return None
    await session.delete(db_task)
    await session.commit()
    return db_task