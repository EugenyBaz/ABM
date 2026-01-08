from aiogram import Router
from aiogram.types import Message
from datetime import datetime, timezone
from collections import defaultdict
import asyncio

from app.schemas.marketing import MarketingMessage, MarketingAttachment
from app.services.email_service import send_marketing_email
from app.core.config import settings

router = Router()

# --- Media group buffers ---
_media_group_buffer: dict[str, list[Message]] = defaultdict(list)
_media_group_tasks: dict[str, asyncio.Task] = {}


# ---------- helpers ----------

def get_sender_name(message: Message) -> str:
    """ Получение имени отправителя пересланного сообщения."""
    if message.forward_from:
        user = message.forward_from
        return " ".join(filter(None, [user.first_name, user.last_name]))
    if message.forward_from_chat:
        return message.forward_from_chat.title
    return "Unknown sender"


async def extract_attachments(message: Message) -> list[MarketingAttachment]:
    """ Извлечение вложений из сообщения Telegram."""
    attachments: list[MarketingAttachment] = []
    bot = message.bot

    # 📄 documents (pdf, xlsx, docx, etc.)
    if message.document:
        file = await bot.get_file(message.document.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=message.document.file_name,
                content=buffer.read(),
                mime_type=message.document.mime_type
                or "application/octet-stream",
            )
        )

    # 🖼 photos (take best quality)
    if message.photo:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=f"photo_{photo.file_id}.jpg",
                content=buffer.read(),
                mime_type="image/jpeg",
            )
        )

    # 🎥 video
    if message.video:
        file = await bot.get_file(message.video.file_id)
        buffer = await bot.download_file(file.file_path)

        attachments.append(
            MarketingAttachment(
                filename=message.video.file_name or "video.mp4",
                content=buffer.read(),
                mime_type=message.video.mime_type or "video/mp4",
            )
        )

    return attachments


async def handle_media_group(messages: list[Message]) -> None:
    """ Обработка группы сообщений (media group).
        Собирает все вложения из группы и отправляет
        одно письмо с общим текстом и вложениями."""

    base_message = messages[0]

    text = (
        base_message.caption
        or base_message.text
        or "[Переслано сообщение без текста]"
    )

    sender = get_sender_name(base_message)

    attachments: list[MarketingAttachment] = []
    for msg in messages:
        attachments.extend(await extract_attachments(msg))

    body_html = (
        text.replace("\n", "<br>")
        + "<br><br><hr>"
        + f"<small>Отправитель: <b>{sender}</b></small>"
    )

    await send_marketing_email(
        MarketingMessage(
            subject=settings.MARKETING_EMAIL_SUBJECT or "[Marketing]",
            body_html=body_html,
            received_at=datetime.now(timezone.utc),
            attachments=attachments,
        )
    )


# ---------- main handler ----------

@router.message()
async def handle_forwarded_message(message: Message) -> None:
    """ Обработка пересланных сообщений для маркетинговой рассылки.
        Поддерживает одиночные сообщения и media group.
        Фильтрует пользователей по whitelist.
        """
    # 1️⃣ whitelist пользователей
    allowed_users = settings.get_allowed_forward_users()
    if allowed_users:
        if not message.from_user or message.from_user.id not in allowed_users:
            return

    # 2️⃣ только forwarded
    if not message.forward_from and not message.forward_from_chat:
        return

    # 3️⃣ media group → буферизация
    if message.media_group_id:
        group_id = message.media_group_id
        _media_group_buffer[group_id].append(message)

        if group_id in _media_group_tasks:
            return

        async def flush():
            await asyncio.sleep(2)
            messages = _media_group_buffer.pop(group_id, [])
            _media_group_tasks.pop(group_id, None)
            if messages:
                await handle_media_group(messages)

        _media_group_tasks[group_id] = asyncio.create_task(flush())
        return

    # 4️⃣ одиночное сообщение
    text = message.text or message.caption or "[Переслано сообщение без текста]"
    sender = get_sender_name(message)
    attachments = await extract_attachments(message)

    body_html = (
        text.replace("\n", "<br>")
        + "<br><br><hr>"
        + f"<small>Отправитель: <b>{sender}</b></small>"
    )

    await send_marketing_email(
        MarketingMessage(
            subject=settings.MARKETING_EMAIL_SUBJECT or "[Marketing]",
            body_html=body_html,
            received_at=datetime.now(timezone.utc),
            attachments=attachments,
        )
    )