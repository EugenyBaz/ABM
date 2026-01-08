from datetime import datetime
from typing import List

from pydantic import BaseModel


class MarketingAttachment(BaseModel):
    """
    Модель вложения для маркетингового письма.

    Используется для передачи файлов (документы, изображения, видео)
    при отправке email.
    """

    filename: str
    content: bytes
    mime_type: str


class MarketingMessage(BaseModel):
    """
    Модель маркетингового письма.

    Описывает структуру письма, отправляемого на email,
    включая HTML-тело и список вложений.
    """

    subject: str
    body_html: str
    received_at: datetime
    attachments: List[MarketingAttachment] = []
