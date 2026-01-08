from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    """
    Middleware для логирования входящих Telegram-сообщений.

    Логирует ID пользователя и текст сообщения
    перед передачей управления обработчику.
    """

    async def __call__(self, handler, event: Message, data) -> Any:
        """Перехват входящего события Telegram."""

        if isinstance(event, Message):
            logger.info(f"TG message | user={event.from_user.id} | text={event.text}")
        return await handler(event, data)
