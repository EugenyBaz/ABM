from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    Обработчик команды /start.
    Логирует запуск бота пользователем и отправляет
    приветственное сообщение."""
    logger.info(f"/start | user={message.from_user.id}")
    await message.answer("Бот ABM запущен и работает ✅")
