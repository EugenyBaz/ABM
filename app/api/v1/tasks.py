from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services.task_service import create_task, get_tasks, get_task, update_task, delete_task
from app.api.deps import get_db, get_current_user  # позже реализуем

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskOut])
async def read_tasks(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await get_tasks(db, user_id)

@router.get("/{task_id}", response_model=TaskOut)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    task = await get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/", response_model=TaskOut)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    return await create_task(db, task, user_id)

@router.put("/{task_id}", response_model=TaskOut)
async def update_existing_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    updated_task = await update_task(db, task_id, user_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", response_model=TaskOut)
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    deleted_task = await delete_task(db, task_id, user_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return deleted_task