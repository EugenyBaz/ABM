from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.core.config import settings
from app.bot.handlers.start import router as start_router
from app.bot.handlers import task, forward_to_email  # подключаем наш handler
from app.bot.handlers.list import router as list_router
from app.bot.handlers.task_actions import router as task_actions_router
from app.bot.handlers.edit_task import router as edit_task_router

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем роутеры
dp.include_router(start_router)
dp.include_router(task.router)
dp.include_router(list_router)
dp.include_router(task_actions_router)
dp.include_router(edit_task_router)
dp.include_router(forward_to_email.router)