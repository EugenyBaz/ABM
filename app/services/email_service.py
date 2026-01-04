from aiosmtplib import SMTP
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
import os
from app.core.config import settings
from app.schemas.marketing import MarketingMessage
from datetime import datetime



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

async def send_task_email(
        to_email: str,
        task,
        subject: str = "Задача",
):
    template = env.get_template("task.html")
    html_content = template.render(task=task)

    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(html_content, subtype="html")

    smtp = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=True,
    )
    await smtp.connect()
    await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    await smtp.send_message(message)
    await smtp.quit()



async def send_marketing_email(message: MarketingMessage) -> None:
    template = env.get_template("marketing.html")

    html_content = template.render(
        content=message.body_html,
        received_at=message.received_at,
    )

    email = EmailMessage()
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER  # отправляем на ТУ ЖЕ почту
    email["Subject"] = message.subject
    email.set_content(html_content, subtype="html")

    smtp = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=True,
    )
    await smtp.connect()
    await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    await smtp.send_message(email)
    await smtp.quit()