from typing import Dict, Any

import httpx
from app.core.config import settings

class BackendClient:
    """ HTTP-клиент для взаимодействия с backend API.
        Используется для выполнения запросов к серверу
        от имени Telegram-пользователя."""

    def __init__(self) -> None:
        """ Инициализация клиента backend API.
                Базовый URL берётся из настроек приложения. """

        self.base_url = settings.API_URL

    async def create_task(self, user_id: int, data: dict) -> Dict[str, Any]:
        """ Создание новой задачи через backend API.
                Отправляет POST-запрос с данными задачи и
                Telegram user id в HTTP-заголовке."""

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks/",
                json=data,
                headers={"X-Telegram-User-Id": str(user_id)},
                timeout=5,
            )
            response.raise_for_status()
            return response.json()