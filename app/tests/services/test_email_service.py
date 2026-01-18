import pytest

from app.services.email_service import send_task_email, send_tasks_email


class FakeSMTP:
    def __init__(self, *args, **kwargs):
        pass

    async def connect(self):
        return None

    async def login(self, *args, **kwargs):
        return None

    async def send_message(self, message):
        self.message = message

    async def quit(self):
        return None


@pytest.mark.asyncio
async def test_send_tasks_email(monkeypatch):
    monkeypatch.setattr(
        "app.services.email_service.SMTP",
        FakeSMTP,
    )

    tasks = [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Desc 1",
            "status": "pending",
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": "Desc 2",
            "status": "done",
        },
    ]

    await send_tasks_email(
        to_email="test@example.com",
        tasks=tasks,
        subject="Test tasks",
    )


@pytest.mark.asyncio
async def test_send_task_email(monkeypatch):
    monkeypatch.setattr(
        "app.services.email_service.SMTP",
        FakeSMTP,
    )

    task = {
        "id": 1,
        "title": "Single task",
        "description": "Details",
        "status": "pending",
    }

    await send_task_email(
        to_email="test@example.com",
        task=task,
        subject="Single task",
    )
