import asyncio
from app.bot.bot import dp, bot
from loguru import logger
from app.core.logging import setup_logging

async def main():
    setup_logging()
    logger.info("🚀 Telegram bot started")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())