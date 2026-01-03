from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import create_task, get_tasks, get_task_by_id, update_task, delete_task
from app.api.deps import get_db, get_current_user_id

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskOut])
async def read_tasks(
    status: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
    return await get_tasks(
        db=db,
        user_id=user_id,
        status=status,
        limit=limit,
        offset=offset,
    )

@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    task = await get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return task

@router.post("/", response_model=TaskOut)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return await create_task(db, task, user_id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_existing_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
):
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
):
    deleted_task, error = await delete_task(db, task_id, user_id)

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Task not found")

    if error == "forbidden":
        raise HTTPException(status_code=403, detail="Access denied")

    return deleted_task

