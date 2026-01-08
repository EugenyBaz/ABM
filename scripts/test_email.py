import asyncio

from app.services.email_service import send_tasks_email

tasks = [
    {"title": "Купить молоко", "status": "pending"},
    {"title": "Сделать отчёт", "status": "in_progress"},
]

asyncio.run(send_tasks_email("eugeny.bazavod@list.ru", tasks))
