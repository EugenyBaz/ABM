import httpx
from app.core.config import settings

# Базовый URL для работы с задачами
API_BASE_URL = f"{settings.API_URL}/tasks"

# Один HTTP-клиент на всё приложение
client = httpx.AsyncClient(
    base_url=API_BASE_URL,
    timeout=httpx.Timeout(5.0),
)


def _auth_headers(user_id: int) -> dict:
    """Заголовки авторизации для API."""
    return {
        "X-Telegram-User-Id": str(user_id),
    }


# ---------- CREATE ----------
async def create_task_api(title: str, description: str, user_id: int) -> dict:
    response = await client.post(
        "",
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
async def get_tasks_api(user_id: int) -> list[dict]:
    response = await client.get(
        "",
        headers=_auth_headers(user_id),
    )
    response.raise_for_status()
    return response.json()


# ---------- READ ONE ----------
async def get_task_api(task_id: int, user_id: int) -> dict:
    response = await client.get(
        f"/{task_id}",
        headers=_auth_headers(user_id),
    )
    response.raise_for_status()
    return response.json()


# ---------- UPDATE ----------
async def mark_task_done_api(task_id: int, user_id: int) -> dict:
    response = await client.put(
        f"/{task_id}",
        json={"status": "done"},
        headers=_auth_headers(user_id),
    )
    response.raise_for_status()
    return response.json()

async def update_task_api(task_id: int, user_id: int, data: dict) -> dict:
    response = await client.put(
        f"/{task_id}",
        json=data,
        headers=_auth_headers(user_id),
    )
    response.raise_for_status()
    return response.json()


# ---------- DELETE ----------
async def delete_task_api(task_id: int, user_id: int) -> bool:
    response = await client.delete(
        f"/{task_id}",
        headers=_auth_headers(user_id),
    )
    response.raise_for_status()
    return True


# ---------- SHUTDOWN ----------
async def close_api_client():
    """Корректно закрыть HTTP-клиент при завершении бота."""
    await client.aclose()