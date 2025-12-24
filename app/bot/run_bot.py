from app.bot.bot import dp, bot
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

async def main():
    print("🚀 Telegram bot started")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())