from aiosmtplib import SMTP
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os
import asyncio
from app.core.config import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates", "emails")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

async def send_tasks_email(to_email: str, tasks: list, subject: str = "Ваши задачи"):
    template = env.get_template("tasks.html")
    html_content = template.render(tasks=tasks)

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(html_content, subtype="html")

    # Для Mail.ru SSL (порт 465)
    smtp = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=True,   # <--- SSL
    )
    await smtp.connect()
    await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    await smtp.send_message(message)
    await smtp.quit()
    print(f"Письмо отправлено на {to_email}")