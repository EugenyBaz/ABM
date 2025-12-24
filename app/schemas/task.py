from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskInDB(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class TaskOut(TaskInDB):
    pass

TaskRead = TaskOut