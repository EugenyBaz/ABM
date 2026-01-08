import httpx
from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.bot.services import create_task_api, get_tasks_api, send_tasks_email_api

router = Router()

# Определяем состояния для FSM
class AddTask(StatesGroup):
    """ FSM-состояния для создания новой задачи."""
    waiting_for_title = State()
    waiting_for_description = State()


# --- Команда /add_task ---
@router.message(F.text.startswith("/add_task"))
async def cmd_add_task(message: types.Message, state: FSMContext) -> None:
    """ Обработчик команды /add_task.
        Запускает сценарий создания задачи и переводит
        пользователя в состояние ввода заголовка."""

    await message.answer("Введите заголовок задачи:")
    await state.set_state(AddTask.waiting_for_title)


# --- Обработка заголовка задачи ---
@router.message(StateFilter(AddTask.waiting_for_title))
async def process_title(message: types.Message, state: FSMContext) -> None:
    """ Обработка ввода заголовка задачи.
        Сохраняет заголовок во FSM и переводит
        пользователя к вводу описания."""

    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(AddTask.waiting_for_description)


# --- Обработка описания задачи ---
@router.message(StateFilter(AddTask.waiting_for_description))
async def process_description(message: types.Message, state: FSMContext) -> None:
    """ Обработка ввода описания задачи.
        Создаёт задачу через API и завершает FSM-сценарий."""

    data = await state.get_data()
    title = data.get("title")
    description = message.text
    user_id = message.from_user.id

    # Создаём задачу через API
    task = await create_task_api(title, description, user_id=user_id)

    await message.answer(f"✅ Задача создана: {task['title']} (ID {task['id']})")

    # Очищаем состояние
    await state.clear()


@router.message(F.text == "/tasks")
async def cmd_tasks(message: types.Message) -> None:
    """ Обработчик команды /tasks.
        Получает список задач пользователя и
        выводит их в кратком виде."""

    user_id = message.from_user.id
    tasks = await get_tasks_api(user_id, view="short")

    if not tasks:
        await message.answer("📭 У вас пока нет задач")
        return

    text = "\n".join(
        f"{t['id']}. {t['title']} ({t['status']})"
        for t in tasks
    )

    await message.answer("📋 Ваши задачи:\n" + text)

@router.message(F.text == "/email")
async def cmd_email_tasks(message: types.Message) -> None:
    """ Обработчик команды /email.
        Отправляет список задач пользователя на email
        через API и сообщает результат."""

    user_id = message.from_user.id

    try:
        result = await send_tasks_email_api(user_id)


        await message.answer(
            "📧 <b>Список задач отправлен</b>\n\n"
            f"📬 Почта: <code>{result['sent_to']}</code>\n"
            f"📝 Количество задач: <b>{result['tasks_count']}</b>",
            parse_mode="HTML",
        )

    except httpx.HTTPStatusError:
        await message.answer("❌ Ошибка при отправке email")
        return


