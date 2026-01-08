import httpx
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.bot.keyboards.task import task_keyboard
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

    if not tasks:
        await message.answer("📝 У тебя пока нет задач")
        return

    await message.answer("📝 <b>Твои задачи:</b>", parse_mode="HTML")

    for task in tasks:
        emoji = STATUS_EMOJI.get(task["status"], "❔")

        await message.answer(
            f"{emoji} <b>{task['title']}</b>",
            parse_mode="HTML",
            reply_markup=task_keyboard(task["id"]),
        )
