from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    """
        Базовая схема задачи.

        Содержит общие поля, используемые
        при создании, обновлении и чтении задач.
        """
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    """
        Схема для создания новой задачи.

        Наследует все поля из TaskBase.
        Используется как входная модель (request body).
        """
    pass

class TaskUpdate(BaseModel):
    """
        Схема для обновления задачи.

        Все поля опциональны, так как обновление
        может затрагивать только часть данных.
        """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskInDB(TaskBase):
    """
        Схема задачи, хранимой в базе данных.

        Используется для сериализации ORM-моделей
        SQLAlchemy в Pydantic.
        """
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class TaskOut(TaskInDB):
    """
        Схема задачи, возвращаемая клиенту.

        Полностью соответствует структуре задачи,
        доступной во внешнем API.
        """
    pass

TaskRead = TaskOut