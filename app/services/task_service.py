from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.tasks import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def get_tasks(
    db: AsyncSession,
    user_id: int,
    status: str | None = None,
    limit: int = 20,
    offset: int = 0,
):
    stmt = select(Task).where(Task.user_id == user_id)

    if status:
        stmt = stmt.where(Task.status == status)

    stmt = stmt.limit(limit).offset(offset)

    result = await db.execute(stmt)
    return result.scalars().all()


# ❗ БЕЗ user_id
async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
):
    return await db.get(Task, task_id)


async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    user_id: int,
):
    db_task = Task(
        **task.model_dump(),
        user_id=user_id,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession,
    task_id: int,
    user_id: int,
    task: TaskUpdate,
):
    db_task = await get_task_by_id(db, task_id)

    if not db_task:
        return None, "not_found"

    if db_task.user_id != user_id:
        return None, "forbidden"

    for field, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)
    return db_task, None


async def delete_task(
    db: AsyncSession,
    task_id: int,
    user_id: int,
):
    db_task = await get_task_by_id(db, task_id)

    if not db_task:
        return None, "not_found"

    if db_task.user_id != user_id:
        return None, "forbidden"

    await db.delete(db_task)
    await db.commit()
    return db_task, None