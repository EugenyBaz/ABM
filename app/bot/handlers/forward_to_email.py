from aiogram import Router
from aiogram.types import Message
from datetime import datetime

from app.schemas.marketing import MarketingMessage
from app.services.email_service import send_marketing_email
from app.core.config import settings

router = Router()


@router.message()
async def handle_forwarded_message(message: Message) -> None:
    print("FORWARD HANDLER CALLED")

    # 1️⃣ Проверка пользователя (whitelist)
    allowed_users = settings.get_allowed_forward_users()

    if allowed_users:
        if not message.from_user or message.from_user.id not in allowed_users:
            print(
                "USER NOT ALLOWED:",
                message.from_user.id if message.from_user else None,
            )
            return

    # 2️⃣ Проверка, что сообщение переслано
    if not message.forward_from and not message.forward_from_chat:
        print("NOT FORWARDED")
        return

    print("FORWARDED MESSAGE OK")

    # 3️⃣ Текст / caption
    text = message.text or message.caption
    if not text:
        text = "[Переслано сообщение без текста]"

    # 4️⃣ Отправка email
    await send_marketing_email(
        MarketingMessage(
            subject=settings.MARKETING_EMAIL_SUBJECT or "[Marketing]",
            body_html=text.replace("\n", "<br>"),
            received_at=datetime.utcnow(),
        )
    )

    print("MARKETING EMAIL SENT")