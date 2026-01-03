from app.bot.bot import dp, bot
import asyncio
import logging
from aiogram.types import BotCommand


logging.basicConfig(level=logging.INFO)

async def setup_commands():
    commands = [
        BotCommand(command="add_task", description="➕ Добавить задачу"),
        BotCommand(command="list", description="📝 Список задач"),
    ]
    await bot.set_my_commands(commands)



async def main():
    print("🚀 Telegram bot started")

    await setup_commands()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())