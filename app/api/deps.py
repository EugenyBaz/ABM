from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import async_session

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session



async def get_current_user() -> int:
    """
    Заглушка текущего пользователя.
    Позже будет интеграция с Telegram ID.
    """
    return 123456789  # сюда можно подставить свой Telegram ID для теста