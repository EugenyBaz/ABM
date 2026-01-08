import httpx
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.bot.callbacks import TaskAction
from app.bot.handlers.edit_task import EditTask
from app.bot.keyboards.edit_task import edit_field_keyboard
from app.bot.services import (delete_task_api, get_task_api,
                              mark_task_done_api, send_task_email_api)

router = Router()


@router.callback_query(TaskAction.filter())
async def handle_task_action(
    callback: CallbackQuery,
    callback_data: TaskAction,
    state: FSMContext,
) -> None:
    """Обработчик callback-действий над задачей.
    Поддерживает просмотр, редактирование, выполнение,
    удаление и отправку задачи по email."""

    action = callback_data.action
    task_id = callback_data.task_id
    user_id = callback.from_user.id

    try:
        # 👁 VIEW
        if action == "view":
            task = await get_task_api(task_id, user_id)
            text = (
                f"📌 <b>{task['title']}</b>\n\n"
                f"🆔 <b>{task['id']}</b>\n\n"
                f"{task['description']}\n\n"
                f"Статус: <b>{task['status']}</b>"
            )
            await callback.message.answer(text, parse_mode="HTML")

        # ✏️ EDIT → вход в FSM
        elif action == "edit":
            await state.set_state(EditTask.waiting_for_value)
            await state.update_data(task_id=task_id)

            await callback.message.answer(
                "✏️ Что редактируем?",
                reply_markup=edit_field_keyboard(),
            )
            await callback.answer()
            return

        # ✅ DONE
        elif action == "done":
            task = await mark_task_done_api(task_id, user_id)
            await callback.message.edit_text(
                f"✅ <b>{task['title']}</b>\n\n" "Задача выполнена 👍",
                parse_mode="HTML",
            )

        # EMAIL
        elif action == "email":
            await send_task_email_api(task_id, user_id)
            await callback.answer("📧 Задача отправлена на почту", show_alert=True)
            return

        # 🗑 DELETE
        elif action == "delete":
            await delete_task_api(task_id, user_id)
            await callback.message.edit_text("🗑 Задача удалена")

        else:
            await callback.answer("Неизвестное действие", show_alert=True)
            return

    except httpx.HTTPStatusError:
        await callback.answer("❌ Ошибка сервера", show_alert=True)
        return

    except httpx.ConnectError:
        await callback.answer("⚠️ Сервис недоступен", show_alert=True)
        return

    # Закрываем callback (убирает «часики»)
    await callback.answer()
