import pytest
from httpx import AsyncClient


# ---------- CREATE ----------
@pytest.mark.asyncio
async def test_create_task(client: AsyncClient, user_1_headers) -> None:
    """Проверка создания задачи."""
    response = await client.post(
        "/tasks/",
        json={
            "title": "Test task",
            "description": "Test description",
        },
        headers=user_1_headers,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["status"] == "pending"
    assert data["user_id"] == 111
    assert "id" in data


# ---------- READ LIST ----------


@pytest.mark.asyncio
async def test_get_tasks_only_own(
    client: AsyncClient, user_1_headers, user_2_headers
) -> None:
    """Проверка получения только собственных задач пользователя."""
    # user 1
    await client.post(
        "/tasks/",
        json={"title": "User1 task"},
        headers=user_1_headers,
    )

    # user 2
    await client.post(
        "/tasks/",
        json={"title": "User2 task"},
        headers=user_2_headers,
    )

    response = await client.get("/tasks/", headers=user_1_headers)
    assert response.status_code == 200

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User1 task"
    assert tasks[0]["user_id"] == 111


# ---------- READ BY ID ----------


@pytest.mark.asyncio
async def test_get_task_by_id(client: AsyncClient, user_1_headers) -> None:
    """Проверка получения задачи по ID владельцем."""
    r = await client.post(
        "/tasks/",
        json={"title": "Single task"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.get(
        f"/tasks/{task_id}",
        headers=user_1_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_forbidden(
    client: AsyncClient, user_1_headers, user_2_headers
) -> None:
    """Проверка запрета доступа к чужой задаче."""
    r = await client.post(
        "/tasks/",
        json={"title": "Private task"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.get(
        f"/tasks/{task_id}",
        headers=user_2_headers,
    )

    assert response.status_code == 403


# ---------- UPDATE ----------


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient, user_1_headers) -> None:
    """Проверка обновления задачи владельцем."""
    r = await client.post(
        "/tasks/",
        json={"title": "Old title"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "New title", "status": "done"},
        headers=user_1_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["status"] == "done"


@pytest.mark.asyncio
async def test_update_task_forbidden(
    client: AsyncClient, user_1_headers, user_2_headers
) -> None:
    """Проверка запрета обновления чужой задачи."""
    r = await client.post(
        "/tasks/",
        json={"title": "Protected task"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.put(
        f"/tasks/{task_id}",
        json={"title": "Hack attempt"},
        headers=user_2_headers,
    )

    assert response.status_code == 403


# ---------- DELETE ----------


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient, user_1_headers) -> None:
    """Проверка удаления задачи владельцем."""
    r = await client.post(
        "/tasks/",
        json={"title": "To be deleted"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.delete(
        f"/tasks/{task_id}",
        headers=user_1_headers,
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_task_forbidden(
    client: AsyncClient, user_1_headers, user_2_headers
) -> None:
    """Проверка запрета удаления чужой задачи."""
    r = await client.post(
        "/tasks/",
        json={"title": "Protected delete"},
        headers=user_1_headers,
    )
    task_id = r.json()["id"]

    response = await client.delete(
        f"/tasks/{task_id}",
        headers=user_2_headers,
    )

    assert response.status_code == 403


# ---------- FILTERS ----------


@pytest.mark.asyncio
async def test_filter_by_status(client: AsyncClient, user_1_headers) -> None:
    """Проверка фильтрации задач по статусу."""
    await client.post(
        "/tasks/",
        json={"title": "Pending task"},
        headers=user_1_headers,
    )

    await client.post(
        "/tasks/",
        json={"title": "Done task", "status": "done"},
        headers=user_1_headers,
    )

    response = await client.get(
        "/tasks/?status=done",
        headers=user_1_headers,
    )

    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "done"
