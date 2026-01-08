import httpx

from app.core.config import settings

API_BASE_URL = f"{settings.API_URL}/tasks"


def _auth_headers(user_id: int) -> dict:
    """Формирование заголовков авторизации для API-запросов.
    Использует Telegram user id для идентификации пользователя."""

    return {
        "X-Telegram-User-Id": str(user_id),
    }


# ---------- CREATE ----------
async def create_task_api(title: str, description: str, user_id: int) -> dict:
    """Создание новой задачи через backend API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/",
            json={
                "title": title,
                "description": description,
                "status": "pending",
            },
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
        return response.json()


# ---------- READ LIST ----------
async def get_tasks_api(user_id: int, view: str = "short") -> list:
    """Получение списка задач пользователя через backend API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{API_BASE_URL}/",
            headers=_auth_headers(user_id),
            params={"view": view},
        )
        response.raise_for_status()
        return response.json()


# ---------- READ ONE ----------
async def get_task_api(task_id: int, user_id: int) -> dict:
    """Получение одной задачи по ID через backend API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(
            f"{API_BASE_URL}/{task_id}",
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
        return response.json()


# ---------- UPDATE ----------
async def mark_task_done_api(task_id: int, user_id: int) -> dict:
    """Отметка задачи как выполненной."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.put(
            f"{API_BASE_URL}/{task_id}",
            json={"status": "done"},
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
        return response.json()


async def update_task_api(task_id: int, user_id: int, data: dict) -> dict:
    """Обновление произвольных полей задачи."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.put(
            f"{API_BASE_URL}/{task_id}",
            json=data,
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
        return response.json()


# ---------- DELETE ----------
async def delete_task_api(task_id: int, user_id: int) -> None:
    """Удаление задачи через backend API."""

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.delete(
            f"{API_BASE_URL}/{task_id}",
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()


# ---------- EMAIL ----------
async def send_tasks_email_api(user_id: int) -> None:
    """Отправка списка всех задач пользователя на email."""

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/email",
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
        return response.json()


async def send_task_email_api(task_id: int, user_id: int) -> None:
    """Отправка одной задачи на email."""

    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post(
            f"{API_BASE_URL}/{task_id}/email",
            headers=_auth_headers(user_id),
        )
        response.raise_for_status()
