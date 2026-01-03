from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.config import settings
from app.bot.handlers.start import router as start_router
from app.bot.handlers import task  # подключаем наш handler
from app.bot.handlers.list import router as list_router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем роутеры
dp.include_router(start_router)
dp.include_router(task.router)
dp.include_router(list_router)