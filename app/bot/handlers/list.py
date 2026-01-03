from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import httpx

from app.bot.services import get_tasks_api

router = Router()

STATUS_EMOJI = {
    "pending": "⏳",
    "done": "✅",
}


@router.message(Command("list", "tasks"))
async def list_tasks(message: Message):
    user_id = message.from_user.id

    try:
        tasks = await get_tasks_api(user_id)
    except httpx.ConnectError:
        await message.answer("⚠️ Сервис временно недоступен")
        return
    except httpx.HTTPStatusError:
        await message.answer("❌ Ошибка при получении задач")
        return

    if not tasks:
        await message.answer("📝 У тебя пока нет задач")
        return

    lines = ["📝 <b>Твои задачи:</b>\n"]

    for i, task in enumerate(tasks, start=1):
        emoji = STATUS_EMOJI.get(task["status"], "❔")
        lines.append(f"{i}. {emoji} <b>{task['title']}</b>")

    await message.answer(
        "\n".join(lines),
        parse_mode="HTML",
    )