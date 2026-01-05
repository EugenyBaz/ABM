from datetime import datetime
from typing import List

from pydantic import BaseModel


class MarketingAttachment(BaseModel):
    filename: str
    content: bytes
    mime_type: str

class MarketingMessage(BaseModel):
    subject: str
    body_html: str
    received_at: datetime
    attachments: List[MarketingAttachment] = []