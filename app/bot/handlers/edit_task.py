from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from app.bot.callbacks import EditField
from app.bot.services import get_task_api, update_task_api

router = Router()


class EditTask(StatesGroup):
    """FSM-состояния для редактирования задачи"""

    waiting_for_field = State()
    waiting_for_value = State()


@router.callback_query(EditField.filter())
async def choose_edit_field(
    callback: CallbackQuery,
    callback_data: EditField,
    state: FSMContext,
) -> None:
    """Обработка callback-запроса выбора поля для редактирования задачи."""
    data = await state.get_data()
    task_id = data["task_id"]
    user_id = callback.from_user.id

    task = await get_task_api(task_id, user_id)
    field = callback_data.field
    current_value = task.get(field, "")

    await state.update_data(field=field)

    await callback.message.answer(
        f"✏️ <b>Редактируйте {field}:</b>\n\n" f"{current_value}",
        parse_mode="HTML",
    )

    await callback.answer()


@router.message(StateFilter(EditTask.waiting_for_value))
async def update_task_value(message: types.Message, state: FSMContext) -> None:
    """Обновление сообщения с новым значением поля задачи."""
    data = await state.get_data()

    task_id = data["task_id"]
    field = data["field"]
    value = message.text
    user_id = message.from_user.id

    task = await update_task_api(
        task_id,
        user_id,
        {field: value},
    )

    await message.answer(
        f"✅ Задача обновлена\n\n" f"📌 <b>{task['title']}</b>",
        parse_mode="HTML",
    )

    await state.clear()
