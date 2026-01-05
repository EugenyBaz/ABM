from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import async_session
from fastapi import Header, HTTPException

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_current_user_id(x_telegram_user_id: int | None = Header(None)):
    if not x_telegram_user_id:
        raise HTTPException(status_code=401, detail="Отсутствует Telegram user id")
    return x_telegram_user_id

# async def get_current_user_id():
#     # 🔹 Тестовая заглушка для бота
#     return 123456789