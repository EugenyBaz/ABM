from typing import Any, Optional
from unittest.mock import AsyncMock

import pytest

from app.bot import services

class FakeResponse:
    """
    Фейковый HTTP-ответ для имитации httpx.Response.

    Используется в тестах для подмены ответов backend API.
    """

    def __init__(self, json_data=None, status_code=200) -> None:
        self._json = json_data
        self.status_code = status_code

    def json(self) -> Optional[Any]:
        """Возвращает JSON-данные ответа"""
        return self._json

    def raise_for_status(self) -> None:
        """
        Имитирует поведение raise_for_status().

        Генерирует исключение при HTTP-ошибке.
        """
        if self.status_code >= 400:
            raise Exception("HTTP error")

class FakeAsyncClient:
    """
    Фейковый AsyncClient для подмены httpx.AsyncClient.

    Используется в unit-тестах для изоляции
    от реальных HTTP-запросов.
    """

    def __init__(self, *args, **kwargs) -> None:
        pass

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass

    async def post(self, *args, **kwargs) -> FakeResponse:
        """Имитирует POST-запрос."""

        return FakeResponse({"status": "ok", "tasks_count": 2})

    async def get(self, *args, **kwargs):
        """Имитирует GET-запрос."""
        return FakeResponse(
            [
                {"id": 1, "title": "Task 1", "status": "pending"},
                {"id": 2, "title": "Task 2", "status": "done"},
            ]
        )

    async def put(self, *args, **kwargs) -> FakeResponse:
        """Имитирует PUT-запрос."""
        return FakeResponse({"id": 1, "title": "Updated", "status": "done"})

    async def delete(self, *args, **kwargs) -> FakeResponse:
        """Имитирует DELETE-запрос."""
        return FakeResponse()

@pytest.mark.asyncio
async def test_get_tasks_api(monkeypatch) -> None:
    """Проверка получения списка задач через API-сервис"""
    monkeypatch.setattr(
        "app.bot.services.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = await services.get_tasks_api(user_id=1)

    assert len(result) == 2
    assert result[0]["title"] == "Task 1"

@pytest.mark.asyncio
async def test_create_task_api(monkeypatch) -> None:
    """Проверка создания задачи через API-сервис."""
    monkeypatch.setattr(
        "app.bot.services.httpx.AsyncClient",
        FakeAsyncClient,
    )

    task = await services.create_task_api(
        title="Test",
        description="Desc",
        user_id=1,
    )

    assert task["status"] == "ok"

@pytest.mark.asyncio
async def test_send_tasks_email_api(monkeypatch) -> None:
    """Проверка отправки email со списком задач."""

    monkeypatch.setattr(
        "app.bot.services.httpx.AsyncClient",
        FakeAsyncClient,
    )

    result = await services.send_tasks_email_api(user_id=1)

    assert result["status"] == "ok"
    assert result["tasks_count"] == 2

@pytest.mark.asyncio
async def test_send_task_email_api(monkeypatch) -> None:
    """Проверка отправки email с одной задачей.

    Тест считается успешным, если исключение не выбрасывается."""

    monkeypatch.setattr(
        "app.bot.services.httpx.AsyncClient",
        FakeAsyncClient,
    )

    # просто не должно упасть
    await services.send_task_email_api(task_id=1, user_id=1)
