from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.bot.services import create_task_api, get_tasks_api

router = Router()

# Определяем состояния для FSM
class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()


# --- Команда /add_task ---
@router.message(F.text.startswith("/add_task"))
async def cmd_add_task(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок задачи:")
    await state.set_state(AddTask.waiting_for_title)


# --- Обработка заголовка задачи ---
@router.message(StateFilter(AddTask.waiting_for_title))
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(AddTask.waiting_for_description)


# --- Обработка описания задачи ---
@router.message(StateFilter(AddTask.waiting_for_description))
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data.get("title")
    description = message.text
    user_id = message.from_user.id

    # Создаём задачу через API
    task = await create_task_api(title, description, user_id=user_id)

    await message.answer(f"✅ Задача создана: {task['title']} (ID {task['id']})")

    # Очищаем состояние
    await state.clear()





