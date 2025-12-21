from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.bot.bot import dp
from app.bot.services import create_task_api

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()

@dp.message_handler(commands=["add_task"])
async def cmd_add_task(message: types.Message):
    await message.answer("Введите заголовок задачи:")
    await AddTask.waiting_for_title.set()

@dp.message_handler(state=AddTask.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await AddTask.waiting_for_description.set()

@dp.message_handler(state=AddTask.waiting_for_description)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data["title"]
    description = message.text
    # Заглушка user_id = 123456789
    task = await create_task_api(title, description, user_id=123456789)
    await message.answer(f"Задача создана: {task['title']} (ID {task['id']})")
    await state.finish()