from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        if isinstance(event, Message):
            logger.info(
                f"TG message | user={event.from_user.id} | text={event.text}"
            )
        return await handler(event, data)