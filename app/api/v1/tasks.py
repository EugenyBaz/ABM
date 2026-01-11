from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id, get_db
from app.core.config import settings
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services.email_service import send_task_email, send_tasks_email
from app.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskOut])
async def read_tasks(
    status: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> List[TaskOut]:
    """Получение списка всех задач"""
    return await get_tasks(
        db=db,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset,
    )


@router.get("/{task_id}", response_model=TaskOut)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    """Получение одной задачи по ID."""

    print("READ TASKS user_id =", user_id)
    task = await get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return task


@router.post("/", response_model=TaskOut)
async def create_new_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    """Создание новой задачи для текущего пользователя."""
    return await create_task(db, task, user_id)


@router.put("/{task_id}", response_model=TaskOut)
async def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    """Обновление существующей задачи"""
    updated_task, error = await update_task(db, task_id, user_id, task)

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Task not found")

    if error == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    return updated_task


@router.delete("/{task_id}", response_model=TaskOut)
async def delete_existing_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> TaskOut:
    """Удаление существующей задачи"""
    deleted_task, error = await delete_task(db, task_id, user_id)

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Task not found")

    if error == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    return deleted_task


@router.post("/email")
async def email_tasks(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> dict[str, Any]:
    """Отправка списка всех задач на email"""
    tasks = await get_tasks(db=db, user_id=user_id)

    if not tasks:
        raise HTTPException(status_code=400, detail="Нет задач для отправки")

    if not settings.REPORT_EMAIL:
        raise HTTPException(status_code=500, detail="REPORT_EMAIL не настроен")

    await send_tasks_email(
        to_email=settings.REPORT_EMAIL,
        tasks=tasks,
        subject="Ваш список задач",
    )

    return {
        "status": "ok",
        "sent_to": settings.REPORT_EMAIL,
        "tasks_count": len(tasks),
    }


@router.post("/{task_id}/email")
async def email_single_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
) -> dict[str, Any]:
    """Отправка одной задачи на email"""
    task = await get_task_by_id(db, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    await send_task_email(
        to_email=settings.REPORT_EMAIL,
        task=task,
        subject=f"Задача #{task.id}: {task.title}",
    )

    return {"status": "ok", "task_id": task_id}
